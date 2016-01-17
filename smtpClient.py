import socket

__author__ = 'Gilad Barak'
__name__ = 'main'

MAIL_SERVER_IP = '54.213.229.251'
PORT = 587


def main():
    client_socket = socket.socket()
    client_socket.connect((MAIL_SERVER_IP, PORT))
    data = client_socket.recv(1024)
    print(data)
    client_socket.send("EHLO\r\n")
    data = client_socket.recv(1024)
    print(data)
    next = "\x00frusta@gmx.com\x00password!".encode('base64').replace('\n', '')
    print(next)
    client_socket.send("AUTH PLAIN " + next + '\r\n')
    data = client_socket.recv(1024)
    print(data)
    client_socket.send('MAIL FROM:<frusta@gmx.com>\r\n')
    data = client_socket.recv(1024)
    print(data)
    client_socket.send('RCPT TO:resha@bads.com\r\n')
    data = client_socket.recv(1024)
    print(data)
    client_socket.send('DATA\r\n')
    data = client_socket.recv(1024)
    print(data)
    client_socket.send('Subject: get Ready!\r\n\r\nbla bla\r\n.\r\n')
    data = client_socket.recv(1024)
    print(data)
    client_socket.send('QUIT\r\n')
    data = client_socket.recv(1024)
    print(data + "YAY")

if __name__ == "main":
    main()
