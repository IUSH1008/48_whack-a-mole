import pygame
import random
from .hole import Hole

# Game Engine

DARK_BROWN = (60, 40, 20)
MOLE_BROWN = (140, 95, 55)
BLACK = (0, 0, 0)


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

        self.spawn_chance = 0.02
        self.mole_up_frames = 45

        self.round_seconds = 30
        self.time_left_frames = self.round_seconds * 60

        self.score = 0
        self.misses = 0

        self.font = pygame.font.SysFont("Arial", 28)
        self.game_over_font = pygame.font.SysFont("Arial", 48)

        self.game_over = False

    def handle_event(self, event):
        # Do not accept normal gameplay input after Game Over
        if self.game_over:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

    def _handle_click(self, pos):
        hit_something = False

        # Task 1:
        # Only hit active moles and stop after the first successful hit.
        # This prevents one click from scoring multiple points.
        for hole in self.holes:
            if hole.active and hole.rect().collidepoint(pos):
                if hole.whack():
                    self.score += 1
                    hit_something = True
                    break

        if not hit_something:
            self.misses += 1

    def handle_input(self):
        # Reserved for continuously-held-key input.
        # This game is entirely mouse-driven.
        pass

    def update(self):
        if self.game_over:
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
        if self.game_over:
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

            screen.blit(
                game_over_text,
                (
                    (self.width - game_over_text.get_width()) // 2,
                    self.height // 2 - 50,
                ),
            )

            screen.blit(
                final_score_text,
                (
                    (self.width - final_score_text.get_width()) // 2,
                    self.height // 2 + 10,
                ),
            )