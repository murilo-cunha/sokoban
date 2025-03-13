"""Main module for the Sokoban game implementation."""

import pyxel


class Sokoban:
    """A Sokoban puzzle game implementation using Pyxel."""

    def __init__(self) -> None:
        """Initialize the Sokoban game with default settings."""
        # Game settings
        self.TITLE = "Sokoban"
        self.WIDTH = 172
        self.HEIGHT = 128
        self.FPS = 30

        # Tile size
        self.TILE_SIZE = 8

        # Colors
        self.COL_BACKGROUND = 0
        self.COL_WALL = 6
        self.COL_PLAYER = 11
        self.COL_BOX = 9
        self.COL_TARGET = 8
        self.COL_BOX_ON_TARGET = 10

        # Game states
        self.PLAYING = 0
        self.COMPLETED = 1

        # Tile types
        self.EMPTY = 0
        self.WALL = 1
        self.PLAYER = 2
        self.BOX = 3
        self.TARGET = 4
        self.BOX_ON_TARGET = 5

        # Player position
        self.player_x = 0
        self.player_y = 0

        # Level data
        self.current_level = 0
        self.game_state = self.PLAYING

        # Game objects
        self.boxes: list[tuple[int, int]] = []
        self.targets: list[tuple[int, int]] = []
        self.grid: list[list[int]] = []

        # Define levels (0=empty, 1=wall, 2=player, 3=box, 4=target, 5=box on target)
        self.levels = [
            # Level 1
            [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 2, 0, 0, 0, 1],
                [1, 0, 3, 3, 4, 0, 1],
                [1, 0, 4, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ],
            # Level 2
            [
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 4, 4, 4, 0, 0, 1],
                [1, 0, 0, 2, 0, 3, 0, 1],
                [1, 0, 3, 0, 3, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
            ],
        ]

        # Initialize game
        self.init_game()

        # Initialize Pyxel
        pyxel.init(self.WIDTH, self.HEIGHT, title=self.TITLE, fps=self.FPS)
        pyxel.run(self.update, self.draw)

    def init_game(self) -> None:
        """Initialize the game state with the current level."""
        self.grid = [row[:] for row in self.levels[self.current_level]]
        self.boxes = []
        self.targets = []

        # Find player, boxes and targets
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == self.PLAYER:
                    self.player_x = x
                    self.player_y = y
                    self.grid[y][x] = self.EMPTY
                elif self.grid[y][x] == self.BOX:
                    self.boxes.append((x, y))
                    self.grid[y][x] = self.EMPTY
                elif self.grid[y][x] == self.TARGET:
                    self.targets.append((x, y))
                    self.grid[y][x] = self.EMPTY
                elif self.grid[y][x] == self.BOX_ON_TARGET:
                    self.boxes.append((x, y))
                    self.targets.append((x, y))
                    self.grid[y][x] = self.EMPTY

    def update(self) -> None:  # noqa: C901, PLR0912
        """Update the game state based on user input and game logic."""
        if self.game_state == self.COMPLETED:
            # R key to restart level
            if pyxel.btnp(pyxel.KEY_R):
                self.init_game()
                self.game_state = self.PLAYING

            # N key to go to next level if available
            if pyxel.btnp(pyxel.KEY_N) and self.current_level < len(self.levels) - 1:
                self.current_level += 1
                self.init_game()
                self.game_state = self.PLAYING

            return

        # Player movement
        new_x, new_y = self.player_x, self.player_y

        if pyxel.btnp(pyxel.KEY_UP):
            new_y -= 1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            new_y += 1
        elif pyxel.btnp(pyxel.KEY_LEFT):
            new_x -= 1
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            new_x += 1

        # If movement occurred
        if new_x != self.player_x or new_y != self.player_y:
            # Check for walls
            if self.grid[new_y][new_x] == self.WALL:
                return

            # Check for boxes
            box_index = -1
            for i, (box_x, box_y) in enumerate(self.boxes):
                if box_x == new_x and box_y == new_y:
                    box_index = i
                    break

            # If there's a box, try to push it
            if box_index != -1:
                box_new_x = new_x + (new_x - self.player_x)
                box_new_y = new_y + (new_y - self.player_y)

                # Check if new box position is valid
                is_wall = self.grid[box_new_y][box_new_x] == self.WALL
                is_box = any(
                    box_x == box_new_x and box_y == box_new_y
                    for box_x, box_y in self.boxes
                )

                if is_wall or is_box:
                    return

                # Move the box
                self.boxes[box_index] = (box_new_x, box_new_y)

                # Check win condition
                if self.check_win():
                    self.game_state = self.COMPLETED

            # Move the player
            self.player_x, self.player_y = new_x, new_y

        # R key to restart level
        if pyxel.btnp(pyxel.KEY_R):
            self.init_game()

    def check_win(self) -> bool:
        """Check if all boxes are on targets."""
        return all(box in self.targets for box in self.boxes)

    def draw(self) -> None:
        """Draw the game state to the screen."""
        pyxel.cls(self.COL_BACKGROUND)

        # Calculate offset to center the level
        level_width = len(self.grid[0]) * self.TILE_SIZE
        level_height = len(self.grid) * self.TILE_SIZE
        offset_x = (self.WIDTH - level_width) // 2
        offset_y = (self.HEIGHT - level_height) // 2

        # Draw walls
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == self.WALL:
                    pyxel.rect(
                        offset_x + x * self.TILE_SIZE,
                        offset_y + y * self.TILE_SIZE,
                        self.TILE_SIZE,
                        self.TILE_SIZE,
                        self.COL_WALL,
                    )

        # Draw targets
        for x, y in self.targets:
            pyxel.rect(
                offset_x + x * self.TILE_SIZE + 2,
                offset_y + y * self.TILE_SIZE + 2,
                self.TILE_SIZE - 4,
                self.TILE_SIZE - 4,
                self.COL_TARGET,
            )

        # Draw boxes
        for x, y in self.boxes:
            color = self.COL_BOX_ON_TARGET if (x, y) in self.targets else self.COL_BOX
            pyxel.rect(
                offset_x + x * self.TILE_SIZE + 1,
                offset_y + y * self.TILE_SIZE + 1,
                self.TILE_SIZE - 2,
                self.TILE_SIZE - 2,
                color,
            )

        # Draw player
        # Calculate center position of the player's tile
        player_center_x = (
            offset_x + self.player_x * self.TILE_SIZE + self.TILE_SIZE // 2
        )
        player_center_y = (
            offset_y + self.player_y * self.TILE_SIZE + self.TILE_SIZE // 2
        )
        # Draw horizontal part of the plus sign
        pyxel.rect(
            player_center_x - (self.TILE_SIZE - 2) // 2,
            player_center_y - 1,
            self.TILE_SIZE - 2,
            2,
            self.COL_PLAYER,
        )
        # Draw vertical part of the plus sign
        pyxel.rect(
            player_center_x - 1,
            player_center_y - (self.TILE_SIZE - 2) // 2,
            2,
            self.TILE_SIZE - 2,
            self.COL_PLAYER,
        )

        # Draw game completed message
        if self.game_state == self.COMPLETED:
            message = "Level Complete!"
            pyxel.text(self.WIDTH // 2 - len(message) * 2, 20, message, 7)

            instructions = "R: Restart"
            pyxel.text(self.WIDTH // 2 - len(instructions) * 2, 30, instructions, 7)

            if self.current_level < len(self.levels) - 1:
                next_level = "N: Next Level"
                pyxel.text(self.WIDTH // 2 - len(next_level) * 2, 40, next_level, 7)
            else:
                congrats = "Congrats! That's all the levels!"
                pyxel.text(self.WIDTH // 2 - len(congrats) * 2, 40, congrats, 7)


if __name__ == "__main__":
    Sokoban()
