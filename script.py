import random
from sympy import isprime
import base64
import sys
import argparse

def save_public_key(filename, n, e):
    with open(filename, 'w') as file:
        data = hex(n)[2:] + '\n' + hex(e)[2:]
        file.write(f'---begin {filename} public key---\n')
        file.write(base64.b64encode(str(data).encode()).decode() + '\n')
        file.write(f'---end {filename} key---\n')

def save_private_key(filename, n, d):
    with open(filename, 'w') as file:
        data = hex(n)[2:] + '\n' + hex(d)[2:]
        file.write(f'---begin {filename} private key---\n')
        file.write(base64.b64encode(str(data).encode()).decode() + '\n')
        file.write(f'---end {filename} key---\n')

def load_key(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        data = lines[1].strip()
        elements = base64.b64decode(data).decode('ascii').strip().split('\n')
        n = int(elements[0], 16)
        d = int(elements[1], 16)
    return n, d

def display_key(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        key = lines[1].strip()
    return key

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
    block_size = len(str(n)) - 1
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

class MonRSA:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Script monRSA par Guilhem Schira')
        self.parser.add_argument('commande', choices=['keygen', 'crypt', 'decrypt', 'help'], help='Commande à exécuter')
        self.parser.add_argument('cle', nargs='?', default='default_key', help='Fichier contenant la clé publique ("crypt") ou privée ("decrypt"). Clé par défaut: default_key')
        self.parser.add_argument('texte', nargs='?', help='Phrase à chiffrer ("crypt") ou déchiffrer ("decrypt")')
        self.parser.add_argument('-f', '--fichier', nargs=1, default=['monRSA'],type=str, help='Noms des fichiers de clé générés (par défaut: monRSA.pub monRSA.priv)')
        self.parser.add_argument('-s', '--size', nargs=1, default=[10], type=int, help='Tailles des clé générées (par défaut: 10)')


    def keygen(self,fichier, size):
        public_file = fichier[0] + ".pub"
        private_file = fichier[0] + ".priv"
        
        public_key, private_key = generate_keys(size[0])
        n, e = public_key
        n, d = private_key

        save_public_key(public_file, n, e)
        save_private_key(private_file, n, d)
        print(f'Génération de la paire de clé et sauvegarde dans {public_file} et {private_file}...')
        print("clé privée : {}".format(public_file))
        print("clé publique : {}".format(private_file))
        print("Clés sauvegardées")


    def crypt(self):
        cle = self.parser.parse_args().cle
        texte = self.parser.parse_args().texte
        # Logique pour chiffrer le texte avec la clé publique spécifiée ou par défaut
        print(f'Chiffrement du texte avec la clé {cle}...')

        #Modifier pour détecter
        encrypted_text = encrypt_with_public_key(texte, load_key(cle))
        print(f'Texte chiffré: {encrypted_text}')

    def decrypt(self):
        cle = self.parser.parse_args().cle
        texte = self.parser.parse_args().texte
        # Logique pour déchiffrer le texte avec la clé privée spécifiée
        print(f'Déchiffrement du texte avec la clé privée {cle}...')
        decrypted_text = decrypt_with_private_key(texte,load_key(cle))
        print(f'Texte déchiffré: {decrypted_text}')

    def run(self):
        args = self.parser.parse_args()

        if args.commande == 'help':
            self.parser.print_help()
        elif args.commande == 'keygen':
            self.keygen(args.fichier, args.size)
        elif args.commande == 'crypt':
            if args.cle is None or args.texte is None:
                print('Erreur: Les paramètres "cle" et "texte" sont obligatoires pour la commande "crypt".')
            else:
                self.crypt()
        elif args.commande == 'decrypt':
            if args.cle is None or args.texte is None:
                print('Erreur: Les paramètres "cle" et "texte" sont obligatoires pour la commande "decrypt".')
            else:
                self.decrypt()

if __name__ == '__main__':
    monRSA = MonRSA()
    monRSA.run()
