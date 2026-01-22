

import pygame
import sys
import time

def main():
    # Initialisation Pygame
    pygame.init()
    
    # Configuration de l'écran
    SCREEN_WIDTH = 64
    SCREEN_HEIGHT = 32
    SCALE = 10
    
    screen = pygame.display.set_mode((SCREEN_WIDTH * SCALE, SCREEN_HEIGHT * SCALE))
    pygame.display.set_caption("Émulateur CHIP-8")
    
    # Initialiser la VM
    from vm import Chip8VM
    vm = Chip8VM()
    
    # Charger une ROM (à adapter)
    rom_file = "roms/pong.ch8"
    # Charger une ROM
    print(f"🔍 Chargement: {rom_file}")
    try:
        with open(rom_file, "rb") as f:
            data = f.read()
            print(f"ROM chargée: {len(data)} octets")
            vm.load_rom(data)
            # Forcer un affichage initial
            for x in range(20, 44):
                for y in range(10, 22):
                    vm.display[x][y] = 1
    except FileNotFoundError:
        print(f"FICHIER NON TROUVÉ: {rom_file}")
        # Mode test
        for x in range(20, 44):
            for y in range(10, 22):
                vm.display[x][y] = 1
    except Exception as e:
        print(f" ERREUR: {e}")
    
    # FORCER redessin
    vm.needs_redraw = True
    print(" needs_redraw = True (forcé)")
    
    print("\n" + "="*50)
    print("Contrôles :")
    print("1 2 3 4    -> 1 2 3 C")
    print("Q W E R    -> 4 5 6 D")
    print("A S D F    -> 7 8 9 E")
    print("Z X C V    -> A 0 B F")
    print("ESPACE     -> Pause/Reprise")
    print("ÉCHAP      -> Quitter")
    print("="*50 + "\n")
    
    # Variables pour la boucle principale
    clock = pygame.time.Clock()
    running = True
    paused = False
    last_timer_update = time.time()
    
    # --- BOUCLE PRINCIPALE ---
    while running:
        current_time = time.time()
        
        # --- Gestion des événements ---
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    status = "⏸️PAUSE" if paused else " REPRISE"
                    print(status)
        
        # --- Si pas en pause, exécuter ---
        if not paused:
            # 1. Mettre à jour l'état des touches
            vm.update_keys(events)
            
            # 2. Exécuter une instruction CHIP-8
            vm.step()
            
# 3. Mettre à jour les timers (60 fois par seconde)
    current_time = pygame.time.get_ticks() / 1000.0
    if current_time - last_timer_update >= 1.0/60.0:
        vm.update_timers()
        last_timer_update = current_time# Debug affichage
print(f"Frame - needs_redraw: {vm.needs_redraw}")
frame_count = 0 if "frame_count" not in locals() else frame_count + 1

# Forcer affichage toutes les 10 frames
if vm.needs_redraw or frame_count % 10 == 0:
    # Effacer l'écran
    screen.fill((0, 0, 0)) # Noir
    print("Effaçage écran")
    
    # Dessiner chaque pixel
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            if vm.display[x][y] != 0:
                # Dessiner un carré blanc 10x10 pixels
                pygame.draw.rect(screen, (255, 255, 255),
                                (x * SCALE, y * SCALE, SCALE, SCALE))

    # Afficher à l'écran
    pygame.display.flip()
    print("Mise à jour écran")
    print(f"Pixels allumés: {sum(sum(row) for row in vm.display)}")
    vm.needs_redraw = False
    # --- Nettoyage et sortie ---
    pygame.quit()
    print("\n" + "="*50)
    print("✔ Émulateur arrêté - Merci d'avoir joué !")
    print("="*50)

# Point d'entrée du programme
if __name__ == "__main__":
    main()
