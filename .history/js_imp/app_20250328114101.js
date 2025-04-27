const { ipcRenderer } = require('electron');
const patterns = require('./drumPatterns');

// Initialize WebMidi
WebMidi.enable()
    .then(onWebMidiEnabled)
    .catch(err => console.error('WebMidi could not be enabled:', err));

let drumSynth;
let currentPattern = 0;
let isPlaying = false;
let midiInput = null;
let noteEvents = [];
let noteVolumes = [];

// Create audio context
const audioContext = new (window.AudioContext || window.webkitAudioContext)();
console.log('Audio context created:', audioContext.state);

// Create noise buffer for drums
function createNoiseBuffer() {
    const bufferSize = audioContext.sampleRate * 2; // 2 seconds of noise
    const buffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate);
    const data = buffer.getChannelData(0);
    
    for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1;
    }
    
    return buffer;
}

const noiseBuffer = createNoiseBuffer();

// Initialize sound engine
async function initializeSoundEngine() {
    try {
        console.log('Initializing sound engine...');
        
        // Create a simple oscillator to test audio context
        const osc = audioContext.createOscillator();
        const gain = audioContext.createGain();
        gain.gain.value = 0.1;
        osc.connect(gain);
        gain.connect(audioContext.destination);
        osc.start();
        osc.stop(audioContext.currentTime + 0.1);

        // Create a better drum synth
        drumSynth = {
            play: async function(note, time, options) {
                const startTime = time || audioContext.currentTime;
                const gain = options.gain || 0.5;
                
                switch(note) {
                    case patterns.DRUMS.BASS_DRUM:
                        this.playBassDrum(startTime, gain);
                        break;
                    case patterns.DRUMS.SNARE_DRUM:
                        this.playSnareDrum(startTime, gain);
                        break;
                    case patterns.DRUMS.HI_HAT_CLOSED:
                        this.playHiHat(startTime, gain);
                        break;
                    case patterns.DRUMS.RIDE_CYMBAL:
                        this.playRideCymbal(startTime, gain);
                        break;
                }
            },

            playBassDrum: function(time, gain) {
                const osc = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                const filter = audioContext.createBiquadFilter();

                osc.frequency.setValueAtTime(150, time);
                osc.frequency.exponentialRampToValueAtTime(0.01, time + 0.15);
                
                gainNode.gain.setValueAtTime(gain, time);
                gainNode.gain.exponentialRampToValueAtTime(0.01, time + 0.15);
                
                filter.type = 'lowpass';
                filter.frequency.setValueAtTime(150, time);
                
                osc.connect(filter);
                filter.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                osc.start(time);
                osc.stop(time + 0.15);
            },

            playSnareDrum: function(time, gain) {
                // Noise component
                const noiseSource = audioContext.createBufferSource();
                const noiseGain = audioContext.createGain();
                const noiseFilter = audioContext.createBiquadFilter();
                
                noiseSource.buffer = noiseBuffer;
                noiseFilter.type = 'highpass';
                noiseFilter.frequency.value = 1000;
                
                noiseGain.gain.setValueAtTime(gain * 0.5, time);
                noiseGain.gain.exponentialRampToValueAtTime(0.01, time + 0.1);
                
                noiseSource.connect(noiseFilter);
                noiseFilter.connect(noiseGain);
                noiseGain.connect(audioContext.destination);
                
                // Tone component
                const osc = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                osc.frequency.value = 250;
                gainNode.gain.setValueAtTime(gain * 0.5, time);
                gainNode.gain.exponentialRampToValueAtTime(0.01, time + 0.1);
                
                osc.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                noiseSource.start(time);
                noiseSource.stop(time + 0.1);
                osc.start(time);
                osc.stop(time + 0.1);
            },

            playHiHat: function(time, gain) {
                const noiseSource = audioContext.createBufferSource();
                const noiseGain = audioContext.createGain();
                const filter = audioContext.createBiquadFilter();
                
                noiseSource.buffer = noiseBuffer;
                
                filter.type = 'highpass';
                filter.frequency.value = 7000;
                
                noiseGain.gain.setValueAtTime(gain * 0.3, time);
                noiseGain.gain.exponentialRampToValueAtTime(0.01, time + 0.05);
                
                noiseSource.connect(filter);
                filter.connect(noiseGain);
                noiseGain.connect(audioContext.destination);
                
                noiseSource.start(time);
                noiseSource.stop(time + 0.05);
            },

            playRideCymbal: function(time, gain) {
                const noiseSource = audioContext.createBufferSource();
                const noiseGain = audioContext.createGain();
                const filter = audioContext.createBiquadFilter();
                
                noiseSource.buffer = noiseBuffer;
                
                filter.type = 'bandpass';
                filter.frequency.value = 5000;
                filter.Q.value = 1;
                
                noiseGain.gain.setValueAtTime(gain * 0.3, time);
                noiseGain.gain.exponentialRampToValueAtTime(0.01, time + 0.3);
                
                noiseSource.connect(filter);
                filter.connect(noiseGain);
                noiseGain.connect(audioContext.destination);
                
                noiseSource.start(time);
                noiseSource.stop(time + 0.3);
            }
        };
        
        console.log('Sound engine initialized successfully');
        document.getElementById('startBtn').disabled = false;
        
    } catch (error) {
        console.error('Error initializing sound engine:', error);
        document.getElementById('status').innerHTML = 'Error: Could not initialize audio. Please check console.';
    }
}

function onWebMidiEnabled() {
    console.log("MIDI Inputs:", WebMidi.inputs);
    
    const statusDiv = document.getElementById('status');
    statusDiv.innerHTML = "Available MIDI inputs:<br>" +
        WebMidi.inputs.map(input => input.name).join('<br>');

    if (WebMidi.inputs.length > 0) {
        midiInput = WebMidi.inputs[0];
        setupMidiListeners();
    }
}

function setupMidiListeners() {
    midiInput.addListener("noteon", e => {
        const now = audioContext.currentTime;
        noteEvents.push({
            time: now,
            note: e.note.number,
            velocity: e.velocity
        });
        noteVolumes.push(e.velocity);
    });
}

class DensityAnalyzer {
    analyze(bpm) {
        const now = audioContext.currentTime;
        const timeWindow = 60 / bpm * 2; // two beats
        
        const recentEvents = noteEvents.filter(event => 
            now - event.time < timeWindow
        );
        
        const density = Math.min(2, Math.floor(recentEvents.length / 4));
        
        const recentVolumes = noteVolumes.slice(-recentEvents.length);
        const avgVolume = recentVolumes.length > 0 
            ? recentVolumes.reduce((a, b) => a + b) / recentVolumes.length 
            : 0;
        
        let volumeLevel;
        if (avgVolume < 0.3) volumeLevel = 0;
        else if (avgVolume < 0.7) volumeLevel = 1;
        else volumeLevel = 2;
        
        return [density, volumeLevel];
    }
}

const densityAnalyzer = new DensityAnalyzer();

// Initialize the sound engine when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing sound engine...');
    initializeSoundEngine();
});

// UI Event Listeners
document.getElementById('startBtn').addEventListener('click', async () => {
    console.log('Start button clicked');
    if (!isPlaying && drumSynth) {
        if (audioContext.state === 'suspended') {
            console.log('Resuming audio context...');
            await audioContext.resume();
            console.log('Audio context resumed:', audioContext.state);
        }
        isPlaying = true;
        console.log('Starting playback...');
        playDrums();
    } else {
        console.log('Cannot start: drumSynth not initialized or already playing');
    }
});

document.getElementById('stopBtn').addEventListener('click', () => {
    console.log('Stop button clicked');
    isPlaying = false;
});

function playDrums() {
    const tempo = parseInt(document.getElementById('tempo').value);
    const timePerBeat = 60 / tempo;
    const tripSpacing = patterns.getTripSpacing(tempo);
    
    console.log(`Playing drums at tempo: ${tempo}`);
    const pattern = new patterns.DrumPattern(drumSynth, audioContext);
    
    function loop() {
        if (!isPlaying) return;
        
        pattern.swingPattern(timePerBeat, tripSpacing);
        currentPattern = patterns.chooseNextPattern(currentPattern, tempo, 1, densityAnalyzer);
        
        setTimeout(loop, timePerBeat * 1000);
    }
    
    loop();
}

// Clean up note events periodically
setInterval(() => {
    const now = audioContext.currentTime;
    noteEvents = noteEvents.filter(event => now - event.time < 5);
    noteVolumes = noteVolumes.slice(-noteEvents.length);
}, 5000);
