''' TODO :
ENTREE - Choix dans une liste :
    0 > Voir les participants
    1 > Voir les X derniers messages (demander ensuite X)
            >> Le serveur conservera tous les messages dans un tableau et l'indice auquel le dernier message
            du client est
    2 > Envoyer un message
            >> Chiffrer le message avant envoie avec la clé que le serveur fournira lors de la 1ere connection
            (utiliser Cipher.py)

'''

import random
import socket
import string
import sys


def choose_username():
    print("---------------------------------")
    print(" 0 : M'attribuer un pseudo")
    print(" 1 : Choisir un pseudo")
    print()
    choice = input("Choisir un nom d'utilisateur ? ")

    name = ""

    if choice == "0":
        for i in range(0, 8):
            name += random.choice(string.ascii_letters)
    else:
        name = input("Pseudo ? ")
    print("---------------------------------")
    return name


def listen():
    print("Ecoute")


'''

MAIN

'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("", 1111))

print("Connecté au server !")

key = s.recv(9999999)
print("Votre cle : " + key.decode())

s.send(choose_username().encode())

msg = input("Message : ")
r = ""
while r != "Disconnected":

    sendMsg = msg

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
