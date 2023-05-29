import wave
import pyaudio
import threading
import numpy as np
from stream_params import StreamParams

class Recorder:
    def __init__(self, stream_params: StreamParams) -> None:
        self.stream_params = stream_params
        self._pyaudio = None
        self._stream = None
        self._wav_file = None
        self._stop_event = threading.Event()
        self._playback_pyaudio = pyaudio.PyAudio()
        self._playback_stream = None

    """
    Crée un flux de lecture PyAudio pour la lecture en direct du son enregistré.
    """
    def _create_playback_stream(self) -> None:
        self._playback_stream = self._playback_pyaudio.open(
            format=self.stream_params.format,
            channels=self.stream_params.channels,
            rate=self.stream_params.rate,
            output=True,
            output_device_index=self.stream_params.output_device_index
        )

    """
    Écrit les données audio sur le flux de lecture.
    """
    def _play_audio_data(self, audio_data) -> None:
        self._playback_stream.write(audio_data)

    """
    Lance l'enregistrement audio pour une durée donnée.
    Crée les ressources nécessaires.
    Le stream de lecture est écrit les données audio dans un fichier WAV
    """
    def record(self, duration: int) -> None:
        print("Start recording...")
        self._create_recording_resources()
        """
        Créer le stream de lecture
        """
        self._create_playback_stream()
        self._write_wav_file_reading_from_stream(duration)
        self._close_recording_resources()
        print("Stop recording")

    """
    Initialise les ressources PyAudio et le stream d'enregistrement.
    """
    def _create_recording_resources(self) -> None:
        self._pyaudio = pyaudio.PyAudio()
        self._stream = self._pyaudio.open(**self.stream_params.to_dict())
        self._create_wav_file()

    """
    Arrête les streams et ferme les ressources PyAudio.
    """
    def _close_recording_resources(self) -> None:
        self._stream.stop_stream()
        self._stream.close()
        self._pyaudio.terminate()
        self._playback_stream.stop_stream()
        self._playback_stream.close()
        self._playback_pyaudio.terminate()

    """
    Crée le fichier WAV de sortie avec les paramètres spécifiés.
    """
    def _create_wav_file(self):
        self._wav_file = wave.open("recording.wav", "wb")
        self._wav_file.setnchannels(self.stream_params.channels)
        self._wav_file.setsampwidth(self._pyaudio.get_sample_size(self.stream_params.format))
        self._wav_file.setframerate(self.stream_params.rate)

    """
    Lit les données audio à partir du stream d'enregistrement et les écrit dans le fichier WAV
    """
    def _write_wav_file_reading_from_stream(self, duration: int) -> None:
        while not self._stop_event.is_set():
            audio_data = self._stream.read(self.stream_params.frames_per_buffer)
            self._wav_file.writeframes(audio_data)
            """
            Jouer le son en direct
            """
            self._play_audio_data(audio_data)

    """
    Démarre un thread qui lance l'enregistrement pour une durée donnée.
    """
    def start_recording(self, duration: int) -> None:
        threading.Thread(target=self.record, args=(duration,), daemon=True).start()

    """
    Arrête l'enregistrement en définissant un événement d'arrêt.
    """
    def stop_recording(self) -> None:
        self._stop_event.set()