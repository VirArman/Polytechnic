import pygame
import chessEngine
import random
import math

# Լայնություն և երկարություն
WIDTH = HEIGHT = 512
# Խաղատախտակի չափը քառակուսիներով 8x8
DIMENSION = 8
# Քառակուսու չափ
SQ_SIZE = WIDTH//DIMENSION
# Խաղաքարերի պատկերներ
IMAGES = {}

def generate_pawn_attacks(row, col, board, color):
    # Ֆունկցիան գեներացնում է զինվորի հարձակման քայլերը
    # Որպես արգւմենտ ստանում է զինվորի գտնվելու սյունակը, տողը, խաղատախտակի վիճակը և զինվորի գույնը
    # և վերադարձնում է բոլոր հնարավոր հարձակման քայլերը
    attacks = []
    directions = []

    if color == "w":
        directions = [(-1, -1), (-1, 1)]  # White pawn attack directions
    elif color == "b":
        directions = [(1, -1), (1, 1)]  # Black pawn attack directions

    for direction in directions:
        new_row = row + direction[0]
        new_col = col + direction[1]

        # Check if the new position is within the bounds of the board
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            piece = board[new_row][new_col]

            # Check if the new position is occupied by an opponent's piece
            if piece != "--" and piece[0] != color:
                attacks.append((new_row, new_col))

    return attacks
        

def generate_king_attacks(row, col, board, color):
    possible_moves = []

    # Define the eight possible directions for king moves
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    for direction in directions:
        new_row = row + direction[0]
        new_col = col + direction[1]

        # Check if the new position is within the bounds of the board
        if 0 <= new_row < DIMENSION and 0 <= new_col < DIMENSION:
            piece = board[new_row][new_col]

            # Check if the new position is empty or occupied by an opponent's piece
            if piece == "--" or piece[0] != color:
                possible_moves.append((new_row, new_col))

    return possible_moves

def generate_queen_moves(row, col, board,color):
    # Գեներացնում է թագուհու քայլերը 
    # Որպես արգւմենտ ստանում է թագուհու գտնվելու սյունակը, տողը, խաղատախտակի վիճակը և թագուհու գույնը
    # և վերադարձնում է բոլոր հնարավոր քայլերը
    possible_moves = []
    #horizontal moves
    for i in range(col-1,-1,-1):
        if board[row][i][0] == color:
            break
        if board[row][i] == "--" or board[row][i][0] != color:
            possible_moves.append((row, i))
        if board[row][i][0] == "b":
            break

    for i in range(col+1,DIMENSION,1):
        if board[row][i][0] == color:
            break
        if board[row][i] == "--" or board[row][i][0] != color:
            possible_moves.append((row, i))
        if board[row][i][0] == "b":
            break
    # vertical moves
    for i in range(row+1,DIMENSION,1):
        if board[i][col][0] == color:
            break
        if board[i][col] == "--" or board[i][col][0] != color :
            possible_moves.append((i, col))
        if board[i][col][0] == "b" :
            break
    
    for i in range(row-1,-1,-1):
        if board[i][col][0] == color:
            break
        if board[i][col] == "--" or board[i][col][0] != color:
            possible_moves.append((i, col))
        if board[i][col][0] == "b":
            break
    #diagonal
    for i in range(1,DIMENSION):
        if row-i >= 0 and col+i<DIMENSION:
            if board[row-i][col+i][0] == color:
                break
            if board[row-i][col+i] == "--" or board[row-i][col+i][0] != color:
                possible_moves.append((row-i, col+i))
            if board[row-i][col+i][0] == "b":
                break
    for i in range(1,DIMENSION):
        if col-i >= 0 and row+i<DIMENSION:
            if board[row+i][col-i][0] == color:
                break
            if board[row+i][col-i] == "--" or board[row+i][col-i][0] != color:
                possible_moves.append((row+i, col-i))
            if board[row+i][col-i][0] == "b":
                break
    for i in range(1,DIMENSION):
        if row-i >= 0 and col-i >= 0:
            if board[row-i][col-i][0] == color:
                break
            if board[row-i][col-i] == "--" or board[row-i][col-i][0] != color:
                possible_moves.append((row-i, col-i))
            if board[row-i][col-i][0] == "b":
                break
    for i in range(1,DIMENSION):
        if row+i < DIMENSION and col+i<DIMENSION:
            if board[row+i][col+i][0] == color:
                break
            if board[row+i][col+i] == "--" or board[row+i][col+i][0] != color:
                possible_moves.append((row+i, col+i))
            if board[row+i][col+i][0] == "b":
                break

    return possible_moves

def max_movable(qr,qc,gs):
    # Ստանում է թագուհու դիրքը և խաղատախտակի վիճակը և հաշվում է ամենաերկար քայլը 
    # հաշվարկի համար օգտագործում է Էվկլիդեսի հեռավորության բանաձևը
    qm = generate_queen_moves(qr,qc,gs.board,"w")
    longest_move = math.sqrt((qm[0][0]-qr)**2 + (qm[0][1]-qc)**2)
    max_move = qm[0]
    for move in qm:
        tmp = math.sqrt((move[0]-qr)**2 + (move[1]-qc)**2)
        if longest_move < tmp:
            longest_move = tmp
            max_move = move
    if longest_move != math.floor(longest_move):
        longest_move = longest_move / math.sqrt(2)
    longest_move = round(longest_move)
    print(max_move)
    return [qm,longest_move]


def load_images(pieces):
    # Վարցնում է նկարները img թղթապանակից և վերածում IMAGES֊ի անդամ օգտագործելով pygame֊ը
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("img/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))

def draw_game_state(screen, gs, qm):
    # Ներկայացնում է խաղի վիճակը գրաֆիկորեն
    draw_board(screen,qm)
    draw_pieces(screen,gs.board)

def draw_board(screen, qm):
    # Պատկերում է խաղատախտակը
    colors = [pygame.Color("white"),pygame.Color("grey")]
    queen_moves = qm 
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            if (r,c) in queen_moves:
                pygame.draw.rect(screen,pygame.Color("dark green"),pygame.Rect(SQ_SIZE*c,SQ_SIZE*r,SQ_SIZE,SQ_SIZE))
            else:
                pygame.draw.rect(screen,color,pygame.Rect(SQ_SIZE*c,SQ_SIZE*r,SQ_SIZE,SQ_SIZE))

def draw_pieces(screen, board):
    # Պատկերումէ խաղատաղտակի վրա խաղաքարերը
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],pygame.Rect(SQ_SIZE*c,SQ_SIZE*r,SQ_SIZE,SQ_SIZE))

def gameplay(figures,gs,qm):
    # Ընդհանուր գրաֆիկական մասի ստեղծման և ընթացքի կարգավորիչ
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    screen.fill(pygame.Color("white"))
    load_images(figures)
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running =False
        draw_game_state(screen, gs, qm)
        pygame.display.flip()

def random_placement(figures,gs):
    # Պատահական դասավորվածություն ապահովող ֆունկցիա
    fr = -1
    fc = -1
    qr = -1
    qc = -1
    white_attack = []
    black_attack = []
    for figure in figures:
        if figure == "wQ":
            qr = random.randint(0,7)
            qc = random.randint(0,7)
            while gs.is_occupied(qr,qc):
                qr = random.randint(0,7)
                qc = random.randint(0,7)
            gs.board[qr][qc] = figure
            white_attack.append(generate_queen_moves(qr,qc,gs.board,"w"))
            continue
        fr = random.randint(0,7)
        fc = random.randint(0,7)
        while gs.is_occupied(fr,fc):
            fr = random.randint(0,7)
            fc = random.randint(0,7)
        while gs.is_occupied(fr,fc) or (figure == "wK" and (fr,fc) in black_attack):
            fr = random.randint(0,7)
            fc = random.randint(0,7)
        while gs.is_occupied(fr,fc) or (figure == "bK" and (fr,fc) in white_attack):
            fr = random.randint(0,7)
            fc = random.randint(0,7)

        gs.board[fr][fc] = figure
        if figure == "wP":
            white_attack.append(generate_pawn_attacks(fr,fc,gs.board,"w"))
        if figure == "wK":
            white_attack.append(generate_king_attacks(fr,fc,gs.board,"w"))
        if figure == "bQ":
            black_attack.append(generate_queen_moves(fr,fc,gs.board,"b"))
        if figure == "bK":
            black_attack.append(generate_king_attacks(fr,fc,gs.board,"b"))
        if figure == "bP":
            black_attack.append(generate_pawn_attacks(fr,fc,gs.board,"b"))
    return [qr,qc]

def custom_placement(figures,gs):
    # Մարդու կողմից դասավորելու համար նախատեսված ֆունկցիա
    qr = -1
    qc = -1
    for figure in figures:
        print("Insert position for ", figure)
        x = int(input("Insert row "))
        y = int(input("Insert column "))
        while gs.is_occupied(x,y):
                x = random.randint(0,7)
                y = random.randint(0,7)
        if figure == "wQ":
            qr = x
            qc = y
        gs.board[x][y] = figure
    return [qr,qc]


def main():
    print("Please insert which mode do you wish to use")
    mode = input("Insert 'r' for random placement or 'c' to customize: ")
    figures = ["wP","wQ","bP","bQ","bK","wK"]
    gs = chessEngine.game_state()
    
    if mode == "r":
        q = random_placement(figures,gs)
        qr = q[0]
        qc = q[1]
    elif mode == "c":
        q = custom_placement(figures,gs)
        qr = q[0]
        qc = q[1]
    else:
        print("You inserted wrong flag")
        return
    qm = max_movable(qr,qc,gs)
    print(qm[1])
    gameplay(figures,gs,qm[0])



if __name__ == "__main__":
    main()

