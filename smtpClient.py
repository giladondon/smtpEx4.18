import socket

__author__ = 'Gilad Barak'
__name__ = 'main'

MAIL_SERVER_IP = '54.213.229.251'
PORT = 587
TEMPLATE_SPACE = "\x00"
HELLO_SERVER = "EHLO\r\n"
KB = 1024
MAIL_DATA_STARTS = "DATA\r\n"
MAIL_FROM = 'MAIL FROM:<{}>\r\n'
RCPT_TO = 'RCPT TO:{}\r\n'
MAIL = 'Subject: {}\r\n\r\n{}\r\n.\r\n'
END_CONNECTION = 'QUIT\r\n'
BASE64 = 'base64'
AUTHENTICATION = "AUTH PLAIN {}\r\n"
NEW_LINE = '\n'
EMPTY = ''
USER_NAME_INDEX = 0
PASSWORD_INDEX = 1
RCPT_TO_INDEX = 0
SUBJECT_INDEX = 1
MAIL_DATA_INDEX = 2


def get_user_details():
    """
    return : tuple of user_name, password from user input
    """
    user_name = raw_input("Username: ")
    password = raw_input("Password: ")
    return user_name, password


def detail_mail():
    """
    return : tuple of rcpt_to, subject, mail data from user input
    """
    rcpt_to = raw_input("Who would you like to send your e-mail to?\r\n")
    subject = raw_input("What is the subject of your message?\r\n")
    mail = raw_input("Type your single line message now.\r\n")
    return rcpt_to, subject, mail


def build_socket():
    """
    Connects to SMTP server and receives first data
    """
    client_socket = socket.socket()
    client_socket.connect((MAIL_SERVER_IP, PORT))
    data = client_socket.recv(KB)
    return client_socket


def hello_socket(client_socket):
    """
    Says hello to server on the other side of socket
    """
    client_socket.send(HELLO_SERVER)
    data = client_socket.recv(KB)


def set_up_mail(user, client_socket):
    """
    Checks user authorizations and sends them encoded to server.
    """
    details = (TEMPLATE_SPACE + user[USER_NAME_INDEX] + TEMPLATE_SPACE + user[PASSWORD_INDEX])\
        .encode(BASE64).replace(NEW_LINE, EMPTY)
    client_socket.send(AUTHENTICATION.format(details))
    data = client_socket.recv(KB)
    client_socket.send(MAIL_FROM.format(user[USER_NAME_INDEX]))
    data = client_socket.recv(KB)


def send_mail(user_data, client_socket):
    """
    Sends mail to server using input from user
    """
    client_socket.send(RCPT_TO.format(user_data[RCPT_TO_INDEX]))
    data = client_socket.recv(KB)
    client_socket.send(MAIL_DATA_STARTS)
    data = client_socket.recv(KB)
    client_socket.send(MAIL.format(user_data[SUBJECT_INDEX], user_data[MAIL_DATA_INDEX]))
    data = client_socket.recv(KB)


def say_bye(client_socket):
    """
    Cuts connection with server
    """
    client_socket.send(END_CONNECTION)
    data = client_socket.recv(KB)
    client_socket.close()


def main():
    """
    Manages the process of sending an e-mail as described in excercise 4.18
    """
    client_socket = build_socket()
    hello_socket(client_socket)
    user = get_user_details()
    set_up_mail(user, client_socket)
    user_data = detail_mail()
    send_mail(user_data, client_socket)
    say_bye(client_socket)

if __name__ == "main":
    main()
