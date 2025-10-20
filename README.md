## Features

* **Client & Server:** Includes both the client (`udp_ping_client.py`) and a simple echo server (`udp_echo_server.py`).
* **Configurable:** Easily set the host, port, packet count, and timeout via command-line arguments.
* **Network Statistics:** Automatically calculates and displays:
    * Minimum, Maximum, and Average RTT (Round Trip Time)
    * Packet Loss Percentage
    * Jitter (the variation in RTT)
* **Cross-Platform:** Written in standard Python, compatible with Windows, macOS, and Linux.

## Requirements

* Python 3 (No external libraries are required)

## Usage

This project consists of two scripts:

* `udp_echo_server.py`: The server that listens for packets and echoes them back.
* `udp_ping_client.py`: The client that sends packets and measures performance.

### 1. Start the Server

On your server or local machine, open a terminal and run the server script. By default, it listens on port 12000 on all interfaces.
```bash
python udp_echo_server.py
```
You can also specify a different port or host:
```bash
python udp_echo_server.py --port 15000 --host 127.0.0.1
```
### 2. Run the Client
On another machine (or in a second terminal on the same machine), run the client script, pointing it at the server.
* **To test a local server:**
```bash
python udp_ping_client.py --host 127.0.0.1 --port 12000
```

* **To test a remote server (e.g., at IP 8.8.8.8) with 20 packets:**
```bash
python udp_ping_client.py --host 8.8.8.8 --port 12000 --count 20
```

* **See all available options:**
```bash
python udp_ping_client.py --help
```
This will output:
```bash
usage: udp_ping_client.py [-h] [--host HOST] [--port PORT] [--count COUNT] [--timeout TIMEOUT]

A simple UDP Ping client

options:
  -h, --help         show this help message and exit
  --host HOST        The server host name or IP to ping (default: 127.0.0.1)
  --port PORT        The server port number (default: 12000)
  --count COUNT      Number of ping packets to send (default: 15)
  --timeout TIMEOUT  Timeout in seconds for each request (default: 0.6)
```

###  Example output:
Here is an example of running the client against a local server:
```bash
$ python udp_ping_client.py --host 127.0.0.1 --count 5
Pinging 127.0.0.1 (127.0.0.1) [Port: 12000] with 5 packets:
Reply from 127.0.0.1: seq=43001, rtt=0.99 ms
Reply from 127.0.0.1: seq=43002, rtt=1.20 ms
Reply from 127.0.0.1: seq=43003, rtt=0.85 ms
Request timed out: seq=43004
Reply from 127.0.0.1: seq=43005, rtt=1.05 ms

--- 127.0.0.1 Ping Statistics ---
    Packets: Sent = 5, Received = 4, Lost = 1 (20.0% loss)
Round Trip Time (RTT) (in ms):
    Minimum = 0.85ms, Maximum = 1.20ms, Average = 1.02ms, Jitter = 0.15ms
Total transmission time: 1045.32 ms
```


