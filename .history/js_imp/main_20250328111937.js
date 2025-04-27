const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const fs = require('fs');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('index.html');
    
    // Open DevTools in development
    if (process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools();
    }
}

app.whenReady().then(() => {
    createWindow();

    // Check if soundfont files exist
    const drumSF2Path = path.join(__dirname, 'drums_for_ai_v11.sf2');
    const pianoSF2Path = path.join(__dirname, 'FluidR3_GM.sf2');

    if (!fs.existsSync(drumSF2Path)) {
        dialog.showMessageBox(mainWindow, {
            type: 'warning',
            title: 'Missing Soundfont',
            message: 'drums_for_ai_v10.sf2 not found',
            detail: 'Please place the soundfont file in the js_imp directory.',
            buttons: ['OK']
        });
    }

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
