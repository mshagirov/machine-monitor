import socket

def check_connection(host="8.8.8.8", port=53, timeout=3):
    """A quick method to check connection to a host (AF_INET address).

    - host   : IP or hostname (str)
    - port   : port number (int)
    - timeout: timeout in seconds (float|int)

    https://stackoverflow.com/a/33117579/12324002
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True, None
    except socket.error as e:
        return False, f"{e}{type(e)}"

