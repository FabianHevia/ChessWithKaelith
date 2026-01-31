"""
Chess with Kaelith - Audio Manager
Copyright (c) 2026 Fabián Hevia
All rights reserved.
===================================
Gestiona la reproducción de música y efectos de sonido.
Usa pygame.mixer para audio no bloqueante.
"""

import os
from pathlib import Path
from typing import Dict, Optional, Callable
import threading

# Intentar importar pygame para audio
try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
    import pygame
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️ pygame no disponible - audio deshabilitado")
except Exception as e:
    AUDIO_AVAILABLE = False
    print(f"⚠️ Error inicializando audio: {e}")


class AudioManager:
    """
    Gestor centralizado de audio.
    Maneja música de fondo y efectos de sonido.
    """
    
    def __init__(self, assets_path: Path):
        """
        Inicializa el gestor de audio.
        
        Args:
            assets_path: Ruta a la carpeta de assets
        """
        self.assets_path = assets_path
        self.audio_path = assets_path / "audio"
        
        # Volúmenes (0.0 - 1.0)
        self._master_volume = 0.7
        self._music_volume = 0.7
        self._effects_volume = 0.8
        
        # Cache de efectos de sonido
        self._effects_cache: Dict[str, 'pygame.mixer.Sound'] = {}
        
        # Estado de la música
        self._current_music: Optional[str] = None
        self._music_playing = False
        
        # Callback para cuando termine la música (opcional)
        self._on_music_end: Optional[Callable] = None
        
        # Cargar efectos de sonido
        if AUDIO_AVAILABLE:
            self._load_sound_effects()
    
    def _load_sound_effects(self):
        """Precarga los efectos de sonido en memoria."""
        if not AUDIO_AVAILABLE:
            return
        
        effects = {
            'button_play': 'Efecto_de_Sonido_Boton_Jugar.mp3',
            'button_options': 'Efecto_Sonido_Opciones_y_Cambiar_Lenguaje.mp3',
            'button_language': 'Efecto_Sonido_Opciones_y_Cambiar_Lenguaje.mp3',
            'button_apply': 'Efecto_de_Sonido_Boton_Aplicar_Cambios.mp3',
            'button_discard': 'Efecto_de_Sonido_Descartar_Cambios_En_Opciones.mp3',
        }
        
        for effect_name, filename in effects.items():
            filepath = self.audio_path / filename
            if filepath.exists():
                try:
                    self._effects_cache[effect_name] = pygame.mixer.Sound(str(filepath))
                except Exception as e:
                    print(f"Error cargando efecto {effect_name}: {e}")
    
    def set_master_volume(self, volume: float):
        """Establece el volumen maestro (0.0 - 1.0)."""
        self._master_volume = max(0.0, min(1.0, volume))
        self._apply_music_volume()
    
    def set_music_volume(self, volume: float):
        """Establece el volumen de música (0.0 - 1.0)."""
        self._music_volume = max(0.0, min(1.0, volume))
        self._apply_music_volume()
    
    def set_effects_volume(self, volume: float):
        """Establece el volumen de efectos (0.0 - 1.0)."""
        self._effects_volume = max(0.0, min(1.0, volume))
    
    def _apply_music_volume(self):
        """Aplica el volumen actual a la música."""
        if AUDIO_AVAILABLE and self._music_playing:
            effective_volume = self._master_volume * self._music_volume
            pygame.mixer.music.set_volume(effective_volume)
    
    def _get_effective_effects_volume(self) -> float:
        """Obtiene el volumen efectivo para efectos."""
        return self._master_volume * self._effects_volume
    
    def play_music(self, music_name: str, loop: bool = True, fade_in_ms: int = 2000) -> str:
        """
        Reproduce música de fondo.
        
        Args:
            music_name: Nombre del archivo de música (sin ruta)
            loop: Si debe repetirse
            fade_in_ms: Milisegundos de fade in
            
        Returns:
            Nombre limpio de la canción para mostrar
        """
        if not AUDIO_AVAILABLE:
            return ""
        
        filepath = self.audio_path / music_name
        if not filepath.exists():
            print(f"Archivo de música no encontrado: {filepath}")
            return ""
        
        try:
            # Detener música actual si hay
            if self._music_playing:
                pygame.mixer.music.fadeout(500)
            
            # Cargar y reproducir
            pygame.mixer.music.load(str(filepath))
            pygame.mixer.music.set_volume(self._master_volume * self._music_volume)
            
            loops = -1 if loop else 0
            pygame.mixer.music.play(loops=loops, fade_ms=fade_in_ms)
            
            self._current_music = music_name
            self._music_playing = True
            
            # Retornar nombre limpio para mostrar
            return self._get_clean_song_name(music_name)
            
        except Exception as e:
            print(f"Error reproduciendo música: {e}")
            return ""
    
    def _get_clean_song_name(self, filename: str) -> str:
        """Obtiene un nombre limpio de la canción para mostrar."""
        # Quitar extensión
        name = filename.rsplit('.', 1)[0]
        # Limpiar formato del nombre
        name = name.replace('_', ' ')
        name = name.replace('Chess With Kaelith - ', '')
        name = name.replace('  ', ' ')
        # Quitar paréntesis extra
        if '(' in name:
            name = name.split('(')[0].strip()
        return name.strip()
    
    def stop_music(self, fade_out_ms: int = 1000):
        """Detiene la música con fade out."""
        if AUDIO_AVAILABLE and self._music_playing:
            pygame.mixer.music.fadeout(fade_out_ms)
            self._music_playing = False
            self._current_music = None
    
    def pause_music(self):
        """Pausa la música."""
        if AUDIO_AVAILABLE and self._music_playing:
            pygame.mixer.music.pause()
    
    def resume_music(self):
        """Reanuda la música pausada."""
        if AUDIO_AVAILABLE and self._music_playing:
            pygame.mixer.music.unpause()
    
    def play_effect(self, effect_name: str):
        """
        Reproduce un efecto de sonido.
        
        Args:
            effect_name: Nombre del efecto ('button_play', 'button_options', etc.)
        """
        if not AUDIO_AVAILABLE:
            return
        
        if effect_name in self._effects_cache:
            try:
                sound = self._effects_cache[effect_name]
                sound.set_volume(self._get_effective_effects_volume())
                sound.play()
            except Exception as e:
                print(f"Error reproduciendo efecto {effect_name}: {e}")
    
    def is_music_playing(self) -> bool:
        """Indica si hay música reproduciéndose."""
        if AUDIO_AVAILABLE:
            return pygame.mixer.music.get_busy()
        return False
    
    def get_current_music(self) -> Optional[str]:
        """Obtiene el nombre de la música actual."""
        return self._current_music
    
    def cleanup(self):
        """Limpia recursos de audio."""
        if AUDIO_AVAILABLE:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
