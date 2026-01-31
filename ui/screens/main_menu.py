"""
Chess with Kaelith - Main Menu Screen
Copyright (c) 2026 Fabián Hevia
All rights reserved.
======================================
Pantalla del menú principal con opciones de juego.
"""

import tkinter as tk
from typing import TYPE_CHECKING, Optional

from ui.screens.base_screen import BaseScreen
from ui.components.widgets import (
    StyledButton,
    StyledSlider,
    LanguageToggle,
    SemiTransparentFrame,
)

if TYPE_CHECKING:
    from core.app import ChessWithKaelithApp
    from core.audio_manager import Track


class MusicNotification(tk.Frame):
    """
    Notificación flotante que muestra la canción actual.
    Se desvanece después de unos segundos.
    """
    
    def __init__(self, parent, song_name: str, now_playing_text: str = "Reproduciendo", **kwargs):
        super().__init__(parent, bg='#1a2318', **kwargs)
        
        self.song_name = song_name
        self._fade_steps = 20
        self._current_step = 0
        
        # Contenedor con borde redondeado simulado
        container = tk.Frame(
            self, 
            bg='#2a3328',
            highlightbackground='#4a6741',
            highlightthickness=1
        )
        container.pack(padx=2, pady=2)
        
        inner = tk.Frame(container, bg='#2a3328')
        inner.pack(padx=15, pady=10)
        
        # Icono de música
        icon = tk.Label(
            inner,
            text="♪",
            font=('Segoe UI Emoji', 18),
            fg='#c4a574',
            bg='#2a3328'
        )
        icon.pack(side=tk.LEFT, padx=(0, 12))
        
        # Contenedor de texto
        text_frame = tk.Frame(inner, bg='#2a3328')
        text_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Texto "Reproduciendo"
        self.now_playing_label = tk.Label(
            text_frame,
            text=now_playing_text,
            font=('Garamond', 9),
            fg='#8b7355',
            bg='#2a3328'
        )
        self.now_playing_label.pack(anchor='w')
        
        # Nombre de la canción
        self.name_label = tk.Label(
            text_frame,
            text=song_name,
            font=('Garamond', 12, 'bold'),
            fg='#f5f0e6',
            bg='#2a3328'
        )
        self.name_label.pack(anchor='w')
        
        # Iniciar animación de desvanecimiento después de 4 segundos
        self.after(4000, self._start_fade_out)
    
    def _start_fade_out(self):
        """Inicia el desvanecimiento gradual."""
        self._current_step = 0
        self._fade_step()
    
    def _fade_step(self):
        """Un paso del desvanecimiento."""
        self._current_step += 1
        
        if self._current_step >= self._fade_steps:
            self.destroy()
        else:
            # Programar siguiente paso
            self.after(50, self._fade_step)


class MainMenuScreen(BaseScreen):
    """
    Pantalla del menú principal.
    Muestra opciones de Jugar, Opciones, idioma y volumen.
    """
    
    def __init__(self, parent: tk.Widget, app: 'ChessWithKaelithApp', **kwargs):
        """Inicializa el menú principal."""
        self._music_notification: Optional[MusicNotification] = None
        super().__init__(parent, app, **kwargs)
        
        # Registrar callback para cambios de pista
        self.app.audio.register_track_change_callback(self._on_track_change)
        
        # Solicitar música de menú (NO reinicia si ya está sonando)
        self.after(100, self._ensure_menu_music)
    
    def _ensure_menu_music(self):
        """
        Asegura que haya música de menú reproduciéndose.
        Solo inicia nueva música si no hay ninguna o si es de otra categoría.
        """
        # request_music retorna None si ya está sonando la misma categoría
        track_name = self.app.audio.request_music('menu')
        
        if track_name:
            # Hubo cambio de pista, mostrar notificación
            self._show_music_notification(track_name)
    
    def _on_track_change(self, track: 'Track'):
        """Callback cuando cambia la pista de música."""
        # Solo mostrar si estamos visibles
        if self.winfo_exists() and track.category == 'menu':
            self._show_music_notification(track.display_name)
    
    def _show_music_notification(self, song_name: str):
        """Muestra la notificación de música en la esquina inferior derecha."""
        # Eliminar notificación anterior si existe
        if self._music_notification:
            try:
                if self._music_notification.winfo_exists():
                    self._music_notification.destroy()
            except:
                pass
        
        # Crear nueva notificación
        now_playing = self.get_text('now_playing') if hasattr(self, 'get_text') else "Reproduciendo"
        self._music_notification = MusicNotification(self, song_name, now_playing)
        self._music_notification.place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)
    
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
            fg='#c4a574',
            bg='#1a2318'
        )
        self.title_label.pack(pady=(0, 10))
        
        # Subtítulo decorativo
        self.subtitle_label = tk.Label(
            inner_frame,
            text="— ♔ —",
            font=('Garamond', 18),
            fg='#6b8b5e',
            bg='#1a2318'
        )
        self.subtitle_label.pack(pady=(0, 30))
        
        # === BOTONES PRINCIPALES ===
        buttons_frame = tk.Frame(inner_frame, bg='#1a2318')
        buttons_frame.pack(pady=10)
        
        # Botón JUGAR (principal, más grande)
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
        
        # Botón OPCIONES (secundario, más pequeño)
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
            command=self._handle_language_toggle
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
        """Maneja el cambio de idioma desde el toggle."""
        self.app.play_effect('button_language')
        self.app.change_language(language)
    
    def _on_volume_change(self, value: float):
        """Maneja el cambio de volumen."""
        self.app.settings.set("volume", value)
        self.app.audio.set_master_volume(value)
    
    def destroy(self):
        """Limpia recursos al destruir la pantalla."""
        # Desregistrar callback de cambio de pista
        try:
            self.app.audio.unregister_track_change_callback(self._on_track_change)
        except:
            pass
        
        # NO detenemos la música - debe continuar entre pantallas
        super().destroy()