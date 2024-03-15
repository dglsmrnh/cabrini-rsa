from socket import *

def encrypt(message, public_key):
    """Criptografa uma mensagem usando a chave pública."""
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

connectedToServer = False

serverName = "10.1.70.32"
serverPort = 15200
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
while True:

    if not connectedToServer:
        # Receber a chave pública do servidor
        serialized_public_key = clientSocket.recv(4096).decode()
        n, e = serialized_public_key.split("|")
        public_key = (int(n), int(e))

        print("Chave pública recebida:\n")
        print(public_key)

        connectedToServer = True

    else:
        rawSentence = input("Input lowercase sentence: ")
        if not rawSentence == "":
            sentence = encrypt(rawSentence, public_key)
            clientSocket.send(bytes(sentence, "utf-8"))
            
            print("Waiting for answer...")

            response = clientSocket.recv(1024)
            responseText = str(response,"utf-8")
            print ("Received from Server: ", responseText)
        else:
            clientSocket.detach()
            connectedToServer = False
            break