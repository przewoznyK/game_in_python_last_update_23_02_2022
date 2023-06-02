import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    
    def __init__(self, ai_settings, screen):
        """Inicjacja statku kosmicznego i jego położenie początkowe."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #Wczytywanie obrazu statku kosmicznego i pobranie jego prostokąta.
        self.image = pygame.image.load(r'C:\Users\zs1pr\Desktop\alien_invasion_v2\images\ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #Każdy nowy statek kosmiczny pojawia się na dole ekranu.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        #Punkt środkowy statku jest przechowywany w postaci liczby zmiennoprzecinkowej.
        self.center = float(self.rect.centerx)
        
        #Opcje wskazujące na poruszanie się statku.
        self.moving_right = False
        self.moving_left = False
    def update(self):
        """
        Uaktualnienie położenia statku na podstawie opcji wskazującej na jego ruch.
        """
        #Uaktualnienie wartości punktu środkowego statku, a nie jego prostokąta.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        
        #Uaktualnienie obiektu rect na podstawie wartości self.center.
        self.rect.centerx = self.center
   
    def blitme(self):
        """Wyświetlenie statku kosmicznego w jego aktualnym położeniu."""
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """Umieszczenie statku na środku przy dolnej krawędzi ekranu."""
        self.center = self.screen_rect.centerx