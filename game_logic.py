import pygame
import random

class GameState:
    def __init__(self):
        # Board size (7x7 grid)
        self.board_size = 7
        
        # Initialize the board (None means empty cell)
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Initialize walls (horizontal and vertical)
        # walls[0] = horizontal walls, walls[1] = vertical walls
        # True means a wall exists
        self.walls = [
            [[False for _ in range(self.board_size)] for _ in range(self.board_size + 1)],  # Horizontal walls
            [[False for _ in range(self.board_size + 1)] for _ in range(self.board_size)]   # Vertical walls
        ]
        
        # Set outer edges as permanent walls
        for i in range(self.board_size):
            # Top and bottom edges
            self.walls[0][0][i] = True
            self.walls[0][self.board_size][i] = True
            # Left and right edges
            self.walls[1][i][0] = True
            self.walls[1][i][self.board_size] = True
        
        # Players (0 = Red, 1 = Blue)
        self.current_player = 0
        self.player_colors = ["Red", "Blue"]
        
        # Pieces (2 per player)
        # Format: [row, col]
        # Initialize with None to indicate pieces need to be placed
        self.pieces = [
            [None, None],  # Red pieces
            [None, None]   # Blue pieces
        ]
        
        # Game state
        self.selected_piece = None
        self.valid_moves = []
        self.phase = "setup"  # "setup", "select", "move", "wall", "game_over"
        self.setup_piece_count = 0  # Track how many pieces have been placed
        self.winner = None
        self.message = f"{self.player_colors[self.current_player]}'s turn: Place your first piece"
        
        # Timing for "stay in place" option
        self.stay_in_place_timer = 0
        self.stay_in_place_delay = 1000  # 1 second in milliseconds (reduced from 2000)
        self.stay_option_available = False
        self.stay_animation_progress = 0.0  # Animation progress from 0.0 to 1.0
        
        # Track isolated pieces (pieces in 1x1 squares)
        self.isolated_pieces = [
            [False, False],  # Red pieces
            [False, False]   # Blue pieces
        ]
        
        # Debug flag
        self.debug = False
    
    def handle_click(self, mouse_pos, cell_size, margin):
        # Adjust mouse position to account for the board margin
        board_x = mouse_pos[0] - margin
        board_y = mouse_pos[1] - margin
        
        # Check if click is within the board boundaries
        if board_x < 0 or board_y < 0 or board_x > cell_size * self.board_size or board_y > cell_size * self.board_size:
            return  # Click is outside the board
        
        # Convert mouse position to grid coordinates
        col = int(board_x // cell_size)
        row = int(board_y // cell_size)
        
        # Handle based on current phase
        if self.phase == "setup":
            self.handle_setup(row, col)
        elif self.phase == "select":
            self.handle_select(row, col)
        elif self.phase == "move":
            self.handle_move(row, col)
        elif self.phase == "wall":
            # Check if clicked on a valid wall position
            self.handle_wall_placement(mouse_pos, cell_size, margin)
    
    def handle_setup(self, row, col):
        # Check if the cell is already occupied
        for player_pieces in self.pieces:
            for piece in player_pieces:
                if piece is not None and piece == (row, col):
                    self.message = "This cell is already occupied. Choose another."
                    return
        
        # Determine which player's turn it is (alternating Red/Blue/Red/Blue)
        player_idx = self.setup_piece_count % 2  # 0 for Red, 1 for Blue
        
        # Determine which piece to place (first or second for each player)
        piece_idx = self.setup_piece_count // 2  # 0 for first piece, 1 for second piece
        
        # Place the piece
        self.pieces[player_idx][piece_idx] = (row, col)
        self.setup_piece_count += 1
        
        # Update message for next piece placement
        if self.setup_piece_count < 4:
            next_player = self.setup_piece_count % 2  # Alternate between Red (0) and Blue (1)
            piece_number = "first" if self.setup_piece_count // 2 == 0 else "second"
            self.message = f"{self.player_colors[next_player]}'s turn: Place your {piece_number} piece"
        else:
        # All pieces placed, start the game
            self.phase = "select"
            self.current_player = random.randint(0, 1)  # Randomly choose Red (0) or Blue (1) to start
            self.message = f"{self.player_colors[self.current_player]}'s turn: Select a piece"
    
    def handle_select(self, row, col):
        # Check if the clicked position contains one of the current player's pieces
        for i, piece in enumerate(self.pieces[self.current_player]):
            if piece == (row, col):
                # Check if this piece is isolated (in a 1x1 square)
                if self.isolated_pieces[self.current_player][i]:
                    self.message = f"This piece is isolated and cannot be moved."
                    return
                
                self.selected_piece = i
                self.valid_moves = self.get_valid_moves(piece)
                self.phase = "move"
                self.message = f"{self.player_colors[self.current_player]}: Move your piece"
                
                # Reset the stay in place timer
                self.stay_in_place_timer = 0
                self.stay_option_available = False
                self.stay_animation_progress = 0.0
                return
        
        self.message = f"{self.player_colors[self.current_player]}: Select your piece"
    
    def handle_move(self, row, col):
        # Check if the clicked position is a valid move
        if (row, col) in self.valid_moves:
            # Move the piece (or stay in place if that's the chosen option)
            self.pieces[self.current_player][self.selected_piece] = (row, col)
            self.phase = "wall"
            self.message = f"{self.player_colors[self.current_player]}: Place a wall"
        elif any(piece == (row, col) for piece in self.pieces[self.current_player]):
            # If player clicked on another of their pieces, select that one instead
            for i, piece in enumerate(self.pieces[self.current_player]):
                if piece == (row, col):
                    self.selected_piece = i
                    self.valid_moves = self.get_valid_moves(piece)
                    self.message = f"{self.player_colors[self.current_player]}: Move your piece"
                    return
        else:
            self.message = "Invalid move. Try again."
    
    def handle_wall_placement(self, mouse_pos, cell_size, margin):
        # Get the position of the moved piece
        piece_row, piece_col = self.pieces[self.current_player][self.selected_piece]
        
        # Calculate the grid position of the click
        board_x = mouse_pos[0] - margin
        board_y = mouse_pos[1] - margin
        
        # Calculate the floating point grid position
        row_float = board_y / cell_size
        col_float = board_x / cell_size
        
        # Round to the nearest integer to get the grid cell
        row_int = int(round(row_float))
        col_int = int(round(col_float))
        
        # Calculate the distance to the nearest horizontal and vertical grid lines
        dist_to_horizontal = abs(row_float - row_int)
        dist_to_vertical = abs(col_float - col_int)
        
        # Threshold for detecting clicks on grid lines
        threshold = 0.2
        
        # Check if the click is close to a grid line
        if dist_to_horizontal < dist_to_vertical:
            # Horizontal wall
            row_wall = round(row_float)
            
            # Ensure row_wall is within bounds
            if 0 <= row_wall <= self.board_size and 0 <= col_int < self.board_size:
                # Check if the distance is within threshold
                if dist_to_horizontal < threshold:
                    if not self.walls[0][row_wall][col_int]:
                        # Check if wall is adjacent to the moved piece
                        if self.is_adjacent_to_piece(row_wall, col_int, "horizontal", piece_row, piece_col):
                            self.walls[0][row_wall][col_int] = True
                            self.end_turn()
                        else:
                            self.message = "Wall must be adjacent to the moved piece"
                    else:
                        self.message = "A wall already exists here"
        else:
            # Vertical wall
            col_wall = round(col_float)
            
            # Ensure col_wall is within bounds
            if 0 <= row_int < self.board_size and 0 <= col_wall <= self.board_size:
                # Check if the distance is within threshold
                if dist_to_vertical < threshold:
                    if not self.walls[1][row_int][col_wall]:
                        # Check if wall is adjacent to the moved piece
                        if self.is_adjacent_to_piece(row_int, col_wall, "vertical", piece_row, piece_col):
                            self.walls[1][row_int][col_wall] = True
                            self.end_turn()
                        else:
                            self.message = "Wall must be adjacent to the moved piece"
                    else:
                        self.message = "A wall already exists here"
    
    def is_adjacent_to_piece(self, wall_row, wall_col, wall_type, piece_row, piece_col):
        """Check if a wall is adjacent to a piece's position."""
        if wall_type == "horizontal":
            # For horizontal walls, check if the wall is directly above or below the piece
            return (wall_row == piece_row and wall_col == piece_col) or \
                   (wall_row == piece_row + 1 and wall_col == piece_col)
        else:  # vertical
            # For vertical walls, check if the wall is directly to the left or right of the piece
            return (wall_col == piece_col and wall_row == piece_row) or \
                   (wall_col == piece_col + 1 and wall_row == piece_row)
    
    def end_turn(self):
        # Check if game is over
        if self.check_game_over():
            self.phase = "game_over"
            # Calculate enclosed areas for each piece
            areas = self.calculate_enclosed_areas()
            red_area = sum(areas[0])
            blue_area = sum(areas[1])
            
            if self.debug:
                print(f"Game over! Areas: Red = {areas[0]}, Blue = {areas[1]}")
            
            if red_area > blue_area:
                self.winner = 0  # Red wins
                self.message = f"Game Over! Red wins with {red_area} squares vs Blue's {blue_area} squares"
            elif blue_area > red_area:
                self.winner = 1  # Blue wins
                self.message = f"Game Over! Blue wins with {blue_area} squares vs Red's {red_area} squares"
            else:
                self.winner = -1  # Tie
                self.message = f"Game Over! It's a tie with {red_area} squares each"
        else:
            # Switch to the other player
            self.current_player = 1 - self.current_player
            self.selected_piece = None
            self.valid_moves = []
            self.phase = "select"
            self.message = f"{self.player_colors[self.current_player]}'s turn: Select a piece"
    
    def update(self):
        # Update the stay in place timer if needed
        current_time = pygame.time.get_ticks()
        
        # If we're in the move phase and have a selected piece
        if self.phase == "move" and self.selected_piece is not None:
            # If the timer hasn't been started yet
            if self.stay_in_place_timer == 0:
                self.stay_in_place_timer = current_time
                self.stay_option_available = False
                self.stay_animation_progress = 0.0
            # If the delay has passed
            elif current_time - self.stay_in_place_timer >= self.stay_in_place_delay:
                self.stay_option_available = True
                self.stay_animation_progress = 1.0
            else:
                # Calculate animation progress (0.0 to 1.0)
                self.stay_animation_progress = (current_time - self.stay_in_place_timer) / self.stay_in_place_delay
        else:
            # Reset the timer if we're not in the move phase
            self.stay_in_place_timer = 0
            self.stay_option_available = False
            self.stay_animation_progress = 0.0
            
        # Update isolated pieces status
        self.update_isolated_pieces()
    
    def update_isolated_pieces(self):
        """Update which pieces are isolated in 1x1 squares."""
        for player in range(2):
            for piece_idx in range(2):
                if self.pieces[player][piece_idx] is not None:
                    row, col = self.pieces[player][piece_idx]
                    
                    # Check if this piece is in a 1x1 square
                    # This means walls on all four sides
                    top_wall = self.walls[0][row][col]  # Wall above
                    bottom_wall = self.walls[0][row + 1][col]  # Wall below
                    left_wall = self.walls[1][row][col]  # Wall to the left
                    right_wall = self.walls[1][row][col + 1]  # Wall to the right
                    
                    # If all four walls exist, the piece is isolated
                    self.isolated_pieces[player][piece_idx] = (top_wall and bottom_wall and left_wall and right_wall)
    
    def get_valid_moves(self, piece):
        row, col = piece
        valid_moves = []
        
        # Add the current position as a valid "move" (stay in place) only if the delay has passed
        if self.stay_option_available:
            valid_moves.append((row, col))
        
        # Check moves in all four directions (up, right, down, left)
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        # First, add all valid one-step moves
        one_step_moves = []
        for dr, dc in directions:
            # Check one step in this direction
            new_row, new_col = row + dr, col + dc
            if self.is_valid_move(row, col, new_row, new_col):
                valid_moves.append((new_row, new_col))
                one_step_moves.append((new_row, new_col, dr, dc))
                
        # Now add all valid two-step moves
        for new_row, new_col, dr, dc in one_step_moves:
            # Continue in the same direction (straight line)
            straight_row, straight_col = new_row + dr, new_col + dc
            if self.is_valid_move(new_row, new_col, straight_row, straight_col):
                valid_moves.append((straight_row, straight_col))
            
            # Add L-shaped moves (turn 90 degrees after first step)
            for turn_dr, turn_dc in directions:
                # Skip continuing in the same direction (already handled)
                if (turn_dr, turn_dc) == (dr, dc) or (turn_dr, turn_dc) == (-dr, -dc):
                    continue
                
                # Check the L-shaped move
                l_row, l_col = new_row + turn_dr, new_col + turn_dc
                if self.is_valid_move(new_row, new_col, l_row, l_col):
                    valid_moves.append((l_row, l_col))
        
        return valid_moves
    
    def is_valid_move(self, from_row, from_col, to_row, to_col):
        # Check if destination is within bounds
        if not (0 <= to_row < self.board_size and 0 <= to_col < self.board_size):
            return False
        
        # Check if destination is occupied by any piece
        for player in range(2):
            for piece in self.pieces[player]:
                if piece is not None and piece == (to_row, to_col):
                    # Allow the destination to be the target piece when checking for paths
                    # This is needed for the has_path function
                    if (to_row, to_col) == (from_row, from_col):
                        continue
                    return False
        
        # Check if there's a wall between the cells
        if from_row == to_row:
            # Horizontal movement
            min_col = min(from_col, to_col)
            max_col = max(from_col, to_col)
            for col in range(min_col, max_col):
                if self.walls[1][from_row][col + 1]:  # Check vertical walls
                    return False
        elif from_col == to_col:
            # Vertical movement
            min_row = min(from_row, to_row)
            max_row = max(from_row, to_row)
            for row in range(min_row, max_row):
                if self.walls[0][row + 1][from_col]:  # Check horizontal walls
                    return False
        
        return True
    
    def check_game_over(self):
        """
        Check if the game is over.
        The game is over when all four pieces are isolated from each other:
        - Red piece 1 cannot reach Red piece 2
        - Blue piece 1 cannot reach Blue piece 2
        - No red piece can reach any blue piece
        """
        # Get all piece positions
        red_pieces = self.pieces[0]
        blue_pieces = self.pieces[1]
        
        # Check if red pieces can reach each other
        if self.has_path(red_pieces[0][0], red_pieces[0][1], red_pieces[1][0], red_pieces[1][1]):
            if self.debug:
                print(f"Red pieces can reach each other")
            return False
        
        # Check if blue pieces can reach each other
        if self.has_path(blue_pieces[0][0], blue_pieces[0][1], blue_pieces[1][0], blue_pieces[1][1]):
            if self.debug:
                print(f"Blue pieces can reach each other")
            return False
        
        # Check if any red piece can reach any blue piece
        for red_piece in red_pieces:
            for blue_piece in blue_pieces:
                if self.has_path(red_piece[0], red_piece[1], blue_piece[0], blue_piece[1]):
                    if self.debug:
                        print(f"Red piece at {red_piece} can reach blue piece at {blue_piece}")
                    return False
        
        # If we get here, all pieces are isolated from each other
        return True
    
    def has_path(self, start_row, start_col, target_row, target_col):
        """Check if there's a path between two positions using BFS."""
        # If start and target are the same, return True
        if (start_row, start_col) == (target_row, target_col):
            return True
            
        # Create a queue for BFS
        queue = [(start_row, start_col)]
        # Create a set to track visited cells
        visited = set([(start_row, start_col)])
        
        # BFS
        while queue:
            row, col = queue.pop(0)
            
            # Try all four directions
            directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                # Check if we've reached the target
                if new_row == target_row and new_col == target_col:
                    # Check if there's no wall between current cell and target
                    if not self.has_wall_between(row, col, new_row, new_col):
                        return True
                
                # Check if the move is valid and the cell hasn't been visited
                if (0 <= new_row < self.board_size and 
                    0 <= new_col < self.board_size and 
                    (new_row, new_col) not in visited and
                    not self.has_wall_between(row, col, new_row, new_col)):
                    queue.append((new_row, new_col))
                    visited.add((new_row, new_col))
        
        # If we've exhausted all possible moves and haven't found the target, there's no path
        return False
    
    def has_wall_between(self, row1, col1, row2, col2):
        """Check if there's a wall between two adjacent cells."""
        # Check horizontal wall
        if row1 == row2:
            # Moving horizontally
            min_col = min(col1, col2)
            return self.walls[1][row1][min_col + 1]
        else:
            # Moving vertically
            min_row = min(row1, row2)
            return self.walls[0][min_row + 1][col1]
    
    def calculate_enclosed_areas(self):
        """Calculate the enclosed area for each piece."""
        areas = [
            [0, 0],  # Red pieces
            [0, 0]   # Blue pieces
        ]
        
        # For each piece, perform a flood fill to find its enclosed area
        for player in range(2):
            for piece_idx in range(2):
                row, col = self.pieces[player][piece_idx]
                
                # Create a visited grid for flood fill
                visited = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
                
                # Perform flood fill from this piece
                self.flood_fill(row, col, visited)
                
                # Count the number of cells in the enclosed area
                area = sum(row.count(True) for row in visited)
                areas[player][piece_idx] = area
        
        return areas
    
    def flood_fill(self, row, col, visited):
        """Perform a flood fill from a given position."""
        # If the cell is out of bounds or already visited, return
        if not (0 <= row < self.board_size and 0 <= col < self.board_size) or visited[row][col]:
            return
        
        # Mark the cell as visited
        visited[row][col] = True
        
        # Try all four directions
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check if the move is valid and the cell hasn't been visited
            if (0 <= new_row < self.board_size and 
                0 <= new_col < self.board_size and 
                not visited[new_row][new_col] and
                not self.has_wall_between(row, col, new_row, new_col)):
                self.flood_fill(new_row, new_col, visited)
