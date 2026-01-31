"""
Chess with Kaelith - Options Menu Screen
Copyright (c) 2026 Fabián Hevia
All rights reserved.
=========================================
Pantalla de opciones con configuraciones de video, sonido y accesibilidad.
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from ui.screens.base_screen import BaseScreen
from ui.components.widgets import StyledButton, StyledSlider, SemiTransparentFrame

if TYPE_CHECKING:
    from core.app import ChessWithKaelithApp


class OptionsTab(tk.Frame):

    """
    Contenedor base para cada pestaña de opciones.
    """
    
    def __init__(self, parent, app: 'ChessWithKaelithApp', **kwargs):
        super().__init__(parent, bg='#1a2318', **kwargs)
        self.app = app
    
    def get_text(self, key: str) -> str:
        return self.app.get_text(key)
    
    def update_texts(self):
        """Actualiza textos. Sobrescribir en subclases."""
        pass


class VideoTab(OptionsTab):

    """Pestaña de opciones de video."""
    
    def __init__(self, parent, app: 'ChessWithKaelithApp', **kwargs):
        super().__init__(parent, app, **kwargs)
        self._build_ui()
    

    def _build_ui(self):

        """Construye la UI de opciones de video."""

        # === PANTALLA COMPLETA ===
        fullscreen_frame = tk.Frame(self, bg='#2a3328')
        fullscreen_frame.pack(fill=tk.X, pady=10, padx=10)
        

        self.fullscreen_label = tk.Label(
            fullscreen_frame,
            text="Pantalla completa",
            font=('Garamond', 13),
            fg='#c4a574',
            bg='#2a3328'
        )
        self.fullscreen_label.pack(side=tk.LEFT, padx=15, pady=12)
        

        # Toggle para activar o desactivar la pantalla completa
        toggle_frame = tk.Frame(fullscreen_frame, bg='#2a3328')
        toggle_frame.pack(side=tk.RIGHT, padx=15, pady=10)
        

        self._fullscreen_var = tk.BooleanVar(
            value=self.app.settings.get("fullscreen", False)
        )
        
        self.windowed_btn = tk.Label(
            toggle_frame,
            text="Ventana",
            font=('Garamond', 11),
            bg='#3a4338',
            fg='#f5f0e6',
            padx=12,
            pady=6,
            cursor='hand2'
        )
        self.windowed_btn.pack(side=tk.LEFT)
        

        self.fullscreen_btn = tk.Label(
            toggle_frame,
            text="Completa",
            font=('Garamond', 11),
            bg='#3a4338',
            fg='#f5f0e6',
            padx=12,
            pady=6,
            cursor='hand2'
        )
        self.fullscreen_btn.pack(side=tk.LEFT)

        
        self._update_fullscreen_toggle()

        
        self.windowed_btn.bind('<Button-1>', lambda e: self._set_fullscreen(False))
        self.fullscreen_btn.bind('<Button-1>', lambda e: self._set_fullscreen(True))
        

        # === RESOLUCIÓN ===
        resolution_frame = tk.Frame(self, bg='#2a3328')
        resolution_frame.pack(fill=tk.X, pady=10, padx=10)
        
        self.resolution_label = tk.Label(
            resolution_frame,
            text="Resolución",
            font=('Garamond', 13),
            fg='#c4a574',
            bg='#2a3328'
        )
        self.resolution_label.pack(side=tk.LEFT, padx=15, pady=12)

        
        # Dropdown de resoluciones
        self._resolution_var = tk.StringVar(
            value=self.app.settings.get("resolution", "1280x720")
        )
        
        resolutions = ["1280x720", "1366x768", "1600x900", "1920x1080"]

        
        self.resolution_dropdown = ttk.Combobox(
            resolution_frame,
            textvariable=self._resolution_var,
            values=resolutions,
            state='readonly',
            width=12,
            font=('Garamond', 11)
        )
        self.resolution_dropdown.pack(side=tk.RIGHT, padx=15, pady=10)
        self.resolution_dropdown.bind('<<ComboboxSelected>>', self._on_resolution_change)

    
    def _update_fullscreen_toggle(self):

        """Actualiza el visual del toggle de pantalla completa."""

        is_fullscreen = self._fullscreen_var.get()
        self.windowed_btn.config(bg='#4a6741' if not is_fullscreen else '#3a4338')
        self.fullscreen_btn.config(bg='#4a6741' if is_fullscreen else '#3a4338')
    

    def _set_fullscreen(self, fullscreen: bool):

        """Establece el modo de pantalla."""

        self._fullscreen_var.set(fullscreen)
        self._update_fullscreen_toggle()
        self.app.set_fullscreen(fullscreen)
    
    
    def _on_resolution_change(self, event):

        """Maneja el cambio de resolución."""

        resolution = self._resolution_var.get()
        self.app.settings.set("resolution", resolution)
        
        # Aplicar resolución si no está en pantalla completa
        if not self._fullscreen_var.get():
            width, height = map(int, resolution.split('x'))
            self.app.root.geometry(f"{width}x{height}")

    
    def update_texts(self):

        """Actualiza los textos."""

        self.fullscreen_label.config(text=self.get_text('fullscreen'))
        self.windowed_btn.config(text=self.get_text('windowed'))
        self.fullscreen_btn.config(text=self.get_text('fullscreen'))
        self.resolution_label.config(text=self.get_text('resolution'))


class SoundTab(OptionsTab):

    """Pestaña de opciones de sonido."""
    

    def __init__(self, parent, app: 'ChessWithKaelithApp', **kwargs):
        super().__init__(parent, app, **kwargs)
        self._build_ui()
    

    def _build_ui(self):

        """Construye la UI de opciones de sonido."""

        # === VOLUMEN GENERAL ===
        self.general_slider = StyledSlider(
            self,
            label="Volumen general",
            from_=0,
            to=100,
            initial=self.app.settings.get("volume", 0.7) * 100,
            command=self._on_general_volume_change,
            width=280
        )
        self.general_slider.pack(fill=tk.X, pady=10, padx=10)
        

        # === VOLUMEN MÚSICA ===
        self.music_slider = StyledSlider(
            self,
            label="Música",
            from_=0,
            to=100,
            initial=self.app.settings.get("music_volume", 0.7) * 100,
            command=self._on_music_volume_change,
            width=280
        )
        self.music_slider.pack(fill=tk.X, pady=10, padx=10)
        

        # === VOLUMEN EFECTOS ===
        self.effects_slider = StyledSlider(
            self,
            label="Efectos",
            from_=0,
            to=100,
            initial=self.app.settings.get("effects_volume", 0.8) * 100,
            command=self._on_effects_volume_change,
            width=280
        )
        self.effects_slider.pack(fill=tk.X, pady=10, padx=10)
    

    # Controlar el volumen
    def _on_general_volume_change(self, value: float):
        self.app.settings.set("volume", value)


    def _on_music_volume_change(self, value: float):
        self.app.settings.set("music_volume", value)
    

    def _on_effects_volume_change(self, value: float):
        self.app.settings.set("effects_volume", value)
    

    def update_texts(self):

        """Actualiza los textos."""

        self.general_slider.set_label(self.get_text('general_volume'))
        self.music_slider.set_label(self.get_text('music_volume'))
        self.effects_slider.set_label(self.get_text('effects_volume'))


class AccessibilityTab(OptionsTab):

    """Pestaña de opciones de accesibilidad."""
    
    def __init__(self, parent, app: 'ChessWithKaelithApp', **kwargs):
        super().__init__(parent, app, **kwargs)
        self._build_ui()
    

    def _build_ui(self):

        """Construye la UI de opciones de accesibilidad."""

        # === TAMAÑO DE TEXTO ===
        text_size_frame = tk.Frame(self, bg='#2a3328')
        text_size_frame.pack(fill=tk.X, pady=10, padx=10)
        
        self.text_size_label = tk.Label(
            text_size_frame,
            text="Tamaño de texto",
            font=('Garamond', 13),
            fg='#c4a574',
            bg='#2a3328'
        )
        self.text_size_label.pack(side=tk.LEFT, padx=15, pady=12)
        

        # Botones de tamaño
        sizes_frame = tk.Frame(text_size_frame, bg='#2a3328')
        sizes_frame.pack(side=tk.RIGHT, padx=15, pady=10)
        
        self._text_size_var = tk.StringVar(
            value=self.app.settings.get("text_size", "medium")
        )
        
        self.size_buttons = {}
        for size in ['small', 'medium', 'large']:
            btn = tk.Label(
                sizes_frame,
                text=size.capitalize(),
                font=('Garamond', 11),
                bg='#3a4338',
                fg='#f5f0e6',
                padx=10,
                pady=6,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT)
            btn.bind('<Button-1>', lambda e, s=size: self._set_text_size(s))
            self.size_buttons[size] = btn
        
        self._update_text_size_buttons()
        

        # === ALTO CONTRASTE ===
        contrast_frame = tk.Frame(self, bg='#2a3328')
        contrast_frame.pack(fill=tk.X, pady=10, padx=10)
        

        self.contrast_label = tk.Label(
            contrast_frame,
            text="Alto contraste",
            font=('Garamond', 13),
            fg='#c4a574',
            bg='#2a3328'
        )
        self.contrast_label.pack(side=tk.LEFT, padx=15, pady=12)
        

        # Toggle de contraste
        toggle_frame = tk.Frame(contrast_frame, bg='#2a3328')
        toggle_frame.pack(side=tk.RIGHT, padx=15, pady=10)
        

        self._contrast_var = tk.BooleanVar(
            value=self.app.settings.get("high_contrast", False)
        )
        

        self.contrast_off_btn = tk.Label(
            toggle_frame,
            text="Off",
            font=('Garamond', 11),
            bg='#3a4338',
            fg='#f5f0e6',
            padx=12,
            pady=6,
            cursor='hand2'
        )
        self.contrast_off_btn.pack(side=tk.LEFT)
        

        self.contrast_on_btn = tk.Label(
            toggle_frame,
            text="On",
            font=('Garamond', 11),
            bg='#3a4338',
            fg='#f5f0e6',
            padx=12,
            pady=6,
            cursor='hand2'
        )
        self.contrast_on_btn.pack(side=tk.LEFT)
        

        self._update_contrast_toggle()
        

        self.contrast_off_btn.bind('<Button-1>', lambda e: self._set_contrast(False))
        self.contrast_on_btn.bind('<Button-1>', lambda e: self._set_contrast(True))
    

    def _update_text_size_buttons(self):

        """Actualiza el visual de los botones de tamaño."""

        current = self._text_size_var.get()
        for size, btn in self.size_buttons.items():
            btn.config(bg='#4a6741' if size == current else '#3a4338')
    

    def _set_text_size(self, size: str):

        """Establece el tamaño de texto."""

        self._text_size_var.set(size)
        self._update_text_size_buttons()
        self.app.settings.set("text_size", size)
    

    def _update_contrast_toggle(self):

        """Actualiza el toggle de contraste."""

        is_on = self._contrast_var.get()
        self.contrast_off_btn.config(bg='#4a6741' if not is_on else '#3a4338')
        self.contrast_on_btn.config(bg='#4a6741' if is_on else '#3a4338')
    

    def _set_contrast(self, enabled: bool):

        """Establece el alto contraste."""

        self._contrast_var.set(enabled)
        self._update_contrast_toggle()
        self.app.settings.set("high_contrast", enabled)
    

    def update_texts(self):

        """Actualiza los textos."""

        self.text_size_label.config(text=self.get_text('text_size'))
        self.contrast_label.config(text=self.get_text('high_contrast'))
        self.contrast_off_btn.config(text=self.get_text('off'))
        self.contrast_on_btn.config(text=self.get_text('on'))
        
        # Actualizar botones de tamaño
        for size, btn in self.size_buttons.items():
            btn.config(text=self.get_text(size))


class OptionsMenuScreen(BaseScreen):

    """
    Pantalla de opciones del juego.
    Organizada en pestañas: Video, Sonido, Accesibilidad.
    """
    

    def __init__(self, parent: tk.Widget, app: 'ChessWithKaelithApp', **kwargs):
        """Inicializa la pantalla de opciones."""
        self.tabs = {}
        self.tab_buttons = {}
        self._current_tab = 'video'
        super().__init__(parent, app, **kwargs)
    

    def _build_ui(self):

        """Construye la interfaz."""

        # Contenedor principal
        self.main_frame = SemiTransparentFrame(
            self,
            alpha=0.92,
            color='#1a2318'
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')
        

        inner = tk.Frame(self.main_frame, bg='#1a2318')
        inner.pack(padx=40, pady=30)
        

        # === TÍTULO ===
        self.title_label = tk.Label(
            inner,
            text="Opciones",
            font=('Palatino Linotype', 28, 'bold'),
            fg='#c4a574',
            bg='#1a2318'
        )
        self.title_label.pack(pady=(0, 20))
        

        # === PESTAÑAS ===
        tabs_frame = tk.Frame(inner, bg='#1a2318')
        tabs_frame.pack(fill=tk.X, pady=(0, 15))
        
        for tab_key in ['video', 'sound', 'accessibility']:
            btn = tk.Label(
                tabs_frame,
                text=tab_key.capitalize(),
                font=('Garamond', 12, 'bold'),
                bg='#2a3328',
                fg='#c4a574',
                padx=20,
                pady=10,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=2)
            btn.bind('<Button-1>', lambda e, k=tab_key: self._switch_tab(k))
            self.tab_buttons[tab_key] = btn
        

        # === CONTENEDOR DE CONTENIDO ===
        self.content_frame = tk.Frame(inner, bg='#1a2318', width=400, height=250)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        self.content_frame.pack_propagate(False)
        

        # Crear pestañas
        self.tabs['video'] = VideoTab(self.content_frame, self.app)
        self.tabs['sound'] = SoundTab(self.content_frame, self.app)
        self.tabs['accessibility'] = AccessibilityTab(self.content_frame, self.app)
        

        # Mostrar pestaña inicial
        self._switch_tab('video')
        

        # === SEPARADOR ===
        separator = tk.Frame(inner, bg='#4a6741', height=2)
        separator.pack(fill=tk.X, pady=20, padx=10)
        


        # === BOTONES ===
        buttons_frame = tk.Frame(inner, bg='#1a2318')
        buttons_frame.pack(fill=tk.X)


        # Botón Descartar (izquierda)
        self.discard_button = StyledButton(
            buttons_frame,
            text="Descartar",
            command=self._on_discard,
            width=150,
            height=45,
            font_size=12,
            primary=False
        )
        self.discard_button.pack(side=tk.LEFT, padx=5)
        

        # Botón Aplicar (centro-izquierda)
        self.apply_button = StyledButton(
            buttons_frame,
            text="Aplicar",
            command=self._on_apply,
            width=150,
            height=45,
            font_size=12,
            primary=True
        )
        self.apply_button.pack(side=tk.LEFT, padx=5)
        

        # Botón Volver (derecha)
        self.back_button = StyledButton(
            buttons_frame,
            text="Volver",
            command=self._on_back,
            width=150,
            height=50,
            font_size=14,
            primary=False
        )
        self.back_button.pack(side=tk.RIGHT, padx=5)
    

    def _switch_tab(self, tab_key: str):

        """Cambia a una pestaña específica."""

        # Ocultar todas las pestañas
        for tab in self.tabs.values():
            tab.pack_forget()
        

        # Mostrar la pestaña seleccionada
        self.tabs[tab_key].pack(fill=tk.BOTH, expand=True)
        self._current_tab = tab_key
        

        # Actualizar visual de botones
        for key, btn in self.tab_buttons.items():
            if key == tab_key:
                btn.config(bg='#4a6741', fg='#f5f0e6')
            else:
                btn.config(bg='#2a3328', fg='#c4a574')
    

    def _update_texts(self):

        """Actualiza los textos."""

        self.title_label.config(text=self.get_text('options'))
        self.discard_button.set_text(self.get_text('discard'))
        self.apply_button.set_text(self.get_text('apply'))
        self.back_button.set_text(self.get_text('back'))
        
        # Actualizar botones de pestañas
        self.tab_buttons['video'].config(text=self.get_text('video'))
        self.tab_buttons['sound'].config(text=self.get_text('sound'))
        self.tab_buttons['accessibility'].config(text=self.get_text('accessibility'))
        
        # Actualizar contenido de pestañas
        for tab in self.tabs.values():
            tab.update_texts()


    def _on_discard(self):

        """Descarta los cambios y recarga las opciones."""

        self.app.play_effect('button_discard')
        # Recargar configuración desde archivo
        self.app.settings._load()
        # Aplicar volúmenes guardados
        self.app.audio.set_master_volume(self.app.settings.get("volume", 0.7))
        self.app.audio.set_music_volume(self.app.settings.get("music_volume", 0.7))
        self.app.audio.set_effects_volume(self.app.settings.get("effects_volume", 0.8))
        # Recargar la pantalla
        self.navigate_to('options')


    def _on_apply(self):

        """Aplica y guarda los cambios."""

        self.app.play_effect('button_apply')
        self.app.settings.save()
    

    def _on_back(self):

        """Vuelve al menú principal."""
        
        self.app.play_effect('button_options')
        self.navigate_to('main_menu')

