import pygame
import sys
import random
from game_logic import GameState
from renderer import GameRenderer

# Initialize pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
SCREEN_TITLE = "WallGo - Red vs Blue"

# Create the game window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption(SCREEN_TITLE)

# Initialize game state and renderer
game_state = GameState()
game_state.debug = True  # Enable debug output
renderer = GameRenderer(screen, WINDOW_SIZE)

# Function to randomize piece placement
def randomize_pieces():
    # Clear any existing pieces
    game_state.pieces = [
        [None, None],  # Red pieces
        [None, None]   # Blue pieces
    ]
    
    # Generate 4 unique random positions
    positions = []
    while len(positions) < 4:
        row = random.randint(0, game_state.board_size - 1)
        col = random.randint(0, game_state.board_size - 1)
        if (row, col) not in positions:
            positions.append((row, col))
    
    # Assign positions to pieces
    game_state.pieces[0][0] = positions[0]  # Red piece 1
    game_state.pieces[0][1] = positions[1]  # Red piece 2
    game_state.pieces[1][0] = positions[2]  # Blue piece 1
    game_state.pieces[1][1] = positions[3]  # Blue piece 2
    
    # Skip setup phase
    game_state.phase = "select"
    game_state.current_player = random.randint(0, 1)  # Randomly choose Red (0) or Blue (1) to start
    game_state.message = f"{game_state.player_colors[game_state.current_player]}'s turn: Select a piece"

# Create buttons with enhanced styling
def create_button(text, x, y, width, height, color, hover_color, text_color):
    return {
        "rect": pygame.Rect(x, y, width, height),
        "text": text,
        "color": color,
        "hover_color": hover_color,
        "text_color": text_color,
        "is_hovered": False
    }

# Add buttons with enhanced styling
random_button = create_button(
    "Randomize Pieces", 
    WINDOW_SIZE - 280, 10, 180, 40, 
    (70, 130, 180),  # Steel Blue
    (100, 149, 237),  # Cornflower Blue
    (255, 255, 255)   # White
)

restart_button = create_button(
    "Restart Game", 
    10, 10, 140, 40, 
    (220, 60, 60),  # Red
    (240, 100, 100),  # Lighter Red
    (255, 255, 255)   # White
)

rules_button = create_button(
    "Rules", 
    WINDOW_SIZE - 90, 10, 80, 40, 
    (60, 179, 113),  # Green
    (80, 200, 130),  # Lighter Green
    (255, 255, 255)   # White
)

# Create a rules window class
class RulesWindow:
    def __init__(self, screen_size):
        self.window_size = (620, 750)  # Width, Height - increased height
        self.position = (
            (screen_size - self.window_size[0]) // 2,
            (screen_size - self.window_size[1]) // 2
        )
        self.visible = False
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 18)  # Reduced from 20 to 18
        
        # Create close button
        self.close_button = create_button(
            "Close",
            self.position[0] + self.window_size[0] - 90,
            self.position[1] + 10,
            80, 30,
            (220, 60, 60),  # Red
            (240, 100, 100),  # Lighter Red
            (255, 255, 255)   # White
        )
        
        # Rules text sections
        self.rules_sections = [
            ("Overview", [
                "WallGo is a two-player abstract strategy game",
                "played on a 7x7 grid. Each player controls two",
                "pieces (Red vs Blue) and strategically moves them",
                "around the board, placing walls to block movement."
            ]),
            ("Setup", [
                "• Each player starts with 2 pieces",
                "• Players take turns placing pieces (Red/Blue/Red/Blue)",
                "• Use the 'Randomize' button for random placement",
                "• No walls are placed at the start",
                "• The outer edges are permanent walls"
            ]),
            ("Movement", [
                "• Move 1 or 2 squares orthogonally (up, down, left, right)",
                "• Move in an L-shape (one step, then one perpendicular)",
                "• Stay in place (after 2-second delay)",
                "• Cannot move through walls or off the board",
                "• Cannot move isolated pieces (in 1x1 squares)"
            ]),
            ("Wall Placement", [
                "• After moving, place a wall adjacent to your piece",
                "• Walls block movement between squares",
                "• Cannot place walls where one already exists",
                "• Cannot place walls outside the board"
            ]),
            ("Winning", [
                "• Game ends when all pieces are isolated from each other",
                "• Red piece 1 cannot reach Red piece 2",
                "• Blue piece 1 cannot reach Blue piece 2",
                "• No red piece can reach any blue piece",
                "• Player with the most enclosed squares wins"
            ])
        ]
    
    def draw(self, screen):
        if not self.visible:
            return
        
        # Draw window background with shadow
        shadow_rect = pygame.Rect(
            self.position[0] + 5,
            self.position[1] + 5,
            self.window_size[0],
            self.window_size[1]
        )
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, 0, 15)
        
        # Draw main window
        window_rect = pygame.Rect(
            self.position[0],
            self.position[1],
            self.window_size[0],
            self.window_size[1]
        )
        pygame.draw.rect(screen, (240, 248, 255), window_rect, 0, 15)  # Light blue background
        pygame.draw.rect(screen, (70, 130, 180), window_rect, 3, 15)   # Steel blue border
        
        # Draw title
        title = self.title_font.render("Game Rules", True, (25, 25, 25))
        title_rect = title.get_rect(center=(self.position[0] + self.window_size[0]//2, self.position[1] + 25))
        screen.blit(title, title_rect)
        
        # Draw close button
        button_color = self.close_button["hover_color"] if self.close_button["is_hovered"] else self.close_button["color"]
        pygame.draw.rect(screen, button_color, self.close_button["rect"], 0, 5)
        pygame.draw.rect(screen, (255, 255, 255), self.close_button["rect"], 2, 5)
        
        close_text = self.small_font.render(self.close_button["text"], True, self.close_button["text_color"])
        close_rect = close_text.get_rect(center=self.close_button["rect"].center)
        screen.blit(close_text, close_rect)
        
        # Draw rules sections
        y_offset = 70
        for section_title, rules in self.rules_sections:
            # Draw section title
            title = self.font.render(section_title, True, (25, 25, 25))
            screen.blit(title, (self.position[0] + 20, self.position[1] + y_offset))
            y_offset += 28  # Further reduced spacing
            
            # Draw rules
            for rule in rules:
                text = self.small_font.render(rule, True, (50, 50, 50))
                screen.blit(text, (self.position[0] + 30, self.position[1] + y_offset))
                y_offset += 22  # Further reduced spacing
            
            y_offset += 8  # Further reduced spacing between sections
    
    def handle_click(self, pos):
        if not self.visible:
            return False
        
        # Check if close button was clicked
        if self.close_button["rect"].collidepoint(pos):
            self.visible = False
            return True
        
        return False
    
    def handle_hover(self, pos):
        if not self.visible:
            return
        
        self.close_button["is_hovered"] = self.close_button["rect"].collidepoint(pos)

# Create rules window
rules_window = RulesWindow(WINDOW_SIZE)

# Font for buttons
button_font = pygame.font.SysFont("Arial", 20)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                
                # Handle rules window clicks first
                if rules_window.handle_click(mouse_pos):
                    continue
                
                # Only handle other clicks if rules window is not visible
                if not rules_window.visible:
                    # Check if restart button was clicked
                    if restart_button["rect"].collidepoint(mouse_pos):
                        # Reset the game
                        game_state = GameState()
                        game_state.debug = True  # Enable debug output
                    
                    # Check if random button was clicked during setup phase
                    elif game_state.phase == "setup" and random_button["rect"].collidepoint(mouse_pos):
                        randomize_pieces()
                    
                    # Check if rules button was clicked
                    elif rules_button["rect"].collidepoint(mouse_pos):
                        rules_window.visible = True
                    
                    # Otherwise handle game board clicks
                    else:
                        game_state.handle_click(mouse_pos, renderer.get_cell_size(), renderer.margin)
        
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            # Update button hover states
            restart_button["is_hovered"] = restart_button["rect"].collidepoint(mouse_pos)
            random_button["is_hovered"] = random_button["rect"].collidepoint(mouse_pos)
            rules_button["is_hovered"] = rules_button["rect"].collidepoint(mouse_pos)
            # Update rules window hover states
            rules_window.handle_hover(mouse_pos)
    
    # Update game state
    game_state.update()
    
    # Render the game
    renderer.render(game_state)
    
    # Draw buttons with hover effects
    # Restart button
    button_color = restart_button["hover_color"] if restart_button["is_hovered"] else restart_button["color"]
    pygame.draw.rect(screen, (0, 0, 0, 100), restart_button["rect"].move(3, 3), 0, 10)  # Shadow
    pygame.draw.rect(screen, button_color, restart_button["rect"], 0, 10)
    pygame.draw.rect(screen, (255, 255, 255), restart_button["rect"], 2, 10)  # Border
    
    text_surf = button_font.render(restart_button["text"], True, restart_button["text_color"])
    text_rect = text_surf.get_rect(center=restart_button["rect"].center)
    screen.blit(text_surf, text_rect)
    
    # Random button (only during setup phase)
    if game_state.phase == "setup":
        button_color = random_button["hover_color"] if random_button["is_hovered"] else random_button["color"]
        pygame.draw.rect(screen, (0, 0, 0, 100), random_button["rect"].move(3, 3), 0, 10)  # Shadow
        pygame.draw.rect(screen, button_color, random_button["rect"], 0, 10)
        pygame.draw.rect(screen, (255, 255, 255), random_button["rect"], 2, 10)  # Border
        
        text_surf = button_font.render(random_button["text"], True, random_button["text_color"])
        text_rect = text_surf.get_rect(center=random_button["rect"].center)
        screen.blit(text_surf, text_rect)
    
    # Rules button
    button_color = rules_button["hover_color"] if rules_button["is_hovered"] else rules_button["color"]
    pygame.draw.rect(screen, (0, 0, 0, 100), rules_button["rect"].move(3, 3), 0, 10)  # Shadow
    pygame.draw.rect(screen, button_color, rules_button["rect"], 0, 10)
    pygame.draw.rect(screen, (255, 255, 255), rules_button["rect"], 2, 10)  # Border
    
    text_surf = button_font.render(rules_button["text"], True, rules_button["text_color"])
    text_rect = text_surf.get_rect(center=rules_button["rect"].center)
    screen.blit(text_surf, text_rect)
    
    # Draw rules window if visible
    rules_window.draw(screen)
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
