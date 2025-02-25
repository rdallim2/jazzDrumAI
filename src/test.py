from magenta.music import sequences_lib, midi_io

# Create a simple MIDI sequence
sequence = sequences_lib.quantize_note_sequence(
    midi_io.midi_file_to_note_sequence("example.mid")
)

print(sequence)