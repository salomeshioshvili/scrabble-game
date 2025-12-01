import tkinter as tk
from tkinter import messagebox, font
from typing import Dict, Tuple, Optional
from ..game import Game
from ..tile import Tile


class ScrabbleUI:
    PREMIUM_COLORS = {
        "★": "#FFB6C1",
        "TW": "#E63946",
        "DW": "#FFB6C1",
        "TL": "#4EA8DE",
        "DL": "#90E0EF",
    }

    PREMIUM_TEXT = {
        "★": "★",
        "TW": "TRIPLE\nWORD\nSCORE",
        "DW": "DOUBLE\nWORD\nSCORE",
        "TL": "TRIPLE\nLETTER\nSCORE",
        "DL": "DOUBLE\nLETTER\nSCORE",
    }

    BOARD_BG = "#0A5F38"
    TILE_COLOR = "#F4E4C1"
    TILE_BORDER = "#8B7355"


    CELL_SIZE = 46
    RACK_TILE_SIZE = 56

    def __init__(self, game: Game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Scrabble")
        self.root.configure(bg="#1a1a1a")

        # Determine a human player to display
        human = None
        if hasattr(self.game, "bot_players"):
            bots = getattr(self.game, "bot_players", []) or []
            for p in self.game.players:
                if p not in bots:
                    human = p
                    break
        if human is None:
            human = self.game.players[0] if self.game.players else None
        self.human_player = human

        # State
        self.board_buttons = []
        self.rack_buttons = []
        self.selected_rack_tile: Optional[Tuple[int, Tile]] = None
        self.placements: Dict[Tuple[int, int], Tile] = {}

        # Fonts
        self.tile_letter_font = font.Font(family="Arial", size=20, weight="bold")
        self.tile_value_font = font.Font(family="Arial", size=8)
        self.premium_font = font.Font(family="Arial", size=6, weight="bold")
        self.button_font = font.Font(family="Arial", size=10, weight="bold")
        self.score_font = font.Font(family="Arial", size=12)

        self.create_ui()
        self.update_display()

        # Auto-play bot if it's their turn
        self.root.after(1000, self.check_bot_turn)

    def create_ui(self):
        """Create the main UI layout."""
        # Main container
        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(padx=20, pady=20)

        # Title
        title = tk.Label(main_frame, text="S C R A B B L E",
                        font=("Arial", 24, "bold"),
                        bg="#1a1a1a", fg="#FFD700")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Left: Board
        board_outer = tk.Frame(main_frame, bg=self.BOARD_BG, padx=10, pady=10)
        board_outer.grid(row=1, column=0, padx=(0, 20), sticky="n")

        self.create_board(board_outer)

        # Right: Controls
        control_frame = tk.Frame(main_frame, bg="#1a1a1a")
        control_frame.grid(row=1, column=1, sticky="n")

        self.create_scoreboard(control_frame)
        self.create_rack(control_frame)
        self.create_buttons(control_frame)
        self.create_status(control_frame)

    def create_board(self, parent):
        """Create 15x15 board with authentic Scrabble styling using Canvas cells (fixed size)."""
        board_frame = tk.Frame(parent, bg=self.BOARD_BG)
        board_frame.pack()

        for row in range(15):
            button_row = []
            for col in range(15):
                bonus = self.game.board.get_bonus(row, col)
                bg_color = self.PREMIUM_COLORS.get(bonus, self.BOARD_BG)

                # Create fixed-size canvas cell with thin outer border frame
                cell_frame = tk.Frame(board_frame, bg="#000000", padx=1, pady=1)
                cell_frame.grid(row=row, column=col, padx=1, pady=1)

                canvas = tk.Canvas(
                    cell_frame,
                    width=self.CELL_SIZE,
                    height=self.CELL_SIZE,
                    highlightthickness=0
                )
                canvas.pack()
                # Store bonus on canvas for quick access (optional)
                canvas._bonus = bonus
                canvas.bind("<Button-1>", lambda e, r=row, c=col: self.cell_clicked(r, c))

                button_row.append(canvas)
            self.board_buttons.append(button_row)

    def create_scoreboard(self, parent):
        """Create score display."""
        score_frame = tk.Frame(parent, bg="#2d2d2d", relief=tk.RAISED, borderwidth=2)
        score_frame.pack(fill=tk.X, pady=(0, 15))

        title = tk.Label(score_frame, text="SCORES",
                        font=("Arial", 12, "bold"),
                        bg="#2d2d2d", fg="#FFD700", pady=5)
        title.pack()

        self.score_labels = []
        for player in self.game.players:
            lbl = tk.Label(score_frame, text="", bg="#2d2d2d", fg="white",
                          font=self.score_font, pady=3)
            lbl.pack()
            self.score_labels.append(lbl)

    def create_rack(self, parent):
        """Create tile rack with fixed-size tile Canvas to prevent resizing."""
        rack_frame = tk.Frame(parent, bg="#8B7355", relief=tk.RAISED, borderwidth=3, padx=8, pady=8)
        rack_frame.pack(fill=tk.X, pady=(0, 15))

        title = tk.Label(rack_frame, text="YOUR TILES",
                        font=("Arial", 10, "bold"),
                        bg="#8B7355", fg="white")
        title.pack(pady=(0, 5))

        tiles_frame = tk.Frame(rack_frame, bg="#8B7355")
        tiles_frame.pack()

        for i in range(7):
            # Tile container with border
            tile_container = tk.Frame(tiles_frame, bg="#000000", padx=2, pady=2)
            tile_container.grid(row=0, column=i, padx=3)

            canvas = tk.Canvas(
                tile_container,
                width=self.RACK_TILE_SIZE,
                height=self.RACK_TILE_SIZE,
                highlightthickness=0
            )
            canvas.pack()
            canvas.bind("<Button-1>", lambda e, idx=i: self.rack_clicked(idx))

            self.rack_buttons.append(canvas)

    def create_buttons(self, parent):
        """Create action buttons."""
        btn_frame = tk.Frame(parent, bg="#1a1a1a")
        btn_frame.pack(pady=(0, 15))

        buttons = [
            ("PLAY WORD", self.submit_move, "#4CAF50"),
            ("CLEAR", self.clear_placements, "#FFC107"),
            ("PASS", self.pass_turn, "#FF9800"),
            ("SHUFFLE", self.shuffle_rack, "#2196F3"),
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                command=command,
                font=self.button_font,
                bg=color,
                fg="#4CAF50",
                width=18,
                height=1,
                relief=tk.RAISED,
                borderwidth=2,
                cursor="hand2"
            )
            btn.pack(pady=3)

    def create_status(self, parent):
        """Create status display."""
        status_frame = tk.Frame(parent, bg="#2d2d2d", relief=tk.SUNKEN, borderwidth=2, padx=10, pady=10)
        status_frame.pack(fill=tk.BOTH, expand=True)

        self.status_label = tk.Label(
            status_frame,
            text="",
            bg="#2d2d2d",
            fg="#90EE90",
            font=("Arial", 10),
            wraplength=220,
            justify=tk.LEFT
        )
        self.status_label.pack()

    def cell_clicked(self, row: int, col: int):
        """Handle board cell click."""
        if self.game.board.get_tile(row, col) is not None:
            return

        if self.selected_rack_tile is not None:
            rack_idx, tile = self.selected_rack_tile

            # Remove from previous placement
            old_pos = None
            for pos, t in list(self.placements.items()):
                if t == tile:
                    old_pos = pos
                    break

            if old_pos:
                del self.placements[old_pos]

            self.placements[(row, col)] = tile
            self.selected_rack_tile = None
            self.update_display()

    def rack_clicked(self, idx: int):
        """Handle rack tile click."""
        if self.human_player is None:
            return

        rack = self.human_player.rack
        if idx >= len(rack):
            return

        # Prevent interaction when it's not the human player's turn
        if self.game.current_player is not self.human_player:
            messagebox.showinfo("Not your turn", "You can view your tiles now. Play when it's your turn.")
            return

        tile = rack[idx]

        if self.selected_rack_tile and self.selected_rack_tile[0] == idx:
            self.selected_rack_tile = None
        else:
            self.selected_rack_tile = (idx, tile)

        self.update_display()

    def submit_move(self):
        """Submit current placements to game."""
        if not self.placements:
            messagebox.showwarning("No Move", "Place tiles on the board first!")
            return

        # Ensure it's the human player's turn before attempting to submit
        if self.human_player is not None and self.game.current_player is not self.human_player:
            messagebox.showwarning("Not your turn", "Wait until it's your turn to submit a move.")
            return

        success = self.game.play_move(self.placements)

        if success:
            self.placements.clear()
            self.selected_rack_tile = None
            self.update_display()

            # Show score gained
            messagebox.showinfo("Success!", "Word accepted!")
            self.root.after(500, self.check_bot_turn)
        else:
            messagebox.showerror("Invalid Move", "Invalid word or placement!")

    def clear_placements(self):
        """Clear all temporary placements."""
        self.placements.clear()
        self.selected_rack_tile = None
        self.update_display()

    def pass_turn(self):
        """Pass the current turn."""
        confirm = messagebox.askyesno("Pass Turn", "Are you sure you want to pass?")
        if confirm:
            self.game.pass_turn()
            self.placements.clear()
            self.selected_rack_tile = None
            self.update_display()
            self.root.after(500, self.check_bot_turn)

    def shuffle_rack(self):
        """Shuffle the current player's rack."""
        self.game.shuffle_rack()
        self.selected_rack_tile = None
        self.update_display()

    def check_bot_turn(self):
        """Check if it's a bot's turn and auto-play."""
        if self.game.is_game_over():
            self.show_game_over()
            return

        if self.game.is_bot_turn():
            self.root.after(1500, self.execute_bot_turn)

    def execute_bot_turn(self):
        """Execute bot's move."""
        bot_name = self.game.current_player.name
        success = self.game.play_bot_move()
        self.update_display()

        if success:
            messagebox.showinfo("Bot Move", f"{bot_name} played a word!")

        self.root.after(500, self.check_bot_turn)

    def show_game_over(self):
        """Display game over message."""
        winner = max(self.game.players, key=lambda p: p.score)
        scores = "\n".join([f"{p.name}: {p.score}" for p in self.game.players])
        msg = f"GAME OVER\n\nWinner: {winner.name}\n\n{scores}"
        messagebox.showinfo("Game Over", msg)

    def update_display(self):
        """Refresh all UI elements."""
        self.update_board()
        self.update_rack()
        self.update_scores()
        self.update_status()

    def update_board(self):
        """Update board display with authentic tile styling using Canvas drawing."""
        for row in range(15):
            for col in range(15):
                canvas = self.board_buttons[row][col]
                canvas.delete("all")

                permanent_tile = self.game.board.get_tile(row, col)
                if permanent_tile:
                    # Draw tile rectangle and letter + value
                    canvas.create_rectangle(2, 2, self.CELL_SIZE-2, self.CELL_SIZE-2, fill=self.TILE_COLOR, outline=self.TILE_BORDER)
                    # Letter centered
                    canvas.create_text(self.CELL_SIZE//2, self.CELL_SIZE//2 - 6, text=permanent_tile.letter, font=self.tile_letter_font, fill="#000000")
                    # Small value bottom-right
                    canvas.create_text(self.CELL_SIZE - 8, self.CELL_SIZE - 8, text=str(permanent_tile.value), font=self.tile_value_font, fill="#000000", anchor="se")
                elif (row, col) in self.placements:
                    temp_tile = self.placements[(row, col)]
                    # Draw temporary tile with slightly different background
                    canvas.create_rectangle(2, 2, self.CELL_SIZE-2, self.CELL_SIZE-2, fill="#FFFACD", outline=self.TILE_BORDER)
                    canvas.create_text(self.CELL_SIZE//2, self.CELL_SIZE//2 - 6, text=temp_tile.letter, font=self.tile_letter_font, fill="#000000")
                    canvas.create_text(self.CELL_SIZE - 8, self.CELL_SIZE - 8, text=str(temp_tile.value), font=self.tile_value_font, fill="#000000", anchor="se")
                else:
                    # Empty square - draw premium background and small label
                    bonus = self.game.board.get_bonus(row, col)
                    bg_color = self.PREMIUM_COLORS.get(bonus, self.BOARD_BG)
                    canvas.create_rectangle(2, 2, self.CELL_SIZE-2, self.CELL_SIZE-2, fill=bg_color, outline="#000000")
                    text = self.PREMIUM_TEXT.get(bonus, "")
                    if text:
                        # multiline premium text centered
                        canvas.create_text(self.CELL_SIZE//2, self.CELL_SIZE//2, text=text, font=self.premium_font, fill="white", justify="center")

    def update_rack(self):
        """Update rack display using fixed-size Canvas tiles and show tile value clearly."""
        # Always show the human player's rack (do not reveal bot racks)
        rack = self.human_player.rack if self.human_player is not None else []
        placed_tiles = set(self.placements.values())

        for i, canvas in enumerate(self.rack_buttons):
            canvas.delete("all")
            if i < len(rack):
                tile = rack[i]

                if tile in placed_tiles:
                    # Grayed out placeholder
                    canvas.create_rectangle(2, 2, self.RACK_TILE_SIZE-2, self.RACK_TILE_SIZE-2, fill="#C0C0C0", outline=self.TILE_BORDER)
                else:
                    is_selected = self.selected_rack_tile and self.selected_rack_tile[0] == i
                    # If it's not the human's turn, show tiles subdued to indicate read-only
                    if self.game.current_player is not self.human_player:
                        bg = "#D3D3D3"  # subdued background
                        fg_color = "#666666"
                    else:
                        bg = "#FFD700" if is_selected else self.TILE_COLOR
                        fg_color = "#000000"
                    canvas.create_rectangle(2, 2, self.RACK_TILE_SIZE-2, self.RACK_TILE_SIZE-2, fill=bg, outline=self.TILE_BORDER)
                    # Large letter
                    canvas.create_text(self.RACK_TILE_SIZE//2, self.RACK_TILE_SIZE//2 - 6, text=tile.letter, font=self.tile_letter_font, fill=fg_color)
                    # Small value in corner
                    canvas.create_text(self.RACK_TILE_SIZE - 10, self.RACK_TILE_SIZE - 10, text=str(tile.value), font=self.tile_value_font, fill=fg_color, anchor="se")
            else:
                # Empty rack slot background
                canvas.create_rectangle(2, 2, self.RACK_TILE_SIZE-2, self.RACK_TILE_SIZE-2, fill="#8B7355", outline=self.TILE_BORDER)

    def update_scores(self):
        """Update score display."""
        for i, player in enumerate(self.game.players):
            is_current = player == self.game.current_player
            prefix = "▶ " if is_current else "   "
            text = f"{prefix}{player.name}: {player.score} pts"
            fg = "#FFD700" if is_current else "white"
            self.score_labels[i].config(text=text, fg=fg, font=("Arial", 12, "bold" if is_current else "normal"))

    def update_status(self):
        """Update status message."""
        player = self.game.current_player
        tiles_left = len(self.game.tile_bag)

        status = f"▶ {player.name}'s Turn\n\n"
        status += f"Tiles Remaining: {tiles_left}\n"
        # Show which player's tiles are being displayed
        if self.human_player:
            status += f"\nViewing tiles: {self.human_player.name}\n"

        if self.placements:
            status += f"\nPlaced: {len(self.placements)} tile(s)"
        else:
            status += f"\nSelect a tile, then click the board"

        self.status_label.config(text=status)

    def show(self):
        """Start the UI main loop."""
        self.root.mainloop()