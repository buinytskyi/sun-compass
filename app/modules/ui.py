import os

import pygame
from datetime import datetime
import os
import math

class Text:
    def __init__(self, screen, color):
        self.screen = screen
        self.color = color

    def draw(self, pos, font_size, value):
        full_text = f"{value}"
        self.font = pygame.font.Font(None, int(font_size))
        text_surface = self.font.render(full_text, True, self.color)
        self.screen.blit(text_surface, pos)

class Cardinal :
    def __init__(self, screen):
        self.screen = screen

    def draw(self, position_x, position_y, filename):
        assets_path = os.path.join(os.path.dirname(__file__), os.pardir, "assets", filename)
        image = pygame.image.load(assets_path).convert_alpha()
        image.set_colorkey((0, 0, 0))
        self.screen.blit(image, (position_x, position_y))

class Circular:
    def __init__(self, screen, center, radius, color, color2, color4, sr_angle, ss_angle):
        self.screen = screen
        self.center = center
        self.radius = radius
        self.color = color
        self.color2 = color2
        self.color4 = color4
        self.font = pygame.font.Font(None, 32)
        self.start_angle = sr_angle
        self.end_angle = ss_angle

    def draw_hour_ticks(self, get_sn_angle):
        for hour in range(24):
            angle_divisions = ((hour * 360 / 24) + get_sn_angle)
            vec_outer = pygame.math.Vector2(0, -self.radius).rotate(angle_divisions)
            vec_inner = pygame.math.Vector2(0, -(self.radius - 15)).rotate(angle_divisions)

            end_x, end_y = self.center[0] + vec_outer.x, self.center[1] + vec_outer.y
            start_x, start_y = self.center[0] + vec_inner.x, self.center[1] + vec_inner.y

            pygame.draw.line(self.screen, self.color, (start_x, start_y), (end_x, end_y), 2)

            digit_vec = pygame.math.Vector2(0, -(self.radius - 25)).rotate(angle_divisions)
            digit_x, digit_y = self.center[0] + digit_vec.x, self.center[1] + digit_vec.y

            digit = self.font.render(str(hour), True, self.color2)
            digit_rect = digit.get_rect(center=(digit_x, digit_y))
            self.screen.blit(digit, digit_rect)

    def draw_clock_hand(self, get_sn_angle, tz):
        cr_angle = (((int(datetime.now(tz).strftime('%H')) * 15) +
                     (int(datetime.now(tz).strftime('%M')) / 4)) + get_sn_angle)

        vec_outer = pygame.math.Vector2(0, -self.radius).rotate(cr_angle)
        vec_inner = pygame.math.Vector2(0, -(self.radius - 390)).rotate(cr_angle)
        vec_shadow_outer = pygame.math.Vector2(0, -self.radius).rotate(cr_angle + 180)
        vec_shadow_inner = pygame.math.Vector2(0, -(self.radius - 390)).rotate(cr_angle + 180)

        end_x, end_y = self.center[0] + vec_outer.x, self.center[1] + vec_outer.y
        start_x, start_y = self.center[0] + vec_inner.x, self.center[1] + vec_inner.y
        end_shadow_x, end_shadow_y = self.center[0] + vec_shadow_outer.x, self.center[1] + vec_shadow_outer.y
        start_shadow_x, start_shadow_y = self.center[0] + vec_shadow_inner.x, self.center[1] + vec_shadow_inner.y

        pygame.draw.line(self.screen, self.color2, (start_x, start_y), (end_x, end_y), 5)
        pygame.draw.line(self.screen, self.color2, (start_shadow_x, start_shadow_y), (end_shadow_x, end_shadow_y), 2)

    def draw_border(self):
        pygame.draw.circle(self.screen, self.color2, self.center, self.radius, 1)

    def draw_sector(self):
        for i in range(int(self.start_angle), int(self.end_angle), 1):
            vec_hand = pygame.math.Vector2(0, -self.radius).rotate(i)
            end_x, end_y = self.center[0] + vec_hand.x, self.center[1] + vec_hand.y
            pygame.draw.line(self.screen, self.color4, self.center, (end_x, end_y), 4)