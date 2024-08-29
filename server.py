import socket
import threading
import pickle

# Définir les variables de contrôle du jeu
board = [None] * 9
current_player = "X"
placement_phase = True

def handle_client(client_socket):
    global board, current_player, placement_phase

    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            data = pickle.loads(data)
            if data['type'] == 'move':
                position = data['position']
                # Mettre à jour le plateau et envoyer le tour suivant
                if placement_phase:
                    if board[position] is None:
                        board[position] = current_player
                        current_player = "O" if current_player == "X" else "X"
                        if board.count("X") == 3 and board.count("O") == 3:
                            placement_phase = False
                else:
                    if board[position] == current_player:
                        board[position] = current_player
                        # Mettez à jour le plateau et passez au joueur suivant
                        current_player = "O" if current_player == "X" else "X"

                # Envoyer l'état mis à jour du jeu à tous les clients
                broadcast({'type': 'update', 'board': board, 'current_player': current_player, 'placement_phase': placement_phase})
        except Exception as e:
            print(f"Erreur: {e}")
            break

    client_socket.close()

def broadcast(message):
    for client in clients:
        try:
            client.send(pickle.dumps(message))
        except:
            client.close()
            clients.remove(client)

# Initialiser le serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen(5)
clients = []

print("Serveur démarré. En attente de connexions...")

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    print(f"Connexion acceptée de {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
