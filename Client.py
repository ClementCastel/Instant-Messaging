""" TODO :
ENTREE - Choix dans une liste :
    0 > Voir tous les messages
    1 > Voir les X derniers messages (demander ensuite X)
            >> Le serveur conservera tous les messages dans un tableau et l'indice auquel le dernier message
            du client est
    2 > Envoyer un message
            >> Chiffrer le message avant envoie avec la clé que le serveur fournira lors de la 1ere connection
            (utiliser Cipher.py)

"""

import random
import socket
import string
import sys
import pickle


def choose_username():
    print("-"*24)
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
    print("-"*24)
    return name


def getMsg():
    print("-"*24)
    print(" 0 : Envoyer un message")
    print(" 1 : Voir les N dernier messages")
    print(" 2 : Voir tous les messages")
    print(" 3 : Quitter")
    print()
    choice = input("Choix ? ")
    if choice == "0":
        message = input("Message ? ")
        print("-"*24)

        return message
    elif choice == "1":
        n = input("n = ")
        print("-" * 24)

        return "/msgn " + str(n)
    elif choice == "3":
        return "/exit"
    else:
        print("-" * 24)
        return "/msgs"


'''

MAIN

'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("", 1111))

print("Connecté au server !")

key = s.recv(9999999)
print("Votre cle : " + key.decode())

s.send(choose_username().encode())

sendMsg = ""

while sendMsg != "/exit":

    sendMsg = getMsg()

    s.send(sendMsg.encode())  # Encode le message généré
    dataB = s.recv(999999)  # Recoit une reponse

    data = pickle.loads(dataB)

    if isinstance(data, list):
        print(*data, sep="\n")

    else:
        print("Message envoyé au serveur avec succès !")
    print("-"*24)

