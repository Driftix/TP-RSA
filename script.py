import random
from sympy import isprime
import base64
import sys
import argparse
import os


def save_public_key(filename, n, e):
    with open(filename, 'w') as file:
        filename = filename.replace('.pub','')
        #On formate la clé pour pourvoir l'enregister
        data = hex(n)[2:] + '\n' + hex(e)[2:]
        file.write(f'---begin {filename} public key---\n')
        file.write(base64.b64encode(str(data).encode()).decode() + '\n')
        file.write(f'---end {filename} key---\n')

def save_private_key(filename, n, d):
    with open(filename, 'w') as file:
        filename = filename.replace('.priv','')
        #On formate la clé pour pourvoir l'enregister
        data = hex(n)[2:] + '\n' + hex(d)[2:]
        file.write(f'---begin {filename} private key---\n')
        file.write(base64.b64encode(str(data).encode()).decode() + '\n')
        file.write(f'---end {filename} key---\n')


#rajouter la fonction isprime de miller Rabin
def load_key(filename):
    with open(filename, 'r') as file:
       
        lines = file.readlines()
        #Vérifier que le fichiers comporte bien la première ligne
        data = lines[1].strip()
        elements = base64.b64decode(data).decode('ascii').strip().split('\n')
        n = int(elements[0], 16)
        d = int(elements[1], 16)
        # else:
        #     raise BadFormat
    return n, d

def generate_keys(size):
    p, q = generate_prime(size), generate_prime(size)
    while p == q:
        q = generate_prime(size)

    n = p * q
    n_prime = (p - 1) * (q - 1)

    e = random.randint(2, n_prime - 1)
    while isprime(e) is False or n_prime % e == 0:
        e = random.randint(2, n_prime - 1)

    d = pow(e, -1, n_prime)

    return (n, e), (n, d)

def generate_prime(size):
    while True:
        num = random.randint(10**(size-1), 10**size - 1)
        if isprime(num):
            return num

def encrypt_with_public_key(message, public_key):
    n, e = public_key
    numeric_message = [ord(char) for char in message]
    encrypted_blocks = []
    for char_code in numeric_message:
        encrypted_blocks.append(pow(char_code, e, n))
    encrypted_text = base64.b64encode(str(encrypted_blocks).encode('ascii')).decode()
    return encrypted_text

def decrypt_with_private_key(encrypted_text, private_key):
    n , d = private_key
    encrypted_blocks = base64.b64decode(encrypted_text.encode()).decode('ascii')
    encrypted_blocks = list(map(int, encrypted_blocks.strip('[]').split(', ')))
    decrypted_blocks = [pow(block, d, n) for block in encrypted_blocks]
    decrypted_message = ''.join([chr(block) for block in decrypted_blocks])
    return decrypted_message


def supprimer_fichiers():
    dossier = os.path.dirname(os.path.abspath(__file__))
    extensions_a_supprimer = ['.pub', '.priv', '.txt']
    try:
        fichiers = os.listdir(dossier)
        for fichier in fichiers:
            if fichier.endswith(tuple(extensions_a_supprimer)):
                chemin_fichier = os.path.join(dossier, fichier)
                os.remove(chemin_fichier)
                print(f'Le fichier {fichier} a été supprimé avec succès.')        
    except OSError as e:
        print(f"Erreur: {e}")

class BadFormat(Exception):
    def __init__(self, message="Le format du fichier n'est pas bon"):
        self.message = message
        super().__init__(self.message)

class MonRSA:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Script monRSA par Guilhem Schira')
        self.parser.add_argument('commande', choices=['keygen', 'crypt', 'decrypt', 'clean', 'help'], help='Commande à exécuter')
        self.parser.add_argument('cle', nargs='?', help='Fichier contenant la clé publique ("crypt") ou privée ("decrypt").')
        self.parser.add_argument('texte', nargs='?', help='Phrase à chiffrer ("crypt") ou déchiffrer ("decrypt")')
        self.parser.add_argument('-f', '--fichier', nargs=1, default=['monRSA'],type=str, help='Noms des fichiers de clé générés (par défaut: monRSA.pub monRSA.priv)')
        self.parser.add_argument('-s', '--size', nargs=1, default=[10], type=int, help='Tailles des clé générées (par défaut: 10)')
        self.parser.add_argument('-i', '--input', nargs=1 ,help='Accepte un fichier texte à la place d\'une chaine (path)')
        self.parser.add_argument('-o', '--output', nargs=1 ,help='Sauvegarde le resultat de cryptage ou decryptage dans un fichier nommé (path)')
        
    def keygen(self,fichier, size):
        #Si le nom de la clé est renseignée on la récupère sinon on prends le nom par défaut "monRSA"
        public_file = fichier[0] + ".pub"
        private_file = fichier[0] + ".priv"
        #On génère les clés
        public_key, private_key = generate_keys(size[0])
        n, e = public_key
        n, d = private_key
        #On sauvegarde les clés dans des fichiers 
        save_public_key(public_file, n, e)
        save_private_key(private_file, n, d)
        print(f'Génération de la paire de clé et sauvegarde dans {public_file} et {private_file}...')

    def crypt(self, i,o ):
        #Si params input
        if(i):
            try : 
                #Lecture du fichier comportant le texte
                f = open(i[0], 'r')
                texte = f.read()
                f.close()
            except :
                print("Path en entrée invalide")
                exit()
        else : 
            #Sinon on prend le texte entré en argument
            texte = self.parser.parse_args().texte

        #récupère le nom de la clé
        cle = self.parser.parse_args().cle + ".pub"

        #Encryption du texte
        encrypted_text = encrypt_with_public_key(texte, load_key(cle))

        #Si params output
        if(o):
            #On écrit un fichier avec le nom du params et on y met la chaine chiffrée
            f = open(o[0],'w')
            f.write(encrypted_text)
            f.close()
            print("Fichier " + o[0] + " enregistré")
        else :
            #Sinon on donne la chaine chiffrée en ligne de commande
            print(f'Texte chiffré: {encrypted_text}')

    def decrypt(self, i, o):
        #Si params input
        if(i):
            try : 
                #Lecture du fichier comportant le texte
                f = open(i[0], 'r')
                texte = f.read()
                f.close()
            except :
                print("Path en entrée invalide")
                exit()
        else :
            #Sinon on prend le texte entré en argument
            texte = self.parser.parse_args().texte

        #récupère le nom de la clé
        cle = self.parser.parse_args().cle + ".priv"
        print(f'Déchiffrement du texte avec la clé privée {cle}...')
        decrypted_text = decrypt_with_private_key(texte,load_key(cle))
        #Si params output
        if(o):
            #On écrit un fichier avec le nom du params et on y met la chaine chiffrée
            f = open(o[0],'w')
            f.write(decrypted_text)
            f.close()
            print("Fichier " + o[0] + " enregistré")
        else :
            #Sinon on donne la chaine chiffrée en ligne de commande
            print(f'Texte chiffré: {decrypted_text}')

    def run(self):
        args = self.parser.parse_args()

        if args.commande == 'help':
            self.parser.print_help()
        elif args.commande == 'keygen':
            self.keygen(args.fichier, args.size)
        elif args.commande == 'crypt':
            if args.cle is None or args.texte is None and args.input is None:
                print('Erreur: Les paramètres "cle" et "texte" sont obligatoires pour la commande "crypt".')
            else:
                self.crypt(args.input, args.output)
        elif args.commande == 'decrypt':
            if args.cle is None or args.texte is None and args.input is None:
                print('Erreur: Les paramètres "cle" et "texte" sont obligatoires pour la commande "decrypt".')
            else:
                self.decrypt(args.input, args.output)
        elif args.commande == 'clean':
            confirmation = input(f'Voulez-vous vraiment supprimer tous les fichiers .pub, .priv, .txt à la racine du projet ? (o/n)').strip().lower()
            if confirmation == 'o':
                supprimer_fichiers()
            else:
                print("abandon de la suppression")

if __name__ == '__main__':
    monRSA = MonRSA()
    monRSA.run()