import socket
import threading
from datetime import datetime
import pickle
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

global names


class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):

        print("Connexion de %s %s" % (self.ip, self.port,))
        self.clientsocket.send(pickle.dumps(publicKey))  # clé publique du serveur
        self.name = self.clientsocket.recv(9999999).decode()
        keyClient = pickle.loads(self.clientsocket.recv(9999999)).decode()
        print("Clé C :")
        print(keyClient)
        print("--")
        cipherE = PKCS1_OAEP.new(RSA.importKey(keyClient))  # Chiffre
        print("CipherE of C ok")

        msg = ""

        while "/exit" not in msg:  # Tant que pas de deconnexion

            r = self.clientsocket.recv(9999999)
            msg = cipherD.decrypt(r).decode()  # Le décode
            print(msg)

            ''' Message possible :
                - /msgs : Envoyer tous les messages : list
                - /msgn X : Envoyer les X derniers messages : list
                - autre : Message normal à ajouter à la liste : "code 0"
            '''

            if "/exit" in msg:
                continue  # On va à la fin de la boucle

            elif "/msgs" in msg:
                dataB = pickle.dumps(data)  # List(tuples) to bytes before sending it to C

            elif "/msgn" in msg:
                n = int(msg.split(" ")[1])
                dataB = pickle.dumps(data[-n:])

            else:
                now = datetime.now()
                data.append((now.strftime("%H:%M:%S"), self.name, msg))
                dataB = pickle.dumps("code 0".encode())

            self.clientsocket.send(cipherE.encrypt(dataB))
        else:
            self.clientsocket.send(pickle.dumps("Disconnected".encode()))
            print("Fin")


data = []  # (date, name, msg)

# RSA
randomGenerator = Random.new().read
keys = RSA.generate(2048, randomGenerator)  # 2048 bits
publicKey = keys.publickey().exportKey('PEM')

cipherD = PKCS1_OAEP.new(keys)  # Déchiffre

# Création du socket serveur
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("", 1111))

while True:
    # Gestion des Threads pour les clients
    tcpsock.listen(30)
    print("En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()
