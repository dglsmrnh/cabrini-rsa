from socket import *
import random
import gmpy2

def is_prime(n, k=5):
    """Função para verificar se um número é provavelmente primo."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0 or n % 5 == 0 or n % 7 == 0:
        return False

    # Teste de primalidade de Fermat
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False

    return True

def generate_large_prime(bits):
    """Função para gerar um número primo de 'bits' de tamanho."""
    while True:
        # Gerar um número aleatório com o número de bits especificado
        p = random.getrandbits(bits)
        
        # Certificar-se de que o número tenha o número correto de bits
        p |= (1 << bits - 1) | 1
        
        # Verificar se o número é primo
        if is_prime(p):
            return p
        
def generate_large_prime(bits):
    """Função para gerar um número primo de 'bits' de tamanho."""
    while True:
        # Gerar um número aleatório com o número de bits especificado
        p = random.getrandbits(bits)
        
        # Certificar-se de que o número tenha o número correto de bits
        p |= (1 << bits - 1) | 1
        
        # Verificar se o número é primo
        if is_prime(p):
            return p

def gcd(a, b):
    """Calcula o maior divisor comum entre dois números."""
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd_recursive(a, b):
    """Calcula o máximo divisor comum estendido de a e b, e os coeficientes x e y."""
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd_recursive(b % a, a)
        return g, x - (b // a) * y, y
    
def extended_gcd(a, b):
    """Calcula o máximo divisor comum estendido de a e b, e os coeficientes x e y."""
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y

def mod_inverse(a, m):
    """Calcula o inverso modular de 'a' módulo 'm'."""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Não há inverso modular para o número ' + str(a) + ' módulo ' + str(m))
    else:
        return x % m

def generate_keypair(prime1, prime2):
    """Gera um par de chaves RSA."""
    n = prime1 * prime2
    phi = (prime1 - 1) * (prime2 - 1)

    # Escolha do expoente público (e)
    while True:
        e = random.randint(2, phi - 1)
        if gcd(e, phi) == 1:
            break

    # Cálculo do expoente privado (d)
    d = mod_inverse(e, phi)

    # Chave pública e chave privada
    public_key = (n, e)
    private_key = (n, d)

    return public_key, private_key

def encrypt(message, public_key):
    """Criptografa uma mensagem usando a chave pública."""
    n, e = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

def decrypt(encrypted_message, private_key):
    d, n = private_key
    decrypted = pow(encrypted_message, d, n)
    return decrypted.to_bytes((decrypted.bit_length() + 7) // 8, 'big').decode()



# Gerar dois números primos de 2048 bits
prime1 = generate_large_prime(2048)
prime2 = generate_large_prime(2048)

# Gerar o par de chaves RSA
public_key, private_key = generate_keypair(prime1, prime2)

# Converter a chave pública para uma sequência de bytes
serialized_public_key = "{}|{}".format(public_key[0], public_key[1])

print("Chave pública:")
print(public_key)

print("\nChave privada:")
print(private_key)

encrypt_test = encrypt("teste", public_key)
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

        while True:  # Communicate with the client until the client closes the connection
            
            if isFirst:
                isFirst = False

                connectionSocket.send(bytes(str(serialized_public_key), "utf-8"))
            else:
                sentence = connectionSocket.recv(1024)
                if not sentence:  # If the client closes the connection, break out of the loop
                    break
                
                received = sentence.decode("utf-8")
                print("Received From Client:", received)
                decryptedSentence = decrypt(received, private_key)
                
                print("decrypted sentence:", decryptedSentence) 

                connectionSocket.send("Info recebida".encode("utf-8"))

    except ConnectionResetError as e:
        print(f"Connection reset by peer: {e}")
    except Exception as e:
        print(f"Error receiving data: {e}")
    print("waiting for connection")

serverSocket.close()  # Close the server socket when done
