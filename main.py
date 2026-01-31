#!/usr/bin/env python3
"""
Chess with Kaelith - Main Entry Point
Copyright (c) 2026 Fabián Hevia
All rights reserved.
=====================================
Aplicación de ajedrez con interfaz gráfica en Tkinter.
Arquitectura modular con separación de UI, lógica y persistencia.
"""

import sys
import os
from pathlib import Path

# Asegurar que el directorio raíz está en el path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from core.app import ChessWithKaelithApp


def main():

    """Punto de entrada principal de la aplicación."""

    try:
        app = ChessWithKaelithApp()
        app.run()

    except Exception as e:
        
        print(f"Error fatal al iniciar la aplicación: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
