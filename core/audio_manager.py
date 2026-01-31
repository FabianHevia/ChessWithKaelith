"""
Chess with Kaelith - Audio Manager
===================================
Motor de audio centralizado para el juego.
Gestiona música de fondo, playlists y efectos de sonido.
Mantiene estado persistente entre navegaciones de pantalla.
"""

import os
import random
from pathlib import Path
from typing import Dict, List, Optional, Callable, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from core.settings import SettingsManager

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


@dataclass
class Track:
    """Representa una pista de audio."""
    filename: str
    display_name: str
    path: Path
    category: str  # 'menu', 'battle', 'victory', etc.
    enabled: bool = True
    
    @classmethod
    def from_file(cls, filepath: Path, category: str) -> 'Track':
        """Crea un Track desde un archivo."""
        filename = filepath.name
        # Limpiar nombre para mostrar
        display_name = filename.rsplit('.', 1)[0]
        display_name = display_name.replace('_', ' ')
        display_name = display_name.replace('Chess With Kaelith - ', '')
        # Quitar sufijos como "(Main Menu Song)"
        if '(' in display_name:
            display_name = display_name.split('(')[0].strip()
        display_name = ' '.join(display_name.split())  # Normalizar espacios
        
        return cls(
            filename=filename,
            display_name=display_name,
            path=filepath,
            category=category
        )


@dataclass
class Playlist:
    """Lista de reproducción con orden configurable."""
    name: str
    tracks: List[Track] = field(default_factory=list)
    current_index: int = 0
    shuffle: bool = False
    repeat: bool = True
    _shuffled_order: List[int] = field(default_factory=list)
    
    def get_enabled_tracks(self) -> List[Track]:
        """Obtiene solo las pistas habilitadas."""
        return [t for t in self.tracks if t.enabled]
    
    def get_current_track(self) -> Optional[Track]:
        """Obtiene la pista actual."""
        enabled = self.get_enabled_tracks()
        if not enabled:
            return None
        
        if self.shuffle and self._shuffled_order:
            idx = self._shuffled_order[self.current_index % len(self._shuffled_order)]
            return enabled[idx] if idx < len(enabled) else enabled[0]
        
        return enabled[self.current_index % len(enabled)]
    
    def next_track(self) -> Optional[Track]:
        """Avanza a la siguiente pista."""
        enabled = self.get_enabled_tracks()
        if not enabled:
            return None
        
        self.current_index += 1
        
        if self.current_index >= len(enabled):
            if self.repeat:
                self.current_index = 0
                if self.shuffle:
                    self._reshuffle()
            else:
                return None
        
        return self.get_current_track()
    
    def previous_track(self) -> Optional[Track]:
        """Retrocede a la pista anterior."""
        enabled = self.get_enabled_tracks()
        if not enabled:
            return None
        
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(enabled) - 1
        
        return self.get_current_track()
    
    def _reshuffle(self):
        """Regenera el orden aleatorio."""
        enabled = self.get_enabled_tracks()
        if enabled:
            self._shuffled_order = list(range(len(enabled)))
            random.shuffle(self._shuffled_order)
    
    def set_shuffle(self, enabled: bool):
        """Activa/desactiva el modo aleatorio."""
        self.shuffle = enabled
        if enabled:
            self._reshuffle()


class AudioManager:
    """
    Motor de audio centralizado.
    
    Características:
    - Gestión de playlists por categoría (menú, batalla, etc.)
    - Estado persistente entre navegaciones
    - Detección automática de pistas
    - Configuración de playlist guardable
    - Efectos de sonido precargados
    """
    
    # Categorías de música soportadas
    CATEGORIES = {
        'menu': 'Main_Menu',
        'battle': 'Battle',
        'victory': 'Victory',
        'defeat': 'Defeat',
    }
    
    def __init__(self, assets_path: Path, settings: Optional['SettingsManager'] = None):
        """
        Inicializa el motor de audio.
        
        Args:
            assets_path: Ruta a la carpeta de assets
            settings: Gestor de configuraciones (opcional, para persistencia)
        """
        self.assets_path = assets_path
        self.audio_path = assets_path / "audio"
        self.settings = settings
        
        # Volúmenes (0.0 - 1.0)
        self._master_volume = 0.7
        self._music_volume = 0.7
        self._effects_volume = 0.8
        
        # Estado de reproducción
        self._current_category: Optional[str] = None
        self._current_track: Optional[Track] = None
        self._is_playing = False
        self._is_paused = False
        
        # Playlists por categoría
        self._playlists: Dict[str, Playlist] = {}
        
        # Cache de efectos de sonido
        self._effects_cache: Dict[str, 'pygame.mixer.Sound'] = {}
        
        # Callbacks para notificaciones
        self._on_track_change: List[Callable[[Track], None]] = []
        
        # Inicializar
        if AUDIO_AVAILABLE:
            self._scan_audio_files()
            self._load_sound_effects()
            self._load_playlist_settings()
    
    def _scan_audio_files(self):
        """Escanea la carpeta de audio y organiza las pistas por categoría."""
        if not self.audio_path.exists():
            return
        
        # Extensiones de audio soportadas
        audio_extensions = ('*.mp3', '*.ogg', '*.wav')
        
        for category, pattern in self.CATEGORIES.items():
            tracks = []
            # Buscar en todas las extensiones soportadas
            for ext in audio_extensions:
                for filepath in self.audio_path.glob(ext):
                    if pattern in filepath.name:
                        track = Track.from_file(filepath, category)
                        tracks.append(track)
            
            if tracks:
                self._playlists[category] = Playlist(name=category, tracks=tracks)
    
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
    
    def _load_playlist_settings(self):
        """Carga las preferencias de playlist desde settings."""
        if not self.settings:
            return
        
        playlist_config = self.settings.get("playlist_config", {})
        
        for category, config in playlist_config.items():
            if category in self._playlists:
                playlist = self._playlists[category]
                
                # Restaurar estado de habilitación de pistas
                enabled_tracks = config.get("enabled_tracks", [])
                if enabled_tracks:
                    for track in playlist.tracks:
                        track.enabled = track.filename in enabled_tracks
                
                # Restaurar orden
                track_order = config.get("track_order", [])
                if track_order:
                    ordered = []
                    remaining = list(playlist.tracks)
                    for filename in track_order:
                        for track in remaining:
                            if track.filename == filename:
                                ordered.append(track)
                                remaining.remove(track)
                                break
                    ordered.extend(remaining)
                    playlist.tracks = ordered
                
                playlist.shuffle = config.get("shuffle", False)
                playlist.repeat = config.get("repeat", True)
    
    def save_playlist_settings(self):
        """Guarda las preferencias de playlist en settings."""
        if not self.settings:
            return
        
        playlist_config = {}
        
        for category, playlist in self._playlists.items():
            playlist_config[category] = {
                "enabled_tracks": [t.filename for t in playlist.tracks if t.enabled],
                "track_order": [t.filename for t in playlist.tracks],
                "shuffle": playlist.shuffle,
                "repeat": playlist.repeat,
            }
        
        self.settings.set("playlist_config", playlist_config)
    
    # ==================== CONTROL DE VOLUMEN ====================
    
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
        if AUDIO_AVAILABLE and self._is_playing:
            effective_volume = self._master_volume * self._music_volume
            pygame.mixer.music.set_volume(effective_volume)
    
    def _get_effective_effects_volume(self) -> float:
        """Obtiene el volumen efectivo para efectos."""
        return self._master_volume * self._effects_volume
    
    # ==================== REPRODUCCIÓN DE MÚSICA ====================
    
    def request_music(self, category: str, force_restart: bool = False) -> Optional[str]:
        """
        Solicita reproducción de música de una categoría.
        
        ⚠️ NO reinicia si ya está reproduciéndose música de la misma categoría,
        a menos que force_restart sea True.
        
        Args:
            category: Categoría de música ('menu', 'battle', etc.)
            force_restart: Forzar reinicio aunque sea la misma categoría
            
        Returns:
            Nombre de la pista actual si hubo cambio, None si ya estaba sonando
        """
        if not AUDIO_AVAILABLE:
            return None
        
        # Si ya está reproduciéndose la misma categoría, NO hacer nada
        if (self._current_category == category and 
            self._is_playing and 
            not force_restart and
            pygame.mixer.music.get_busy()):
            return None  # Retorna None para indicar que NO hubo cambio
        
        # Cambiar a nueva categoría o forzar reinicio
        return self._start_playlist(category)
    
    def get_current_track_name(self) -> Optional[str]:
        """Obtiene el nombre de la pista actual sin iniciar música."""
        if self._current_track:
            return self._current_track.display_name
        return None
    
    def _start_playlist(self, category: str) -> Optional[str]:
        """Inicia la reproducción de una playlist."""
        if category not in self._playlists:
            return None
        
        playlist = self._playlists[category]
        
        # Si shuffle está activo, seleccionar pista aleatoria
        if playlist.shuffle:
            enabled = playlist.get_enabled_tracks()
            if enabled:
                playlist.current_index = random.randint(0, len(enabled) - 1)
        
        track = playlist.get_current_track()
        
        if not track:
            return None
        
        return self._play_track(track, category)
    
    def _play_track(self, track: Track, category: str, fade_ms: int = 2000) -> Optional[str]:
        """Reproduce una pista específica."""
        if not AUDIO_AVAILABLE or not track.path.exists():
            return None
        
        try:
            # Detener música actual con fade out si hay
            if self._is_playing and pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(300)
                pygame.time.wait(300)
            
            # Cargar y reproducir
            pygame.mixer.music.load(str(track.path))
            pygame.mixer.music.set_volume(self._master_volume * self._music_volume)
            pygame.mixer.music.play(loops=-1, fade_ms=fade_ms)  # loops=-1 para loop infinito
            
            # Actualizar estado
            self._current_category = category
            self._current_track = track
            self._is_playing = True
            self._is_paused = False
            
            # Notificar cambio de pista
            self._notify_track_change(track)
            
            return track.display_name
            
        except Exception as e:
            print(f"Error reproduciendo música: {e}")
            return None
    
    def play_next(self) -> Optional[str]:
        """Reproduce la siguiente pista de la playlist actual."""
        if not self._current_category:
            return None
        
        playlist = self._playlists.get(self._current_category)
        if not playlist:
            return None
        
        track = playlist.next_track()
        if track:
            return self._play_track(track, self._current_category, fade_ms=1000)
        return None
    
    def play_previous(self) -> Optional[str]:
        """Reproduce la pista anterior de la playlist actual."""
        if not self._current_category:
            return None
        
        playlist = self._playlists.get(self._current_category)
        if not playlist:
            return None
        
        track = playlist.previous_track()
        if track:
            return self._play_track(track, self._current_category, fade_ms=1000)
        return None
    
    def stop_music(self, fade_out_ms: int = 1000):
        """Detiene la música con fade out."""
        if AUDIO_AVAILABLE and self._is_playing:
            pygame.mixer.music.fadeout(fade_out_ms)
            self._is_playing = False
            self._is_paused = False
            self._current_track = None
            self._current_category = None
    
    def pause_music(self):
        """Pausa la música."""
        if AUDIO_AVAILABLE and self._is_playing and not self._is_paused:
            pygame.mixer.music.pause()
            self._is_paused = True
    
    def resume_music(self):
        """Reanuda la música pausada."""
        if AUDIO_AVAILABLE and self._is_paused:
            pygame.mixer.music.unpause()
            self._is_paused = False
    
    def toggle_pause(self):
        """Alterna entre pausa y reproducción."""
        if self._is_paused:
            self.resume_music()
        else:
            self.pause_music()
    
    # ==================== EFECTOS DE SONIDO ====================
    
    def play_effect(self, effect_name: str):
        """Reproduce un efecto de sonido."""
        if not AUDIO_AVAILABLE:
            return
        
        if effect_name in self._effects_cache:
            try:
                sound = self._effects_cache[effect_name]
                sound.set_volume(self._get_effective_effects_volume())
                sound.play()
            except Exception as e:
                print(f"Error reproduciendo efecto {effect_name}: {e}")
    
    # ==================== ESTADO Y QUERIES ====================
    
    def is_playing(self) -> bool:
        """Indica si hay música reproduciéndose."""
        if AUDIO_AVAILABLE:
            return pygame.mixer.music.get_busy() or self._is_paused
        return False
    
    def is_paused(self) -> bool:
        """Indica si la música está pausada."""
        return self._is_paused
    
    def get_current_track(self) -> Optional[Track]:
        """Obtiene la pista actual."""
        return self._current_track
    
    def get_current_category(self) -> Optional[str]:
        """Obtiene la categoría de música actual."""
        return self._current_category
    
    def get_playlist(self, category: str) -> Optional[Playlist]:
        """Obtiene una playlist por categoría."""
        return self._playlists.get(category)
    
    def get_available_categories(self) -> List[str]:
        """Obtiene las categorías con música disponible."""
        return list(self._playlists.keys())
    
    # ==================== CONFIGURACIÓN DE PLAYLIST ====================
    
    def set_track_enabled(self, category: str, filename: str, enabled: bool):
        """Habilita/deshabilita una pista en una playlist."""
        playlist = self._playlists.get(category)
        if playlist:
            for track in playlist.tracks:
                if track.filename == filename:
                    track.enabled = enabled
                    break
            self.save_playlist_settings()
    
    def reorder_tracks(self, category: str, new_order: List[str]):
        """Reordena las pistas de una playlist."""
        playlist = self._playlists.get(category)
        if playlist:
            ordered = []
            remaining = list(playlist.tracks)
            for filename in new_order:
                for track in remaining:
                    if track.filename == filename:
                        ordered.append(track)
                        remaining.remove(track)
                        break
            ordered.extend(remaining)
            playlist.tracks = ordered
            self.save_playlist_settings()
    
    def set_shuffle(self, category: str, enabled: bool):
        """Activa/desactiva modo aleatorio para una playlist."""
        playlist = self._playlists.get(category)
        if playlist:
            playlist.set_shuffle(enabled)
            self.save_playlist_settings()
    
    def set_repeat(self, category: str, enabled: bool):
        """Activa/desactiva repetición para una playlist."""
        playlist = self._playlists.get(category)
        if playlist:
            playlist.repeat = enabled
            self.save_playlist_settings()
    
    # ==================== CALLBACKS ====================
    
    def register_track_change_callback(self, callback: Callable[[Track], None]):
        """Registra un callback para cuando cambie la pista."""
        self._on_track_change.append(callback)
    
    def unregister_track_change_callback(self, callback: Callable[[Track], None]):
        """Elimina un callback de cambio de pista."""
        if callback in self._on_track_change:
            self._on_track_change.remove(callback)
    
    def _notify_track_change(self, track: Track):
        """Notifica a los callbacks de un cambio de pista."""
        for callback in self._on_track_change:
            try:
                callback(track)
            except Exception as e:
                print(f"Error en callback de cambio de pista: {e}")
    
    # ==================== LIMPIEZA ====================
    
    def cleanup(self):
        """Limpia recursos de audio."""
        if AUDIO_AVAILABLE:
            pygame.mixer.music.stop()
            pygame.mixer.quit()