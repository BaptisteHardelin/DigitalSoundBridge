import pyaudio
from dataclasses import dataclass, asdict

"""
Contient les paramètres de flux audio.
"""
@dataclass
class StreamParams:
    format: int = pyaudio.paInt16
    channels: int = 1
    rate: int = 44100
    frames_per_buffer: int = 1024
    input: bool = True
    output: bool = True
    output_device_index: int = None

    def to_dict(self) -> dict:
        return asdict(self)
