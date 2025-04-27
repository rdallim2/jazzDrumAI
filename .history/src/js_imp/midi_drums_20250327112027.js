import * as Tone from "tone";

// MIDI Note values for drums
const RIDE_CYMBAL = 54;
const BASS_DRUM = 25;
const SNARE_DRUM = 37;
const HI_HAT_CLOSED = 42;

const synth = new Tone.Sampler({
    "C3": "https://tonejs.github.io/audio/drum-samples/CR78/kick.mp3",
    "D3": "https://tonejs.github.io/audio/drum-samples/CR78/snare.mp3",
    "E3": "https://tonejs.github.io/audio/drum-samples/CR78/hihat.mp3",
    "F3": "https://tonejs.github.io/audio/drum-samples/CR78/ride.mp3"
}).toDestination();

function getTripSpacing(tempo) {
    if (tempo < 200) return 0.666;
    if (tempo > 275) return 0.5;
    return 0.5 + (0.666 - 0.5) * ((275 - tempo) / (275 - 200));
}

function playPattern(tempo) {
    const timePerBeat = 60 / tempo;
    const tripSpacing = getTripSpacing(tempo);

    const now = Tone.now();
    synth.triggerAttackRelease("C3", "8n", now); // Bass drum
    synth.triggerAttackRelease("F3", "8n", now); // Ride cymbal

    Tone.Transport.scheduleOnce((time) => {
        synth.triggerAttackRelease("C3", "8n", time);
        synth.triggerAttackRelease("F3", "8n", time);
        synth.triggerAttackRelease("E3", "8n", time);
    }, now + timePerBeat * tripSpacing);

    Tone.Transport.scheduleOnce((time) => {
        synth.triggerAttackRelease("F3", "8n", time);
    }, now + timePerBeat);

    Tone.Transport.start();
}

async function startPlayback(tempo = 220) {
    await Tone.start();
    playPattern(tempo);
}

// Example usage: Call startPlayback() to play the pattern
startPlayback();
