#!/usr/bin/env python3
import sys
import os

# Ajoute ce dossier au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import
import vm

import pygame
import time

def main():
    if len(sys.argv) < 2:
        print("Donne un fichier ROM!")
        return
    
    rom = sys.argv[1]
    
    pygame.init()
    screen = pygame.display.set_mode((640, 320))
    
    # Créer VM
    machine = vm.Chip8VM()
    
    # Charger ROM
    try:
        with open(rom, "rb") as f:
            machine.load_rom(f.read())
        print("ROM chargée!")
    except:
        print("Erreur ROM")
        return
    
    print("Appuie sur Échap pour quitter")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Exécuter une instruction
        machine.step()
        
        # Dessiner
        screen.fill((0,0,0))
        for x in range(64):
            for y in range(32):
                if machine.display[x, y]:
                    pygame.draw.rect(screen, (255,255,255), (x*10, y*10, 10, 10))
        pygame.display.flip()
        
        # Ralentir
        pygame.time.delay(50)
    
    pygame.quit()

if __name__ == "__main__":
    main()
