import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien
from button import Title

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Reakcja na niciśnięcie klawisza."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


        
def fire_bullet(ai_settings, screen, ship, bullets):
        """Wystrzelenie pocisku, jeśli nie przekroczono ustalonego limitu."""
        #Utworzenie nowego pocisku i dodanie go do grupy pocisków.
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

def check_keyup_events(event, ship):
    """Reakcja na zwolnienie klawisza."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Rekacja na zdarzenia generowane przez klawiaturę i mysz."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
           check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
            
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Rozpoczęcie nowej gry po kliknięciu przycisku Gra przez użytkownika."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Wyzerowanie ustawień dotyczących gry.
        ai_settings.initialize_dynamic_settings()
        # Ukrycie kursora myszy.
        pygame.mouse.set_visible(False)
        # Ukrycie kursora myszy.
        pygame.mouse.set_visible(False)
        #Wyzerowanie danych statystycznych gry.
        stats.reset_stats()
        stats.game_active = True
        
        # Wyzerowanie obrazów tablicy wyników.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        #Usunięcie zawartości list aliens i bullets.
        aliens.empty()
        bullets.empty()
        
        #Utworzenie nowej floty i iwyśrodkowanie statku.
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Uaktualnienie położenia pocisków i usunięcie tych niewidocznych na ekranie."""
    #Uaktualnienie położenia pocisków.
    bullets.update()
        
    # Usunięcie pocisków, które znajdują się poza ekranem.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Reakcja na kolizję między pociskiem i obcym."""
    # Usunięcie wszystkich pocisków i obcych, między którymi doszło do kolizji.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        #Jeżeli całą flota została zniszczona, gracz przechodzi kolejny poziom.
        # Usunięcie istniejących pocisków, przyśpieszenie gry i utworzenie nowej floty.
        bullets.empty()
        ai_settings.increase_speed()
        
        #Inkrementacja numeru poziomu.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens)
                                
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Uaktualnienie obrazów na ekranie i przejście do nowego ekranu."""
    #title.blitme()
    #Odświeżanie ekranu w trakcie każdej iteracji pętli.
    screen.fill(ai_settings.bg_color)
    
    #Ponowne wyświetlenie wszystkich pocisków pod warstwami statku kosmicznego i obcych.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    
    aliens.draw(screen)
    #Wyświetlenie informacji o punktacji.
    sb.show_score()
    #Wyświetlenie przycisku tylko wtedy, gdy gra jest nieaktywna.
    if not stats.game_active:
        play_button.draw_button()
    
    #Wyświetlenie ostatnio zmodyfikowanego ekranu.
    pygame.display.flip()
    
    
    
def create_fleet(ai_settings, screen, aliens):
    """Utworzenie pełnej floty obcych."""
    #Utworzenie obcego i ustalenie liczby obcych, którzy zmieszczą się w rzędzie.
    #Odległość między poszczególnymi obcymi jest równa szerokości obcego.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    
    #Utworzenie pierwszego rzędu obcych.
    for alien_number in range(number_aliens_x):
        #Utworzenie obcego i umieszczenie go w rzędzie.
        alien = Alien(ai_settings, screen)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        aliens.add(alien)


def check_fleet_edges(ai_settings, aliens):
    """Odpowiednia reakcja, gdy obcy dotrze do krawędzi ekranu."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
def change_fleet_direction(ai_settings, aliens):
    """Przesunięcie całej floty w dół i zmiana kierunku, w którym się
    ona porusza."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Reakcja na uderzenie obcego w statek."""
    if stats.ships_left > 0:
        # Zmniejszenie wartości przechowywanej w ships_left.
        stats.ships_left -= 1
        # Uaktualnienie tablicy wyników.
        sb.prep_ships()
        print(stats.ships_left)
        # Usunięcie zawartości list aliens i bullets.
        aliens.empty()
        bullets.empty()
        # Utworzenie nowej floty i wyśrodkowanie statku.
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()
        # Pauza.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Sprawdzenie, czy którykolwiek obcy dotarł do dolnej krawędzi ekranu."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Tak samo jak w przypadku zderzenia statku z obcym.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
            
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Sprawdzenie, czy flota znajduje się przy krawędzi ekranu,
    a następnie uaktualnienie położenia wszystkich obcych we flocie.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
     # Wykrywanie kolizji między obcym i statkiem.
    if pygame.sprite.spritecollideany(ship, aliens):
        print("Statek został trafiony!!!") 
    # Wykrywanie kolizji między obcym i statkiem.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    # Wyszukiwanie obcych docierających do dolnej krawędzi ekranu.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets) 

def check_high_score(stats, sb):
    """Sprawdzenie, czy mamy nowy najlepszy wynik osiągnięty dotąd w grze."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
     