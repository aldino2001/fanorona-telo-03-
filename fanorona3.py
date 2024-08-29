import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

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

# Initialisation du plateau (None signifie que la position est vide)
board = [None] * 9

# Variables de contrôle
current_player = "X"
selected_token = None
move_mode = False
placement_phase = True  # Variable pour vérifier si nous sommes encore en phase de placement
game_over = False

def draw_grid():
    # Dessiner les lignes du plateau
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

def check_winner():
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Lignes
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Colonnes
        (0, 4, 8), (2, 4, 6)              # Diagonales
    ]
    
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] is not None:
            return board[combo[0]]
    
    return None

def handle_move(pos):
    global selected_token, move_mode, current_player, placement_phase, game_over

    for i, position in enumerate(positions):
        if pos[0] in range(position[0] - POINT_RADIUS, position[0] + POINT_RADIUS) and pos[1] in range(position[1] - POINT_RADIUS, position[1] + POINT_RADIUS):
            if placement_phase:
                # Placement des jetons
                if board[i] is None:
                    board[i] = current_player
                    current_player = "O" if current_player == "X" else "X"
                    if board.count("X") == 3 and board.count("O") == 3:
                        placement_phase = False  # Passer en phase de déplacement
            else:
                # Déplacement des jetons
                if move_mode:
                    if board[i] is None:
                        board[i] = current_player
                        board[selected_token] = None
                        winner = check_winner()
                        if winner:
                            show_message(f"Le joueur {winner} a gagné!", GREEN)
                            game_over = True
                        current_player = "O" if current_player == "X" else "X"
                    move_mode = False
                else:
                    if board[i] == current_player:
                        selected_token = i
                        move_mode = True
            break

def show_intro():
    screen.fill(WHITE)
    show_message("Bienvenue au Jeu de Grille!", BLACK)
    show_message("Cliquez pour commencer!", BLACK)

def main():
    show_intro()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_move(event.pos)

        if not game_over:
            screen.fill(WHITE)
            draw_grid()
            draw_markers()
            if placement_phase:
                draw_status(f"Joueur {current_player} ")
            elif move_mode:
                draw_status(f"joueur {current_player}")
            else:
                draw_status(f"joueur {current_player}")

            pygame.display.update()

if __name__ == "__main__":
    main()
