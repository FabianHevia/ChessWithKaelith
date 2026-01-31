"""
Chess with Kaelith - Profile Creation Screen
Copyright (c) 2026 Fabián Hevia
All rights reserved.
=============================================
Pantalla para crear nuevos perfiles de jugador.
"""

import tkinter as tk
from typing import TYPE_CHECKING

from ui.screens.base_screen import BaseScreen
from ui.components.widgets import StyledButton, StyledEntry, SemiTransparentFrame

if TYPE_CHECKING:
    from core.app import ChessWithKaelithApp


class ProfileCreateScreen(BaseScreen):

    """
    Pantalla de creación de nuevo perfil.
    Solicita un nickname único para el jugador.
    """
    
    def __init__(self, parent: tk.Widget, app: 'ChessWithKaelithApp', **kwargs):

        """Inicializa la pantalla de creación de perfil."""

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
        inner.pack(padx=50, pady=40)
        

        # === TÍTULO ===
        self.title_label = tk.Label(
            inner,
            text="Nuevo Perfil",
            font=('Palatino Linotype', 28, 'bold'),
            fg='#c4a574',
            bg='#1a2318'
        )
        self.title_label.pack(pady=(0, 10))

        
        # Icono decorativo
        icon_label = tk.Label(
            inner,
            text="✨ 👤 ✨",
            font=('Segoe UI Emoji', 32),
            bg='#1a2318'
        )
        icon_label.pack(pady=(0, 20))
        

        # === INSTRUCCIONES ===
        self.instruction_label = tk.Label(
            inner,
            text="Introduce tu apodo",
            font=('Garamond', 14),
            fg='#8b7355',
            bg='#1a2318'
        )
        self.instruction_label.pack(pady=(0, 15))
        

        # === CAMPO DE ENTRADA ===
        self.nickname_entry = StyledEntry(
            inner,
            placeholder="Escribe tu nombre...",
            width=300
        )
        self.nickname_entry.pack(pady=10)
        

        # Mensaje de error (oculto inicialmente)
        self.error_label = tk.Label(
            inner,
            text="",
            font=('Garamond', 11),
            fg='#cc4444',
            bg='#1a2318'
        )
        self.error_label.pack(pady=5)
        

        # === SEPARADOR ===
        separator = tk.Frame(inner, bg='#4a6741', height=2)
        separator.pack(fill=tk.X, pady=20, padx=10)
        

        # === BOTONES ===
        buttons_frame = tk.Frame(inner, bg='#1a2318')
        buttons_frame.pack(fill=tk.X)
        

        # Botón Crear
        self.create_button = StyledButton(
            buttons_frame,
            text="Crear",
            command=self._on_create,
            width=180,
            height=55,
            font_size=16,
            primary=True
        )
        self.create_button.pack(side=tk.LEFT, padx=10)
        

        # Botón Cancelar
        self.cancel_button = StyledButton(
            buttons_frame,
            text="Cancelar",
            command=self._on_cancel,
            width=150,
            height=50,
            font_size=14,
            primary=False
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=10)
        

        # Bind Enter key
        self.nickname_entry.entry.bind('<Return>', lambda e: self._on_create())
    

    def _update_texts(self):
        """Actualiza los textos."""
        self.title_label.config(text=self.get_text('new_profile'))
        self.instruction_label.config(text=self.get_text('enter_nickname'))
        self.nickname_entry.set_placeholder(self.get_text('nickname_placeholder'))
        self.create_button.set_text(self.get_text('create'))
        self.cancel_button.set_text(self.get_text('cancel'))

    
    def _show_error(self, message: str):
        """Muestra un mensaje de error."""
        self.error_label.config(text=message)

    
    def _clear_error(self):
        """Limpia el mensaje de error."""
        self.error_label.config(text="")

    
    def _on_create(self):
        """Maneja la creación del perfil."""
        self._clear_error()
        
        nickname = self.nickname_entry.get().strip()
        

        # Validar nickname
        if not nickname:
            self._show_error(self.get_text('nickname_empty'))
            return
        
        
        if len(nickname) > 20:
            nickname = nickname[:20]

        
        # Intentar crear perfil
        profile = self.app.profiles.create_profile(nickname)

        
        if profile is None:
            # Verificar si es por nombre duplicado o límite
            if not self.app.profiles.can_create_profile:
                self._show_error(self.get_text('profile_limit'))
            else:
                self._show_error(self.get_text('nickname_exists'))
            return
        
        
        # Éxito: establecer como activo y navegar
        self.app.profiles.set_active_profile(profile.id)
        self.navigate_to('profile_select')
        
    
    def _on_cancel(self):
        """Cancela y vuelve a selección de perfil."""
        self.navigate_to('profile_select')
