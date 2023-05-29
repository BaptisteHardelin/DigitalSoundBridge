"""
Ce script permet d'enregistrer du son à l'aide de PyAudio et de le sauvegarder dans un fichier WAV, 
tout en jouant le son en direct pendant l'enregistrement.
"""
from stream_params import StreamParams
from recorder import Recorder
import tkinter as tk

window = tk.Tk()
window.title("Sound Bridge")


if __name__ == "__main__":
    stream_params = StreamParams()
    recorder = Recorder(stream_params)
    recorder.start_recording(99999999999)

    window.mainloop()

    input("Appuyez sur Entrée pour arrêter l'enregistrement...")
    recorder.stop_recording()
