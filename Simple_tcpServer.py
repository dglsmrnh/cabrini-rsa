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
    p = generate_prime(bits)
    q = generate_prime(bits)
    while p == q:
        q = generate_prime(bits)

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



# Testando a geração de chave de 4096 bits
public_key, private_key = generate_keypair(4096)
print("Chave pública:", public_key)
print("Chave privada:", private_key)

# Converter a chave pública para uma sequência de bytes
serialized_public_key = "{}|{}".format(public_key[0], public_key[1])

encrypt_test = encrypt("The information security is of significant importance to ensure the privacy of communications", public_key)
print("\Palavra criptografada:")
print(encrypt_test)

decrypt_test = decrypt(encrypt_test, private_key)
print("\Palavra descriptografada:")
print(decrypt_test)

serverPort = 15200

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)  # The argument "listen" tells the socket library that we want to queue up to 5 connection requests (usually the maximum) before starting to refuse external connections. If the rest of the code is written correctly, this should be enough.
print("TCP Server\n")

while True:  # Keep the server running indefinitely
    try:
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection from {addr} established.")

        # Enviar a chave pública para o cliente
        # serverSocket.sendall(bytes(str(serialized_public_key), "utf-8"))

        isFirst = True
        isSecond = False
        client_public_key = (public_key, private_key)

        while True:  # Communicate with the client until the client closes the connection
            
            if isFirst:
                isFirst = False
                isSecond = True

                connectionSocket.send(bytes(serialized_public_key, "utf-8"))
            elif isSecond:
                isSecond = False
                serialized_public_key = connectionSocket.recv(5000)
                n, e = serialized_public_key.split("|")
                client_public_key = (int(n), int(e))
            else:
                sentence = connectionSocket.recv(5000)
                if not sentence:  # If the client closes the connection, break out of the loop
                    break
                
                received = sentence
                print("Received From Client:", received)
                decryptedSentence = decrypt(received, private_key)
                
                print("decrypted sentence:", decryptedSentence) 

                encryptedSentence = encrypt(received.upper(), client_public_key)

                connectionSocket.send(bytes(encryptedSentence, "utf-8"))

    except ConnectionResetError as e:
        print(f"Connection reset by peer: {e}")
    except Exception as e:
        print(f"Error receiving data: {e}")
    print("waiting for connection")

serverSocket.close()  # Close the server socket when done
