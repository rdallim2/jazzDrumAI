note_map = {
    "A0": 21, "A#0": 22, "Bb0": 22, "B0": 23,
    "C1": 24, "C#1": 25, "Db1": 25, "D1": 26, "D#1": 27, "Eb1": 27, "E1": 28, "F1": 29, "F#1": 30, "Gb1": 30, "G1": 31, "G#1": 32, "Ab1": 32, "A1": 33, "A#1": 34, "Bb1": 34, "B1": 35,
    "C2": 36, "C#2": 37, "Db2": 37, "D2": 38, "D#2": 39, "Eb2": 39, "E2": 40, "F2": 41, "F#2": 42, "Gb2": 42, "G2": 43, "G#2": 44, "Ab2": 44, "A2": 45, "A#2": 46, "Bb2": 46, "B2": 47,
    "C3": 48, "C#3": 49, "Db3": 49, "D3": 50, "D#3": 51, "Eb3": 51, "E3": 52, "F3": 53, "F#3": 54, "Gb3": 54, "G3": 55, "G#3": 56, "Ab3": 56, "A3": 57, "A#3": 58, "Bb3": 58, "B3": 59,
    "C4": 60, "C#4": 61, "Db4": 61, "D4": 62, "D#4": 63, "Eb4": 63, "E4": 64, "F4": 65, "F#4": 66, "Gb4": 66, "G4": 67, "G#4": 68, "Ab4": 68, "A4": 69, "A#4": 70, "Bb4": 70, "B4": 71,
    "C5": 72, "C#5": 73, "Db5": 73, "D5": 74, "D#5": 75, "Eb5": 75, "E5": 76, "F5": 77, "F#5": 78, "Gb5": 78, "G5": 79, "G#5": 80, "Ab5": 80, "A5": 81, "A#5": 82, "Bb5": 82, "B5": 83,
    "C6": 84, "C#6": 85, "Db6": 85, "D6": 86, "D#6": 87, "Eb6": 87, "E6": 88, "F6": 89, "F#6": 90, "Gb6": 90, "G6": 91, "G#6": 92, "Ab6": 92, "A6": 93, "A#6": 94, "Bb6": 94, "B6": 95,
    "C7": 96, "C#7": 97, "Db7": 97, "D7": 98, "D#7": 99, "Eb7": 99, "E7": 100, "F7": 101, "F#7": 102, "Gb7": 102, "G7": 103, "G#7": 104, "Ab7": 104, "A7": 105, "A#7": 106, "Bb7": 106, "B7": 107,
    "C8": 108
}

piano_chord_members = {
    "C7": {note_map["C4"], note_map["E4"], note_map["G4"], note_map["Bb4"]},
    "D7": {note_map["D4"], note_map["F#4"], note_map["A4"], note_map["C5"]},
    "E7": {note_map["E4"], note_map["G#4"], note_map["B4"], note_map["D5"]},
    "F7": {note_map["F4"], note_map["A4"], note_map["C5"], note_map["Eb5"]},
    "G7": {note_map["G4"], note_map["B4"], note_map["D5"], note_map["F5"]},
    "A7": {note_map["A4"], note_map["C#5"], note_map["E5"], note_map["G5"]},
    "B7": {note_map["B4"], note_map["D#5"], note_map["F#5"], note_map["A5"]}
}

bass_note_map = {
    "E0": 16, "F0": 17, "F#0": 18, "Gb0": 18, "G0": 19, "G#0": 20, "Ab0": 20, "A0": 21, "A#0": 22, "Bb0": 22, "B0": 23,
    "C1": 24, "C#1": 25, "Db1": 25, "D1": 26, "D#1": 27, "Eb1": 27, "E1": 28, "F1": 29, "F#1": 30, "Gb1": 30, "G1": 31, "G#1": 32, "Ab1": 32, "A1": 33, "A#1": 34, "Bb1": 34, "B1": 35,
    "C2": 36, "C#2": 37, "Db2": 37, "D2": 38, "D#2": 39, "Eb2": 39, "E2": 40, "F2": 41, "F#2": 42, "Gb2": 42, "G2": 43, "G#2": 44, "Ab2": 44, "A2": 45, "A#2": 46, "Bb2": 46, "B2": 47,
    "C3": 48, "C#3": 49, "Db3": 49, "D3": 50, "D#3": 51, "Eb3": 51, "E3": 52, "F3": 53, "F#3": 54, "Gb3": 54, "G3": 55, "G#3": 56, "Ab3": 56, "A3": 57, "A#3": 58, "Bb3": 58, "B3": 59

}

bass_chord_members = {
       "C7": {note_map["C2"], note_map["E2"], note_map["G2"], note_map["Bb2"]},
    "D7": {note_map["D2"], note_map["F#2"], note_map["A2"], note_map["C3"]},
    "E7": {note_map["E2"], note_map["G#2"], note_map["B2"], note_map["D3"]},
    "F7": {note_map["F2"], note_map["A2"], note_map["C3"], note_map["Eb3"]},
    "G7": {note_map["G2"], note_map["B2"], note_map["D3"], note_map["F3"]},
    "A7": {note_map["A2"], note_map["C#3"], note_map["E3"], note_map["G3"]},
    "B7": {note_map["B2"], note_map["D#3"], note_map["F#3"], note_map["A3"]}
}