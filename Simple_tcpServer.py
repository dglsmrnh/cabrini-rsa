from socket import *
import random

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

def encrypt_old(message, public_key):
    """Criptografa uma mensagem usando a chave pública."""
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

def decrypt_old(encrypted_message, private_key):
    """Descriptografa uma mensagem usando a chave privada."""
    d, n = private_key
    decrypted_chars = []
    for char in encrypted_message:
        decrypted_char = pow(char, d, n)
        print("\ndecrypted char\n")
        print(decrypted_char)
        decrypted_chars.append(chr(decrypted_char))

    decrypted_message = ''.join(decrypted_chars)
    return decrypted_message

def encrypt(msg, public_key):
    """Criptografa uma mensagem usando a chave pública."""
    e, n = public_key
    
    # Convertendo a mensagem em uma sequência de valores ASCII
    ascii_values = [str(ord(char)) for char in msg]  # Preenche com zeros à direita para ter 3 dígitos

    # Concatenando os valores ASCII em uma única string
    msg_str = ''.join(ascii_values)
    print("\nASCII word\n")
    print(msg_str)

    # Convertendo a string para um número grande
    msg_bigint = int(msg_str)

    # Calculando C = M^e mod N
    result = pow(msg_bigint, e, n)

    # Convertendo o resultado para string
    encrypted_message = str(result)

    return encrypted_message


def decrypt(encrypted_message, private_key):
    """Descriptografa uma mensagem usando a chave privada."""
    d, n = private_key
    
    # Convertendo a cifra para um número grande
    encrypt_bigint = int(encrypted_message)

    # Calculando cifrada_bigint^d mod n
    result = pow(encrypt_bigint, d, n)

    # Convertendo o resultado de volta para uma string
    result_str = str(result).zfill(3)
    print("\nASCII word\n")
    print(result_str)

    # Reconstruindo a mensagem original convertendo cada bloco de volta para seu caractere ASCII correspondente
    i = 0
    decrypted_message = ''
    while i < len(result_str):
        # Obtendo o valor ASCII de cada bloco
        ascii_value = int(result_str[i:i+3])  # Supondo que cada bloco tem 3 dígitos
        # Convertendo o valor ASCII de volta para um caractere
        decrypted_message += chr(ascii_value)
        # Avançando para o próximo bloco
        i += 3

    return decrypted_message


# Gerar dois números primos de 2048 bits
prime1 = generate_large_prime(3)
prime2 = generate_large_prime(3)

# Gerar o par de chaves RSA
public_key, private_key = generate_keypair(prime1, prime2)

# Converter a chave pública para uma sequência de bytes
serialized_public_key = "{}|{}".format(public_key[0], public_key[1])

print("Chave pública:")
print(public_key)

print("\nChave privada:")
print(private_key)

encrypt_test = encrypt("A", public_key)
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
                
                received = sentence
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
