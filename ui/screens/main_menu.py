"""
Chess with Kaelith - Main Menu Screen
Copyright (c) 2026 Fabián Hevia
All rights reserved.
======================================
Pantalla del menú principal con opciones de juego.
"""

import tkinter as tk
from typing import TYPE_CHECKING
import random

from ui.screens.base_screen import BaseScreen
from ui.components.widgets import (
    StyledButton,
    StyledSlider,
    LanguageToggle,
    SemiTransparentFrame,
)

if TYPE_CHECKING:
    from core.app import ChessWithKaelithApp


class MusicNotification(tk.Frame):

    """
    Notificación flotante que muestra la canción actual.
    Se desvanece después de unos segundos.
    """
    
    def __init__(self, parent, song_name: str, **kwargs):

        super().__init__(parent, bg='#1a2318', **kwargs)
        
        self.song_name = song_name
        self._alpha = 1.0
        

        # Contenedor con borde
        container = tk.Frame(self, bg='#2a3328', padx=15, pady=8)
        container.pack()
        

        # Icono de música
        icon = tk.Label(
            container,
            text="♪",
            font=('Segoe UI Emoji', 16),
            fg='#c4a574',
            bg='#2a3328'
        )
        icon.pack(side=tk.LEFT, padx=(0, 8))
        

        # Texto "Reproduciendo"
        now_playing = tk.Label(
            container,
            text="Reproduciendo",
            font=('Garamond', 9),
            fg='#8b7355',
            bg='#2a3328'
        )
        now_playing.pack(anchor='w')
        

        # Nombre de la canción
        self.name_label = tk.Label(
            container,
            text=song_name,
            font=('Garamond', 11, 'bold'),
            fg='#f5f0e6',
            bg='#2a3328'
        )
        self.name_label.pack(anchor='w')
        

        # Iniciar animación de desvanecimiento después de 4 segundos
        self.after(4000, self._start_fade_out)
    

    def _start_fade_out(self):
        """Inicia el desvanecimiento gradual."""
        self._fade_step()
    

    def _fade_step(self):
        """Un paso del desvanecimiento."""
        self._alpha -= 0.05
        if self._alpha <= 0:
            self.destroy()
        else:
            # Tkinter no soporta alpha real, simulamos con color
            self.after(50, self._fade_step)



class MainMenuScreen(BaseScreen):

    """
    Pantalla del menú principal.
    Muestra opciones de Jugar, Opciones, idioma y volumen.
    """

    # Canciones disponibles para el menú
    MENU_SONGS = [
        'Chess_With_Kaelith_-_Chill_Fantasy_Hills__Main_Menu_Song_.mp3',
        'Chess_With_Kaelith_-_So_Quiet_Scream__Main_Menu_Song_.mp3',
    ]
    
    def __init__(self, parent: tk.Widget, app: 'ChessWithKaelithApp', **kwargs):

        """Inicializa el menú principal."""

        self._music_notification = None
        super().__init__(parent, app, **kwargs)

        # Iniciar música después de construir la UI
        self.after(500, self._start_music)
    

    def _build_ui(self):

        """Construye la interfaz del menú principal."""

        # Contenedor central con fondo semi-transparente
        self.center_frame = SemiTransparentFrame(
            self,
            alpha=0.9,
            color='#1a2318'
        )
        self.center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Padding interno
        inner_frame = tk.Frame(self.center_frame, bg='#1a2318')
        inner_frame.pack(padx=50, pady=40)
        
        # === TÍTULO ===
        self.title_label = tk.Label(
            inner_frame,
            text="Chess with Kaelith",
            font=('Palatino Linotype', 36, 'bold'),
            fg='#c4a574',  # Dorado
            bg='#1a2318'
        )
        self.title_label.pack(pady=(0, 10))
        

        # Subtítulo decorativo
        self.subtitle_label = tk.Label(
            inner_frame,
            text="— ♔ —",
            font=('Garamond', 18),
            fg='#6b8b5e',  # Verde claro
            bg='#1a2318'
        )
        self.subtitle_label.pack(pady=(0, 30))
        

        # === BOTONES PRINCIPALES ===
        buttons_frame = tk.Frame(inner_frame, bg='#1a2318')
        buttons_frame.pack(pady=10)
        
        # Botón JUGAR (Principal)
        self.play_button = StyledButton(
            buttons_frame,
            text="Jugar",
            command=self._on_play,
            width=320,
            height=70,
            font_size=22,
            primary=True
        )
        self.play_button.pack(pady=10)
        

        # Botón OPCIONES (Secundario, más pequeño)
        self.options_button = StyledButton(
            buttons_frame,
            text="Opciones",
            command=self._on_options,
            width=240,
            height=50,
            font_size=16,
            primary=False
        )
        self.options_button.pack(pady=8)
        

        # Botón SALIR
        self.quit_button = StyledButton(
            buttons_frame,
            text="Salir",
            command=self._on_quit,
            width=180,
            height=45,
            font_size=14,
            primary=False
        )
        self.quit_button.pack(pady=8)

        
        # === SEPARADOR ===
        separator = tk.Frame(inner_frame, bg='#4a6741', height=2)
        separator.pack(fill=tk.X, pady=25, padx=20)

        
        # === CONTROLES INFERIORES ===
        controls_frame = tk.Frame(inner_frame, bg='#1a2318')
        controls_frame.pack(fill=tk.X)

        
        # Frame izquierdo para idioma
        left_frame = tk.Frame(controls_frame, bg='#1a2318')
        left_frame.pack(side=tk.LEFT, padx=10)
        

        self.language_label = tk.Label(
            left_frame,
            text="Idioma",
            font=('Garamond', 11),
            fg='#8b7355',
            bg='#1a2318'
        )
        self.language_label.pack(anchor='w')

        
        current_lang = self.app.settings.get("language", "es")
        self.language_toggle = LanguageToggle(
            left_frame,
            current_language=current_lang,
            command=self._handle_language_toggle  # Método separado para el toggle
        )
        self.language_toggle.pack(pady=5)

        
        # Frame derecho para volumen
        right_frame = tk.Frame(controls_frame, bg='#1a2318')
        right_frame.pack(side=tk.RIGHT, padx=10)

        
        self.volume_slider = StyledSlider(
            right_frame,
            label="Volumen",
            from_=0,
            to=100,
            initial=self.app.settings.get("volume", 0.7) * 100,
            command=self._on_volume_change,
            width=200
        )
        self.volume_slider.pack(pady=5)

        
        # === VERSIÓN ===
        version_label = tk.Label(
            inner_frame,
            text="v0.1.0 - Alpha",
            font=('Garamond', 9),
            fg='#555555',
            bg='#1a2318'
        )
        version_label.pack(pady=(20, 0))


    def _start_music(self):

        """Inicia la música del menú."""

        # Seleccionar canción aleatoria
        song = random.choice(self.MENU_SONGS)
        song_name = self.app.audio.play_music(song, loop=True, fade_in_ms=2000)
        
        if song_name:
            self._show_music_notification(song_name)
    

    def _show_music_notification(self, song_name: str):

        """Muestra la notificación de música en la esquina inferior derecha."""
        # Eliminar notificación anterior si existe
        if self._music_notification and self._music_notification.winfo_exists():
            self._music_notification.destroy()
        
        # Crear nueva notificación
        self._music_notification = MusicNotification(self, song_name)
        self._music_notification.place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)
    

    def _update_texts(self):
        """Actualiza los textos con el idioma actual."""
        self.play_button.set_text(self.get_text('play'))
        self.options_button.set_text(self.get_text('options'))
        self.quit_button.set_text(self.get_text('quit'))
        self.language_label.config(text=self.get_text('language'))
        self.volume_slider.set_label(self.get_text('volume'))
    

    def _on_play(self):

        """Maneja el clic en Jugar."""

        self.app.play_effect('button_play')
        self.navigate_to('profile_select')
    

    def _on_options(self):

        """Maneja el clic en Opciones."""

        self.app.play_effect('button_options')
        self.navigate_to('options')
    

    def _on_quit(self):

        """Maneja el clic en Salir."""

        self.app.quit()


    def _handle_language_toggle(self, language: str):

        """
        Maneja el cambio de idioma desde el toggle.
        Método separado para no colisionar con _on_language_change de BaseScreen.
        """

        self.app.play_effect('button_language')
        self.app.change_language(language)
    
    
    def _on_volume_change(self, value: float):
        """Maneja el cambio de volumen."""
        self.app.settings.set("volume", value)


    def destroy(self):

        """Limpia recursos al destruir la pantalla."""
        # No detenemos la música aquí para permitir transiciones suaves
        super().destroy()
