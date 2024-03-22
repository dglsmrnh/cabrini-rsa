from socket import *
import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    if n % 5 == 0:
        return False

    d = n - 1
    while d % 2 == 0:
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        while d != n - 1:
            x = (x * x) % n
            d *= 2
            if x == 1:
                return False
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True

def generate_prime(bits):
    while True:
        n = random.getrandbits(bits)
        if n % 2 != 0:
            if is_prime(n):
                return n

def generate_keypair(bits):
    bits2 = bits // 2
    p = generate_prime(bits2)
    q = generate_prime(bits2)
    while p == q:
        q = generate_prime(bits2)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(message, public_key):
    """Criptografa uma mensagem usando a chave pública."""
    e, n = public_key
    encrypted_message = pow(int.from_bytes(message.encode(), 'big'), e, n)
    return encrypted_message

def decrypt(encrypted_message, private_key):
    """Descriptografa uma mensagem usando a chave privada."""
    d, n = private_key
    decrypted_message = pow(encrypted_message, d, n)
    return decrypted_message.to_bytes((decrypted_message.bit_length() + 7) // 8, 'big').decode()

connectedToServer = False

# Testando a geração de chave de 4096 bits
public_key, private_key = generate_keypair(4096)
print("Chave pública:", public_key)
print("Chave privada:", private_key)

# Converter a chave pública para uma sequência de bytes
serialized_public_key = "{}|{}".format(public_key[0], public_key[1])

serverName = "10.1.70.32"
serverPort = 15200
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
print(connectedToServer)
while True:

    if not connectedToServer:
        print ("Não conectou")
        # Receber a chave pública do servidor
        setence_public_key = clientSocket.recv(5000).decode()
        n, e = setence_public_key.split("|")

        server_public_key = int(n), int(e)

        print("Chave pública recebida:\n")
        print(server_public_key)

        connectedToServer = True

        clientSocket.send(bytes(serialized_public_key, "utf-8"))

    else:
        rawSentence = input("Input lowercase sentence: ")
        if not rawSentence == "":
            sentence = encrypt(rawSentence, server_public_key)
            clientSocket.send(bytes(str(sentence), "utf-8"))
            
            print("Waiting for answer...")

            response = int(clientSocket.recv(5000).decode())
            print(response)
            responseText = decrypt(response, private_key)
            print ("Received from Server: ", responseText)
        else:
            clientSocket.detach()
            connectedToServer = False
            break