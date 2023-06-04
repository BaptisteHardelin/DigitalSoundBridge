"""
Ce script permet d'enregistrer du son à l'aide de PyAudio et de le sauvegarder dans un fichier WAV, 
tout en jouant le son en direct pendant l'enregistrement.
"""
from stream_params import StreamParams
from recorder import Recorder
import tkinter as tk
import sounddevice as sd

window = tk.Tk()
window.title("Sound Bridge")

def get_audio_devices():
    return sd.query_devices()

def get_default_input_device():
    return sd.default.device[0]  # Indice du périphérique d'entrée par défaut

def get_default_output_device():
    return sd.default.device[1]  # Indice du périphérique de sortie par défaut

def display_audio_devices():
    devices = get_audio_devices()
    default_input_device = get_default_input_device()
    default_output_device = get_default_output_device()

    label = tk.Label(window, text="Audio Devices")
    label.pack()

    for device in devices:
        device_info = f"{device['index']} "
        if device['index'] == default_input_device:
            device_info += "> "
        elif device['index'] == default_output_device:
            device_info += "< "
        device_info += f"{device['name']}, {device['hostapi']} ("
        device_info += f"{device['max_input_channels']} in, {device['max_output_channels']} out)"
        device_label = tk.Label(window, text=device_info, justify='left')
        device_label.pack(anchor='w')


if __name__ == "__main__":
    stream_params = StreamParams()
    recorder = Recorder(stream_params)
    recorder.start_recording(99999999999)

    display_audio_devices()
    window.mainloop()

    input("Appuyez sur Entrée pour arrêter l'enregistrement...")
    recorder.stop_recording()