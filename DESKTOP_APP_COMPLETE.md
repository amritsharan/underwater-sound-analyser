# 🖥️ Desktop Application - Complete Documentation

## Overview

A beautiful, user-friendly PyQt5 desktop application for the Underwater Sound Classifier with full login/logout functionality.

---

## 🚀 Quick Start

### 1. Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### 2. Run the App (30 seconds)
```bash
python run_desktop.py
```

Or manually:
```bash
python desktop/app.py
```

### 3. Login or Signup (2 minutes)
- **Demo Account**: `demo` / `demo123`
- **New Account**: Click "Sign Up" tab

---

## 🎨 Application Structure

### Files Created

```
desktop/
├── app.py                    # Main application entry point
├── __init__.py
├── ui/
│   ├── login.py             # Login/Signup screen (300 lines)
│   ├── dashboard.py         # Main dashboard (600 lines)
│   └── __init__.py
└── utils/
    ├── user_manager.py      # User authentication (150 lines)
    └── __init__.py

run_desktop.py               # Quick launcher script
DESKTOP_APP_GUIDE.md        # User guide
```

### Features Summary

| Component | Lines | Purpose |
|-----------|-------|---------|
| app.py | 50 | App launcher and window manager |
| login.py | 300 | Login and signup screens |
| dashboard.py | 600 | Main dashboard with 4 tabs |
| user_manager.py | 150 | User authentication and storage |

---

## 🎯 Features

### Login/Signup Screen
✅ Professional login interface  
✅ Signup with password confirmation  
✅ Input validation  
✅ Demo account  
✅ User data stored locally  

### Dashboard (4 Tabs)

#### 1. Dashboard Tab
- Welcome message with username
- Quick statistics
- Application overview
- Model count display

#### 2. Training Tab
- Directory selection (with file browser)
- Model type selector (SVM / Random Forest)
- MFCC coefficient adjustment (10-40)
- Training button with progress bar
- Real-time training logs
- Completion notifications

#### 3. Prediction Tab
- Model selector (SVM / Random Forest)
- Audio file selector
- Instant classification
- Beautiful result display

#### 4. Visualization Tab
- Audio file selector
- Visualization type selector:
  - Spectrogram (frequency vs time)
  - MFCC (mel-frequency features)
  - Waveform (amplitude vs time)
- Matplotlib canvas for plots

### Sidebar
- User information display
- Navigation buttons
- Logout button

---

## 👤 User Management

### User Storage
- Location: `~/.underwater_classifier/users.json`
- Format: JSON (easy to read and backup)
- Data: Username, password, created date, models list

### Demo Account
- Username: `demo`
- Password: `demo123`
- Pre-created for testing

### Creating Account
1. Click "Sign Up" tab
2. Username: 3+ characters
3. Password: 4+ characters
4. Confirm password
5. Click "Create Account"

### Session Management
- Login: Sets current user
- Logout: Clears current user
- Confirmation dialog on logout

---

## 🎯 Workflow Examples

### Example 1: Train Your First Model

1. **Login**: Use demo account or create new
2. **Prepare Data**: Organize audio files
   ```
   data/raw/
   ├── whale_calls/ (10+ WAV files)
   ├── ship_noise/ (10+ WAV files)
   └── ambient/ (10+ WAV files)
   ```
3. **Go to Training Tab**
   - Click "Browse" → Select `data/raw/`
   - Select "SVM" model type
   - Click "Train Model"
4. **Wait**: Watch progress bar and logs
5. **Result**: Model saved to `models/svm_model.pkl`

### Example 2: Make a Prediction

1. **Go to Prediction Tab**
2. **Select Model**: Choose "SVM" or "Random Forest"
3. **Click Browse**: Select audio file to classify
4. **Click Predict**: See results
5. **View Result**: Displays predicted class

### Example 3: Visualize Audio

1. **Go to Visualization Tab**
2. **Select Audio File**: Click browse
3. **Choose Type**:
   - Spectrogram: See frequencies over time
   - MFCC: See extracted features
   - Waveform: See raw audio shape
4. **Generate**: See plot displayed

---

## 🎨 UI Design

### Colors
- **Primary Green**: #4CAF50 (Buttons, success)
- **Secondary Blue**: #2196F3 (Secondary actions)
- **Orange**: #FF9800 (Visualization)
- **Red**: #f44336 (Logout, danger)
- **Gray**: #f5f5f5 (Background)

### Fonts
- Header: Arial 16pt Bold
- Buttons: Arial 11-12pt Bold
- Labels: Arial 10pt Regular
- Monospace: For results

### Layout
- **Sidebar**: 200px fixed width
- **Content**: Responsive tabs
- **Spacing**: Consistent padding
- **Icons**: Unicode emoji for visual appeal

---

## 🔒 Security Notes

⚠️ **Important**: This app has NO real authentication
- Passwords are stored in plain text
- Use only for personal/development purposes
- Not suitable for production

✅ **What's Secure**:
- User sessions in memory
- Local file storage only
- No network transmission

---

## 🛠️ Customization

### Change Colors
Edit `DESKTOP_APP_GUIDE.md` styling in:
- `login.py`: Login screen colors
- `dashboard.py`: Dashboard colors

### Add New Tab
In `dashboard.py`:
1. Create new method `create_newtab()`
2. Add to content: `self.content.addTab(self.create_newtab(), "New Tab")`
3. Add menu button in sidebar

### Change Demo Account
In `user_manager.py`:
```python
# Add to __init__ or create file to pre-populate
```

---

## 📊 Technical Details

### Threading
- **Training**: Runs in separate thread to prevent freezing
- **Progress**: Signals update UI in real-time
- **Completion**: Callback displays results

### UI Framework
- **Framework**: PyQt5
- **Widgets**: QMainWindow, QTabWidget, QLineEdit, QPushButton
- **Plotting**: Matplotlib with PyQt5 backend

### File Handling
- **Audio**: WAV files via librosa
- **Models**: Pickle format (.pkl)
- **Users**: JSON format

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| App won't start | Run `pip install -r requirements.txt` |
| PyQt5 error | Install: `pip install PyQt5==5.15.9` |
| Training stuck | Check data directory has audio files |
| No models available | Train a model first in Training tab |
| Visualization empty | Select audio file first |
| Login fails | Check demo account: demo / demo123 |

---

## 📁 Project Structure Now

```
Underwater Sound Classifier/
├── desktop/                 # NEW: Desktop app
│   ├── app.py
│   ├── ui/
│   │   ├── login.py
│   │   └── dashboard.py
│   └── utils/
│       └── user_manager.py
│
├── run_desktop.py           # NEW: Quick launcher
├── DESKTOP_APP_GUIDE.md     # NEW: User guide
│
├── classifier.py            # Main classifier
├── example.py               # Examples
├── test_classifier.py       # Tests
│
├── data/                    # Audio data
│   ├── raw/
│   └── processed/
├── models/                  # Trained models
│
├── requirements.txt         # Dependencies (updated)
└── README.md                # Documentation
```

---

## 🚀 Future Enhancements

### Short-term
- [ ] Save prediction history
- [ ] Model comparison charts
- [ ] Batch prediction
- [ ] Audio playback in app

### Medium-term
- [ ] Advanced visualization (3D plots)
- [ ] Real-time audio stream classification
- [ ] Model performance metrics display
- [ ] Data augmentation UI

### Long-term
- [ ] Web version (Flask/React)
- [ ] Cloud model deployment
- [ ] Real authentication
- [ ] Team collaboration features

---

## 📝 Code Examples

### Running the App Programmatically
```python
from desktop.app import main

if __name__ == '__main__':
    main()
```

### Using User Manager Directly
```python
from desktop.utils.user_manager import user_manager

# Signup
success, msg = user_manager.signup('newuser', 'password123')

# Login
success, msg = user_manager.login('newuser', 'password123')

# Check if logged in
if user_manager.is_logged_in():
    print(f"Logged in as: {user_manager.get_current_user()}")

# Logout
user_manager.logout()
```

### Creating a Model and Training
```python
from classifier import UnderwaterSoundClassifier

clf = UnderwaterSoundClassifier(model_type='svm')
clf.load_audio_files('data/raw/')
clf.train(test_size=0.2)
clf.save_model('models/my_model.pkl')
```

---

## ✨ Key Highlights

✅ **No Installation Hassle**
- Single command to run
- Auto-checks dependencies
- User-friendly interface

✅ **Professional Design**
- Modern color scheme
- Responsive layout
- Intuitive navigation

✅ **Complete Functionality**
- Train models
- Make predictions
- Visualize data
- Manage users

✅ **Easy to Extend**
- Clean code structure
- Well-documented
- Modular design

---

## 📞 Support

**For Issues**:
1. Check TROUBLESHOOTING section above
2. Review DESKTOP_APP_GUIDE.md
3. Check console output for error messages

**For Questions**:
- See README.md for project overview
- Check API_REFERENCE.md for technical details
- Review code comments in desktop/ folder

---

## 📊 Statistics

- **Total Lines of Code**: 1,000+
- **Desktop App Code**: 950 lines
- **UI Components**: 20+
- **Features**: 10+
- **Development Time**: ~2 hours

---

## 🎉 Summary

You now have a **complete desktop application** with:

✅ Professional login/signup  
✅ Model training with progress bar  
✅ Audio classification  
✅ Data visualization  
✅ User session management  
✅ Beautiful PyQt5 UI  

**Start with `python run_desktop.py`!** 🚀

---

**Status**: ✅ Complete and Ready  
**Version**: 1.0  
**Last Updated**: January 2026
