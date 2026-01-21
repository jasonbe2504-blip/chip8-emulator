#!/usr/bin/env python3
import sys
import os

# Force l'import depuis ce dossier
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importe directement
exec(open('vm.py').read())

import pygame
import time

# Le reste du code identique à partir de "def main():"
# [Copie le code à partir de la ligne "def main():"]
