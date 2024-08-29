import socket

# Configuration du client
HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 1024

def print_board(board_state):
    board = board_state.split(',')
    for i in range(3):
        print(' | '.join(board[i*3:i*3+3]))
        if i < 2:
            print('-' * 5)

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        
        while True:
            board_state = client_socket.recv(BUFFER_SIZE).decode()
            print_board(board_state)
            
            message = client_socket.recv(BUFFER_SIZE).decode()
            print(message)
            
            if "gagné" in message or "Égalité" in message:
                print("Le jeu est terminé.")
                break
            
            move = input("Entrez votre coup (0-8) : ")
            client_socket.sendall(move.encode())

if __name__ == "__main__":
    start_client()
