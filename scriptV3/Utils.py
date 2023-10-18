import base64
import os

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