import socket
import threading
import time

def server_function(server_socket):
    try:
        print("Waiting for a connection...")
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        conn.close()
    except OSError:
        print("Server socket closed.")
    finally:
        server_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 12345))
server.listen(1)

server_thread = threading.Thread(target=server_function, args=(server,))
server_thread.start()

# Simulate shutdown after 5 seconds
time.sleep(5)
print("Shutting down server...")
server.shutdown(socket.SHUT_RDWR)
server.close()
server_thread.join()
