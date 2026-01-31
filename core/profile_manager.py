"""
Chess with Kaelith - Profile Manager
Copyright (c) 2026 Fabián Hevia
All rights reserved.
=====================================
Gestiona la creación, almacenamiento y recuperación de perfiles de jugador.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class PlayerProfile:
    """Representa un perfil de jugador."""
    id: str
    nickname: str
    created_at: str
    last_played: str
    games_played: int = 0
    games_won: int = 0
    games_lost: int = 0
    games_draw: int = 0
    current_level: int = 1
    experience: int = 0
    
    @classmethod
    def create_new(cls, nickname: str) -> 'PlayerProfile':
        """Crea un nuevo perfil con valores iniciales."""
        now = datetime.now().isoformat()
        return cls(
            id=str(uuid.uuid4()),
            nickname=nickname,
            created_at=now,
            last_played=now,
        )
    
    def update_last_played(self):
        """Actualiza la fecha de última partida."""
        self.last_played = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convierte el perfil a diccionario."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PlayerProfile':
        """Crea un perfil desde un diccionario."""
        return cls(**data)
    
    @property
    def win_rate(self) -> float:
        """Calcula el porcentaje de victorias."""
        if self.games_played == 0:
            return 0.0
        return (self.games_won / self.games_played) * 100


class ProfileManager:
    """
    Gestor de perfiles de jugador.
    Maneja la persistencia y CRUD de perfiles.
    """
    
    MAX_PROFILES = 5  # Máximo número de perfiles permitidos
    
    def __init__(self, filepath: Path):
        """
        Inicializa el gestor de perfiles.
        
        Args:
            filepath: Ruta al archivo de perfiles
        """
        self.filepath = filepath
        self._profiles: Dict[str, PlayerProfile] = {}
        self._active_profile_id: Optional[str] = None
        self._load()
    
    def _load(self):
        """Carga los perfiles desde el archivo."""
        if self.filepath.exists():
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Cargar perfiles
                    profiles_data = data.get('profiles', {})
                    for profile_id, profile_data in profiles_data.items():
                        self._profiles[profile_id] = PlayerProfile.from_dict(profile_data)
                    
                    # Cargar perfil activo
                    self._active_profile_id = data.get('active_profile_id')
                    
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error cargando perfiles: {e}")
    
    def _save(self):
        """Guarda los perfiles en el archivo."""
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                'profiles': {
                    profile_id: profile.to_dict() 
                    for profile_id, profile in self._profiles.items()
                },
                'active_profile_id': self._active_profile_id
            }
            
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except IOError as e:
            print(f"Error guardando perfiles: {e}")
    
    def create_profile(self, nickname: str) -> Optional[PlayerProfile]:
        """
        Crea un nuevo perfil de jugador.
        
        Args:
            nickname: Apodo del jugador
            
        Returns:
            El nuevo perfil creado, o None si hay error
        """
        # Verificar límite de perfiles
        if len(self._profiles) >= self.MAX_PROFILES:
            return None
        
        # Verificar que el nickname no esté vacío
        nickname = nickname.strip()
        if not nickname:
            return None
        
        # Verificar que no exista un perfil con el mismo nombre
        for profile in self._profiles.values():
            if profile.nickname.lower() == nickname.lower():
                return None
        
        # Crear nuevo perfil
        profile = PlayerProfile.create_new(nickname)
        self._profiles[profile.id] = profile
        self._save()
        
        return profile
    
    def get_profile(self, profile_id: str) -> Optional[PlayerProfile]:
        """
        Obtiene un perfil por su ID.
        
        Args:
            profile_id: ID del perfil
            
        Returns:
            El perfil, o None si no existe
        """
        return self._profiles.get(profile_id)
    
    def get_all_profiles(self) -> List[PlayerProfile]:
        """
        Obtiene todos los perfiles ordenados por última partida.
        
        Returns:
            Lista de perfiles
        """
        return sorted(
            self._profiles.values(),
            key=lambda p: p.last_played,
            reverse=True
        )
    
    def delete_profile(self, profile_id: str) -> bool:
        """
        Elimina un perfil.
        
        Args:
            profile_id: ID del perfil a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        if profile_id in self._profiles:
            del self._profiles[profile_id]
            
            if self._active_profile_id == profile_id:
                self._active_profile_id = None
            
            self._save()
            return True
        return False
    
    def set_active_profile(self, profile_id: str) -> bool:
        """
        Establece el perfil activo.
        
        Args:
            profile_id: ID del perfil a activar
            
        Returns:
            True si se estableció, False si no existe el perfil
        """
        if profile_id in self._profiles:
            self._active_profile_id = profile_id
            self._profiles[profile_id].update_last_played()
            self._save()
            return True
        return False
    
    def get_active_profile(self) -> Optional[PlayerProfile]:
        """
        Obtiene el perfil activo.
        
        Returns:
            El perfil activo, o None si no hay
        """
        if self._active_profile_id:
            return self._profiles.get(self._active_profile_id)
        return None
    
    def update_profile(self, profile_id: str, **kwargs) -> bool:
        """
        Actualiza datos de un perfil.
        
        Args:
            profile_id: ID del perfil
            **kwargs: Campos a actualizar
            
        Returns:
            True si se actualizó, False si no existe
        """
        profile = self._profiles.get(profile_id)
        if profile:
            for key, value in kwargs.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            self._save()
            return True
        return False
    
    @property
    def profile_count(self) -> int:
        """Número de perfiles existentes."""
        return len(self._profiles)
    
    @property
    def can_create_profile(self) -> bool:
        """Indica si se pueden crear más perfiles."""
        return len(self._profiles) < self.MAX_PROFILES
