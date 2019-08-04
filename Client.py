import random
import socket
import string
import pickle
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random

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

keyServer = pickle.loads(s.recv(9999999)).decode()

print("Cle publique Serveur : ")
print(keyServer)
cipherE = PKCS1_OAEP.new(RSA.importKey(keyServer))
print(cipherE)
print("--")

# RSA
randomGenerator = Random.new().read
keys = RSA.generate(2048, randomGenerator)  # 2048 bits
publicKey = keys.publickey().exportKey('PEM')

cipherD = PKCS1_OAEP.new(keys)  # Déchiffre

s.send(choose_username().encode())
s.send(pickle.dumps(publicKey))  # Clé publique client

sendMsg = ""

while sendMsg != "/exit":

    sendMsg = getMsg()

    print("Message envoyé : ")
    print(cipherE.encrypt(sendMsg.encode()))
    s.send(cipherE.encrypt(sendMsg.encode()))  # Encode le message généré
    dataB = s.recv(999999)  # Recoit une reponse

    print("Recu")
    print(dataB)
    print("--")

    data = pickle.loads(cipherD.decrypt(dataB))

    if isinstance(data, list):
        print(*data, sep="\n")

    else:
        print("Message envoyé au serveur avec succès !")
    print("-"*24)

