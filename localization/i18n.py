"""
Chess with Kaelith - Internationalization (i18n)
Copyright (c) 2026 Fabián Hevia
All rights reserved.
=================================================
Sistema de traducciones para soporte multiidioma.
"""

import json
from pathlib import Path
from typing import Dict, Optional


class I18nManager:

    """
    Gestor de internacionalización.
    Maneja las traducciones de la aplicación.
    """
    
    SUPPORTED_LANGUAGES = {
        'es': 'Español',
        'en': 'English',
    }
    
    DEFAULT_LANGUAGE = 'es'
    
    def __init__(self, localization_path: Path):

        """
        Inicializa el gestor de i18n.
        
        Args:
            localization_path: Ruta al directorio de localizaciones
        """

        self.localization_path = localization_path
        self._current_language = self.DEFAULT_LANGUAGE
        self._translations: Dict[str, Dict[str, str]] = {}
        
        # Cargar traducciones por defecto
        self._load_default_translations()
        
        # Intentar cargar desde archivos
        self._load_translations()
    

    def _load_default_translations(self):

        """Carga las traducciones por defecto embebidas."""

        self._translations = {

            'es': {

                # Menú principal
                'app_title': 'Chess with Kaelith',
                'play': 'Jugar',
                'options': 'Opciones',
                'quit': 'Salir',
                'language': 'Idioma',
                'volume': 'Volumen',
                
                # Perfiles
                'select_profile': 'Seleccionar Perfil',
                'create_profile': 'Crear Perfil',
                'new_profile': 'Nuevo Perfil',
                'enter_nickname': 'Introduce tu apodo',
                'nickname': 'Apodo',
                'nickname_placeholder': 'Escribe tu nombre...',
                'create': 'Crear',
                'cancel': 'Cancelar',
                'back': 'Volver',
                'delete': 'Eliminar',
                'confirm_delete': '¿Eliminar este perfil?',
                'yes': 'Sí',
                'no': 'No',
                'no_profiles': 'No hay perfiles creados',
                'profile_limit': 'Límite de perfiles alcanzado',
                'nickname_exists': 'Este apodo ya existe',
                'nickname_empty': 'El apodo no puede estar vacío',
                'games_played': 'Partidas jugadas',
                'wins': 'Victorias',
                'level': 'Nivel',
                
                # Opciones
                'video': 'Vídeo',
                'sound': 'Sonido',
                'accessibility': 'Accesibilidad',
                'fullscreen': 'Pantalla completa',
                'windowed': 'Ventana',
                'resolution': 'Resolución',
                'general_volume': 'Volumen general',
                'music_volume': 'Música',
                'effects_volume': 'Efectos',
                'text_size': 'Tamaño de texto',
                'small': 'Pequeño',
                'medium': 'Mediano',
                'large': 'Grande',
                'high_contrast': 'Alto contraste',
                'on': 'Activado',
                'off': 'Desactivado',
                'apply': 'Aplicar',
                'discard': 'Descartar',
                'reset_defaults': 'Restablecer valores',
                
                # Otros
                'loading': 'Cargando...',
                'error': 'Error',
                'success': 'Éxito',
                'continue': 'Continuar',
            },

            'en': {

                # Main menu
                'app_title': 'Chess with Kaelith',
                'play': 'Play',
                'options': 'Options',
                'quit': 'Quit',
                'language': 'Language',
                'volume': 'Volume',
                
                # Profiles
                'select_profile': 'Select Profile',
                'create_profile': 'Create Profile',
                'new_profile': 'New Profile',
                'enter_nickname': 'Enter your nickname',
                'nickname': 'Nickname',
                'nickname_placeholder': 'Type your name...',
                'create': 'Create',
                'cancel': 'Cancel',
                'back': 'Back',
                'delete': 'Delete',
                'confirm_delete': 'Delete this profile?',
                'yes': 'Yes',
                'no': 'No',
                'no_profiles': 'No profiles created',
                'profile_limit': 'Profile limit reached',
                'nickname_exists': 'This nickname already exists',
                'nickname_empty': 'Nickname cannot be empty',
                'games_played': 'Games played',
                'wins': 'Wins',
                'level': 'Level',
                
                # Options
                'video': 'Video',
                'sound': 'Sound',
                'accessibility': 'Accessibility',
                'fullscreen': 'Fullscreen',
                'windowed': 'Windowed',
                'resolution': 'Resolution',
                'general_volume': 'General volume',
                'music_volume': 'Music',
                'effects_volume': 'Effects',
                'text_size': 'Text size',
                'small': 'Small',
                'medium': 'Medium',
                'large': 'Large',
                'high_contrast': 'High contrast',
                'on': 'On',
                'off': 'Off',
                'apply': 'Apply',
                'discard': 'Discard',
                'reset_defaults': 'Reset to defaults',
                
                # Others
                'loading': 'Loading...',
                'error': 'Error',
                'success': 'Success',
                'continue': 'Continue',
            }
        }
    

    def _load_translations(self):

        """Intenta cargar traducciones desde archivos externos."""
        
        for lang_code in self.SUPPORTED_LANGUAGES:
            filepath = self.localization_path / f"{lang_code}.json"
            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self._translations[lang_code].update(json.load(f))
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error cargando traducciones de {lang_code}: {e}")
    

    def set_language(self, language: str):

        """
        Establece el idioma actual.
        
        Args:
            language: Código del idioma ('es' o 'en')
        """

        if language in self.SUPPORTED_LANGUAGES:
            self._current_language = language
    

    def get_language(self) -> str:

        """
        Obtiene el idioma actual.
        
        Returns:
            Código del idioma actual
        """

        return self._current_language
    

    def get(self, key: str, default: Optional[str] = None) -> str:

        """
        Obtiene una traducción.
        
        Args:
            key: Clave de la traducción
            default: Valor por defecto si no existe
            
        Returns:
            Texto traducido
        """

        translations = self._translations.get(self._current_language, {})
        

        if key in translations:
            return translations[key]
        

        # Fallback al idioma por defecto
        if self._current_language != self.DEFAULT_LANGUAGE:
            default_translations = self._translations.get(self.DEFAULT_LANGUAGE, {})
            if key in default_translations:
                return default_translations[key]
        

        # Si no hay traducción, devolver la clave o el default
        return default if default is not None else key
    

    def get_language_name(self, language: Optional[str] = None) -> str:

        """
        Obtiene el nombre del idioma.
        
        Args:
            language: Código del idioma (usa el actual si es None)
            
        Returns:
            Nombre del idioma
        """

        lang = language or self._current_language
        return self.SUPPORTED_LANGUAGES.get(lang, lang)
    

    def get_available_languages(self) -> Dict[str, str]:

        """
        Obtiene los idiomas disponibles.
        
        Returns:
            Diccionario con códigos y nombres de idiomas
        """
        
        return self.SUPPORTED_LANGUAGES.copy()
