"""
Chess with Kaelith - UI Components
Copyright (c) 2026 Fabián Hevia
All rights reserved.
===================================
Componentes de interfaz reutilizables con estilo personalizado.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Tuple
from PIL import Image, ImageTk, ImageDraw, ImageFilter


class StyledButton(tk.Canvas):
    """
    Botón estilizado con efecto hover y diseño personalizado.
    Inspirado en la estética del bosque místico.
    """
    
    def __init__(
        self, 
        parent, 
        text: str,
        command: Optional[Callable] = None,
        width: int = 280,
        height: int = 60,
        font_size: int = 18,
        primary: bool = True,
        **kwargs
    ):
        """
        Crea un botón estilizado.
        
        Args:
            parent: Widget padre
            text: Texto del botón
            command: Función a ejecutar al hacer clic
            width: Ancho del botón
            height: Alto del botón
            font_size: Tamaño de la fuente
            primary: Si es botón primario (más destacado)
        """
        super().__init__(
            parent, 
            width=width, 
            height=height, 
            highlightthickness=0,
            **kwargs
        )
        
        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.font_size = font_size
        self.primary = primary
        
        # Estados
        self._is_hovered = False
        self._is_pressed = False
        self._is_enabled = True
        
        # Colores según tipo
        if primary:
            self.colors = {
                'bg': '#4a6741',
                'bg_hover': '#5a7751',
                'bg_pressed': '#3a5331',
                'border': '#6b8b5e',
                'text': '#f5f0e6',
                'shadow': '#1a2318',
            }
        else:
            self.colors = {
                'bg': '#3d4a38',
                'bg_hover': '#4d5a48',
                'bg_pressed': '#2d3a28',
                'border': '#5a6b55',
                'text': '#e5e0d6',
                'shadow': '#1a2318',
            }
        
        # Crear imagen del botón
        self._create_button_image()
        
        # Bindings
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)
    
    def _create_button_image(self):
        """Crea la imagen del botón con efectos."""
        # Determinar color según estado
        if not self._is_enabled:
            bg_color = '#555555'
            text_color = '#888888'
        elif self._is_pressed:
            bg_color = self.colors['bg_pressed']
            text_color = self.colors['text']
        elif self._is_hovered:
            bg_color = self.colors['bg_hover']
            text_color = self.colors['text']
        else:
            bg_color = self.colors['bg']
            text_color = self.colors['text']
        
        # Crear imagen base con transparencia
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Dibujar sombra
        shadow_offset = 3 if not self._is_pressed else 1
        draw.rounded_rectangle(
            [shadow_offset, shadow_offset, self.width - 2, self.height - 2],
            radius=12,
            fill=self.colors['shadow'] + '80'
        )
        
        # Dibujar fondo del botón
        y_offset = 2 if self._is_pressed else 0
        draw.rounded_rectangle(
            [2, y_offset, self.width - 4, self.height - 4 + y_offset],
            radius=10,
            fill=bg_color,
            outline=self.colors['border'],
            width=2
        )
        
        # Efecto de brillo en la parte superior
        if not self._is_pressed:
            for i in range(8):
                alpha = int(30 - i * 3)
                draw.line(
                    [(10 + i, 6 + i), (self.width - 12 - i, 6 + i)],
                    fill=f'#ffffff{alpha:02x}',
                    width=1
                )
        
        self._button_image = ImageTk.PhotoImage(img)
        
        # Limpiar y redibujar
        self.delete('all')
        self.create_image(0, 0, image=self._button_image, anchor='nw')
        
        # Añadir texto
        text_y = self.height // 2 + (2 if self._is_pressed else 0)
        self.create_text(
            self.width // 2,
            text_y,
            text=self.text,
            fill=text_color,
            font=('Garamond', self.font_size, 'bold'),
            anchor='center'
        )
    
    def _on_enter(self, event):
        """Maneja el evento de entrada del mouse."""
        if self._is_enabled:
            self._is_hovered = True
            self._create_button_image()
            self.configure(cursor='hand2')
    
    def _on_leave(self, event):
        """Maneja el evento de salida del mouse."""
        self._is_hovered = False
        self._is_pressed = False
        self._create_button_image()
        self.configure(cursor='')
    
    def _on_press(self, event):
        """Maneja el evento de presionar el botón."""
        if self._is_enabled:
            self._is_pressed = True
            self._create_button_image()
    
    def _on_release(self, event):
        """Maneja el evento de soltar el botón."""
        if self._is_enabled and self._is_pressed:
            self._is_pressed = False
            self._create_button_image()
            if self.command:
                self.command()
    
    def set_text(self, text: str):
        """Actualiza el texto del botón."""
        self.text = text
        self._create_button_image()
    
    def set_enabled(self, enabled: bool):
        """Habilita o deshabilita el botón."""
        self._is_enabled = enabled
        self._create_button_image()


class StyledSlider(tk.Frame):
    """
    Slider estilizado con etiqueta y valor.
    """
    
    def __init__(
        self,
        parent,
        label: str = "",
        from_: float = 0,
        to: float = 100,
        initial: float = 50,
        command: Optional[Callable[[float], None]] = None,
        show_value: bool = True,
        width: int = 300,
        **kwargs
    ):
        """
        Crea un slider estilizado.
        
        Args:
            parent: Widget padre
            label: Etiqueta del slider
            from_: Valor mínimo
            to: Valor máximo
            initial: Valor inicial
            command: Callback cuando cambia el valor
            show_value: Mostrar valor numérico
            width: Ancho del slider
        """
        super().__init__(parent, bg='#1a2318', **kwargs)
        
        self.command = command
        self.show_value = show_value
        self._value = tk.DoubleVar(value=initial)
        
        # Contenedor con fondo semi-transparente
        self.container = tk.Frame(self, bg='#2a3328')
        self.container.pack(fill=tk.X, padx=5, pady=5)
        
        # Etiqueta
        if label:
            self.label = tk.Label(
                self.container,
                text=label,
                font=('Garamond', 12),
                fg='#c4a574',
                bg='#2a3328',
                anchor='w'
            )
            self.label.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        # Frame para slider y valor
        slider_frame = tk.Frame(self.container, bg='#2a3328')
        slider_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Slider
        self.slider = ttk.Scale(
            slider_frame,
            from_=from_,
            to=to,
            variable=self._value,
            orient=tk.HORIZONTAL,
            command=self._on_change,
            length=width - 80 if show_value else width - 20
        )
        self.slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Valor numérico
        if show_value:
            self.value_label = tk.Label(
                slider_frame,
                text=f"{int(initial)}%",
                font=('Garamond', 11),
                fg='#f5f0e6',
                bg='#2a3328',
                width=5
            )
            self.value_label.pack(side=tk.RIGHT, padx=(10, 0))
    
    def _on_change(self, value):
        """Maneja el cambio de valor."""
        val = float(value)
        if self.show_value:
            self.value_label.config(text=f"{int(val)}%")
        if self.command:
            self.command(val / 100)  # Normalizar a 0-1
    
    def get(self) -> float:
        """Obtiene el valor actual (0-1)."""
        return self._value.get() / 100
    
    def set(self, value: float):
        """Establece el valor (0-1)."""
        self._value.set(value * 100)
        if self.show_value:
            self.value_label.config(text=f"{int(value * 100)}%")
    
    def set_label(self, text: str):
        """Actualiza la etiqueta."""
        if hasattr(self, 'label'):
            self.label.config(text=text)


class StyledEntry(tk.Frame):
    """
    Campo de entrada estilizado.
    """
    
    def __init__(
        self,
        parent,
        placeholder: str = "",
        width: int = 300,
        **kwargs
    ):
        """
        Crea un campo de entrada estilizado.
        
        Args:
            parent: Widget padre
            placeholder: Texto placeholder
            width: Ancho del campo
        """
        super().__init__(parent, bg='#2a3328', **kwargs)
        
        self.placeholder = placeholder
        self._has_placeholder = True
        
        # Contenedor con borde
        self.container = tk.Frame(
            self,
            bg='#3a4338',
            highlightbackground='#6b8b5e',
            highlightthickness=2,
            highlightcolor='#8bab7e'
        )
        self.container.pack(padx=2, pady=2)
        
        # Entry
        self.entry = tk.Entry(
            self.container,
            font=('Garamond', 14),
            bg='#3a4338',
            fg='#888888',
            insertbackground='#f5f0e6',
            relief=tk.FLAT,
            width=width // 10
        )
        self.entry.pack(padx=10, pady=8)
        
        # Insertar placeholder
        if placeholder:
            self.entry.insert(0, placeholder)
        
        # Bindings
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
    
    def _on_focus_in(self, event):
        """Maneja el foco."""
        if self._has_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg='#f5f0e6')
            self._has_placeholder = False
    
    def _on_focus_out(self, event):
        """Maneja la pérdida de foco."""
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg='#888888')
            self._has_placeholder = True
    
    def get(self) -> str:
        """Obtiene el texto."""
        if self._has_placeholder:
            return ""
        return self.entry.get()
    
    def set(self, text: str):
        """Establece el texto."""
        self._has_placeholder = False
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.entry.config(fg='#f5f0e6')
    
    def clear(self):
        """Limpia el campo."""
        self.entry.delete(0, tk.END)
        if self.placeholder:
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg='#888888')
            self._has_placeholder = True
    
    def set_placeholder(self, text: str):
        """Actualiza el placeholder."""
        self.placeholder = text
        if self._has_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, text)


class LanguageToggle(tk.Frame):
    """
    Toggle para cambio de idioma con banderas.
    """
    
    def __init__(
        self,
        parent,
        current_language: str = 'es',
        command: Optional[Callable[[str], None]] = None,
        **kwargs
    ):
        """
        Crea el toggle de idioma.
        
        Args:
            parent: Widget padre
            current_language: Idioma actual
            command: Callback al cambiar idioma
        """
        super().__init__(parent, bg='#1a2318', **kwargs)
        
        self.command = command
        self._current = current_language
        
        # Frame contenedor
        self.container = tk.Frame(self, bg='#2a3328')
        self.container.pack(padx=2, pady=2)
        
        # Botones de idioma
        self.es_btn = tk.Label(
            self.container,
            text="🇪🇸 ES",
            font=('Garamond', 11, 'bold'),
            bg='#4a6741' if current_language == 'es' else '#3a4338',
            fg='#f5f0e6',
            padx=12,
            pady=6,
            cursor='hand2'
        )
        self.es_btn.pack(side=tk.LEFT)
        
        self.en_btn = tk.Label(
            self.container,
            text="🇬🇧 EN",
            font=('Garamond', 11, 'bold'),
            bg='#4a6741' if current_language == 'en' else '#3a4338',
            fg='#f5f0e6',
            padx=12,
            pady=6,
            cursor='hand2'
        )
        self.en_btn.pack(side=tk.LEFT)
        
        # Bindings
        self.es_btn.bind('<Button-1>', lambda e: self._select('es'))
        self.en_btn.bind('<Button-1>', lambda e: self._select('en'))
    
    def _select(self, language: str):
        """Selecciona un idioma."""
        if language != self._current:
            self._current = language
            
            # Actualizar visual
            self.es_btn.config(bg='#4a6741' if language == 'es' else '#3a4338')
            self.en_btn.config(bg='#4a6741' if language == 'en' else '#3a4338')
            
            if self.command:
                self.command(language)
    
    def get(self) -> str:
        """Obtiene el idioma actual."""
        return self._current
    
    def set(self, language: str):
        """Establece el idioma."""
        self._select(language)


class SemiTransparentFrame(tk.Frame):
    """
    Frame con efecto de fondo semi-transparente.
    """
    
    def __init__(
        self,
        parent,
        alpha: float = 0.85,
        color: str = '#1a2318',
        **kwargs
    ):
        """
        Crea un frame semi-transparente.
        
        Args:
            parent: Widget padre
            alpha: Nivel de transparencia (0-1)
            color: Color base
        """
        # Simular transparencia con un color oscuro
        super().__init__(parent, bg=color, **kwargs)
        
        self.alpha = alpha
        self.base_color = color
