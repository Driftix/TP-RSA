import argparse
from FileManager import FileManager
from Utils import Utils
from KeyManager import KeyParameters, KeyManager

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