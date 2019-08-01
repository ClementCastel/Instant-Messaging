""" TODO :

METHODES :
    > Générer une clé
    > Chiffrer un message avec la clé fournie + message
    > Déchiffrer un message avec la clé fournie + message

"""


class Cipher(object):
    pass

    @staticmethod
    def crypt(key="", data=""):
        print("Chiffrer")
        print("Key : ")
        print(key)
        print("Data : ")
        print(data)
        return "Chiffré !"

    @staticmethod
    def decrypt(key="", data=""):
        print("DÉchiffrer")
        print("Key : ")
        print(key)
        print("Data : ")
        print(data)
        return "Déchiffré"
