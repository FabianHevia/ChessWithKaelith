"""
Chess with Kaelith - Base Screen
Copyright (c) 2026 Fabián Hevia
All rights reserved.
=================================
Clase base para todas las pantallas de la aplicación.
"""

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.app import ChessWithKaelithApp


class BaseScreen(tk.Frame):

    """
    Clase base para todas las pantallas.
    Proporciona funcionalidad común y acceso a la aplicación.
    """
    
    def __init__(self, parent: tk.Widget, app: 'ChessWithKaelithApp', **kwargs):

        """
        Inicializa la pantalla base.
        
        Args:
            parent: Widget padre
            app: Referencia a la aplicación principal
        """

        super().__init__(parent, bg='#1a2318', **kwargs)
        
        self.app = app
        self.parent = parent
        
        # Frame transparente para mostrar el background
        
        # Registrar callback de idioma
        self.app.register_language_callback(self._on_language_change)
        
        # Construir UI
        self._build_ui()
        
        # Actualizar textos
        self._update_texts()
    

    def _build_ui(self):

        """
        Construye la interfaz de usuario.
        Debe ser sobrescrito por las subclases.
        """

        pass
    

    def _update_texts(self):

        """
        Actualiza todos los textos con las traducciones actuales.
        Debe ser sobrescrito por las subclases.
        """

        pass
    

    def _on_language_change(self):

        """Callback cuando cambia el idioma."""
        self._update_texts()

    
    def get_text(self, key: str) -> str:

        """
        Obtiene un texto traducido.
        
        Args:
            key: Clave del texto
            
        Returns:
            Texto traducido
        """

        return self.app.get_text(key)
    
    
    def navigate_to(self, screen_name: str, **kwargs):

        """
        Navega a otra pantalla.
        
        Args:
            screen_name: Nombre de la pantalla destino
            **kwargs: Argumentos adicionales
        """

        self.app.navigate_to(screen_name, **kwargs)

    
    def destroy(self):

        """Destruye la pantalla y limpia recursos."""
        
        # Desregistrar callback de idioma
        self.app.unregister_language_callback(self._on_language_change)
        super().destroy()
       
