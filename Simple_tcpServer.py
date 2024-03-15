from socket import *

serverPort = 15200
g = 11
n = 33
y = 3
r2 = g**y%n

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)  # The argument "listen" tells the socket library that we want to queue up to 5 connection requests (usually the maximum) before starting to refuse external connections. If the rest of the code is written correctly, this should be enough.
print("TCP Server\n")

while True:  # Keep the server running indefinitely
    try:
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection from {addr} established.")

        isFirst = True
        k = 0

        while True:  # Communicate with the client until the client closes the connection
            sentence = connectionSocket.recv(1024)
            if not sentence:  # If the client closes the connection, break out of the loop
                break
            
            received = sentence.decode("utf-8")
            print("Received From Client:", received)

            if received.lower() == 'exit':
                connectionSocket.close()
                break  # Exit the loop and wait for a new connection

            if isFirst:
                r1 = int(received)
                k = r1**y%n
                isFirst = False

                connectionSocket.send(bytes(str(r2), "utf-8"))
            else:
                decryptedSentence = ""
                for c in received:
                    decryptedSentence += chr(ord(c) - k)

                print("decrypted sentence:", decryptedSentence) 
                encryptedSentence = ""  # Process the received data

                for c in decryptedSentence.upper():
                    encryptedSentence += chr(ord(c) + k)

                connectionSocket.send(encryptedSentence.encode("utf-8"))

                print("Sent back to Client:", encryptedSentence)

    except ConnectionResetError as e:
        print(f"Connection reset by peer: {e}")
    except Exception as e:
        print(f"Error receiving data: {e}")
    print("waiting for connection")

serverSocket.close()  # Close the server socket when done
