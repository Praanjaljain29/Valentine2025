import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
BASKET_WIDTH, BASKET_HEIGHT = 80, 80
BASKET_Y = HEIGHT - 80
BASKET_SPEED = 10
HEART_SIZE = 60
WHITE, RED, PINK , BLACK= (255, 255, 255), (255, 0, 0), (255, 182, 193),(0,0,0)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catching Your LOVE 💖")

# Load Images
basket_img = pygame.image.load("assets/basket.png")
basket_img = pygame.transform.scale(basket_img, (BASKET_WIDTH, BASKET_HEIGHT))

heart_img = pygame.image.load("assets/heart.png")
heart_img = pygame.transform.scale(heart_img, (HEART_SIZE, HEART_SIZE))

# Basket Position
basket = pygame.Rect(WIDTH // 2 - BASKET_WIDTH // 2, BASKET_Y, BASKET_WIDTH, BASKET_HEIGHT)

# List to Track Hearts
hearts = []
score = 0
font = pygame.font.Font(None, 36)
message_font = pygame.font.Font(None, 50)

# Game Loop
running = True
name_entered = False  # Flag to track if the name has been entered
clock = pygame.time.Clock()
message_shown = False
message_y = HEIGHT // 2  # Initial Y position of message for floating effect
message_direction = 1  # Controls floating movement
user_input = ""  # Storing User name


def first_screen():
    # Displaying the prompt
    prompt_text = font.render("Hi cutie, What's your name?", True, RED)
    screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 3))

    # Blinking cursor logic
    cursor = "_" if pygame.time.get_ticks() // 500 % 2 == 0 else ""  # Blinks every 500ms

    # Displaying the user's input with the cursor
    input_text = font.render(user_input + cursor, True, RED)
    screen.blit(input_text, (WIDTH // 2 - input_text.get_width() // 2, HEIGHT // 2))


def main_game():
    global score, message_shown, message_y, message_direction

    # Move Basket
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket.x > 0:
        basket.x -= BASKET_SPEED
    if keys[pygame.K_RIGHT] and basket.x < WIDTH - BASKET_WIDTH:
        basket.x += BASKET_SPEED

    # Spawn Hearts at Random Intervals
    if random.randint(1, 20) == 1:
        hearts.append([random.randint(0, WIDTH - HEART_SIZE), 0, random.randint(3, 6)])  # Each heart has (x, y, speed)

    # Move Hearts and Check Collision
    hearts_to_remove = []
    for heart in hearts:
        heart[1] += heart[2]  # Move heart down at its own speed

        # Collision check: If the heart is inside the basket
        if heart[1] + HEART_SIZE > BASKET_Y and basket.x < heart[0] < basket.x + BASKET_WIDTH:
            score += 1  # Increment score
            hearts_to_remove.append(heart)

        elif heart[1] > HEIGHT:
            hearts_to_remove.append(heart)

    # Remove caught or missed hearts
    for heart in hearts_to_remove:
        hearts.remove(heart)

    # Draw Hearts First (Behind Basket)
    for heart in hearts:
        screen.blit(heart_img, (heart[0], heart[1]))

    # Draw Basket Last (Top)
    screen.blit(basket_img, (basket.x, basket.y))

    # Score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Valentine's Message
    if score >= 10 and not message_shown:
        for _ in range(20):  # Heart shower effect
            hearts.append([random.randint(0, WIDTH - HEART_SIZE), random.randint(-100, 0), random.randint(3, 7)])

        for _ in range(50):  # Create a heart rain effect over time
            hearts.append([random.randint(0, WIDTH - HEART_SIZE), random.randint(-200, 0), random.randint(3, 7)])

        message_shown = True  # Ensure message is displayed only once

    # Animate Floating Message
    if message_shown:
        message_y += message_direction
        if message_y > HEIGHT // 2 + 10 or message_y < HEIGHT // 2 - 10:
            message_direction *= -1  # Reverse direction to float up and down

        disp_message = f"{user_input}\nwill you be my Valentine?"  # Display message with name

        lines = disp_message.split('\n')
        for i, line in enumerate(lines):
            message_text = message_font.render(line, True, RED)
            text_rect = message_text.get_rect(center=(WIDTH // 2, message_y + i * 40))
            screen.blit(message_text, text_rect)


def how_to_play_screen():
    # Scale images
    heart_img_scaled = pygame.transform.scale(heart_img, (50, 50))
    basket_img_scaled = pygame.transform.scale(basket_img, (80, 50))

    # Display the title
    title_text = font.render("How to Play?", True, BLACK)
    title_x = (WIDTH - title_text.get_width()) // 2
    screen.blit(title_text, (title_x, 50))

    # Display the heart, basket, and heart images in a row
    def image_disp(pos_y):
        total_width = heart_img_scaled.get_width() + basket_img_scaled.get_width() + heart_img_scaled.get_width() + 40  # 40 is the spacing
        start_x = (WIDTH - total_width) // 2
        screen.blit(heart_img_scaled, (start_x, pos_y))  # First heart image
        screen.blit(basket_img_scaled, (start_x + heart_img_scaled.get_width() + 20, pos_y))  # Basket image
        screen.blit(heart_img_scaled, (start_x + heart_img_scaled.get_width() + basket_img_scaled.get_width() + 40, pos_y))  # Second heart image

    image_disp(100)

    # Display the instructions
    instructions ="""Use Left and Right arrow keys to move the basket.\nCatch hearts to increase your score.\nPress Enter to start the game."""
    instructions = instructions.split('\n')
    
    ins_font = pygame.font.Font(None, 30)
    for i, line in enumerate(instructions):
        instruction_text = ins_font.render(line, True, RED)
        instruction_x = (WIDTH - instruction_text.get_width()) // 2
        screen.blit(instruction_text, (instruction_x, 170 + i * 40))  # Start below the images
    
    image_disp(300)

current_screen = "first_screen"

while running:
    screen.fill(PINK)  # Background Color

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_screen == "first_screen":
                if event.key == pygame.K_RETURN:
                    current_screen = "how_to_play_screen"
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
            elif current_screen == "how_to_play_screen":
                if event.key == pygame.K_RETURN:
                    current_screen = "main_game"
        
                
    # Display the appropriate screen
    if current_screen == "first_screen":
        first_screen()
    elif current_screen == "how_to_play_screen":
        how_to_play_screen()
    elif current_screen == "main_game":
        main_game()
    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()