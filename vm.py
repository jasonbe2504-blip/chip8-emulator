import pygame

class Chip8VM:
    def __init__(self):
        self.memory = [0] * 4096
        self.V = [0] * 16
        self.I = 0
        self.pc = 0x200
        self.stack = []
        self.delay_timer = 0
        self.sound_timer = 0
        self.display = [[0 for _ in range(32)] for _ in range(64)]
        self.needs_redraw = False
        self.keys = [0] * 16
        
        # Police CHIP-8
        font = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, 0x20, 0x60, 0x20, 0x20, 0x70,
            0xF0, 0x10, 0xF0, 0x80, 0xF0, 0xF0, 0x10, 0xF0, 0x10, 0xF0,
            0x90, 0x90, 0xF0, 0x10, 0x10, 0xF0, 0x80, 0xF0, 0x10, 0xF0,
            0xF0, 0x80, 0xF0, 0x90, 0xF0, 0xF0, 0x10, 0x20, 0x40, 0x40,
            0xF0, 0x90, 0xF0, 0x90, 0xF0, 0xF0, 0x90, 0xF0, 0x10, 0xF0,
            0xF0, 0x90, 0xF0, 0x90, 0x90, 0xE0, 0x90, 0xE0, 0x90, 0xE0,
            0xF0, 0x80, 0x80, 0x80, 0xF0, 0xE0, 0x90, 0x90, 0x90, 0xE0,
            0xF0, 0x80, 0xF0, 0x80, 0xF0, 0xF0, 0x80, 0xF0, 0x80, 0x80
        ]
        for i in range(len(font)):
            self.memory[i] = font[i]
    
    def load_rom(self, data):
        for i, byte in enumerate(data):
            if 0x200 + i < 4096:
                self.memory[0x200 + i] = byte
    
    def step(self):
        # Simulation d'exécution
        self.pc += 2
        self.needs_redraw = True
    
    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
    
    def update_keys(self, events):
        """Gestion des touches pour les jeux"""
        # Mapping clavier CHIP-8
        keymap = {
            pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
            pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
            pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
            pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF
        }
        
        # Réinitialiser
        self.keys = [0] * 16
        
        # Mettre à jour
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in keymap:
                    self.keys[keymap[event.key]] = 1
            elif event.type == pygame.KEYUP:
                if event.key in keymap:
                    self.keys[keymap[event.key]] = 0
