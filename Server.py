''' TODO :

LANCEMENT:
    > Demander si l'on veut proteger le serveur avec un mot de passe

NOUVEAU CLIENT :
    > Créer une clé pour chiffrer les messages (utiliser Cipher.py)
    > Lui transmettre
    > Attribuer un ID unique que l'on affichera avec son message
        >> [date] [nom] # [ID] : [message]

ARRET :
    > Quand il y a eu au moins 1 client de créé et que tous les clients ont été fermés
    > threading.activeCount() retourne le nombre de Threads actifs


'''

import socket
import threading

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):

        i = 0
        print("Connexion de %s %s" % (self.ip, self.port,))
        self.clientsocket.send("Vous etes connecté au serveur !".encode())
        msg = ""

        while "# deco" not in msg:  # Tant que pas de message de deconnexion

            print("Ecoute")
            r = self.clientsocket.recv(9999999)  # On recoit un message
            print(i)  # On affiche le nombre de fois que l'on a écouté le port
            msg = r.decode()  # Le décode

            if "# deco" not in msg:  # Si le message a été envoyé par un client

                print(msg)
                self.clientsocket.send("Message recu par le server".encode())  # On envoie un message de confirmation

            i += 1
        else:
            self.clientsocket.send("Disconnected".encode())
            print("Fin")


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
