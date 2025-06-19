import tkinter as tk
import random
import copy
import time
from tkinter import messagebox, font

class UltimateTicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ultimate Tic-Tac-Toe")
        self.root.configure(bg="#333")
        
        # Game state
        self.board = [[[[' ' for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.small_board_status = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.next_board = None  # (row, col) of next small board, None if any
        self.game_over = False
        self.winner = None
        
        # AI settings
        self.player_mode = "Human vs AI"  # Default mode
        self.ai_difficulty = "Medium"     # Default difficulty
        
        # Colors
        self.bg_color = "#333"
        self.board_color = "#444"
        self.x_color = "#ff6b6b"
        self.o_color = "#48dbfb"
        self.highlight_color = "#f7d794"
        self.won_board_colors = {
            'X': "#ffcccc",
            'O': "#cce5ff",
            'D': "#999999",  # Add this line for drawn boards
            ' ': "#444"
        }
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Create control frame
        self.control_frame = tk.Frame(self.main_frame, bg=self.bg_color, pady=10)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Mode selection
        self.mode_label = tk.Label(self.control_frame, text="Mode:", bg=self.bg_color, fg="white")
        self.mode_label.pack(side=tk.LEFT, padx=5)
        
        self.mode_var = tk.StringVar(value=self.player_mode)
        self.mode_menu = tk.OptionMenu(self.control_frame, self.mode_var, 
                                      "Human vs Human", "Human vs AI", "AI vs AI",
                                      command=self.change_mode)
        self.mode_menu.config(bg="#555", fg="white", activebackground="#666", activeforeground="white")
        self.mode_menu["menu"].config(bg="#555", fg="white", activebackground="#666", activeforeground="white")
        self.mode_menu.pack(side=tk.LEFT, padx=5)
        
        # AI difficulty
        self.difficulty_label = tk.Label(self.control_frame, text="AI Difficulty:", bg=self.bg_color, fg="white")
        self.difficulty_label.pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value=self.ai_difficulty)
        self.difficulty_menu = tk.OptionMenu(self.control_frame, self.difficulty_var, 
                                           "Easy", "Medium", "Hard",
                                           command=self.change_difficulty)
        self.difficulty_menu.config(bg="#555", fg="white", activebackground="#666", activeforeground="white")
        self.difficulty_menu["menu"].config(bg="#555", fg="white", activebackground="#666", activeforeground="white")
        self.difficulty_menu.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        self.reset_button = tk.Button(self.control_frame, text="New Game", command=self.reset_game,
                                    bg="#28a745", fg="white", activebackground="#218838", padx=10)
        self.reset_button.pack(side=tk.RIGHT, padx=5)
        
        # Status frame
        self.status_frame = tk.Frame(self.main_frame, bg=self.bg_color, pady=10)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status message
        self.status_var = tk.StringVar(value="Player X's turn")
        self.status_label = tk.Label(self.status_frame, textvariable=self.status_var, 
                                  bg=self.bg_color, fg="white", font=("Arial", 14))
        self.status_label.pack(expand=True)
        
        # Game board frame
        self.game_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.game_frame.pack(expand=True, pady=10)
        
        # Create the board GUI
        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                # Create a frame for each small board
                board_frame = tk.Frame(self.game_frame, bg=self.board_color, padx=5, pady=5,
                                     highlightbackground="white", highlightthickness=1)
                board_frame.grid(row=i, column=j, padx=5, pady=5)
                
                small_board_buttons = []
                for m in range(3):
                    row_small_buttons = []
                    for n in range(3):
                        btn = tk.Button(board_frame, text=' ', width=3, height=1, font=('Arial', 14),
                                       bg="white", command=lambda i=i, j=j, m=m, n=n: self.make_move(i, j, m, n))
                        btn.grid(row=m, column=n, padx=1, pady=1)
                        row_small_buttons.append(btn)
                    small_board_buttons.append(row_small_buttons)
                row_buttons.append(small_board_buttons)
            self.buttons.append(row_buttons)
        
        # Initialize the board highlighting
        self.update_board_highlighting()
    
    def change_mode(self, mode):
        self.player_mode = mode
        self.reset_game()
    
    def change_difficulty(self, difficulty):
        self.ai_difficulty = difficulty
    
    def reset_game(self):
        # Reset game state
        self.board = [[[[' ' for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.small_board_status = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.next_board = None
        self.game_over = False
        self.winner = None
        
        # Reset GUI buttons
        for i in range(3):
            for j in range(3):
                for m in range(3):
                    for n in range(3):
                        self.buttons[i][j][m][n].config(text=' ', bg="white", state=tk.NORMAL)
                
                # Reset small board background colors
                self.buttons[i][j][0][0].master.config(bg=self.board_color)
        
        # Update status
        self.status_var.set("Player X's turn")
        
        # Update highlighting
        self.update_board_highlighting()
        
        # Start AI if needed
        if self.player_mode != "Human vs Human" and self.current_player == 'O':
            self.root.after(500, self.make_ai_move)
        elif self.player_mode == "AI vs AI":
            self.root.after(500, self.make_ai_move)
    
    def update_board_highlighting(self):
        # Reset all small board highlights
        for i in range(3):
            for j in range(3):
                board_frame = self.buttons[i][j][0][0].master
                
                if self.small_board_status[i][j] != ' ':
                    # Won board
                    board_frame.config(bg=self.won_board_colors[self.small_board_status[i][j]])
                elif self.next_board is None or (self.next_board[0] == i and self.next_board[1] == j):
                    # Active board
                    board_frame.config(bg=self.highlight_color)
                else:
                    # Inactive board
                    board_frame.config(bg=self.board_color)
    
    def check_small_board_win(self, i, j):
        board = self.board[i][j]
        
        # Check rows
        for row in range(3):
            if board[row][0] != ' ' and board[row][0] == board[row][1] == board[row][2]:
                return board[row][0]
        
        # Check columns
        for col in range(3):
            if board[0][col] != ' ' and board[0][col] == board[1][col] == board[2][col]:
                return board[0][col]
        
        # Check diagonals
        if board[0][0] != ' ' and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        if board[0][2] != ' ' and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]
        
        # Check if board is full (draw)
        is_full = True
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    is_full = False
                    break
            if not is_full:
                break
        
        if is_full:
            return 'D'  # Draw
        
        return ' '  # Game continues
    
    def check_big_board_win(self):
        # Check rows
        for row in range(3):
            if self.small_board_status[row][0] != ' ' and self.small_board_status[row][0] != 'D' and \
               self.small_board_status[row][0] == self.small_board_status[row][1] == self.small_board_status[row][2]:
                return self.small_board_status[row][0]
        
        # Check columns
        for col in range(3):
            if self.small_board_status[0][col] != ' ' and self.small_board_status[0][col] != 'D' and \
               self.small_board_status[0][col] == self.small_board_status[1][col] == self.small_board_status[2][col]:
                return self.small_board_status[0][col]
        
        # Check diagonals
        if self.small_board_status[0][0] != ' ' and self.small_board_status[0][0] != 'D' and \
           self.small_board_status[0][0] == self.small_board_status[1][1] == self.small_board_status[2][2]:
            return self.small_board_status[0][0]
        if self.small_board_status[0][2] != ' ' and self.small_board_status[0][2] != 'D' and \
           self.small_board_status[0][2] == self.small_board_status[1][1] == self.small_board_status[2][0]:
            return self.small_board_status[0][2]
        
        # Check if big board is full (draw)
        is_full = True
        for row in range(3):
            for col in range(3):
                if self.small_board_status[row][col] == ' ':
                    is_full = False
                    break
            if not is_full:
                break
        
        if is_full:
            return 'D'  # Draw
        
        return None  # Game continues
    
    def is_valid_move(self, i, j, m, n):
        # Check if the game is over
        if self.game_over:
            return False
        
        # Check if the cell is empty
        if self.board[i][j][m][n] != ' ':
            return False
        
        # Check if we're in the correct small board
        if self.next_board is not None and (i, j) != self.next_board:
            return False
        
        # Check if the small board is already won
        if self.small_board_status[i][j] != ' ':
            return False
        
        return True
    
    def make_move(self, i, j, m, n):
        if not self.is_valid_move(i, j, m, n):
            return False
        
        # Human player's turn check
        if ((self.current_player == 'X' and self.player_mode in ["Human vs Human", "Human vs AI"]) or
            (self.current_player == 'O' and self.player_mode == "Human vs Human")):
            pass  # Allow human move
        else:
            return False  # Not human's turn
        
        # Make the move
        self.execute_move(i, j, m, n)
        
        # AI's turn
        if not self.game_over and ((self.current_player == 'O' and self.player_mode == "Human vs AI") or 
                                  self.player_mode == "AI vs AI"):
            self.root.after(500, self.make_ai_move)
        
        return True
    
    def execute_move(self, i, j, m, n):
        # Update the board state
        self.board[i][j][m][n] = self.current_player
        
        # Update the button
        button = self.buttons[i][j][m][n]
        button.config(text=self.current_player, 
                     bg=self.x_color if self.current_player == 'X' else self.o_color,
                     state=tk.DISABLED)
        
        # Check for small board win
        small_win = self.check_small_board_win(i, j)
        if small_win != ' ':
            self.small_board_status[i][j] = small_win
            
            # Update small board visuals
            if small_win != 'D':
                board_frame = self.buttons[i][j][0][0].master
                board_frame.config(bg=self.won_board_colors[small_win])
        
        # Determine next board
        if self.small_board_status[m][n] == ' ':
            self.next_board = (m, n)
        else:
            self.next_board = None  # Can play anywhere
        
        # Check for big board win
        big_win = self.check_big_board_win()
        if big_win:
            self.game_over = True
            self.winner = big_win
            if big_win == 'D':
                self.status_var.set("Game Over: It's a Draw!")
            else:
                self.status_var.set(f"Game Over: Player {big_win} Wins!")
            return
        
        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        # Update status message
        if self.next_board:
            self.status_var.set(f"Player {self.current_player}'s turn in board ({self.next_board[0]}, {self.next_board[1]})")
        else:
            self.status_var.set(f"Player {self.current_player}'s turn (any board)")
        
        # Update highlighting
        self.update_board_highlighting()
    
    def get_legal_moves(self):
        legal_moves = []
        
        if self.next_board:
            i, j = self.next_board
            for m in range(3):
                for n in range(3):
                    if self.board[i][j][m][n] == ' ':
                        legal_moves.append((i, j, m, n))
        else:
            for i in range(3):
                for j in range(3):
                    if self.small_board_status[i][j] == ' ':
                        for m in range(3):
                            for n in range(3):
                                if self.board[i][j][m][n] == ' ':
                                    legal_moves.append((i, j, m, n))
        
        return legal_moves
    
    def make_ai_move(self):
        if self.game_over:
            return
        
        # Use appropriate AI algorithm based on difficulty
        if self.ai_difficulty == "Easy":
            move = self.ai_easy_move()
        elif self.ai_difficulty == "Medium":
            move = self.ai_medium_move()
        else:  # Hard
            move = self.ai_csp_move()
        
        if move:
            i, j, m, n = move
            self.execute_move(i, j, m, n)
            
            # If AI vs AI, schedule next move
            if self.player_mode == "AI vs AI" and not self.game_over:
                self.root.after(500, self.make_ai_move)
    
    def ai_easy_move(self):
        # Easy AI: Random legal move
        legal_moves = self.get_legal_moves()
        if legal_moves:
            return random.choice(legal_moves)
        return None
    
    def ai_medium_move(self):
        # Medium AI: Try to win small boards or block opponent from winning
        legal_moves = self.get_legal_moves()
        if not legal_moves:
            return None
        
        # Check if AI can win in any small board
        for move in legal_moves:
            i, j, m, n = move
            # Make temporary move
            self.board[i][j][m][n] = self.current_player
            win = self.check_small_board_win(i, j)
            # Undo move
            self.board[i][j][m][n] = ' '
            
            if win == self.current_player:
                return move
        
        # Check if AI needs to block opponent
        opponent = 'X' if self.current_player == 'O' else 'O'
        for move in legal_moves:
            i, j, m, n = move
            # Make temporary move for opponent
            self.board[i][j][m][n] = opponent
            win = self.check_small_board_win(i, j)
            # Undo move
            self.board[i][j][m][n] = ' '
            
            if win == opponent:
                return move
        
        # Strategic preference: center of boards
        center_moves = [move for move in legal_moves if move[2] == 1 and move[3] == 1]
        if center_moves:
            return random.choice(center_moves)
        
        # Corners are good too
        corner_moves = [move for move in legal_moves if 
                       (move[2] == 0 and move[3] == 0) or 
                       (move[2] == 0 and move[3] == 2) or 
                       (move[2] == 2 and move[3] == 0) or 
                       (move[2] == 2 and move[3] == 2)]
        if corner_moves:
            return random.choice(corner_moves)
        
        # Otherwise, random move
        return random.choice(legal_moves)
    
    def ai_csp_move(self):
        """Advanced AI using CSP (Constraint Satisfaction Problem) approach"""
        # Start with a light minimax with CSP constraints
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        depth = 3  # Deeper for harder AI
        
        legal_moves = self.get_legal_moves()
        # Forward checking - prioritize moves that don't send to a won board
        # Sort moves to try promising ones first (center, corners)
        legal_moves = self.order_moves(legal_moves)
        
        for move in legal_moves:
            i, j, m, n = move
            # Apply constraint: simulate move
            board_copy = copy.deepcopy(self.board)
            status_copy = copy.deepcopy(self.small_board_status)
            next_board_copy = self.next_board
            player_copy = self.current_player
            
            # Make move
            self.board[i][j][m][n] = self.current_player
            
            # Check for small board win
            small_win = self.check_small_board_win(i, j)
            if small_win != ' ':
                self.small_board_status[i][j] = small_win
            
            # Determine next board
            if self.small_board_status[m][n] == ' ':
                self.next_board = (m, n)
            else:
                self.next_board = None
            
            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
            # Minimax with alpha-beta pruning
            score = self.minimax(depth - 1, alpha, beta, False)
            
            # Restore state
            self.board = board_copy
            self.small_board_status = status_copy
            self.next_board = next_board_copy
            self.current_player = player_copy
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        
        return best_move
    
    def order_moves(self, moves):
        """Order moves for alpha-beta efficiency (MRV heuristic)"""
        # Prioritize center positions
        center_moves = []
        corner_moves = []
        edge_moves = []
        
        for move in moves:
            i, j, m, n = move
            # Center of a small board
            if m == 1 and n == 1:
                center_moves.append(move)
            # Corners of a small board
            elif (m == 0 and n == 0) or (m == 0 and n == 2) or (m == 2 and n == 0) or (m == 2 and n == 2):
                corner_moves.append(move)
            # Edges
            else:
                edge_moves.append(move)
        
        # Apply MRV (Minimum Remaining Values) - sort by how constrained next boards are
        def sort_key(move):
            _, _, m, n = move
            # If sending to a board that's almost full, it's a good move (constrains opponent)
            filled_cells = 0
            if self.small_board_status[m][n] == ' ':  # Only if board is not won
                for r in range(3):
                    for c in range(3):
                        if self.board[m][n][r][c] != ' ':
                            filled_cells += 1
                return -filled_cells  # Negative so more filled = higher priority
            return 0  # Already won board
            
        center_moves.sort(key=sort_key)
        corner_moves.sort(key=sort_key)
        edge_moves.sort(key=sort_key)
        
        # Return ordered list
        return center_moves + corner_moves + edge_moves
    
    def minimax(self, depth, alpha, beta, is_maximizing):
        """Minimax algorithm with alpha-beta pruning and CSP integration"""
        # CSP constraint: check game end
        big_win = self.check_big_board_win()
        if big_win:
            if big_win == 'X':
                return 100 + depth  # Maximizing player wins (more depth = quicker win)
            elif big_win == 'O':
                return -100 - depth  # Minimizing player wins (more depth = quicker loss)
            else:
                return 0  # Draw
        
        if depth == 0:
            return self.evaluate_board()
        
        legal_moves = self.get_legal_moves()
        
        # Arc consistency (AC-3): Filter out moves that lead to immediate loss
        if len(legal_moves) > 5:  # Only apply for efficiency when moves > 5
            legal_moves = self.filter_moves_with_arc_consistency(legal_moves)
        
        # Forward checking: prioritize moves
        legal_moves = self.order_moves(legal_moves)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                i, j, m, n = move
                # Apply constraints
                board_copy = copy.deepcopy(self.board)
                status_copy = copy.deepcopy(self.small_board_status)
                next_board_copy = self.next_board
                player_copy = self.current_player
                
                # Make move
                self.board[i][j][m][n] = self.current_player
                
                # CSP constraint: check for small board win
                small_win = self.check_small_board_win(i, j)
                if small_win != ' ':
                    self.small_board_status[i][j] = small_win
                
                # CSP constraint: determine next board
                if self.small_board_status[m][n] == ' ':
                    self.next_board = (m, n)
                else:
                    self.next_board = None
                
                # Switch player
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                
                eval_score = self.minimax(depth - 1, alpha, beta, False)
                
                # Restore state
                self.board = board_copy
                self.small_board_status = status_copy
                self.next_board = next_board_copy
                self.current_player = player_copy
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, max_eval)
                if alpha >= beta:
                    break  # Beta cutoff
            
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                i, j, m, n = move
                # Apply constraints
                board_copy = copy.deepcopy(self.board)
                status_copy = copy.deepcopy(self.small_board_status)
                next_board_copy = self.next_board
                player_copy = self.current_player
                
                # Make move
                self.board[i][j][m][n] = self.current_player
                
                # CSP constraint: check for small board win
                small_win = self.check_small_board_win(i, j)
                if small_win != ' ':
                    self.small_board_status[i][j] = small_win
                
                # CSP constraint: determine next board
                if self.small_board_status[m][n] == ' ':
                    self.next_board = (m, n)
                else:
                    self.next_board = None
                
                # Switch player
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                
                eval_score = self.minimax(depth - 1, alpha, beta, True)
                
                # Restore state
                self.board = board_copy
                self.small_board_status = status_copy
                self.next_board = next_board_copy
                self.current_player = player_copy
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval
    
    def filter_moves_with_arc_consistency(self, moves):
        """Implement Arc Consistency (AC-3) to filter out inconsistent moves"""
        consistent_moves = []
        for move in moves:
            i, j, m, n = move
            # If this move would send opponent to a full/won board -> consistent
            if self.small_board_status[m][n] != ' ':
                consistent_moves.append(move)
                continue
            
            # Count opponent's options in the next board
            options = 0
            for r in range(3):
                for c in range(3):
                    if self.board[m][n][r][c] == ' ':
                        options += 1
            
            # If sending to a board with limited options -> consistent
            if options <= 3:  # Limited options is good for constraint
                consistent_moves.append(move)
            
            # If move creates a two-in-a-row for us -> consistent
            self.board[i][j][m][n] = self.current_player
            if self.check_almost_win(i, j, self.current_player):
                consistent_moves.append(move)
            self.board[i][j][m][n] = ' '
        
        # If filtering removes all moves, return original list
        return consistent_moves if consistent_moves else moves
    
    def check_almost_win(self, i, j, player):
        """Check if there are two in a row with an empty third space"""
        board = self.board[i][j]
        
        # Check rows
        for row in range(3):
            if (board[row].count(player) == 2 and board[row].count(' ') == 1):
                return True
        
        # Check columns
        for col in range(3):
            column = [board[0][col], board[1][col], board[2][col]]
            if column.count(player) == 2 and column.count(' ') == 1:
                return True
        
        # Check diagonals
        diag1 = [board[0][0], board[1][1], board[2][2]]
        diag2 = [board[0][2], board[1][1], board[2][0]]
        
        if diag1.count(player) == 2 and diag1.count(' ') == 1:
            return True
        if diag2.count(player) == 2 and diag2.count(' ') == 1:
            return True
        
        return False
    
        def evaluate_board(self):
       
        # Check if game is won
            big_win = self.check_big_board_win()
            if big_win == 'X':
              return 100
            elif big_win == 'O':
              return -100
            elif big_win == 'D':
              return 0
            
            score = 0
            
            # Evaluate small boards
            for i in range(3):
              for j in range(3):
                if self.small_board_status[i][j] == 'X':
                  score += 10
                elif self.small_board_status[i][j] == 'O':
                  score -= 10
            else:
            # Evaluate potential small board wins
             small_score = self.evaluate_small_board(i, j)
             score += small_score
            
            # Strategic positions on the big board
            # Center board is valuable
            if self.small_board_status[1][1] == 'X':
             score += 3
            elif self.small_board_status[1][1] == 'O':
             score -= 3
            
            # Corner boards are valuable
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            for i, j in corners:
             if self.small_board_status[i][j] == 'X':
               score += 2
             elif self.small_board_status[i][j] == 'O':
               score -= 2
            
            # Check for potential two-in-a-row on big board
            # Rows
            for i in range(3):
                row = [self.small_board_status[i][0], self.small_board_status[i][1], self.small_board_status[i][2]]
            if row.count('X') == 2 and row.count(' ') == 1:
               score += 5
            if row.count('O') == 2 and row.count(' ') == 1:
               score -= 5
            
            # Columns
            for j in range(3):
                col = [self.small_board_status[0][j], self.small_board_status[1][j], self.small_board_status[2][j]]
            if col.count('X') == 2 and col.count(' ') == 1:
             score += 5
            if col.count('O') == 2 and col.count(' ') == 1:
             score -= 5
            
            # Diagonals
            diag1 = [self.small_board_status[0][0], self.small_board_status[1][1], self.small_board_status[2][2]]
            if diag1.count('X') == 2 and diag1.count(' ') == 1:
             score += 5
            if diag1.count('O') == 2 and diag1.count(' ') == 1:
             score -= 5
            
            diag2 = [self.small_board_status[0][2], self.small_board_status[1][1], self.small_board_status[2][0]]
            if diag2.count('X') == 2 and diag2.count(' ') == 1:
             score += 5
            if diag2.count('O') == 2 and diag2.count(' ') == 1:
             score -= 5
            
            # Consider the number of legal moves available (mobility)
            if self.current_player == 'X':
              score += len(self.get_legal_moves()) * 0.1
            else:
              score -= len(self.get_legal_moves()) * 0.1
            
            return score
    
    def evaluate_small_board(self, i, j):
        """Evaluate a single small board"""
        board = self.board[i][j]
        score = 0
        
        # Check for potential wins in rows
        for row in range(3):
            if board[row].count('X') == 2 and board[row].count(' ') == 1:
                score += 1
            if board[row].count('O') == 2 and board[row].count(' ') == 1:
                score -= 1
        
        # Check for potential wins in columns
        for col in range(3):
            column = [board[0][col], board[1][col], board[2][col]]
            if column.count('X') == 2 and column.count(' ') == 1:
                score += 1
            if column.count('O') == 2 and column.count(' ') == 1:
                score -= 1
        
        # Check for potential wins in diagonals
        diag1 = [board[0][0], board[1][1], board[2][2]]
        if diag1.count('X') == 2 and diag1.count(' ') == 1:
            score += 1
        if diag1.count('O') == 2 and diag1.count(' ') == 1:
            score -= 1
        
        diag2 = [board[0][2], board[1][1], board[2][0]]
        if diag2.count('X') == 2 and diag2.count(' ') == 1:
            score += 1
        if diag2.count('O') == 2 and diag2.count(' ') == 1:
            score -= 1
        
        # Center position is valuable in small boards too
        if board[1][1] == 'X':
            score += 0.5
        elif board[1][1] == 'O':
            score -= 0.5
        
        return score
    
    def run(self):
        self.root.mainloop()


class UltimateTicTacToeCSP:
    """Class implementing the Constraint Satisfaction Problem formulation"""
    
    def __init__(self, game):
        self.game = game
    
    def get_variables(self):
        """
        Variables: Each cell in each small board is a variable
        Returns all variables that are not yet assigned (empty spaces)
        """
        variables = []
        for i in range(3):
            for j in range(3):
                if self.game.small_board_status[i][j] == ' ':  # Only in active boards
                    for m in range(3):
                        for n in range(3):
                            if self.game.board[i][j][m][n] == ' ':
                                variables.append((i, j, m, n))
        return variables
    
    def get_domain(self, variable):
        """
        Domain: Each variable can be 'X', 'O', or empty ' '
        For CSP, we only consider the current player's symbol as the domain
        """
        i, j, m, n = variable
        
        # If this is not a valid move, return empty domain
        if not self.check_constraints(variable, self.game.current_player):
            return []
        
        return [self.game.current_player]
    
    def check_constraints(self, variable, value):
        """Check if assigning value to variable satisfies all constraints"""
        i, j, m, n = variable
        
        # Constraint 1: Cell must be empty
        if self.game.board[i][j][m][n] != ' ':
            return False
        
        # Constraint 2: Small board must be active and not already won
        if self.game.small_board_status[i][j] != ' ':
            return False
        
        # Constraint 3: If next_board is specified, must play in that board
        if self.game.next_board is not None and (i, j) != self.game.next_board:
            return False
        
        return True
    
    def forward_check(self, variable, value):
        """Forward checking to prune inconsistent values"""
        i, j, m, n = variable
        
        # Temporarily assign the value
        self.game.board[i][j][m][n] = value
        
        # Check if this assignment creates a win in the small board
        small_win = self.game.check_small_board_win(i, j)
        next_player = 'O' if value == 'X' else 'X'
        
        # Check if the next player has any valid moves
        next_board = (m, n) if self.game.small_board_status[m][n] == ' ' else None
        has_valid_moves = False
        
        if next_board:
            # Check if there are valid moves in the next board
            for r in range(3):
                for c in range(3):
                    if self.game.board[m][n][r][c] == ' ':
                        has_valid_moves = True
                        break
                if has_valid_moves:
                    break
        else:
            # Check if there are valid moves in any board
            for r in range(3):
                for c in range(3):
                    if self.game.small_board_status[r][c] == ' ':
                        has_valid_moves = True
                        break
                if has_valid_moves:
                    break
        
        # Undo the assignment
        self.game.board[i][j][m][n] = ' '
        
        # Return result of forward checking
        return has_valid_moves
    
    def ac3(self):
        """Arc Consistency algorithm (AC-3)"""
        # For Ultimate TTT, we implement a simplified AC-3
        # We check if any move would lead to immediate small board win
        arcs = []
        
        # Get all potential arcs (variable pairs with constraints between them)
        variables = self.get_variables()
        for var1 in variables:
            for var2 in variables:
                if var1 != var2:
                    # Variables in same small board have arc constraints
                    if var1[0] == var2[0] and var1[1] == var2[1]:
                        arcs.append((var1, var2))
        
        # Process arcs until queue is empty
        while arcs:
            var1, var2 = arcs.pop(0)
            
            if self.revise(var1, var2):
                # If domain of var1 becomes empty, no solution
                if not self.get_domain(var1):
                    return False
                
                # Add neighbors of var1 back to queue
                for var3 in variables:
                    if var3 != var1 and var3 != var2:
                        if var3[0] == var1[0] and var3[1] == var1[1]:
                            arcs.append((var3, var1))
        
        return True
    
    def revise(self, var1, var2):
        """Check if var1's domain needs revision based on var2"""
        revised = False
        
        # For Ultimate TTT, we check if assigning values to var1 and var2
        # would lead to constraint violations
        for value1 in self.get_domain(var1):
            # Check if there's a valid value for var2 compatible with value1
            compatible = False
            for value2 in self.get_domain(var2):
                # Temporarily assign both values
                i1, j1, m1, n1 = var1
                i2, j2, m2, n2 = var2
                
                self.game.board[i1][j1][m1][n1] = value1
                self.game.board[i2][j2][m2][n2] = value2
                
                # Check if assignment violates any constraint
                valid = self.check_board_consistency()
                
                # Restore board
                self.game.board[i1][j1][m1][n1] = ' '
                self.game.board[i2][j2][m2][n2] = ' '
                
                if valid:
                    compatible = True
                    break
            
            if not compatible:
                # No compatible value found, remove value1 from domain
                revised = True
                break
        
        return revised
    
    def check_board_consistency(self):
        """Check if current board state is consistent with game rules"""
        # This is a simplified check for consistency
        # In a real implementation, we would check all game constraints
        
        # Check if any small board has multiple winners
        for i in range(3):
            for j in range(3):
                wins_x = self.check_win_for_player(i, j, 'X')
                wins_o = self.check_win_for_player(i, j, 'O')
                if wins_x and wins_o:
                    return False  # Cannot have both players winning same board
        
        return True
    
    def check_win_for_player(self, i, j, player):
        """Check if player has won the small board at position (i,j)"""
        board = self.game.board[i][j]
        
        # Check rows
        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] == player:
                return True
        
        # Check columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] == player:
                return True
        
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] == player:
            return True
        if board[0][2] == board[1][1] == board[2][0] == player:
            return True
        
        return False
    
    def backtracking_search(self):
        """CSP Backtracking search with forward checking and MRV"""
        return self.backtrack({})
    
    def backtrack(self, assignment):
        """Backtracking search algorithm"""
        if len(assignment) == len(self.get_variables()):
            return assignment  # All variables assigned
        
        # Select unassigned variable using MRV (Minimum Remaining Values)
        var = self.select_unassigned_variable(assignment)
        if not var:
            return None
        
        # Try each value in the domain
        for value in self.get_domain(var):
            # Check if value is consistent with assignment
            if self.consistent(var, value, assignment):
                # Add {var = value} to assignment
                assignment[var] = value
                i, j, m, n = var
                self.game.board[i][j][m][n] = value
                
                # Forward checking
                if self.forward_check(var, value):
                    # Recursive call
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
                
                # If we get here, need to backtrack
                del assignment[var]
                self.game.board[i][j][m][n] = ' '
        
        return None
    
    def select_unassigned_variable(self, assignment):
        """
        Select unassigned variable using MRV (Minimum Remaining Values)
        """
        unassigned = [var for var in self.get_variables() if var not in assignment]
        if not unassigned:
            return None
        
        # Use MRV to select variable with fewest legal values
        return min(unassigned, key=lambda var: len(self.get_domain(var)) if len(self.get_domain(var)) > 0 else float('inf'))
    
    def consistent(self, var, value, assignment):
        """Check if assignment is consistent with constraints"""
        # Check if value conflicts with any assignment
        for assigned_var, assigned_val in assignment.items():
            if var == assigned_var:
                continue
            
            # Check basic constraint: same cell can't have two values
            if var == assigned_var and value != assigned_val:
                return False
            
            # Check if this assignment would create inconsistent board state
            i, j, m, n = var
            self.game.board[i][j][m][n] = value
            consistent = self.check_board_consistency()
            self.game.board[i][j][m][n] = ' '
            
            if not consistent:
                return False
        
        return True


def main():
    """Main function to run the game"""
    game = UltimateTicTacToe()
    game.run()


if __name__ == "__main__":
    main()
