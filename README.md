# slowlorisE
A simple Slowloris HTTP DoS attack tool, destroyer of worlds (or at least unpatched threaded servers).

slowlorisE is written in Python and allows the user to perform a Slowloris attack on a selected target, using a specified port number, amount of connections and sending delay.

Tested on a server running Apache 2.4.18.

## What/why
Slowloris is a simple and elegant denial of service attack that uses minimal bandwidth. It relies on the fact that the HTTP protocol by design requires requests to be completely received by the server before they are processed. Slowloris establishes many simultaneous connections to the victim server and holds these open for as long as possible by very slowly sending HTTP headers, but never completing the requests. This keeps the server busy waiting for the rest of the data, and if the maximum current connection pool is filled, actual clients attempting to connect to the server will fail.

This tool can be used to test for vulnerability against such attacks.

## Usage
slowlorisE.py [-h] -t TARGET [-p PORT] [-s SOCKETS] [-i INTERVAL]

Example: python slowlorisE.py -t 127.0.0.1 -p 80 -s 200 -i 10<br>
Performs an attack on 127.0.0.1:80 using 200 simultaneous connections and a 10 second interval between sending headers.

## Important
This program was written for educational purposes. Use responsibly and do not point the tool at servers that you do not own/control. It's illegal and you are liable for damage caused.
