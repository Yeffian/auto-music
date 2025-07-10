from music21 import stream, note, scale, meter
import random
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk
from markov import RhthymController



def generate_markov_melody_with_phrases(
        tonic='C',
        scaleType=scale.MajorScale,
        num_notes=16,
        start_octave=4,
        octave_range=1,
        phrase_length_bars=2
):
    beat_probabilities = {
        1: {0.5: 0.45, 0.25: 0.4, 1: 0.1, -1: 0.05},
        0.5: {0.25: 0.4, 0.5: 0.25, 1: 0.15, -1: 0.2},
        0.25: {0.25: 0.5, 0.5: 0.25, 1: 0.05, -1: 0.2},
        -1: {0.25: 0.5, 0.5: 0.3, 1: 0.1, -1: 0.1}
    }
    beat_chain = RhthymController(beat_probabilities)
    beat_sequence = beat_chain.produce_complete(num_notes)

    sc = scaleType(tonic)
    scale_notes = []
    for octave in range(start_octave, start_octave + octave_range):
        for degree in range(1, 8):
            p = sc.pitchFromDegree(degree)
            p.octave = octave
            scale_notes.append(p.nameWithOctave)

    melody = stream.Part()
    melody.append(meter.TimeSignature("4/4"))

    current_measure = stream.Measure()
    current_duration = 0.0
    bar_number = 1
    for i, duration in enumerate(beat_sequence):
        length = 1.0 if duration == 1 else abs(duration)
        if current_duration + length > 4.0:
            # Pad with rest if measure not full
            if current_duration < 4.0:
                pad_rest = note.Rest(quarterLength=4.0 - current_duration)
                current_measure.append(pad_rest)

            melody.append(current_measure)
            bar_number += 1
            current_measure = stream.Measure(number=bar_number)
            current_duration = 0.0

        if duration == -1:
            n = note.Rest(quarterLength=length)
        else:
            pitch = random.choice(scale_notes)
            n = note.Note(pitch, quarterLength=length)
        current_measure.append(n)
        current_duration += length

    if current_duration < 4.0:
        current_measure.append(note.Rest(quarterLength=4.0 - current_duration))
    melody.append(current_measure)

    # End on the tonic at the end of each phrase
    measures = list(melody.getElementsByClass(stream.Measure))
    for i in range(phrase_length_bars - 1, len(measures), phrase_length_bars):
        tonic_note = note.Note(tonic + str(start_octave), quarterLength=1.0)
        measures[i].append(tonic_note)

    # Show or return
    melody.show('midi')
    melody.show('text')


def ui():
    def btn_callback():
        tonic = tonic_select.get()
        modality = modality_select.get()
        bars = bar_count.get()
        scale_type = (
            scale.MajorScale if modality == 'Major' else
            scale.MinorScale if modality == 'Minor' else
            scale.MixolydianScale if modality == 'Mixolydian' else
            None
        )
        generate_markov_melody_with_phrases(tonic=tonic, scaleType=scale_type, num_notes=24, phrase_length_bars=int(bars),start_octave=4,octave_range=2)
        showinfo('Success', 'The melody has been generated as a MIDI file. Please use a compatible MIDI editor/Digital '
                            'Audio Workstation to listen/edit the file.')

    global tonic_select, modality_select, bar_count

    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    modality = ['Major', 'Minor', 'Mixolydian']

    root = tk.Tk()
    root.geometry("350x300")
    root.wm_title("Music Generator")

    w = tk.Label(root, text='Algorithmic Music Generator', font=('Helvetica', 15, 'bold'), pady=20)
    w.grid(row=0, column=0, columnspan=2)

    label1 = tk.Label(root, text='Tonic Note:')
    label1.grid(row=1, column=0, padx=10, pady=10, sticky='e')

    tonic_select = ttk.Combobox(root, values=notes, width=20)
    tonic_select.set("Select tonic note")
    tonic_select.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    label2 = tk.Label(root, text='Modality:')
    label2.grid(row=2, column=0, padx=10, pady=10, sticky='e')

    modality_select = ttk.Combobox(root, values=modality, width=20)
    modality_select.set("Select modality")
    modality_select.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    generate_btn = tk.Button(root, text='Generate', command=btn_callback)
    generate_btn.grid(row=3, column=0, columnspan=2, pady=3)

    label3 = tk.Label(root, text='Bar Count:')
    label3.grid(row=3, column=0, padx=10, pady=5, sticky='e')

    bar_count = tk.Entry(root, width=22)
    bar_count.insert(0, "8")  # Default value
    bar_count.grid(row=3, column=1, padx=10, pady=5, sticky='w')

    generate_btn = tk.Button(root, text='Generate', command=btn_callback)
    generate_btn.grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()



ui()
