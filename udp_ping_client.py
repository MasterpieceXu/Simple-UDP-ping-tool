import sys
import time
import random
import argparse  # For parsing command-line arguments
from socket import *

def run_ping(server_host, server_port, count, timeout_sec):
    """
    Executes the UDP Ping test.
    """
    
    try:
        # Resolve hostname to IP address
        server_ip = gethostbyname(server_host)
    except gaierror as e:
        print(f'Could not resolve host: {server_host}. Error: {e}')
        return

    print(f'Pinging {server_host} ({server_ip}) [Port: {server_port}] with {count} packets:')

    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(timeout_sec)  # Use the provided timeout

    number = random.randint(40000, 50000)
    rtts = []
    lost = 0
    start_time = time.time() # Record the total start time

    for i in range(count):
        seq = number + i
        send_time = time.time()
        message = f'Ping {seq} {send_time}'
        
        try:
            client_socket.sendto(message.encode('utf-8'), (server_ip, server_port))
            
            # Wait for the reply
            modified_message, server_address = client_socket.recvfrom(2048)
            receive_time = time.time()
            
            # **[Fix]** RTT should be multiplied by 1000 to get milliseconds (ms)
            rtt = round((receive_time - send_time) * 1000, 2)
            rtts.append(rtt)
            print(f'Reply from {server_ip}: seq={seq}, rtt={rtt} ms')
            
            # A small delay to avoid flooding
            time.sleep(0.1) 

        except timeout:
            print(f'Request timed out: seq={seq}')
            lost += 1
        except Exception as e:
            print(f'An error occurred: {e}')
            lost += 1
            
    end_time = time.time() # Record the total end time

    # --- Statistics ---
    print(f'\n--- {server_host} Ping Statistics ---')
    
    packet_lost_percent = (lost / count) * 100
    total_time_ms = round((end_time - start_time) * 1000, 2)

    print(f'    Packets: Sent = {count}, Received = {count - lost}, Lost = {lost} ({round(packet_lost_percent, 1)}% loss)')

    # **[Fix]** Statistics logic: Only calculate RTT if at least one packet was received
    if len(rtts) > 0:
        min_rtt = round(min(rtts), 2)
        max_rtt = round(max(rtts), 2)
        avg_rtt = round(sum(rtts) / len(rtts), 2)
        
        # **[Fix]** Jitter calculation logic
        # Jitter is often calculated as the average difference between consecutive RTTs
        jitter = 0
        if len(rtts) > 1:
            jitter_sum = 0
            for j in range(1, len(rtts)):
                jitter_sum += abs(rtts[j] - rtts[j-1])
            jitter = round(jitter_sum / (len(rtts) - 1), 2)
        
        print('Round Trip Time (RTT) (in ms):')
        print(f'    Minimum = {min_rtt}ms, Maximum = {max_rtt}ms, Average = {avg_rtt}ms, Jitter = {jitter}ms')
    else:
        # **[Fix]** If all packets are lost, RTT stats are not applicable
        print('Round Trip Time (RTT) (in ms):')
        print('    (All packets lost, cannot calculate RTT)')

    print(f'Total transmission time: {total_time_ms} ms')
    
    client_socket.close()


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='A simple UDP Ping client')
    
    # Add arguments
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='The server host name or IP to ping (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=12000,
                        help='The server port number (default: 12000)')
    parser.add_argument('--count', type=int, default=15,
                        help='Number of ping packets to send (default: 15)')
    parser.add_argument('--timeout', type=float, default=0.6,
                        help='Timeout in seconds for each request (default: 0.6)')
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    # Run the ping
    run_ping(args.host, args.port, args.count, args.timeout)

if __name__ == '__main__':
    main()