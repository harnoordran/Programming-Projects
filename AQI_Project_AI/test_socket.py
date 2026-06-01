import socket
import sys

def test_bind(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', port))
        s.listen(1)
        print(f"Successfully bound to 127.0.0.1:{port}")
        s.close()
        return True
    except Exception as e:
        print(f"Failed to bind to 127.0.0.1:{port}: {e}")
        return False

if __name__ == "__main__":
    test_bind(8501)
    test_bind(8080)
    test_bind(0) # Let OS pick a port
