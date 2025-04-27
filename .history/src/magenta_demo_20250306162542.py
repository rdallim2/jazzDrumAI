import os
import tensorflow as tf
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.music import constants
from note_seq.protobuf import generator_pb2
from note_seq.protobuf import music_pb2
import note_seq

def generate_drums():
    # Initialize the model
    bundle = drums_rnn_sequence_generator.get_bundle()
    generator = drums_rnn_sequence_generator.DrumsRnnSequenceGenerator(
        model=bundle.generator_pb2.GeneratorDetails.id,
        details=bundle.generator_pb2.GeneratorDetails(),
        steps_per_quarter=4,
        checkpoint=None,
        bundle=bundle)

    # Create a simple drum sequence as input
    steps_per_bar = 16
    bars = 4
    primer_sequence = music_pb2.NoteSequence()
    primer_sequence.tempos.add(qpm=120)
    
    # Add a basic kick drum pattern
    time = 0
    step = 0.25  # quarter note
    for i in range(bars * steps_per_bar):
        if i % 4 == 0:  # Add kick drum on every beat
            note = primer_sequence.notes.add()
            note.pitch = 36  # MIDI pitch for kick drum
            note.start_time = time
            note.end_time = time + step
            note.velocity = 80
            note.instrument = 9  # MIDI channel 10 (drums)
            note.is_drum = True
        time += step

    # Set generation parameters
    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args['temperature'].float_value = 1.0
    generator_options.generate_sections.add(
        start_time=primer_sequence.total_time,
        end_time=8.0)  # Generate 8 seconds of music

    # Generate the sequence
    sequence = generator.generate(primer_sequence, generator_options)
    
    # Save as MIDI file
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    note_seq.sequence_proto_to_midi_file(sequence, os.path.join(output_dir, 'generated_drums.mid'))
    print(f"Generated drum sequence saved to {output_dir}/generated_drums.mid")

if __name__ == '__main__':
    print("Initializing Magenta drum sequence generator...")
    generate_drums() 