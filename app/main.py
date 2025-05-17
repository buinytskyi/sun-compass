from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz
import pygame
from suntime import Sun
from stateful.config import Config
from modules.scanline import Scanline
from modules.globemap import Globemap
from modules.ui import Circular, Text, Cardinal

class SolarCompass:
    def __init__(self):
        db = Config(db_name="config.db")
        if db.check():
            tz = "UTC"
            self.lon = 0
            self.lat = 0
        else:
            db.get()
            tz = db.tz
            self.lon = float(db.lon)
            self.lat = float(db.lat)

        global lon_center, lat_center, center_x, center_y, radius, geojson_data, country_border_data, width, height
        width = 800
        height = 800
        center_x = width // 2
        center_y = height // 2
        self.tz = pytz.timezone(tz)

        self.radius = 400

        sun = Sun(self.lat, self.lon)
        self.today_sr = sun.get_sunrise_time()
        self.today_ss = sun.get_sunset_time()

        self.tz = pytz.timezone(str(self.tz))
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.SCALED | pygame.FULLSCREEN )
        self.clock = pygame.time.Clock()
        self.running = False
        self.font = pygame.font.Font(None, 24)
        self.color = pygame.Color('forestgreen')
        self.color2 = pygame.Color('lime')
        self.color3 = pygame.Color('darkgreen')
        self.color4 = pygame.Color('grey6')
        self.center = self.screen.get_rect().center

        #Class init
        self.scanline_manager = Scanline(self.screen, width, height, speed=10)
        self.globemap = Globemap()
        self.circular = Circular( self.screen, self.center, self.radius, self.color, self.color2, self.color4, self.font, self.get_sr_angle(), self.get_ss_angle() )
        self.text = Text(self.screen, self.font, self.color)
        self.cardinal = Cardinal(self.screen)

    def get_cr(self):
        return datetime.now(self.tz).strftime('%H:%M')

    def get_sr(self):
        return self.today_sr.astimezone(self.tz).strftime('%H:%M')

    def get_ss(self):
        return self.today_ss.astimezone(self.tz).strftime('%H:%M')

    def get_dd(self):
        self.today_dd = datetime.strptime(self.get_ss(), '%H:%M') - datetime.strptime(self.get_sr(), '%H:%M')
        return self.today_dd

    def get_sn(self):
        self.today_sn = (self.get_dd() / 2) + self.today_sr.astimezone(self.tz)
        return self.today_sn.strftime('%H:%M')

    def get_sn_angle(self):
        self.today_sn = (self.get_dd() / 2) + self.today_sr.astimezone(self.tz)
        angle = 540 - ((int(self.today_sn.strftime('%H')) * 15) + (int(self.today_sn.strftime('%M')) / 4))
        return angle

    def get_sr_angle(self):
        angle = self.get_sn_angle() + ((int(self.today_sr.astimezone(self.tz).strftime('%H')) * 15) + (int(self.today_sr.astimezone(self.tz).strftime('%M')) / 4))
        return angle

    def get_ss_angle(self):
        angle = self.get_sn_angle() + ((int(self.today_ss.astimezone(self.tz).strftime('%H')) * 15) + (int(self.today_ss.astimezone(self.tz).strftime('%M')) / 4))
        return angle

    def screen_main(self):
        self.screen.fill((0, 0, 0))
        self.circular.draw_sector()
        self.globemap.draw_geojson_coastlines(self.lon, self.lat, self.color3)  # Map
        self.globemap.draw_geojson_country_borders(self.lon, self.lat, self.color3)
        self.text.draw(f"Day durration: ", (600, 760), self.get_dd())
        self.text.draw(f"{self.tz.zone}", (20, 760), self.get_cr())
        self.cardinal.draw(349, 10, "n_direction.png" )
        self.cardinal.draw(690, 350, "e_direction.png")
        self.cardinal.draw(352, 690, "s_direction.png" )
        self.cardinal.draw(10, 352, "w_direction.png")
        self.cardinal.draw(375, 375, "center.png")
        self.circular.draw_hour_ticks(self.get_sn_angle())
        self.circular.draw_clock_hand(self.get_sn_angle(), self.tz)
        self.circular.draw_border()
        self.scanline_manager.update()
        self.scanline_manager.draw()
        pygame.display.flip()

    def get_size(self):
        return width, height

    def get_rect(self):
        return pygame.Rect(0, 0, width, height)

    def loop(self):
        self.running = True
        lon_center = self.lon
        lat_center = self.lat
        prev_mouse_pos = None
        left_button = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        left_button = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        tf = TimezoneFinder()
                        tz = tf.timezone_at(lat=lat_center, lng=lon_center)
                        db = Config(db_name='config.db')
                        db.save(tz, lon_center, lat_center)
                        self.__init__()
                        self.running = False
                        self.loop()
                        left_button = False
                if event.type == pygame.MOUSEMOTION:
                    if left_button:
                        current_mouse_pos = event.pos
                        if prev_mouse_pos is None:
                            prev_mouse_pos = current_mouse_pos
                        else:

                            dx = prev_mouse_pos[0] - current_mouse_pos[0]
                            dy = prev_mouse_pos[1] - current_mouse_pos[1]

                            if dx > 0:
                                lon_center = min(lon_center + 0.5, 180)  # Move right
                                print(lon_center)
                            elif dx < 0:
                                lon_center = max(lon_center - 0.5, -180)  # Move left
                                print(lon_center)

                            if dy > 0:
                                lat_center = max(lat_center - 0.5, -66)  # Move down
                            elif dy < 0:
                                lat_center = min(lat_center + 0.5, 66)  # Move up

                        prev_mouse_pos = current_mouse_pos
            self.lon = lon_center
            self.lat = lat_center
            self.screen_main()

if __name__ == '__main__':
    screen = SolarCompass()
    screen.loop()
