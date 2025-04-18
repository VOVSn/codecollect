import os
import sys
import random

from ollama import chat, ChatResponse

OLLAMA_MODEL = "deepseek-r1:14b"

def read_self():
    with open(__file__, 'r', encoding='utf-8') as file:
        return file.read()

def get_next_filename():
    base_name, ext = os.path.splitext(__file__)
    num = ''.join(filter(str.isdigit, base_name.split('_')[-1]))
    new_num = int(num) + 1 if num else 1
    new_name = f"{base_name.rstrip(num)}{new_num}{ext}"
    return new_name

def write_self(new_code):
    next_file = get_next_filename()
    with open(next_file, 'w', encoding='utf-8') as file:
        file.write(new_code)
    print(f"The script has been saved as: {next_file}")

def infer_ollama(message):
    try:
        response = chat(
            model=OLLAMA_MODEL,
            messages=[
                {'role': 'user', 'content': message}
            ],
            options={
                'temperature': 0
            }
        )
        return response.message.content
    
    except Exception as e:
        print(f'Error querying Ollama: {e}')
        return None

def improve_code(instruction):
    code = read_self()
    prompt = f"""
    Hello, AI assistant! Please improve this Python code.
    Ensure the following:
    1. Retain functionality.
    2. Add or modify functionality as per the instruction below.
    Instruction: {instruction}
    Code:
    ```python
    {code}
    ```
    Output the improved code in a single Python block:
    ```python
    <code>
    ```
    """
    response = infer_ollama(prompt)
    
    if response:
        start = response.find('```python') + len('```python')
        end = response.rfind('```')
        
        if start != -1 and end != -1:
            return response[start:end].strip()
    
    return code

def draw_sun():
    sun_art = """
       ,"".
      /   \\
     :     :
     :  *  :
     :     :
      \\___/
         |
    """
    print(sun_art)

# Removed the function to print Pi
# def print_pi_hundred_numbers():
#     import math
#     pi_str = str(math.pi)
#     # Remove the decimal point and take the first 100 digits of Pi
#     pi_digits = pi_str.replace('.', '')[:100]
#     print(pi_digits)

def snake_game():
    import pygame

    width, height = 20, 20
    x, y = random.randint(0, width - 1), random.randint(0, height - 1)
    food_x, food_y = random.randint(0, width - 1), random.randint(0, height - 1)

    pygame.init()
    screen = pygame.display.set_mode((width * 20, height * 20))
    clock = pygame.time.Clock()

    def draw_snake(snake_body):
        for part in snake_body:
            pygame.draw.rect(screen, (0, 255, 0), (part[0] * 20, part[1] * 20, 20, 20))

    while True:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (255, 0, 0), (food_x * 20, food_y * 20, 20, 20))
        draw_snake([(x, y)])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and y > 0: y -= 1
        if keys[pygame.K_DOWN] and y < height - 1: y += 1
        if keys[pygame.K_LEFT] and x > 0: x -= 1
        if keys[pygame.K_RIGHT] and x < width - 1: x += 1

        pygame.display.flip()
        clock.tick(10)

def tic_tac_toe():
    board = [' ' for _ in range(9)]
    player = 'X'

    def draw_board(board):
        print(f"{board[0]} | {board[1]} | {board[2]}\n---+---+---\n{board[3]} | {board[4]} | {board[5]}\n---+---+---\n{board[6]} | {board[7]} | {board[8]}\n")

    def check_win(board, player):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
                return True
        return False

    while ' ' in board and not check_win(board, player):
        draw_board(board)
        move = int(input(f"Player {player}, enter your move (1-9): ")) - 1
        if board[move] != ' ':
            print("Invalid move. Try again.")
            continue
        board[move] = player
        player = 'O' if player == 'X' else 'X'

    draw_board(board)
    if check_win(board, player):
        print(f"Player {player} wins!")
    else:
        print("It's a tie!")

def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'make':
        instruction = ' '.join(sys.argv[2:])
        updated_code = improve_code(instruction)
        
        if updated_code:
            write_self(updated_code)
        else:
            print("Failed to update the script.")
    elif len(sys.argv) > 1 and sys.argv[1].lower() == 'draw_sun':
        draw_sun()
    elif len(sys.argv) > 1 and sys.argv[1].lower() == 'snake_game':
        snake_game()
    elif len(sys.argv) > 1 and sys.argv[1].lower() == 'tic_tac_toe':
        tic_tac_toe()
    else:
        print(f"Usage: python {__file__} make <your instructions> or python program.py draw_sun or python program.py snake_game or python program.py tic_tac_toe")

if __name__ == "__main__":
    main()