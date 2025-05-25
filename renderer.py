import pygame
import math
import random

class GameRenderer:
    def __init__(self, screen, window_size):
        self.screen = screen
        self.window_size = window_size
        
        # Colors - enhanced color palette
        self.colors = {
            "background": (240, 248, 255),  # Alice Blue
            "grid": (176, 196, 222),  # Light Steel Blue
            "wall": (47, 79, 79),  # Dark Slate Gray
            "red_player": (220, 60, 60),  # Crimson Red
            "blue_player": (65, 105, 225),  # Royal Blue
            "selected": (255, 215, 0),  # Gold
            "valid_move": (60, 179, 113),  # Medium Sea Green
            "text": (25, 25, 25),  # Near Black
            "highlight": (255, 255, 224, 180),  # Light Yellow with transparency
            "stay_option": (0, 191, 255),  # Deep Sky Blue
            "timer": (255, 165, 0),  # Orange
            "isolated": (128, 128, 128),  # Gray
            "board_border": (70, 130, 180),  # Steel Blue
            "button": (70, 130, 180),  # Steel Blue
            "button_hover": (100, 149, 237),  # Cornflower Blue
            "button_text": (255, 255, 255)  # White
        }
        
        # Font
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 24)
        self.large_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 18)
        
        # Calculate cell size based on window size and board size
        self.board_size = 7  # This should match the game state's board size
        self.margin = 80
        self.board_pixel_size = window_size - 2 * self.margin
        self.cell_size = self.board_pixel_size / self.board_size
        
        # Load and scale background texture
        self.background = pygame.Surface((window_size, window_size))
        self.background.fill(self.colors["background"])
        
        # Create wood texture pattern for the board
        self.board_texture = self.create_board_texture()
        
        # Animation variables
        self.animation_time = 0
        self.pulse_speed = 0.005  # Speed of pulsing animations
        
        # Animation for piece movement
        self.moving_piece = None
        self.move_start_pos = None
        self.move_end_pos = None
        self.move_progress = 0
        self.move_duration = 300  # milliseconds
        self.move_start_time = 0
        
        # Animation for wall placement
        self.new_wall = None
        self.wall_animation_progress = 0
        self.wall_animation_duration = 300  # milliseconds
        self.wall_animation_start_time = 0
        
        # Load textures
        self.load_textures()
    
    def load_textures(self):
        # Create textures programmatically
        
        # Wood texture for the board
        self.wood_texture = pygame.Surface((200, 200))
        self.wood_texture.fill((210, 180, 140))  # Base wood color
        
        # Add wood grain
        for i in range(100):
            x = random.randint(0, 199)
            y = random.randint(0, 199)
            width = random.randint(5, 50)
            height = random.randint(1, 3)
            color_var = random.randint(-20, 20)
            color = (210 + color_var, 180 + color_var, 140 + color_var)
            pygame.draw.ellipse(self.wood_texture, color, (x, y, width, height))
        
        # Scale the texture to the board size
        self.wood_texture = pygame.transform.scale(self.wood_texture, (int(self.board_pixel_size), int(self.board_pixel_size)))
        
        # Create marble texture for pieces
        self.red_marble = self.create_marble_texture((220, 60, 60))
        self.blue_marble = self.create_marble_texture((65, 105, 225))
        
        # Create stone texture for walls
        self.wall_texture = self.create_stone_texture()
        
        # Create background pattern
        self.bg_pattern = self.create_background_pattern()
    
    def create_marble_texture(self, base_color):
        # Create a marble-like texture for pieces
        size = int(self.cell_size * 0.8)
        texture = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Base color
        r, g, b = base_color
        
        # Fill with base color
        texture.fill((r, g, b))
        
        # Add marble veins
        for i in range(15):
            vein_r = min(255, r + random.randint(20, 50))
            vein_g = min(255, g + random.randint(20, 50))
            vein_b = min(255, b + random.randint(20, 50))
            
            start_x = random.randint(0, size)
            start_y = random.randint(0, size)
            
            points = [(start_x, start_y)]
            for j in range(random.randint(3, 8)):
                next_x = max(0, min(size, points[-1][0] + random.randint(-10, 10)))
                next_y = max(0, min(size, points[-1][1] + random.randint(-10, 10)))
                points.append((next_x, next_y))
            
            pygame.draw.lines(texture, (vein_r, vein_g, vein_b, 150), False, points, random.randint(1, 3))
        
        # Add highlight
        highlight = pygame.Surface((size, size), pygame.SRCALPHA)
        highlight_rect = pygame.Rect(size//4, size//4, size//2, size//2)
        pygame.draw.ellipse(highlight, (255, 255, 255, 80), highlight_rect)
        texture.blit(highlight, (0, 0))
        
        return texture
    
    def create_stone_texture(self):
        # Create a stone-like texture for walls
        width = int(self.cell_size * 0.2)
        height = int(self.cell_size)
        texture = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Base color - dark gray
        base_color = (60, 60, 60)
        texture.fill(base_color)
        
        # Add stone pattern
        for i in range(20):
            color_var = random.randint(-15, 15)
            color = (base_color[0] + color_var, base_color[1] + color_var, base_color[2] + color_var)
            
            x = random.randint(0, width-5)
            y = random.randint(0, height-5)
            w = random.randint(3, width//2)
            h = random.randint(3, height//5)
            
            pygame.draw.ellipse(texture, color, (x, y, w, h))
        
        # Add highlight
        for i in range(5):
            x = random.randint(0, width-3)
            y = random.randint(0, height-3)
            w = random.randint(2, 4)
            h = random.randint(2, 4)
            pygame.draw.ellipse(texture, (150, 150, 150), (x, y, w, h))
        
        return texture
    
    def create_background_pattern(self):
        # Create a subtle background pattern
        pattern_size = 100
        pattern = pygame.Surface((pattern_size, pattern_size), pygame.SRCALPHA)
        
        # Fill with transparent color
        pattern.fill((0, 0, 0, 0))
        
        # Add subtle circles
        for i in range(5):
            x = random.randint(0, pattern_size)
            y = random.randint(0, pattern_size)
            radius = random.randint(10, 30)
            color = (200, 220, 255, 10)  # Very light blue, very transparent
            pygame.draw.circle(pattern, color, (x, y), radius)
        
        # Create a larger surface by tiling the pattern
        bg_width, bg_height = self.window_size, self.window_size
        bg_pattern = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        
        for x in range(0, bg_width, pattern_size):
            for y in range(0, bg_height, pattern_size):
                bg_pattern.blit(pattern, (x, y))
        
        return bg_pattern
    
    def create_board_texture(self):
        # Create a wood-like texture for the board
        texture = pygame.Surface((self.board_pixel_size, self.board_pixel_size))
        base_color = (210, 180, 140)  # Tan
        
        # Fill with base color
        texture.fill(base_color)
        
        # Add some grain lines
        for i in range(0, self.board_pixel_size, 4):
            grain_color = (base_color[0] - 10, base_color[1] - 5, base_color[2] - 15)
            pygame.draw.line(texture, grain_color, (0, i), (self.board_pixel_size, i), 1)
        
        # Add some random darker spots for texture
        for i in range(100):
            x = pygame.time.get_ticks() % self.board_pixel_size
            y = (pygame.time.get_ticks() * 1.5) % self.board_pixel_size
            radius = pygame.time.get_ticks() % 5 + 2
            spot_color = (base_color[0] - 20, base_color[1] - 15, base_color[2] - 25)
            pygame.draw.circle(texture, spot_color, (int(x), int(y)), radius)
        
        return texture
    
    def get_cell_size(self):
        return self.cell_size
    
    def render(self, game_state):
        # Update animation time
        self.animation_time = pygame.time.get_ticks() * self.pulse_speed
        
        # Clear the screen with the background
        self.screen.fill(self.colors["background"])
        
        # Draw decorative elements
        self.draw_decorations()
        
        # Draw the board background
        self.draw_board_background()
        
        # Draw the grid
        self.draw_grid(game_state)
        
        # Draw valid moves
        if game_state.phase == "move" and game_state.selected_piece is not None:
            self.draw_valid_moves(game_state)
        
        # Draw walls
        self.draw_walls(game_state)
        
        # Draw the pieces
        self.draw_pieces(game_state)
        
        # Draw the stay option on top of everything else
        if game_state.phase == "move" and game_state.selected_piece is not None:
            self.draw_stay_option(game_state)
        
        # Draw UI elements
        self.draw_ui(game_state)
    
    def draw_decorations(self):
        # Draw some decorative elements around the board
        # Draw a subtle pattern in the background
        for i in range(0, self.window_size, 40):
            alpha = (math.sin(self.animation_time + i * 0.1) + 1) * 10 + 5
            color = (200, 200, 220, int(alpha))
            pygame.draw.line(self.screen, color, (0, i), (self.window_size, i), 1)
            pygame.draw.line(self.screen, color, (i, 0), (i, self.window_size), 1)
    
    def draw_board_background(self):
        # Draw the board background with texture
        board_rect = pygame.Rect(
            self.margin - 10, 
            self.margin - 10, 
            self.board_pixel_size + 20, 
            self.board_pixel_size + 20
        )
        
        # Draw a shadow for the board
        shadow_rect = board_rect.copy()
        shadow_rect.move_ip(8, 8)
        pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, 0, 10)
        
        # Draw board background with rounded corners
        pygame.draw.rect(self.screen, (180, 140, 100), board_rect, 0, 10)
        
        # Draw the wood texture
        texture_rect = pygame.Rect(
            self.margin, 
            self.margin, 
            self.board_pixel_size, 
            self.board_pixel_size
        )
        self.screen.blit(self.board_texture, texture_rect)
        
        # Draw a border around the board
        pygame.draw.rect(self.screen, self.colors["board_border"], board_rect, 4, 10)
    
    def draw_grid(self, game_state):
        # Draw the grid
        for i in range(game_state.board_size + 1):
            # Vertical lines
            pygame.draw.line(
                self.screen,
                self.colors["grid"],
                (self.margin + i * self.cell_size, self.margin),
                (self.margin + i * self.cell_size, self.margin + self.board_pixel_size),
                2
            )
            
            # Horizontal lines
            pygame.draw.line(
                self.screen,
                self.colors["grid"],
                (self.margin, self.margin + i * self.cell_size),
                (self.margin + self.board_pixel_size, self.margin + i * self.cell_size),
                2
            )
    
    def draw_pieces(self, game_state):
        # First, store the selected piece position if there is one
        selected_piece_pos = None
        if game_state.phase != "game_over" and game_state.selected_piece is not None:
            selected_piece_pos = game_state.pieces[game_state.current_player][game_state.selected_piece]
        
        # Draw red pieces
        for i, piece in enumerate(game_state.pieces[0]):
            if piece is not None:  # Only draw pieces that have been placed
                # Skip the selected piece if it's the current player's turn - we'll draw it last
                if game_state.phase != "game_over" and game_state.current_player == 0 and game_state.selected_piece == i:
                    continue
                
                row, col = piece
                color = self.colors["selected"] if game_state.phase != "game_over" and game_state.current_player == 0 and game_state.selected_piece == i else self.colors["red_player"]
                self.draw_piece(row, col, color, game_state.isolated_pieces[0][i], "Red")
        
        # Draw blue pieces
        for i, piece in enumerate(game_state.pieces[1]):
            if piece is not None:  # Only draw pieces that have been placed
                # Skip the selected piece if it's the current player's turn - we'll draw it last
                if game_state.phase != "game_over" and game_state.current_player == 1 and game_state.selected_piece == i:
                    continue
                
                row, col = piece
                color = self.colors["selected"] if game_state.phase != "game_over" and game_state.current_player == 1 and game_state.selected_piece == i else self.colors["blue_player"]
                self.draw_piece(row, col, color, game_state.isolated_pieces[1][i], "Blue")
        
        # Now draw the selected piece last (on top of everything else)
        if selected_piece_pos is not None:
            row, col = selected_piece_pos
            color = self.colors["selected"]
            player_idx = game_state.current_player
            piece_idx = game_state.selected_piece
            self.draw_piece(row, col, color, game_state.isolated_pieces[player_idx][piece_idx], game_state.player_colors[player_idx])
    
    def draw_piece(self, row, col, color, is_isolated=False, player_name=""):
        center_x = self.margin + col * self.cell_size + self.cell_size / 2
        center_y = self.margin + row * self.cell_size + self.cell_size / 2
        radius = self.cell_size * 0.4
        
        # Draw shadow
        shadow_offset = 3
        pygame.draw.circle(self.screen, (0, 0, 0, 100), (center_x + shadow_offset, center_y + shadow_offset), radius)
        
        # Draw a black outline for better visibility
        pygame.draw.circle(self.screen, (0, 0, 0), (center_x, center_y), radius + 2)
        
        # Draw the piece with a subtle gradient effect
        for r in range(int(radius), 0, -2):
            # Lighten the color as we get closer to the center, but more subtly
            factor = 1 - (radius - r) / radius * 0.3  # Reduced from 0.5 to 0.3
            current_color = (
                min(255, int(color[0] * factor + 20)),  # Reduced from +50 to +20
                min(255, int(color[1] * factor + 20)),
                min(255, int(color[2] * factor + 20))
            )
            pygame.draw.circle(self.screen, current_color, (center_x, center_y), r)
        
        # If the piece is isolated, draw an indicator
        if is_isolated:
            # Draw an X over the piece to indicate it's isolated
            x_size = radius * 0.6
            pygame.draw.line(self.screen, (0, 0, 0), 
                           (center_x - x_size, center_y - x_size),
                           (center_x + x_size, center_y + x_size), 3)
            pygame.draw.line(self.screen, (0, 0, 0), 
                           (center_x + x_size, center_y - x_size),
                           (center_x - x_size, center_y + x_size), 3)
            
            # Draw "Isolated" text below the piece
            isolated_text = self.small_font.render("Isolated", True, (0, 0, 0))
            text_rect = isolated_text.get_rect(center=(center_x, center_y + radius + 15))
            self.screen.blit(isolated_text, text_rect)
    
    def draw_valid_moves(self, game_state):
        # Draw all valid moves
        for row, col in game_state.valid_moves:
            center_x = self.margin + col * self.cell_size + self.cell_size / 2
            center_y = self.margin + row * self.cell_size + self.cell_size / 2
            
            # If this is the current position (stay in place option), we'll draw it later
            piece_row, piece_col = game_state.pieces[game_state.current_player][game_state.selected_piece]
            if (row, col) == (piece_row, piece_col):
                # Skip drawing here - we'll draw it after the pieces
                continue
            else:
                # Regular valid move indicator with minimal pulsing
                pulse = (math.sin(self.animation_time * 1.5) + 1) * 0.05 + 0.95  # Value between 0.95 and 1.05 (very subtle)
                radius = self.cell_size * 0.2 * pulse
                pygame.draw.circle(self.screen, self.colors["valid_move"], (center_x, center_y), radius)
                
                # Draw a subtle shadow
                shadow_radius = radius * 0.8
                pygame.draw.circle(self.screen, (0, 0, 0, 30), (center_x + 2, center_y + 2), shadow_radius)
            
        # Highlight the selected piece's position
        if game_state.selected_piece is not None:
            piece_row, piece_col = game_state.pieces[game_state.current_player][game_state.selected_piece]
            center_x = self.margin + piece_col * self.cell_size + self.cell_size / 2
            center_y = self.margin + piece_row * self.cell_size + self.cell_size / 2
            
            # Draw a subtle highlight around the selected piece's position
            pulse = (math.sin(self.animation_time * 1.5) + 1) * 0.05 + 0.95  # Value between 0.95 and 1.05 (very subtle)
            rect_size = self.cell_size * pulse
            
            pygame.draw.rect(
                self.screen,
                self.colors["selected"],
                (
                    self.margin + piece_col * self.cell_size + (self.cell_size - rect_size) / 2,
                    self.margin + piece_row * self.cell_size + (self.cell_size - rect_size) / 2,
                    rect_size,
                    rect_size
                ),
                3,  # Border width
                5   # Rounded corners
            )
    
    def draw_stay_option(self, game_state):
        # Only draw if we're in move phase and have a selected piece
        if game_state.phase == "move" and game_state.selected_piece is not None:
            # Get the position of the selected piece
            piece_row, piece_col = game_state.pieces[game_state.current_player][game_state.selected_piece]
            center_x = self.margin + piece_col * self.cell_size + self.cell_size / 2
            center_y = self.margin + piece_row * self.cell_size + self.cell_size / 2
            
            # Draw an expanding circle animation for the "stay in place" option
            piece_radius = self.cell_size * 0.4  # Radius of the piece
            
            # Calculate the animation radius based on progress
            # Start from a small dot and expand to almost the piece size
            min_radius = piece_radius * 0.2
            max_radius = piece_radius * 0.9
            animation_radius = min_radius + (max_radius - min_radius) * game_state.stay_animation_progress
            
            # Use a bright contrasting color for the circle - white with thick border
            circle_color = (255, 255, 255)  # White
            border_color = (0, 0, 0)       # Black border
            
            # Draw the expanding circle with a black border to ensure visibility
            pygame.draw.circle(
                self.screen, 
                circle_color, 
                (center_x, center_y), 
                animation_radius, 
                0  # Filled circle
            )
            
            # Draw a border around the circle
            pygame.draw.circle(
                self.screen, 
                border_color, 
                (center_x, center_y), 
                animation_radius, 
                max(2, int(4 * (1 - game_state.stay_animation_progress)))  # Thicker border
            )
            
            # If the animation is complete, show "Stay" text in the center of the token
            if game_state.stay_option_available:
                # Draw text with black outline for better visibility
                stay_text = self.small_font.render("Stay", True, (0, 0, 0))  # Black text
                text_rect = stay_text.get_rect(center=(center_x, center_y))
                
                # Draw the text with a slight offset in multiple directions for an outline effect
                for offset_x, offset_y in [(1,1), (-1,1), (1,-1), (-1,-1)]:
                    offset_rect = text_rect.copy()
                    offset_rect.x += offset_x
                    offset_rect.y += offset_y
                    self.screen.blit(stay_text, offset_rect)
                
                # Draw the main text in a bright color
                stay_text = self.small_font.render("Stay", True, (255, 255, 0))  # Yellow text
                self.screen.blit(stay_text, text_rect)
    
    def draw_walls(self, game_state):
        # Draw horizontal walls
        for row in range(game_state.board_size + 1):
            for col in range(game_state.board_size):
                if game_state.walls[0][row][col]:
                    start_x = self.margin + col * self.cell_size
                    start_y = self.margin + row * self.cell_size
                    end_x = start_x + self.cell_size
                    end_y = start_y
                    
                    # Draw a shadow
                    shadow_offset = 3
                    pygame.draw.line(
                        self.screen, 
                        (0, 0, 0, 100), 
                        (start_x + shadow_offset, start_y + shadow_offset), 
                        (end_x + shadow_offset, end_y + shadow_offset), 
                        8
                    )
                    
                    # Draw the wall
                    pygame.draw.line(self.screen, self.colors["wall"], (start_x, start_y), (end_x, end_y), 6)
        
        # Draw vertical walls
        for row in range(game_state.board_size):
            for col in range(game_state.board_size + 1):
                if game_state.walls[1][row][col]:
                    start_x = self.margin + col * self.cell_size
                    start_y = self.margin + row * self.cell_size
                    end_x = start_x
                    end_y = start_y + self.cell_size
                    
                    # Draw a shadow
                    shadow_offset = 3
                    pygame.draw.line(
                        self.screen, 
                        (0, 0, 0, 100), 
                        (start_x + shadow_offset, start_y + shadow_offset), 
                        (end_x + shadow_offset, end_y + shadow_offset), 
                        8
                    )
                    
                    # Draw the wall
                    pygame.draw.line(self.screen, self.colors["wall"], (start_x, start_y), (end_x, end_y), 6)
        
        # If in wall placement phase, highlight grid lines near the moved piece
        if game_state.phase == "wall":
            piece_row, piece_col = game_state.pieces[game_state.current_player][game_state.selected_piece]
            
            # Highlight horizontal walls that can be placed
            for row in [piece_row, piece_row + 1]:
                if 0 <= row <= game_state.board_size:
                    start_x = self.margin + piece_col * self.cell_size
                    start_y = self.margin + row * self.cell_size
                    end_x = start_x + self.cell_size
                    end_y = start_y
                    
                    if not game_state.walls[0][row][piece_col]:
                        # Very subtle pulsing effect
                        pulse = (math.sin(self.animation_time * 1.5) + 1) * 0.05 + 0.95  # Value between 0.95 and 1.05
                        
                        # Draw a glowing line
                        for i in range(2, 0, -1):
                            alpha = 100 - i * 30
                            color = (100, 200, 255, alpha)
                            width = int(3 * pulse) + i
                            pygame.draw.line(self.screen, color, (start_x, start_y), (end_x, end_y), width)
                        
                        # Draw the main line
                        pygame.draw.line(
                            self.screen, 
                            (100, 200, 255), 
                            (start_x, start_y), 
                            (end_x, end_y), 
                            3
                        )
            
            # Highlight vertical walls that can be placed
            for col in [piece_col, piece_col + 1]:
                if 0 <= col <= game_state.board_size:
                    start_x = self.margin + col * self.cell_size
                    start_y = self.margin + piece_row * self.cell_size
                    end_x = start_x
                    end_y = start_y + self.cell_size
                    
                    if not game_state.walls[1][piece_row][col]:
                        # Very subtle pulsing effect
                        pulse = (math.sin(self.animation_time * 1.5 + 1) + 1) * 0.05 + 0.95  # Value between 0.95 and 1.05
                        
                        # Draw a glowing line
                        for i in range(2, 0, -1):
                            alpha = 100 - i * 30
                            color = (100, 200, 255, alpha)
                            width = int(3 * pulse) + i
                            pygame.draw.line(self.screen, color, (start_x, start_y), (end_x, end_y), width)
                        
                        # Draw the main line
                        pygame.draw.line(
                            self.screen, 
                            (100, 200, 255), 
                            (start_x, start_y), 
                            (end_x, end_y), 
                            3
                        )
                        
            # Draw a highlight around the moved piece's position
            pygame.draw.rect(
                self.screen,
                (255, 200, 0, 128),  # Orange-yellow with transparency
                (
                    self.margin + piece_col * self.cell_size,
                    self.margin + piece_row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                ),
                2,  # Border width
                5   # Rounded corners
            )
    
    def draw_ui(self, game_state):
        # Draw game title
        title_text = self.large_font.render("WallGo", True, self.colors["text"])
        title_rect = title_text.get_rect(center=(self.window_size / 2, self.margin / 2 - 10))
        self.screen.blit(title_text, title_rect)
        
        # Draw the current player indicator (only if not game over)
        if game_state.phase != "game_over":
            player_color = self.colors["red_player"] if game_state.current_player == 0 else self.colors["blue_player"]
            player_name = game_state.player_colors[game_state.current_player]
            
            # Extract the instruction part from the message
            message = game_state.message
            instruction_part = ""
            if ":" in message:
                instruction_part = message.split(":", 1)[1].strip()
            
            # Create a rounded rectangle for the player indicator
            indicator_width = 400  # Increased width to accommodate instructions
            indicator_height = 40
            indicator_x = (self.window_size - indicator_width) / 2
            indicator_y = self.window_size - self.margin / 2 - indicator_height / 2
            
            # Draw the indicator background with a shadow
            shadow_rect = pygame.Rect(indicator_x + 3, indicator_y + 3, indicator_width, indicator_height)
            pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, 0, 10)
            
            indicator_rect = pygame.Rect(indicator_x, indicator_y, indicator_width, indicator_height)
            pygame.draw.rect(self.screen, player_color, indicator_rect, 0, 10)
            pygame.draw.rect(self.screen, (255, 255, 255), indicator_rect, 2, 10)
            
            # Draw the player name and instruction
            player_text = self.font.render(f"{player_name}'s Turn: {instruction_part}", True, (255, 255, 255))
            player_text_rect = player_text.get_rect(center=(indicator_x + indicator_width / 2, indicator_y + indicator_height / 2))
            self.screen.blit(player_text, player_text_rect)
        
        # If in setup phase, draw placement instructions
        if game_state.phase == "setup":
            # No additional instructions needed here anymore
            pass
        
        # If in move phase, draw movement instructions
        elif game_state.phase == "move":
            move_text = "Click on a highlighted cell to move (including current position to stay)"
            move_surface = self.font.render(move_text, True, self.colors["text"])
            move_rect = move_surface.get_rect(center=(self.window_size / 2, self.window_size - self.margin / 2 - 60))
            self.screen.blit(move_surface, move_rect)
        
        # If in wall phase, draw wall placement instructions
        elif game_state.phase == "wall":
            wall_text = "Click on a highlighted line to place a wall"
            wall_surface = self.font.render(wall_text, True, self.colors["text"])
            wall_rect = wall_surface.get_rect(center=(self.window_size / 2, self.window_size - self.margin / 2 - 60))
            self.screen.blit(wall_surface, wall_rect)
        
        # If game is over, display the winner in the center of the screen
        elif game_state.phase == "game_over":
            if game_state.winner == 0:
                winner_text = "Red Wins!"
                color = self.colors["red_player"]
            elif game_state.winner == 1:
                winner_text = "Blue Wins!"
                color = self.colors["blue_player"]
            else:
                winner_text = "It's a Tie!"
                color = self.colors["text"]
            
            # Extract the score information from the message
            score_info = game_state.message.split("Game Over! ")[1]
            
            # Pre-render all text to calculate the required box size
            game_over_surface = self.font.render("Game Over!", True, (255, 255, 255))
            winner_surface = self.large_font.render(winner_text, True, (255, 255, 255))
            score_surface = self.font.render(score_info, True, (255, 255, 255))
            play_again_surface = self.font.render("Click 'Restart Game' to play again", True, (255, 255, 255))
            
            # Calculate the required width and height for the box
            required_width = max(
                game_over_surface.get_width(),
                winner_surface.get_width(),
                score_surface.get_width(),
                play_again_surface.get_width()
            ) + 60  # Add padding
            
            required_height = (
                game_over_surface.get_height() +
                winner_surface.get_height() +
                score_surface.get_height() +
                play_again_surface.get_height() +
                80  # Add spacing between elements and padding
            )
            
            # Create a properly sized winner announcement box
            winner_box_width = 450  # Increased width
            winner_box_height = 250  # Increased height
            
            winner_box_rect = pygame.Rect(
                self.window_size / 2 - winner_box_width / 2,
                self.window_size / 2 - winner_box_height / 2,
                winner_box_width,
                winner_box_height
            )
            
            # Draw a shadow
            shadow_rect = winner_box_rect.copy()
            shadow_rect.move_ip(8, 8)
            pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, 0, 15)
            
            # Draw the background
            pygame.draw.rect(self.screen, color, winner_box_rect, 0, 15)
            pygame.draw.rect(self.screen, (255, 255, 255), winner_box_rect, 3, 15)
            
            # Draw "Game Over!" text
            game_over_rect = game_over_surface.get_rect(center=(winner_box_rect.centerx, winner_box_rect.centery - 100))
            self.screen.blit(game_over_surface, game_over_rect)
            
            # Draw the winner text with a glow effect
            winner_rect = winner_surface.get_rect(center=(winner_box_rect.centerx, winner_box_rect.centery - 60))
            
            # Add glow effect
            for i in range(3, 0, -1):
                glow_rect = winner_rect.copy()
                glow_rect.move_ip(i, i)
                self.screen.blit(winner_surface, glow_rect)
            
            # Draw the main text
            self.screen.blit(winner_surface, winner_rect)
            
            # Draw the score information
            score_rect = score_surface.get_rect(center=(winner_box_rect.centerx, winner_box_rect.centery - 10))
            self.screen.blit(score_surface, score_rect)
            
            # Draw "Play Again?" text with more prominence
            play_again_surface = self.large_font.render("Press Restart to Play Again", True, (255, 255, 255))
            play_again_rect = play_again_surface.get_rect(center=(winner_box_rect.centerx, winner_box_rect.centery + 50))
            self.screen.blit(play_again_surface, play_again_rect)
            
            # No arrow - removed to avoid strange white line
