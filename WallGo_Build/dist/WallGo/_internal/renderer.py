import pygame
import math

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
        # Draw red pieces
        for i, piece in enumerate(game_state.pieces[0]):
            if piece is not None:  # Only draw pieces that have been placed
                row, col = piece
                # Only show selection highlight if game is not over
                color = self.colors["selected"] if game_state.phase != "game_over" and game_state.current_player == 0 and game_state.selected_piece == i else self.colors["red_player"]
                self.draw_piece(row, col, color, game_state.isolated_pieces[0][i], "Red")
        
        # Draw blue pieces
        for i, piece in enumerate(game_state.pieces[1]):
            if piece is not None:  # Only draw pieces that have been placed
                row, col = piece
                # Only show selection highlight if game is not over
                color = self.colors["selected"] if game_state.phase != "game_over" and game_state.current_player == 1 and game_state.selected_piece == i else self.colors["blue_player"]
                self.draw_piece(row, col, color, game_state.isolated_pieces[1][i], "Blue")
    
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
            
            # If this is the current position (stay in place option), draw it differently
            piece_row, piece_col = game_state.pieces[game_state.current_player][game_state.selected_piece]
            if (row, col) == (piece_row, piece_col):
                # Draw a subtle pulsing highlight for the "stay in place" option
                pulse = (math.sin(self.animation_time * 2) + 1) * 0.1 + 0.9  # Value between 0.9 and 1.1 (much subtler)
                radius = self.cell_size * 0.35 * pulse
                pygame.draw.circle(self.screen, self.colors["stay_option"], (center_x, center_y), radius, 3)
                
                # Draw a timer indicator
                if not game_state.stay_option_available:
                    # Calculate the progress of the timer (0.0 to 1.0)
                    current_time = pygame.time.get_ticks()
                    elapsed = current_time - game_state.stay_in_place_timer
                    progress = min(1.0, elapsed / game_state.stay_in_place_delay)
                    
                    # Draw a progress arc
                    start_angle = -90  # Start at the top
                    end_angle = start_angle + (360 * progress)
                    rect = pygame.Rect(
                        center_x - radius, 
                        center_y - radius, 
                        radius * 2, 
                        radius * 2
                    )
                    pygame.draw.arc(self.screen, self.colors["timer"], rect, 
                                   math.radians(start_angle), 
                                   math.radians(end_angle), 
                                   3)
                    
                    # Draw "Wait..." text if still waiting
                    if progress < 1.0:
                        wait_text = self.small_font.render("Wait...", True, self.colors["timer"])
                        text_rect = wait_text.get_rect(center=(center_x, center_y + radius + 15))
                        self.screen.blit(wait_text, text_rect)
                else:
                    # Draw "Stay" text when option is available
                    stay_text = self.small_font.render("Stay", True, self.colors["stay_option"])
                    text_rect = stay_text.get_rect(center=(center_x, center_y + radius + 15))
                    self.screen.blit(stay_text, text_rect)
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
        
        # Draw the current player and game state message (only if not game over)
        if game_state.phase != "game_over":
            message = game_state.message
            text_surface = self.font.render(message, True, self.colors["text"])
            text_rect = text_surface.get_rect(center=(self.window_size / 2, self.margin / 2 + 20))
            self.screen.blit(text_surface, text_rect)
        
        # Draw the current player indicator (only if not game over)
        if game_state.phase != "game_over":
            player_color = self.colors["red_player"] if game_state.current_player == 0 else self.colors["blue_player"]
            player_name = game_state.player_colors[game_state.current_player]
            
            # Create a rounded rectangle for the player indicator
            indicator_width = 200
            indicator_height = 40
            indicator_x = (self.window_size - indicator_width) / 2
            indicator_y = self.window_size - self.margin / 2 - indicator_height / 2
            
            # Draw the indicator background with a shadow
            shadow_rect = pygame.Rect(indicator_x + 3, indicator_y + 3, indicator_width, indicator_height)
            pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, 0, 10)
            
            indicator_rect = pygame.Rect(indicator_x, indicator_y, indicator_width, indicator_height)
            pygame.draw.rect(self.screen, player_color, indicator_rect, 0, 10)
            pygame.draw.rect(self.screen, (255, 255, 255), indicator_rect, 2, 10)
            
            # Draw the player name
            player_text = self.font.render(f"{player_name}'s Turn", True, (255, 255, 255))
            player_text_rect = player_text.get_rect(center=(indicator_x + indicator_width / 2, indicator_y + indicator_height / 2))
            self.screen.blit(player_text, player_text_rect)
        
        # If in setup phase, draw placement instructions
        if game_state.phase == "setup":
            setup_text = "Click on the board to place your pieces or use the Randomize button"
            setup_surface = self.font.render(setup_text, True, self.colors["text"])
            setup_rect = setup_surface.get_rect(center=(self.window_size / 2, self.window_size - self.margin / 2 - 60))
            self.screen.blit(setup_surface, setup_rect)
        
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
            winner_box_width = max(400, required_width)  # At least 400px wide
            winner_box_height = max(200, required_height)  # At least 200px tall
            
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
            
            # Calculate vertical positions for each text element
            spacing = 40  # Space between elements
            total_content_height = (
                game_over_surface.get_height() +
                winner_surface.get_height() +
                score_surface.get_height() +
                play_again_surface.get_height() +
                spacing * 3  # Three spaces between four elements
            )
            
            start_y = winner_box_rect.centery - total_content_height / 2
            
            # Draw "Game Over!" text
            game_over_rect = game_over_surface.get_rect(center=(winner_box_rect.centerx, start_y + game_over_surface.get_height() / 2))
            self.screen.blit(game_over_surface, game_over_rect)
            
            # Draw the winner text with a glow effect
            winner_rect = winner_surface.get_rect(center=(winner_box_rect.centerx, game_over_rect.bottom + spacing + winner_surface.get_height() / 2))
            
            # Add glow effect
            for i in range(3, 0, -1):
                glow_rect = winner_rect.copy()
                glow_rect.move_ip(i, i)
                self.screen.blit(winner_surface, glow_rect)
            
            # Draw the main text
            self.screen.blit(winner_surface, winner_rect)
            
            # Draw the score information
            score_rect = score_surface.get_rect(center=(winner_box_rect.centerx, winner_rect.bottom + spacing + score_surface.get_height() / 2))
            self.screen.blit(score_surface, score_rect)
            
            # Draw "Play Again?" text
            play_again_rect = play_again_surface.get_rect(center=(winner_box_rect.centerx, score_rect.bottom + spacing + play_again_surface.get_height() / 2))
            self.screen.blit(play_again_surface, play_again_rect)
