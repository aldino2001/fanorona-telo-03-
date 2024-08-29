import pygame
import socket
import pickle
import sys
import threading

# Initialisation de Pygame
pygame.init()

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Taille de la fenêtre
WIDTH, HEIGHT = 400, 400
LINE_WIDTH = 5
POINT_RADIUS = 20

# Initialisation de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de Grille avec Déplacement")

# Définir les positions des intersections
positions = [
    (WIDTH//6, HEIGHT//6), (WIDTH//2, HEIGHT//6), (5*WIDTH//6, HEIGHT//6),
    (WIDTH//6, HEIGHT//2), (WIDTH//2, HEIGHT//2), (5*WIDTH//6, HEIGHT//2),
    (WIDTH//6, 5*HEIGHT//6), (WIDTH//2, 5*HEIGHT//6), (5*WIDTH//6, 5*HEIGHT//6)
]

# Variables de contrôle
board = [None] * 9
current_player = "X"
selected_token = None
move_mode = False
placement_phase = True
game_over = False

def draw_grid():
    pygame.draw.line(screen, BLACK, positions[0], positions[2], LINE_WIDTH)
    pygame.draw.line(screen, BLACK, positions[0], positions[6], LINE_WIDTH)
    pygame.draw.line(screen, BLACK, positions[6], positions[8], LINE_WIDTH)
    pygame.draw.line(screen, BLACK, positions[2], positions[8], LINE_WIDTH)
    pygame.draw.line(screen, BLACK, positions[1], positions[7], LINE_WIDTH)
    pygame.draw.line(screen, BLACK, positions[3], positions[5], LINE_WIDTH)
    pygame.draw.line(screen, BLACK, positions[0], positions[8], LINE_WIDTH)
    pygame.draw.line(screen, BLACK, positions[2], positions[6], LINE_WIDTH)

def draw_markers():
    for i in range(9):
        if board[i] == "X":
            pygame.draw.circle(screen, RED, positions[i], POINT_RADIUS)
        elif board[i] == "O":
            pygame.draw.circle(screen, BLUE, positions[i], POINT_RADIUS)

def draw_status(message):
    font = pygame.font.SysFont(None, 36)
    text = font.render(message, True, BLACK)
    screen.blit(text, (10, HEIGHT - 40))

def show_message(message, color=BLACK):
    font = pygame.font.SysFont(None, 48)
    text = font.render(message, True, color)
    screen.fill(WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.wait(2000)

def connect_to_server():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))  # Connecte-toi à l'adresse IP et au port du serveur

def send_move(position):
    message = {'type': 'move', 'position': position}
    client_socket.send(pickle.dumps(message))

def receive_updates():
    global board, current_player, placement_phase
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            data = pickle.loads(data)
            if data['type'] == 'update':
                board = data['board']
                current_player = data['current_player']
                placement_phase = data['placement_phase']
        except Exception as e:
            print(f"Erreur de réception: {e}")
            break

def handle_move(pos):
    global selected_token, move_mode, current_player, placement_phase, game_over

    for i, position in enumerate(positions):
        if pos[0] in range(position[0] - POINT_RADIUS, position[0] + POINT_RADIUS) and pos[1] in range(position[1] - POINT_RADIUS, position[1] + POINT_RADIUS):
            if placement_phase:
                if board[i] is None:
                    send_move(i)
            else:
                if move_mode:
                    if board[i] is None:
                        send_move(i)
                        move_mode = False
                    else:
                        if board[i] == current_player:
                            selected_token = i
                            move_mode = True
            break

def main():
    global game_over
    connect_to_server()
    threading.Thread(target=receive_updates, daemon=True).start()

    show_message("Bienvenue au Jeu de Grille!", BLACK)
    show_message("Cliquez pour commencer!", BLACK)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_move(event.pos)

        screen.fill(WHITE)
        draw_grid()
        draw_markers()
        if placement_phase:
            draw_status(f"Tour du joueur {current_player} - Phase de placement")
        elif move_mode:
            draw_status(f"Déplacez le jeton du joueur {current_player}")
        else:
            draw_status(f"Tour du joueur {current_player}")

        pygame.display.update()

if __name__ == "__main__":
    main()
