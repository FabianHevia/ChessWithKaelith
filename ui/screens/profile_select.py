"""
Chess with Kaelith - Profile Selection Screen
Copyright (c) 2026 Fabián Hevia
All rights reserved.
==============================================
Pantalla para seleccionar o crear perfiles de jugador.
"""

import tkinter as tk
from tkinter import messagebox
from typing import TYPE_CHECKING, Optional

from ui.screens.base_screen import BaseScreen
from ui.components.widgets import StyledButton, SemiTransparentFrame
from core.profile_manager import PlayerProfile

if TYPE_CHECKING:
    from core.app import ChessWithKaelithApp


class ProfileCard(tk.Frame):

    """
    Tarjeta visual para mostrar un perfil de jugador.
    """
    
    def __init__(
        self,
        parent,
        profile: PlayerProfile,
        on_select=None,
        on_delete=None,
        texts: dict = None,
        **kwargs
    ):
        
        """
        Crea una tarjeta de perfil.
        
        Args:
            parent: Widget padre
            profile: Datos del perfil
            on_select: Callback al seleccionar
            on_delete: Callback al eliminar
            texts: Diccionario de textos traducidos
        """

        super().__init__(parent, bg='#2a3328', **kwargs)
        
        self.profile = profile
        self.on_select = on_select
        self.on_delete = on_delete
        self.texts = texts or {}
        
        self._is_hovered = False
        self._build_ui()
        
        # Bindings
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)
    

    def _build_ui(self):

        """Construye la UI de la tarjeta."""
        # Marco con borde
        self.configure(
            highlightbackground='#4a6741',
            highlightthickness=2,
            highlightcolor='#6b8b5e'
        )
        

        # Contenedor interno
        inner = tk.Frame(self, bg='#2a3328')
        inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        

        # Fila superior: Nombre y nivel
        top_row = tk.Frame(inner, bg='#2a3328')
        top_row.pack(fill=tk.X)
        

        # Icono de perfil
        icon_label = tk.Label(
            top_row,
            text="👤",
            font=('Segoe UI Emoji', 24),
            bg='#2a3328',
            fg='#c4a574'
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        

        # Info del perfil
        info_frame = tk.Frame(top_row, bg='#2a3328')
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        

        # Nickname
        self.name_label = tk.Label(
            info_frame,
            text=self.profile.nickname,
            font=('Garamond', 16, 'bold'),
            fg='#f5f0e6',
            bg='#2a3328',
            anchor='w'
        )
        self.name_label.pack(fill=tk.X)
        

        # Estadísticas
        level_text = self.texts.get('level', 'Nivel')
        stats_text = f"{level_text} {self.profile.current_level}"
        self.stats_label = tk.Label(
            info_frame,
            text=stats_text,
            font=('Garamond', 11),
            fg='#8b7355',
            bg='#2a3328',
            anchor='w'
        )
        self.stats_label.pack(fill=tk.X)
        

        # Botón eliminar
        self.delete_btn = tk.Label(
            top_row,
            text="✕",
            font=('Arial', 14, 'bold'),
            fg='#666666',
            bg='#2a3328',
            cursor='hand2'
        )
        self.delete_btn.pack(side=tk.RIGHT, padx=5)
        self.delete_btn.bind('<Button-1>', self._on_delete_click)
        self.delete_btn.bind('<Enter>', lambda e: self.delete_btn.config(fg='#cc4444'))
        self.delete_btn.bind('<Leave>', lambda e: self.delete_btn.config(fg='#666666'))
        

        # Fila inferior: Partidas
        bottom_row = tk.Frame(inner, bg='#2a3328')
        bottom_row.pack(fill=tk.X, pady=(8, 0))
        

        games_text = self.texts.get('games_played', 'Partidas')
        wins_text = self.texts.get('wins', 'Victorias')
        

        games_label = tk.Label(
            bottom_row,
            text=f"🎮 {games_text}: {self.profile.games_played}",
            font=('Garamond', 10),
            fg='#6b8b5e',
            bg='#2a3328'
        )
        games_label.pack(side=tk.LEFT)
        

        wins_label = tk.Label(
            bottom_row,
            text=f"🏆 {wins_text}: {self.profile.games_won}",
            font=('Garamond', 10),
            fg='#c4a574',
            bg='#2a3328'
        )
        wins_label.pack(side=tk.RIGHT)
        

        # Hacer que los labels internos también disparen el evento
        for widget in [inner, top_row, info_frame, self.name_label, 
                       self.stats_label, bottom_row, games_label, wins_label, icon_label]:
            widget.bind('<Enter>', self._on_enter)
            widget.bind('<Leave>', self._on_leave)
            widget.bind('<Button-1>', self._on_click)
    

    def _on_enter(self, event):
        """Hover enter."""
        self._is_hovered = True
        self.configure(highlightbackground='#6b8b5e')
        self.configure(cursor='hand2')
    

    def _on_leave(self, event):
        """Hover leave."""
        self._is_hovered = False
        self.configure(highlightbackground='#4a6741')
        self.configure(cursor='')
    

    def _on_click(self, event):
        """Click en la tarjeta."""
        if self.on_select:
            self.on_select(self.profile)
    

    def _on_delete_click(self, event):
        """Click en eliminar."""
        event.widget.master.master.master  # Stop propagation
        if self.on_delete:
            self.on_delete(self.profile)
        return "break"
    

    def update_texts(self, texts: dict):
        """Actualiza los textos."""
        self.texts = texts
        level_text = self.texts.get('level', 'Nivel')
        self.stats_label.config(text=f"{level_text} {self.profile.current_level}")


class ProfileSelectScreen(BaseScreen):

    """
    Pantalla de selección de perfil.
    Permite seleccionar un perfil existente o crear uno nuevo.
    """
    

    def __init__(self, parent: tk.Widget, app: 'ChessWithKaelithApp', **kwargs):
        """Inicializa la pantalla de selección de perfil."""
        self.profile_cards = []
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
            text="Seleccionar Perfil",
            font=('Palatino Linotype', 28, 'bold'),
            fg='#c4a574',
            bg='#1a2318'
        )
        self.title_label.pack(pady=(0, 25))
        

        # === CONTENEDOR DE PERFILES ===
        self.profiles_frame = tk.Frame(inner, bg='#1a2318')
        self.profiles_frame.pack(fill=tk.BOTH, expand=True)
        

        # Cargar perfiles
        self._load_profiles()
        

        # === SEPARADOR ===
        separator = tk.Frame(inner, bg='#4a6741', height=2)
        separator.pack(fill=tk.X, pady=20, padx=10)
        

        # === BOTONES ===
        buttons_frame = tk.Frame(inner, bg='#1a2318')
        buttons_frame.pack(fill=tk.X)
        

        # Botón Crear Nuevo
        self.create_button = StyledButton(
            buttons_frame,
            text="Crear Perfil",
            command=self._on_create_profile,
            width=220,
            height=50,
            font_size=14,
            primary=True
        )
        self.create_button.pack(side=tk.LEFT, padx=5)
        

        # Botón Volver
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

    
    def _load_profiles(self):

        """Carga y muestra los perfiles existentes."""

        # Limpiar tarjetas existentes
        for card in self.profile_cards:
            card.destroy()
        self.profile_cards.clear()
        
        # Limpiar contenedor
        for widget in self.profiles_frame.winfo_children():
            widget.destroy()
        
        profiles = self.app.profiles.get_all_profiles()
        
        if not profiles:
            # Mensaje si no hay perfiles
            self.no_profiles_label = tk.Label(
                self.profiles_frame,
                text=self.get_text('no_profiles'),
                font=('Garamond', 14),
                fg='#8b7355',
                bg='#1a2318',
                pady=30
            )
            self.no_profiles_label.pack()

        else:
            # Mostrar perfiles
            texts = {
                'level': self.get_text('level'),
                'games_played': self.get_text('games_played'),
                'wins': self.get_text('wins'),
            }
            
            for profile in profiles:
                card = ProfileCard(
                    self.profiles_frame,
                    profile=profile,
                    on_select=self._on_profile_select,
                    on_delete=self._on_profile_delete,
                    texts=texts
                )
                card.pack(fill=tk.X, pady=6, padx=5)
                self.profile_cards.append(card)
        

        # Actualizar estado del botón crear
        if not self.app.profiles.can_create_profile:
            self.create_button.set_enabled(False)
    

    def _update_texts(self):

        """Actualiza los textos."""

        self.title_label.config(text=self.get_text('select_profile'))
        self.create_button.set_text(self.get_text('create_profile'))
        self.back_button.set_text(self.get_text('back'))

        
        # Actualizar mensaje si no hay perfiles
        if hasattr(self, 'no_profiles_label'):
            self.no_profiles_label.config(text=self.get_text('no_profiles'))
        
        # Actualizar tarjetas
        texts = {
            'level': self.get_text('level'),
            'games_played': self.get_text('games_played'),
            'wins': self.get_text('wins'),
        }
        for card in self.profile_cards:
            card.update_texts(texts)
    

    def _on_profile_select(self, profile: PlayerProfile):
        """Maneja la selección de un perfil."""
        self.app.profiles.set_active_profile(profile.id)
        # Aquí navegaríamos a la pantalla de juego
        # Por ahora, mostramos mensaje de confirmación
        print(f"Perfil seleccionado: {profile.nickname}")
        # TODO: self.navigate_to('game_lobby')

    
    def _on_profile_delete(self, profile: PlayerProfile):
        """Maneja la eliminación de un perfil."""
        # Confirmar eliminación
        confirm = messagebox.askyesno(
            self.get_text('delete'),
            f"{self.get_text('confirm_delete')}\n\n{profile.nickname}",
            parent=self
        )
        
        if confirm:
            self.app.profiles.delete_profile(profile.id)
            self._load_profiles()

    
    def _on_create_profile(self):
        """Navega a la creación de perfil."""
        self.navigate_to('profile_create')
        
    
    def _on_back(self):
        """Vuelve al menú principal."""
        self.navigate_to('main_menu')
