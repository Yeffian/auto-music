from music21 import stream, note, scale, meter, tempo
import random
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk
from markov import RhthymController

def generate_markov_melody_with_wave_contour(tonic='C',scaleType=scale.MajorScale,num_bars=8,start_octave=4,octave_range=1,phrase_length_bars=2,bpm=100):
    sc = scaleType(tonic)

    # sort by MIDI value
    scale_notes = []
    for octave in range(start_octave, start_octave + octave_range):
        for degree in range(1, 8):  # scale degrees 1–7
            p = sc.pitchFromDegree(degree)
            p.octave = octave
            scale_notes.append(p)

    scale_notes.sort(key=lambda p: p.midi)  # ascending order
    num_scale_notes = len(scale_notes)

    melody = stream.Part()
    mark = tempo.MetronomeMark(number=bpm)
    melody.insert(0, mark)
    melody.append(meter.TimeSignature("4/4"))

    beat_probs = {
        1: {0.5: 0.45, 0.25: 0.4, 1: 0.1, -1: 0.05},
        0.5: {0.25: 0.4, 0.5: 0.25, 1: 0.15, -1: 0.2},
        0.25: {0.25: 0.5, 0.5: 0.25, 1: 0.05, -1: 0.2},
        -1: {0.25: 0.5, 0.5: 0.3, 1: 0.1, -1: 0.1}
    }

    beat_chain = RhthymController(beat_probs)

    # Initialize contour position
    current_idx = len(scale_notes) // 2  # start in middle
    going_up = random.choice([True, False])  # first direction in wave

    for bar_num in range(num_bars):
        m = stream.Measure(number=bar_num + 1)
        bar_rhythm = beat_chain.generate_bar(start=1, max_beats=4.0)

        for dur in bar_rhythm:
            length = abs(dur)

            if dur == -1:
                n = note.Rest(quarterLength=length)
            else:
                # wave contour: move 1–2 steps in current direction
                step = random.choice([1, 2])
                if going_up:
                    current_idx = min(current_idx + step, num_scale_notes - 1)
                else:
                    current_idx = max(current_idx - step, 0)

                pitch_obj = scale_notes[current_idx]
                n = note.Note(pitch_obj.nameWithOctave, quarterLength=length)

                # random direction
                going_up = random.choice([True, False])

            m.append(n)

        # end on the tonic
        if (bar_num + 1) % phrase_length_bars == 0:
            m.append(note.Note(tonic + str(start_octave), quarterLength=1.0))

        melody.append(m)

    melody.show('text')
    melody.show('midi')


def ui():
    def btn_callback():
        tonic = tonic_select.get()
        modality = modality_select.get()
        bars = bar_count.get()
        bpm = bpm_entry.get()
        scale_type = (
            scale.MajorScale if modality == 'Major' else
            scale.MinorScale if modality == 'Minor' else
            scale.MixolydianScale if modality == 'Mixolydian' else
            None
        )
        generate_markov_melody_with_wave_contour(tonic=tonic, scaleType=scale_type, phrase_length_bars=int(bars),start_octave=4,octave_range=2,bpm=bpm)
        showinfo('Success', 'The melody has been generated as a MIDI file. Please use a compatible MIDI editor/Digital '
                            'Audio Workstation to listen/edit the file.')

    global tonic_select, modality_select, bar_count, bpm_entry

    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    modality = ['Major', 'Minor', 'Mixolydian']

    root = tk.Tk()
    root.geometry("350x350")
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

    label3 = tk.Label(root, text='Bar Count:')
    label3.grid(row=3, column=0, padx=10, pady=5, sticky='e')

    bar_count = tk.Entry(root, width=22)
    bar_count.insert(0, "8")
    bar_count.grid(row=3, column=1, padx=10, pady=5, sticky='w')

    label4 = tk.Label(root, text='Tempo:')
    label4.grid(row=4, column=0, padx=10, pady=5, sticky='e')

    bpm_entry = tk.Entry(root, width=22)
    bpm_entry.insert(0, "120")
    bpm_entry.grid(row=4, column=1, padx=10, pady=5, sticky='w')

    generate_btn = tk.Button(root, text='Generate', command=btn_callback)
    generate_btn.grid(row=5, column=0, columnspan=2, pady=15)

    root.mainloop()



ui()
