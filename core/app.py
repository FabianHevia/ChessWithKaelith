"""
Chess with Kaelith - Application Controller
Copyright (c) 2026 Fabián Hevia
All rights reserved.
============================================
Controlador central que maneja la ventana principal,
navegación entre pantallas y estado global.
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
from typing import Dict, Type, Optional, Callable
from PIL import Image

from core.settings import SettingsManager
from core.profile_manager import ProfileManager
from core.audio_manager import AudioManager
from localization.i18n import I18nManager


class ChessWithKaelithApp:
    """
    Controlador principal de la aplicación.
    Gestiona la ventana, navegación y estado global.
    """
    
    # Configuración de ventana
    DEFAULT_WIDTH = 1280
    DEFAULT_HEIGHT = 720
    MIN_WIDTH = 960
    MIN_HEIGHT = 540
    
    def __init__(self):
        """Inicializa la aplicación y todos sus componentes."""
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("Chess with Kaelith")
        self.root.geometry(f"{self.DEFAULT_WIDTH}x{self.DEFAULT_HEIGHT}")
        self.root.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        
        # Centrar ventana
        self._center_window()
        
        # Rutas importantes
        self.root_path = Path(__file__).parent.parent
        self.assets_path = self.root_path / "assets"
        self.data_path = self.root_path / "data"
        
        # Asegurar que existe el directorio de datos
        self.data_path.mkdir(exist_ok=True)
        
        # Inicializar managers
        self.settings = SettingsManager(self.data_path / "settings.json")
        self.profiles = ProfileManager(self.data_path / "profiles.json")
        self.i18n = I18nManager(self.root_path / "localization")
        self.audio = AudioManager(self.assets_path, self.settings)
        
        # Aplicar volúmenes guardados
        self.audio.set_master_volume(self.settings.get("volume", 0.7))
        self.audio.set_music_volume(self.settings.get("music_volume", 0.7))
        self.audio.set_effects_volume(self.settings.get("effects_volume", 0.8))
        
        # Cargar idioma guardado
        saved_language = self.settings.get("language", "es")
        self.i18n.set_language(saved_language)
        
        # Estado de la aplicación
        self.current_screen: Optional[tk.Frame] = None
        self.screens: Dict[str, Type] = {}
        
        # Referencia a imagen de fondo original (usada por las pantallas)
        self._original_bg: Optional[Image.Image] = None
        
        # Callbacks para actualización de idioma
        self._language_callbacks: list[Callable] = []
        
        # Configurar estilo
        self._setup_styles()
        
        # Configurar fondo de la ventana (color de fallback)
        self.root.configure(bg='#1a2318')
        
        # Cargar imagen de fondo original (se usará en cada pantalla)
        self._load_background_image()
        
        # El contenedor principal es el root directamente
        self.main_container = self.root
        
        # Registrar pantallas
        self._register_screens()
        
        # Aplicar configuración de pantalla completa si está guardada
        if self.settings.get("fullscreen", False):
            self.root.attributes("-fullscreen", True)
    
    def _center_window(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        width = self.DEFAULT_WIDTH
        height = self.DEFAULT_HEIGHT
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _setup_styles(self):
        """Configura los estilos ttk personalizados."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colores del tema (basados en el background del bosque)
        self.colors = {
            'primary': '#4a6741',
            'primary_dark': '#3a5331',
            'primary_light': '#6b8b5e',
            'secondary': '#8b7355',
            'accent': '#c4a574',
            'text_light': '#f5f0e6',
            'text_dark': '#2d3a29',
            'bg_dark': '#1a2318',
            'button_hover': '#5a7751',
        }
    
    def _load_background_image(self):
        """Carga la imagen de fondo original (soporta png, jpg, webp)."""
        # Buscar en orden de preferencia
        supported_formats = ['background.webp', 'background.png', 'background.jpg']
        
        for filename in supported_formats:
            bg_path = self.assets_path / filename
            if bg_path.exists():
                try:
                    # Abrir imagen
                    img = Image.open(bg_path)
                    # IMPORTANTE: Forzar carga completa de la imagen
                    # (PIL hace lazy loading por defecto)
                    img.load()
                    # Convertir a RGBA para consistencia
                    self._original_bg = img.convert('RGBA')
                    print(f"Background cargado: {filename} ({img.width}x{img.height})")
                    return
                except Exception as e:
                    print(f"Error cargando {filename}: {e}")
                    import traceback
                    traceback.print_exc()
        
        print(f"Background no encontrado en: {self.assets_path}")
        self._original_bg = None
    
    def _register_screens(self):
        """Registra todas las pantallas disponibles."""
        from ui.screens.main_menu import MainMenuScreen
        from ui.screens.profile_select import ProfileSelectScreen
        from ui.screens.profile_create import ProfileCreateScreen
        from ui.screens.options_menu import OptionsMenuScreen
        
        self.screens = {
            'main_menu': MainMenuScreen,
            'profile_select': ProfileSelectScreen,
            'profile_create': ProfileCreateScreen,
            'options': OptionsMenuScreen,
        }
    
    def navigate_to(self, screen_name: str, **kwargs):
        """
        Navega a una pantalla específica.
        
        Args:
            screen_name: Nombre de la pantalla destino
            **kwargs: Argumentos adicionales para la pantalla
        """
        if screen_name not in self.screens:
            print(f"Pantalla '{screen_name}' no encontrada")
            return
        
        # Destruir pantalla actual si existe
        if self.current_screen is not None:
            self.current_screen.destroy()
        
        # Crear nueva pantalla (sobre el background)
        new_screen = self.screens[screen_name](self.main_container, self, **kwargs)
        self.current_screen = new_screen
        # Usar place() para que la pantalla se coloque sobre el background
        new_screen.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    def register_language_callback(self, callback: Callable):
        """Registra un callback para actualización de idioma."""
        self._language_callbacks.append(callback)
    
    def unregister_language_callback(self, callback: Callable):
        """Elimina un callback de actualización de idioma."""
        if callback in self._language_callbacks:
            self._language_callbacks.remove(callback)
    
    def change_language(self, language: str):
        """
        Cambia el idioma de la aplicación.
        
        Args:
            language: Código del idioma ('es' o 'en')
        """
        self.i18n.set_language(language)
        self.settings.set("language", language)
        
        # Notificar a todos los callbacks
        for callback in self._language_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error en callback de idioma: {e}")
    
    def get_text(self, key: str) -> str:
        """Obtiene un texto traducido."""
        return self.i18n.get(key)
    
    def set_fullscreen(self, fullscreen: bool):
        """Activa o desactiva pantalla completa."""
        self.root.attributes("-fullscreen", fullscreen)
        self.settings.set("fullscreen", fullscreen)
        # Actualizar background después del cambio
        self.root.after(100, self._update_background)
    
    def toggle_fullscreen(self):
        """Alterna el modo pantalla completa."""
        current = self.root.attributes("-fullscreen")
        self.set_fullscreen(not current)
    
    def play_effect(self, effect_name: str):
        """Reproduce un efecto de sonido."""
        self.audio.play_effect(effect_name)
    
    def run(self):
        """Inicia el loop principal de la aplicación."""
        # Mostrar menú principal
        self.navigate_to('main_menu')
        
        # Iniciar loop
        self.root.mainloop()
    
    def quit(self):
        """Cierra la aplicación de forma segura."""
        self.audio.stop_music()
        self.audio.cleanup()
        self.settings.save()
        self.root.quit()