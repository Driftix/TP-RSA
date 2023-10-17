import random
from sympy import isprime
import base64
import sys
import argparse
import os

class KeyManager:
    def __init__(self,params):
        self.params = params
 
    def generate_keys(self):
        name = self.params.name
        size = self.params.size

        p, q = self.__generate_prime(size), self.__generate_prime(size)
        while p == q:
            q = self.__generate_prime(size)

        n = p * q
        n_prime = (p - 1) * (q - 1)

        e = random.randint(2, n_prime - 1)
        while isprime(e) is False or n_prime % e == 0:
            e = random.randint(2, n_prime - 1)

        d = pow(e, -1, n_prime)

        return (n, e), (n, d)
    def __generate_prime(self, size):
        while True:
            num = random.randint(10**(size-1), 10**size - 1)
            if isprime(num):
                return num

    def generate_keys_b64(self):
        pub_key , priv_key = self.generate_keys()
        n1 , e  = pub_key
        n2 , d = priv_key
        if n1 == n2:
            pub_key_b64 = base64.b64encode(str(hex(n1)[2:] + '\n' + hex(e)[2:]).encode()).decode()
            priv_key_b64 = base64.b64encode(str(hex(n2)[2:] + '\n' + hex(d)[2:]).encode()).decode()
        else :
            raise SystemExit("Mauvais calcul de n")
        return pub_key_b64 , priv_key_b64

class KeyParameters():
    def __init__(self, name, size):
        self.name = name
        self.size = size
    
class FileManager():

    def save_key(self, filename, fileType, key):
        if fileType == "public key":
            file = filename + ".pub"
        elif fileType == "private key":
            file = filename + ".priv"
        else:
            raise SystemExit("FileType invalid")

        with open(file,'w') as f:
            f.write(f'---begin {filename} {fileType}---\n')
            f.write(key + '\n')
            f.write(f'---end {filename} key---\n')

    def load_key(self, filename, fileType):
        if fileType == "public key":
            file = filename + ".pub"
        elif fileType == "private key":
            file = filename + ".priv"
        else:
            raise SystemExit("FileType invalid")

        with open(file ,'r') as f:
            line = f.readlines()
            verification_line = line[0]
            if verification_line  == f'---begin {filename} {fileType}---\n':
                return line[1].strip()
            else:
                raise SystemExit("Format de fichier non valide")
            
    def readText(self, path):
        try : 
            f = open(path, 'r')
            text = f.read()
            f.close()
            return text
        except Exception:
            raise SystemExit("Path en entrée invalide")

    def writeText(self, path, text):
        try :
            f = open(path,'w')
            f.write(text)
            f.close()
        except Exception:
            raise SystemExit("Path en entrée invalide")


class Utils():
    def encrypt(self, message, public_key):
        n, e = public_key
        numeric_message = [ord(char) for char in message]
        encrypted_blocks = []
        for char_code in numeric_message:
            encrypted_blocks.append(pow(char_code, e, n))
        encrypted_text = base64.b64encode(str(encrypted_blocks).encode('ascii')).decode()
        return encrypted_text

    def decrypt(self, encrypted_text, private_key):
        n , d = private_key
        encrypted_blocks = base64.b64decode(encrypted_text.encode()).decode('ascii')
        encrypted_blocks = list(map(int, encrypted_blocks.strip('[]').split(', ')))
        decrypted_blocks = [pow(block, d, n) for block in encrypted_blocks]
        decrypted_message = ''.join([chr(block) for block in decrypted_blocks])
        return decrypted_message
    
    def decompose(self, key_b64):
        elements = base64.b64decode(key_b64).decode('ascii').strip().split('\n')
        n = int(elements[0], 16)
        de = int(elements[1], 16)
        return n , de
    
    def delete_files(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        extensions_a_supprimer = ['.pub', '.priv', '.txt']
        try:
            files = os.listdir(folder)
            for file in files:
                if file.endswith(tuple(extensions_a_supprimer)):
                    path = os.path.join(folder, file)
                    os.remove(path)
                    print(f'Le fichier {file} a été supprimé avec succès.')        
        except Exception:
            raise SystemExit("Erreur lors de la suppression des fichiers")


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Script monRSA par Guilhem Schira')
        self.parser.add_argument('commande', choices=['keygen', 'crypt', 'decrypt', 'clean', 'help'], help='Commande à exécuter')
        self.parser.add_argument('cle', nargs='?', help='Fichier contenant la clé publique ("crypt") ou privée ("decrypt").')
        self.parser.add_argument('texte', nargs='?', help='Phrase à chiffrer ("crypt") ou déchiffrer ("decrypt")')
        self.parser.add_argument('-f', '--fichier', nargs=1, default=['monRSA'],type=str, help='Noms des fichiers de clé générés (par défaut: monRSA.pub monRSA.priv)')
        self.parser.add_argument('-s', '--size', nargs=1, default=[10], type=int, help='Tailles des clé générées (par défaut: 10)')
        self.parser.add_argument('-i', '--input', nargs=1 ,help='Accepte un fichier texte à la place d\'une chaine (path)')
        self.parser.add_argument('-o', '--output', nargs=1 ,help='Sauvegarde le resultat de cryptage ou decryptage dans un fichier nommé (path)')
    
    def run(self):
        command = Commands()
        args = self.parser.parse_args()
        if args.commande == 'help':
            self.parser.print_help()
        elif args.commande == 'keygen':
            command.keygen(args.fichier, args.size)
        elif args.commande == 'crypt':
            if args.cle is None or args.texte is None and args.input is None:
                print('Erreur: Les paramètres "cle" et "texte" sont obligatoires pour la commande "crypt".')
            else:
                command.crypt(args.input, args.output)
        elif args.commande == 'decrypt':
            if args.cle is None or args.texte is None and args.input is None:
                print('Erreur: Les paramètres "cle" et "texte" sont obligatoires pour la commande "decrypt".')
            else:
                command.decrypt(args.input, args.output)
        elif args.commande == 'clean':
            confirmation = input(f'Voulez-vous vraiment supprimer tous les fichiers .pub, .priv, .txt à la racine du projet ? (o/n)').strip().lower()
            if confirmation == 'o':
                command.clean()
            else:
                print("abandon de la suppression")

class Commands(CLI):
    def __init__(self):
        super().__init__()
        self.file_Manager = FileManager()
        self.utils = Utils()

    def keygen(self,fichier, size):
        size = size[0]
        fileName = fichier[0]

        key_params = KeyParameters(fileName, size)
        key_Manager = KeyManager(key_params)
        public_key_b64 , private_key_b64 = key_Manager.generate_keys_b64()

        self.file_Manager.save_key(fileName, "public key", public_key_b64)
        self.file_Manager.save_key(fileName, "private key", private_key_b64)

        print(f'Génération de la paire de clé et sauvegarde dans {fileName + ".pub"} et {fileName + ".priv"}...')

    def crypt(self, i, o):
        if(i):
            #Lecture du fichier comportant le texte
            text = self.file_Manager.readText(i[0])
        else : 
            #Sinon on prend le texte entré en argument
            text = self.parser.parse_args().texte
        #récupère le nom de la clé
        cle = self.parser.parse_args().cle
        public_key_b64 = self.file_Manager.load_key(cle, "public key")
        public_key = self.utils.decompose(public_key_b64)
        #Encryption du texte
        encrypted_text = self.utils.encrypt(text, public_key)
        #Si params output
        if(o):
            #On écrit un fichier avec le nom du params et on y met la chaine chiffrée
            self.file_Manager.writeText(o[0],encrypted_text)
            print(f'Texte chiffré et sauvegardé : {o[0]}')
        else :
            #Sinon on donne la chaine chiffrée en ligne de commande
            print(f'Texte chiffré: {encrypted_text}')

    def decrypt(self, i, o):
        #Si params input
        if(i):
            text = self.file_Manager.readText(i[0])
        else :
            #Sinon on prend le texte entré en argument
            text = self.parser.parse_args().texte

        #récupère le nom de la clé
        cle = self.parser.parse_args().cle
        private_key_b64 = self.file_Manager.load_key(cle, "private key")
        private_key = self.utils.decompose(private_key_b64)
        #Encryption du texte
        decrypted_text = self.utils.decrypt(text, private_key)
        #Si params output
        if(o):
            #On écrit un fichier avec le nom du params et on y met la chaine chiffrée
            self.file_Manager.writeText(o[0], decrypted_text)
            print(f'Texte chiffré et sauvegardé : {o[0]}')
        else :
            #Sinon on donne la chaine chiffrée en ligne de commande
            print(f'Texte chiffré: {decrypted_text}')
    
    def clean(self):
        self.utils.delete_files()

if __name__ == '__main__':
    cli = CLI()
    cli.run()







    

    
