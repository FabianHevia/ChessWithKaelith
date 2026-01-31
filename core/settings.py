"""
Chess with Kaelith - Settings Manager
Copyright (c) 2026 Fabián Hevia
All rights reserved.
======================================
Gestiona la persistencia de configuraciones de la aplicación.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


class SettingsManager:

    """
    Gestor de configuraciones del juego.
    Persiste en formato JSON.
    """
    
    # Valores por defecto
    DEFAULTS = {
        "language": "es",
        "volume": 0.7,
        "music_volume": 0.7,
        "effects_volume": 0.8,
        "fullscreen": False,
        "resolution": "1280x720",
        "text_size": "medium",
        "high_contrast": False,
    }
    
    def __init__(self, filepath: Path):

        """
        Inicializa el gestor de configuraciones.
        
        Args:
            filepath: Ruta al archivo de configuración
        """
        self.filepath = filepath
        self._settings: Dict[str, Any] = {}
        self._load()
    

    def _load(self):

        """Carga las configuraciones desde el archivo."""

        if self.filepath.exists():
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self._settings = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error cargando configuración: {e}")
                self._settings = {}
        

        # Aplicar valores por defecto para claves faltantes
        for key, default_value in self.DEFAULTS.items():
            if key not in self._settings:
                self._settings[key] = default_value
    

    def save(self):

        """Guarda las configuraciones en el archivo."""

        try:
            # Asegurar que el directorio existe
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error guardando configuración: {e}")
    

    def get(self, key: str, default: Any = None) -> Any:

        """
        Obtiene un valor de configuración.
        
        Args:
            key: Clave de la configuración
            default: Valor por defecto si no existe
            
        Returns:
            Valor de la configuración
        """

        return self._settings.get(key, default if default is not None else self.DEFAULTS.get(key))
    

    def set(self, key: str, value: Any):

        """
        Establece un valor de configuración.
        
        Args:
            key: Clave de la configuración
            value: Nuevo valor
        """

        self._settings[key] = value
        self.save()  # Auto-guardar
    
    def reset(self, key: Optional[str] = None):

        """
        Resetea configuraciones a valores por defecto.
        
        Args:
            key: Clave específica a resetear, o None para resetear todo
        """

        if key is not None:
            if key in self.DEFAULTS:
                self._settings[key] = self.DEFAULTS[key]
        else:
            self._settings = self.DEFAULTS.copy()
        self.save()
    
    def get_all(self) -> Dict[str, Any]:

        """
        Obtiene todas las configuraciones.
        
        Returns:
            Diccionario con todas las configuraciones
        """
        
        return self._settings.copy()
