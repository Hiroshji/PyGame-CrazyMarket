import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
CONVEYOR_Y = 200
CONVEYOR_HEIGHT = 80
SCANNER_AREA = pygame.Rect(300, 290, 200, 70)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GREY = (200, 200, 200)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crazy Market")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Item class
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.grabbed = False
        self.scanned = False
        self.scored = False

    def update(self):
        if not self.grabbed:
            if CONVEYOR_Y <= self.rect.centery <= CONVEYOR_Y + CONVEYOR_HEIGHT:
                self.rect.x += 2  # Move only on the conveyor belt
            else:
                self.rect.y += 5  # Fall if outside the conveyor belt

            # Game Over condition for unscanned items
            if self.rect.x > SCREEN_WIDTH and not self.scanned:
                global running
                running = False
                print("Game Over: Unscanned item reached the end!")
            
            # Scoring for scanned items
            if self.rect.x > SCREEN_WIDTH and self.scanned and not self.scored:
                global score
                score += 1
                self.scored = True

# Create sprite groups
all_sprites = pygame.sprite.Group()
items = pygame.sprite.Group()

# Game variables
score = 0
font = pygame.font.Font(None, 36)
grabbing_item = None  # Track the currently grabbed item
spawn_timer = 0  # Timer for spawning items
running = True

def spawn_item():
    """Spawns an item at the left side of the conveyor belt."""
    item = Item(-40, random.randint(CONVEYOR_Y, CONVEYOR_Y + CONVEYOR_HEIGHT - 40))
    all_sprites.add(item)
    items.add(item)

# Main game loop
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Grab and release items with the mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not grabbing_item:  # Ensure only one item can be grabbed
                for item in items:
                    if item.rect.collidepoint(event.pos):
                        grabbing_item = item
                        grabbing_item.grabbed = True
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if grabbing_item:
                grabbing_item.grabbed = False
                grabbing_item = None

    # Handle dragging of grabbed items
    if grabbing_item and grabbing_item.grabbed:
        grabbing_item.rect.center = pygame.mouse.get_pos()
        # Scan the item while hovering over the scanner
        if SCANNER_AREA.colliderect(grabbing_item.rect) and not grabbing_item.scanned:
            grabbing_item.scanned = True
            print("Item scanned!")

    # Spawn new items at random intervals
    spawn_timer += 1
    if spawn_timer > random.randint(60, 120):  # Spawn every 1-2 seconds
        spawn_item()
        spawn_timer = 0

    # Draw the conveyor belt
    conveyor_belt = pygame.Rect(0, CONVEYOR_Y, SCREEN_WIDTH, CONVEYOR_HEIGHT)
    pygame.draw.rect(screen, LIGHT_GREY, conveyor_belt)

    # Draw the scanner area
    pygame.draw.rect(screen, BLUE, SCANNER_AREA, 2)
    scanner_text = font.render("Scanner", True, BLACK)
    screen.blit(scanner_text, (SCANNER_AREA.x + 50, SCANNER_AREA.y - 20))

    # Draw and update all sprites
    all_sprites.update()
    all_sprites.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Game Over screen
screen.fill(WHITE)
game_over_text = font.render("Game Over", True, RED)
final_score_text = font.render(f"Final Score: {score}", True, BLACK)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 30))
screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 10))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
