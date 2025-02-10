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
WHITE, RED, PINK = (255, 255, 255), (255, 0, 0), (255, 182, 193)

#Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catching Your LOVE 💖")

#Load Images
basket_img = pygame.image.load("assets/basket.png")
basket_img = pygame.transform.scale(basket_img, (BASKET_WIDTH, BASKET_HEIGHT))

heart_img = pygame.image.load("assets/heart.png")
heart_img = pygame.transform.scale(heart_img, (HEART_SIZE, HEART_SIZE))

#Basket Position
basket = pygame.Rect(WIDTH // 2 - BASKET_WIDTH // 2, BASKET_Y, BASKET_WIDTH, BASKET_HEIGHT)

#List to Track Hearts
hearts = []
score = 0
font = pygame.font.Font(None, 36)
message_font = pygame.font.Font(None, 50)

#Game Loop
running = True
clock = pygame.time.Clock()
message_shown = False
message_y = HEIGHT // 2  # Initial Y position of message for floating effect
message_direction = 1  # Controls floating movement

while running:
    screen.fill(PINK)  # Background Color

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move Basket
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket.x > 0:
        basket.x -= BASKET_SPEED
    if keys[pygame.K_RIGHT] and basket.x < WIDTH - BASKET_WIDTH:
        basket.x += BASKET_SPEED

    # Spawn Hearts at Random Intervals
    if random.randint(1, 20) == 1:
        hearts.append([random.randint(0, WIDTH - HEART_SIZE), 0, random.randint(3, 6)])  
        # Each heart has (x, y, speed)

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

    #Score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    #Valentine's Message
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

        message_text = message_font.render("Will you be my Valentine?", True, RED)
        text_rect = message_text.get_rect(center=(WIDTH // 2, message_y))  # Correctly indented
        screen.blit(message_text, text_rect)  # Correctly indented


    pygame.display.flip()
    clock.tick(30)  #30 FPS

pygame.quit()