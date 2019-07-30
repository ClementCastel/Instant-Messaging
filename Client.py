import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("", 1111))

print("Connecté au server !")
valid = s.recv(9999999)
print(valid.decode())

name = input("Comment voulez-vous vous nommer ? ")
msg = input("Message : ")
r = ""
while r != "Disconnected":

    sendMsg = name + " # " + msg

    s.send(sendMsg.encode())

    print("--- Le message a été envoyé : '" + msg + "' ---")
    print()

    try:
        r = s.recv(9999999)  # On attends le message de confirmation avant de continuer
    except ConnectionResetError:
        sys.exit(0)

    if r.decode() == "Message recu par le server":
        msg = input("Message : ")
    else:
        sys.exit(0)
