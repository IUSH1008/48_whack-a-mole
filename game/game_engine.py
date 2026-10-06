import pygame
import random
from .hole import Hole

# Game Engine

DARK_BROWN = (60, 40, 20)
MOLE_BROWN = (140, 95, 55)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)


class GameEngine:
    def __init__(self, width, height, rows=3, cols=3):
        self.width = width
        self.height = height

        self.holes = []
        spacing_x = width // (cols + 1)
        spacing_y = (height - 80) // (rows + 1)

        for r in range(rows):
            for c in range(cols):
                cx = spacing_x * (c + 1)
                cy = 80 + spacing_y * (r + 1)
                self.holes.append(Hole(cx, cy))

        # Default difficulty
        self.spawn_chance = 0.02
        self.mole_up_frames = 45

        self.round_seconds = 30
        self.time_left_frames = self.round_seconds * 60

        self.score = 0
        self.misses = 0

        self.font = pygame.font.SysFont("Arial", 28)
        self.game_over_font = pygame.font.SysFont("Arial", 48)
        self.menu_font = pygame.font.SysFont("Arial", 32)

        self.game_over = False
        self.replay_menu = False
        self.running = True

    def handle_event(self, event):
    # Game over screen
     if self.game_over and not self.replay_menu:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.replay_menu = True
            elif event.key == pygame.K_q:
                self.running = False
        return

    # Difficulty selection menu
     if self.replay_menu:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                self.start_new_round("Easy")

            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                self.start_new_round("Medium")

            elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                self.start_new_round("Hard")

            elif event.key == pygame.K_q:
                self.running = False
        return

    # Normal gameplay
     if event.type == pygame.MOUSEBUTTONDOWN:
        self._handle_click(event.pos)

    def _handle_click(self, pos):
        hit_something = False

        # Task 1:
        # Only hit active moles and stop after the first successful hit.
        for hole in self.holes:
            if hole.active and hole.rect().collidepoint(pos):
                if hole.whack():
                    self.score += 1
                    hit_something = True
                    break

        if not hit_something:
            self.misses += 1

    def handle_input(self):
        pass

    def update(self):
        if self.game_over or self.replay_menu:
            return

        self.time_left_frames -= 1

        if self.time_left_frames <= 0:
            self.time_left_frames = 0
            self.game_over = True
            return

        for hole in self.holes:
            hole.update()

            if not hole.active and random.random() < self.spawn_chance:
                hole.pop_up(self.mole_up_frames)

    def start_new_round(self, difficulty):
        # Reset all holes
        for hole in self.holes:
            hole.active = False
            hole.timer = 0

        # Set difficulty
        if difficulty == "Easy":
            self.spawn_chance = 0.015
            self.mole_up_frames = 60

        elif difficulty == "Medium":
            self.spawn_chance = 0.025
            self.mole_up_frames = 45

        elif difficulty == "Hard":
            self.spawn_chance = 0.04
            self.mole_up_frames = 30

        # Reset game values
        self.score = 0
        self.misses = 0
        self.time_left_frames = self.round_seconds * 60

        self.game_over = False
        self.replay_menu = False

    def render(self, screen):
        # Draw holes and moles
        for hole in self.holes:
            pygame.draw.circle(
                screen,
                DARK_BROWN,
                (hole.center_x, hole.center_y),
                40,
            )

            if hole.active:
                pygame.draw.circle(
                    screen,
                    MOLE_BROWN,
                    (hole.center_x, hole.center_y),
                    32,
                )

        # Display current score
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            BLACK,
        )
        screen.blit(score_text, (10, 10))

        # Display countdown timer
        seconds_left = max(0, self.time_left_frames // 60)

        timer_text = self.font.render(
            f"Time: {seconds_left}s",
            True,
            BLACK,
        )
        screen.blit(
            timer_text,
            (self.width - 140, 10),
        )

        # Task 2: Game Over screen
        if self.game_over and not self.replay_menu:
            game_over_text = self.game_over_font.render(
                "GAME OVER",
                True,
                BLACK,
            )

            final_score_text = self.font.render(
                f"Final Score: {self.score}",
                True,
                BLACK,
            )

            replay_text = self.menu_font.render(
                "Press R to Replay",
                True,
                BLACK,
            )

            exit_text = self.menu_font.render(
                "Press Q to Exit",
                True,
                BLACK,
            )

            screen.blit(
                game_over_text,
                (
                    (self.width - game_over_text.get_width()) // 2,
                    self.height // 2 - 90,
                ),
            )

            screen.blit(
                final_score_text,
                (
                    (self.width - final_score_text.get_width()) // 2,
                    self.height // 2 - 30,
                ),
            )

            screen.blit(
                replay_text,
                (
                    (self.width - replay_text.get_width()) // 2,
                    self.height // 2 + 30,
                ),
            )

            screen.blit(
                exit_text,
                (
                    (self.width - exit_text.get_width()) // 2,
                    self.height // 2 + 70,
                ),
            )

        # Task 3: Difficulty selection
        if self.replay_menu:
            menu_title = self.menu_font.render(
                "Choose Difficulty",
                True,
                BLACK,
            )

            easy_text = self.menu_font.render(
                "1 - Easy",
                True,
                BLACK,
            )

            medium_text = self.menu_font.render(
                "2 - Medium",
                True,
                BLACK,
            )

            hard_text = self.menu_font.render(
                "3 - Hard",
                True,
                BLACK,
            )

            exit_text = self.menu_font.render(
                "Q - Exit",
                True,
                BLACK,
            )

            screen.blit(
                menu_title,
                (
                    (self.width - menu_title.get_width()) // 2,
                    150,
                ),
            )

            screen.blit(
                easy_text,
                (
                    (self.width - easy_text.get_width()) // 2,
                    220,
                ),
            )

            screen.blit(
                medium_text,
                (
                    (self.width - medium_text.get_width()) // 2,
                    270,
                ),
            )

            screen.blit(
                hard_text,
                (
                    (self.width - hard_text.get_width()) // 2,
                    320,
                ),
            )

            screen.blit(
                exit_text,
                (
                    (self.width - exit_text.get_width()) // 2,
                    370,
                ),
            )