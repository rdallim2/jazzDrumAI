// MIDI note numbers for drums
const DRUMS = {
    RIDE_CYMBAL: 51,  // Changed to standard GM drum map
    BASS_DRUM: 36,    // Changed to standard GM drum map
    SNARE_DRUM: 38,   // Changed to standard GM drum map
    H_TOM: 50,        // Changed to standard GM drum map
    HI_HAT_CLOSED: 42, // Changed to standard GM drum map
    CRASH_SIZ_V1: 49,  // Changed to standard GM drum map
    CRASH_SIZ_V2: 57,  // Changed to standard GM drum map
    CRASH_SIZ_V3: 55   // Changed to standard GM drum map
};

// Transition matrix for drum patterns
const drumTransitionMatrix = [
    [0.7, 0.0545, 0.0273, 0.0273, 0.0164, 0.0709, 0.0382, 0.0327, 0.0327],
    [0.4, 0.01, 0.19, 0.03, 0.1, 0.08, 0.04, 0.09, 0.06],
    [0.3, 0.03, 0.04, 0.1, 0.01, 0.08, 0.06, 0.18, 0.2],
    [0.4, 0.02, 0.08, 0.07, 0.16, 0.04, 0.03, 0.12, 0.08],
    [0.5, 0.07, 0.04, 0.05, 0.02, 0.15, 0.08, 0.06, 0.03],
    [0.2, 0.08, 0.03, 0.1, 0.1, 0.3, 0.2, 0.02, 0.06],
    [0.2, 0.08, 0.03, 0.1, 0.04, 0.3, 0.2, 0.04, 0.01],
    [0.30, 0.08, 0.1, 0.06, 0.01, 0.2, 0.19, 0.02, 0.04],
    [0.3, 0.01, 0.09, 0.06, 0.01, 0.14, 0.17, 0.2, 0.02]
];

function getTripSpacing(tempo) {
    if (tempo < 200) return 0.666;
    if (tempo > 275) return 0.5;
    return 0.5 + (0.666 - 0.5) * ((275 - tempo) / (275 - 200));
}

class DrumPattern {
    constructor(synth) {
        this.synth = synth;
    }

    async playNote(note, velocity = 0.7, duration = 0.1) {
        if (this.synth) {
            try {
                console.log(`Playing note: ${note} with velocity: ${velocity}`);
                await this.synth.play(note, 0, {
                    gain: velocity,
                    duration: duration,
                    attack: 0,
                    decay: 0.1,
                    sustain: 0.1,
                    release: 0.1
                });
            } catch (error) {
                console.error('Error playing note:', error);
            }
        }
    }

    async swingPattern(timePerBeat, tripSpacing) {
        const now = this.synth.context.currentTime;
        console.log(`Playing swing pattern at ${timePerBeat}s per beat`);
        
        // First beat
        await this.playNote(DRUMS.BASS_DRUM, 0.15);
        await this.playNote(DRUMS.RIDE_CYMBAL, 0.9);
        
        // Second beat with swing
        setTimeout(async () => {
            await this.playNote(DRUMS.BASS_DRUM, 0.15);
            await this.playNote(DRUMS.RIDE_CYMBAL, 1.05);
            await this.playNote(DRUMS.HI_HAT_CLOSED, 0.7);
        }, timePerBeat * 1000);
        
        // Third beat with swing
        setTimeout(async () => {
            await this.playNote(DRUMS.RIDE_CYMBAL, 0.95);
        }, (timePerBeat + (timePerBeat * tripSpacing)) * 1000);
    }
}

function chooseNextPattern(currentState, tempo, playerCount, densityAnalyzer) {
    if (playerCount === 1) {
        return weightedRandomChoice(drumTransitionMatrix[currentState]);
    }

    const [density, volume] = densityAnalyzer.analyze(tempo);
    
    if (density === 0) {
        return weightedRandomChoice(drumTransitionMatrix[currentState]);
    } else if (density === 1) {
        if (volume === 0) {
            return Math.floor(Math.random() * 6);
        } else if (volume === 1) {
            return weightedRandomChoice(drumTransitionMatrix[currentState]);
        } else {
            return 4 + Math.floor(Math.random() * 5);
        }
    } else if (density === 2) {
        if (volume === 0) {
            return Math.floor(Math.random() * 6);
        } else if (volume === 1) {
            return weightedRandomChoice(drumTransitionMatrix[currentState]);
        } else {
            return 5 + Math.floor(Math.random() * 3);
        }
    }
    return 0;
}

function weightedRandomChoice(weights) {
    const total = weights.reduce((a, b) => a + b, 0);
    const r = Math.random() * total;
    let sum = 0;
    for (let i = 0; i < weights.length; i++) {
        sum += weights[i];
        if (r <= sum) return i;
    }
    return 0;
}

module.exports = { DrumPattern, chooseNextPattern, getTripSpacing, DRUMS };
