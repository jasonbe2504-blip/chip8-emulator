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
    pygame.display.set_caption("Émulateur CHIP-8 - PONG")
    
    # Initialiser la VM
    from vm import Chip8VM
    vm = Chip8VM()
    
    # Charger PONG
    rom_file = "roms/pong.ch8"
    print(f"🔍 Chargement ROM: {rom_file}")
    
    try:
        with open(rom_file, "rb") as f:
            data = f.read()
            print(f"✅ ROM chargée: {len(data)} octets")
            vm.load_rom(data)
            # Dessiner un rectangle de test
            for x in range(20, 44):
                for y in range(10, 22):
                    vm.display[x][y] = 1
    except FileNotFoundError:
        print(f"❌ FICHIER NON TROUVÉ: {rom_file}")
        print("   Création mode test...")
        # Dessiner un X
        for i in range(64):
            vm.display[i][i] = 1
            vm.display[i][31-i] = 1
    except Exception as e:
        print(f"❌ ERREUR: {e}")
    
    # FORCER le premier affichage
    vm.needs_redraw = True
    print("🎨 Premier affichage forcé")
    
    print("\n" + "="*50)
    print("Contrôles :")
    print("  1 2 3 4    -> 1 2 3 C")
    print("  Q W E R    -> 4 5 6 D")
    print("  A S D F    -> 7 8 9 E")
    print("  Z X C V    -> A 0 B F")
    print("  ESPACE     -> Pause/Reprise")
    print("  ÉCHAP      -> Quitter")
    print("="*50 + "\n")
    
    # Variables pour la boucle principale
    clock = pygame.time.Clock()
    running = True
    paused = False
    last_timer_update = time.time()
    frame_count = 0
    
    # --- BOUCLE PRINCIPALE ---
    while running:
        current_time = time.time()
        frame_count += 1
        
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
                    status = "⏸️  PAUSE" if paused else "▶️  REPRISE"
                    print(status)
        
        # --- Si pas en pause, exécuter ---
        if not paused:
            # 1. Mettre à jour l'état des touches
            vm.update_keys(events)
            
            # 2. Exécuter une instruction CHIP-8
            vm.step()
            
            # 3. Mettre à jour les timers (60 fois par seconde)
            if current_time - last_timer_update >= 1.0/60.0:
                vm.update_timers()
                last_timer_update = current_time
            
            # 4. Mettre à jour l'affichage si nécessaire
            # FORCER l'affichage toutes les 5 frames au début
            if vm.needs_redraw or frame_count < 30:
                print(f"🎨 Frame {frame_count}: Redessin...")
                
                # Effacer l'écran
                screen.fill((0, 0, 0))
                
                # Dessiner chaque pixel
                pixels_allumes = 0
                for x in range(SCREEN_WIDTH):
                    for y in range(SCREEN_HEIGHT):
                        if vm.display[x][y] != 0:
                            # Dessiner un carré blanc 10x10 pixels
                            pygame.draw.rect(screen, (255, 255, 255),
                                             (x * SCALE, y * SCALE, SCALE, SCALE))
                            pixels_allumes += 1
                
                print(f"   📊 Pixels allumés: {pixels_allumes}")
                
                # Afficher à l'écran
                pygame.display.flip()
                vm.needs_redraw = False
        
        # --- Limiter la vitesse (environ 500 instructions/sec) ---
        clock.tick(500)
        
        # Arrêter les logs après 30 frames
        if frame_count == 30:
            print("✅ Mode silencieux activé...")
    
    # --- Nettoyage et sortie ---
    pygame.quit()
    print("\n" + "="*50)
    print("✔ Émulateur arrêté - Merci d'avoir joué !")
    print("="*50)

# Point d'entrée du programme
if __name__ == "__main__":
    main()
