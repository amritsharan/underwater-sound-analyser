# 🖥️ Desktop Application Guide

## Running the Desktop App

The Underwater Sound Classifier now has a beautiful PyQt5 desktop application with user login/logout features!

### Quick Start

1. **Install PyQt5** (if not already installed):
```bash
pip install -r requirements.txt
```

2. **Run the Desktop App**:
```bash
python -m desktop.app
```

Or directly:
```bash
python desktop/app.py
```

### Login Screen

**Demo Account** (created automatically):
- Username: `demo`
- Password: `demo123`

**Create New Account**:
- Click "Sign Up" tab
- Enter username (3+ characters)
- Enter password (4+ characters)
- Click "Create Account"

### Features

#### 📊 Dashboard Tab
- Welcome message
- Quick statistics
- Application overview

#### 🎯 Training Tab
- Select data directory (organized by class)
- Choose model type (SVM or Random Forest)
- Adjust MFCC coefficients
- Click "Train Model"
- View training progress and logs

#### 🔮 Prediction Tab
- Select trained model
- Choose audio file to classify
- View prediction result
- Instant classification

#### 📈 Visualization Tab
- Select audio file
- Choose visualization type (Spectrogram, MFCC, Waveform)
- Generate and display visualization

### User Management

**Login**: Username + Password  
**Signup**: Create new account with confirmation  
**Logout**: Click "Logout" in sidebar (asks for confirmation)

User data is stored locally in `~/.underwater_classifier/users.json`

### Features

✅ **User Authentication**
- Login/Signup interface
- Session management
- Logout functionality

✅ **Model Training**
- Visual progress bar
- Training logs
- Real-time feedback

✅ **Audio Prediction**
- Instant classification
- Result display
- Model selection

✅ **Visualization**
- Spectrogram plots
- MFCC visualization
- Waveform display

✅ **User-Friendly UI**
- Clean, modern design
- Intuitive navigation
- Easy file selection

### Directory Structure

```
desktop/
├── app.py              # Main entry point
├── __init__.py
├── ui/
│   ├── login.py        # Login screen
│   ├── dashboard.py    # Main dashboard
│   └── __init__.py
└── utils/
    ├── user_manager.py # User management
    └── __init__.py
```

### Preparing Data for Training

Organize audio files in this structure:
```
data/raw/
├── whale_calls/
│   ├── whale_001.wav
│   ├── whale_002.wav
│   └── ...
├── ship_noise/
│   ├── ship_001.wav
│   └── ...
└── ambient/
    ├── ambient_001.wav
    └── ...
```

Then in the Training tab:
1. Click "Browse" to select `data/raw/`
2. Choose model type
3. Click "Train Model"

### Making Predictions

1. Go to "Prediction" tab
2. Select model (SVM or Random Forest)
3. Click "Browse" to select audio file
4. Click "Predict"
5. View the predicted class

### Visualization

1. Go to "Visualization" tab
2. Select audio file
3. Choose visualization type:
   - **Spectrogram**: Frequency content over time
   - **MFCC**: Mel-frequency features
   - **Waveform**: Audio amplitude over time
4. Click "Generate Visualization"

### Troubleshooting

**Q: "ModuleNotFoundError: PyQt5"**  
A: Run `pip install -r requirements.txt`

**Q: App doesn't start**  
A: Make sure you're in the project directory and run `python -m desktop.app`

**Q: Training takes too long**  
A: This is normal for the first time. It depends on your data size. Reduce sample data or use fewer MFCC coefficients.

**Q: "No audio files found"**  
A: Ensure your audio files are in `data/raw/class_name/` directory structure

### Tips

- Use demo account to test the app first
- Keep audio files WAV format, 16-30 seconds each
- Balanced number of files per class works best
- Start with SVM for smaller datasets
- Use Random Forest for larger datasets (100+ samples per class)

### System Requirements

- Python 3.7+
- Windows/Mac/Linux
- 2+ GB RAM
- PyQt5 compatible graphics

### Keyboard Shortcuts

- `Ctrl+Q`: Quit application
- `Tab`: Switch between input fields
- `Enter`: Submit form (login/prediction)

---

**Status**: ✅ Desktop app ready to use!  
**Version**: 1.0  
**Created**: January 2026
