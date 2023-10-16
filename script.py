import random
from sympy import isprime
import base64

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

def generate_keys():
    p, q = generate_prime(), generate_prime()
    while p == q:
        q = generate_prime()

    n = p * q
    n_prime = (p - 1) * (q - 1)

    e = random.randint(2, n_prime - 1)
    while isprime(e) is False or n_prime % e == 0:
        e = random.randint(2, n_prime - 1)

    d = pow(e, -1, n_prime)

    return (n, e), (n, d)

def generate_prime():
    while True:
        num = random.randint(10**9, 10**10 - 1)
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
    n, d = private_key
    encrypted_blocks = base64.b64decode(encrypted_text.encode()).decode('ascii')
    encrypted_blocks = list(map(int, encrypted_blocks.strip('[]').split(', ')))
    decrypted_blocks = [pow(block, d, n) for block in encrypted_blocks]
    decrypted_message = ''.join([chr(block) for block in decrypted_blocks])
    return decrypted_message

if __name__ == "__main__":
    public_key, private_key = generate_keys()
    n, e = public_key
    n, d = private_key


    print("clé privée {}".format(public_key))
    print("clé publique {}".format(private_key))


    save_public_key('monRSA.pub', n, e)
    save_private_key('monRSA.priv', n, d)

    print("Clés générées et sauvegardées avec succès.")

    message = "zone à danger"
    public_key_file = load_key('monRSA.pub')
    encrypted_text = encrypt_with_public_key(message, public_key_file)
    print("Texte chiffré : {}".format(encrypted_text))

    private_key_file = load_key('monRSA.priv')
    decrypted_text = decrypt_with_private_key(encrypted_text, private_key_file)
    print("Texte déchiffré : {}".format(decrypted_text))
