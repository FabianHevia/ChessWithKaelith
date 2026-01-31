"""
Chess with Kaelith - Core Module
Copyright (c) 2026 Fabián Hevia
All rights reserved.
=================================
Módulo central con la lógica de la aplicación.
"""

from .app import ChessWithKaelithApp
from .settings import SettingsManager
from .profile_manager import ProfileManager, PlayerProfile

__all__ = [
    'ChessWithKaelithApp',
    'SettingsManager',
    'ProfileManager',
    'PlayerProfile',
]
