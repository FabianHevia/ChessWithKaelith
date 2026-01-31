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
    Incluye soporte para background de imagen.
    """
    
    # Color de fondo por defecto (oscuro)
    BG_COLOR = '#1a2318'
    
    def __init__(self, parent: tk.Widget, app: 'ChessWithKaelithApp', **kwargs):
        """
        Inicializa la pantalla base.
        
        Args:
            parent: Widget padre
            app: Referencia a la aplicación principal
        """
        super().__init__(parent, bg=self.BG_COLOR, **kwargs)
        
        self.app = app
        self.parent = parent
        
        # Referencia al background propio de esta pantalla
        self._screen_bg_label = None
        self._screen_bg_photo = None
        self._bg_initialized = False
        
        # Crear el label del background PRIMERO (pero sin imagen aún)
        self._create_background_label()
        
        # Registrar callback de idioma
        self.app.register_language_callback(self._on_language_change)
        
        # Construir UI (los widgets se crearán encima del background label)
        self._build_ui()
        
        # DESPUÉS de construir la UI, enviar el background al fondo
        # y actualizar la imagen
        self._finalize_background()
        
        # Bind para actualizar background al redimensionar
        self.bind('<Configure>', self._on_screen_resize)
        
        # Actualizar textos
        self._update_texts()
    
    def _create_background_label(self):
        """Crea el label que contendrá la imagen de fondo."""
        self._screen_bg_label = tk.Label(self, bg=self.BG_COLOR, bd=0, highlightthickness=0)
        self._screen_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    def _finalize_background(self):
        """Finaliza la configuración del background después de crear la UI."""
        # Enviar el background label a la capa más baja (detrás de todo)
        self._screen_bg_label.lower()
        
        # Programar la actualización de la imagen
        # Usamos un delay más largo para asegurar que el widget tenga tamaño
        self.after(150, self._update_screen_background)
    
    def _update_screen_background(self):
        """Actualiza la imagen de fondo de esta pantalla."""
        # Verificar que la imagen original existe
        if not hasattr(self.app, '_original_bg') or self.app._original_bg is None:
            print("DEBUG: _original_bg no disponible")
            return
        
        # Verificar que el label existe
        if self._screen_bg_label is None:
            print("DEBUG: _screen_bg_label no existe")
            return
        
        try:
            # Obtener dimensiones actuales
            width = self.winfo_width()
            height = self.winfo_height()
            
            # Si el widget aún no tiene tamaño, reintentar
            if width < 10 or height < 10:
                self.after(100, self._update_screen_background)
                return
            
            # Importar PIL
            from PIL import Image, ImageTk
            
            # Obtener la imagen original
            img = self.app._original_bg
            
            # Calcular dimensiones manteniendo aspecto (modo "cover")
            img_ratio = img.width / img.height
            win_ratio = width / height
            
            if win_ratio > img_ratio:
                # Ventana más ancha que imagen
                new_width = width
                new_height = int(width / img_ratio)
            else:
                # Ventana más alta que imagen
                new_height = height
                new_width = int(height * img_ratio)
            
            # Redimensionar imagen
            resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Centrar y recortar para cubrir exactamente el área
            left = (new_width - width) // 2
            top = (new_height - height) // 2
            cropped = resized.crop((left, top, left + width, top + height))
            
            # Crear PhotoImage (IMPORTANTE: mantener referencia para evitar GC)
            self._screen_bg_photo = ImageTk.PhotoImage(cropped)
            
            # Actualizar el label con la imagen
            self._screen_bg_label.configure(image=self._screen_bg_photo)
            
            # Marcar como inicializado
            self._bg_initialized = True
            
        except Exception as e:
            print(f"Error actualizando background de pantalla: {e}")
            import traceback
            traceback.print_exc()
    
    def _on_screen_resize(self, event):
        """Maneja el redimensionamiento de la pantalla."""
        # Solo procesar eventos de este widget
        if event.widget != self:
            return
        
        # Actualizar background con debounce (evitar múltiples llamadas)
        if hasattr(self, '_resize_timer'):
            try:
                self.after_cancel(self._resize_timer)
            except:
                pass
        
        self._resize_timer = self.after(100, self._update_screen_background)
    
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
        # Cancelar timer de resize si existe
        if hasattr(self, '_resize_timer'):
            try:
                self.after_cancel(self._resize_timer)
            except:
                pass
        
        # Limpiar referencia de imagen
        self._screen_bg_photo = None
        
        # Desregistrar callback de idioma
        try:
            self.app.unregister_language_callback(self._on_language_change)
        except:
            pass
        
        super().destroy()