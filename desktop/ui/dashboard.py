"""
Main Dashboard for Desktop Application
Handles audio classification, training, and visualization
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFileDialog, QTabWidget,
                             QMessageBox, QProgressBar, QComboBox, QListWidget,
                             QListWidgetItem, QTextEdit, QSpinBox, QGroupBox,
                             QFormLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis
from PyQt5.QtCore import QTimer, QRect
from PyQt5.QtGui import QColor

import sys
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from classifier import UnderwaterSoundClassifier
from desktop.utils.user_manager import user_manager


class TrainingWorker(QThread):
    """Worker thread for model training"""
    
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str, float)
    
    def __init__(self, data_dir, model_type):
        """Initialize training worker"""
        super().__init__()
        self.data_dir = data_dir
        self.model_type = model_type
    
    def run(self):
        """Run training in separate thread"""
        try:
            self.progress.emit(10)
            
            # Load and train
            classifier = UnderwaterSoundClassifier(model_type=self.model_type)
            classifier.load_audio_files(self.data_dir)
            self.progress.emit(50)
            
            classifier.train(test_size=0.2)
            self.progress.emit(90)
            
            # Save model
            model_path = f'models/{self.model_type}_model.pkl'
            classifier.save_model(model_path)
            self.progress.emit(100)
            
            # Get accuracy
            accuracy = getattr(classifier, 'accuracy', 0.0)
            self.finished.emit(True, f"Model trained successfully!\nAccuracy achieved: {accuracy*100:.2f}%", accuracy)
        except Exception as e:
            self.finished.emit(False, f"Training failed: {str(e)}", 0.0)


class Dashboard(QMainWindow):
    """Main application dashboard"""
    
    def __init__(self, username):
        """Initialize dashboard"""
        super().__init__()
        self.username = username
        self.user_manager = user_manager
        self.classifier = None
        self.training_worker = None
        
        self.init_ui()
        self.show()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle(f'🐋 Underwater Sound Classifier - {self.username}')
        self.setGeometry(50, 50, 1200, 700)
        self.set_style()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar, 1)
        
        # Right content area
        content = self.create_content()
        main_layout.addWidget(content, 3)
        
        central_widget.setLayout(main_layout)
    
    def create_sidebar(self):
        """Create left sidebar"""
        sidebar = QWidget()
        layout = QVBoxLayout()
        
        # User info
        user_label = QLabel(f"👤 {self.username}")
        user_label.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(user_label)
        
        user_info = QLabel("Logged In")
        user_info.setStyleSheet("color: #4CAF50; font-weight: bold;")
        layout.addWidget(user_info)
        
        layout.addSpacing(20)
        
        # Menu buttons
        menu_items = [
            ("📊 Dashboard", 0),
            ("🎯 Train Model", 1),
            ("🔮 Predict", 2),
            ("📈 Visualize", 3),
        ]
        
        self.menu_buttons = {}
        for text, index in menu_items:
            btn = QPushButton(text)
            btn.setMinimumHeight(40)
            btn.setFont(QFont('Arial', 10))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #4CAF50;
                    color: white;
                }
            """)
            btn.clicked.connect(lambda checked, i=index: self.show_page(i))
            self.menu_buttons[index] = btn
            layout.addWidget(btn)
        
        layout.addSpacing(20)
        
        # Logout button
        logout_btn = QPushButton('🚪 Logout')
        logout_btn.setMinimumHeight(40)
        logout_btn.setFont(QFont('Arial', 10, QFont.Bold))
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        layout.addStretch()
        
        sidebar.setLayout(layout)
        sidebar.setMaximumWidth(200)
        sidebar.setStyleSheet("background-color: #fafafa; border-right: 1px solid #ddd;")
        
        return sidebar
    
    def create_content(self):
        """Create main content area"""
        self.content = QTabWidget()
        self.content.setTabPosition(QTabWidget.West)
        
        # Tab 0: Dashboard
        self.content.addTab(self.create_dashboard_tab(), "Dashboard")
        
        # Tab 1: Training
        self.content.addTab(self.create_training_tab(), "Training")
        
        # Tab 2: Prediction
        self.content.addTab(self.create_prediction_tab(), "Prediction")
        
        # Tab 3: Visualization
        self.content.addTab(self.create_visualization_tab(), "Visualization")
        
        return self.content
    
    def create_dashboard_tab(self):
        """Create dashboard tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Welcome message
        welcome = QLabel(f"Welcome, {self.username}! 👋")
        welcome.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(welcome)
        
        info = QLabel("""
        🐋 Underwater Sound Classifier
        
        This application helps you classify underwater sounds using Machine Learning.
        
        Features:
        • Train models on your audio data
        • Classify new audio files
        • Visualize spectrograms and features
        • Save and manage multiple models
        
        To get started:
        1. Go to "Training" tab
        2. Select your audio files (organized by class)
        3. Click "Train Model"
        4. Use "Prediction" tab to classify new audio
        """)
        info.setStyleSheet("color: #666; line-height: 1.6;")
        layout.addWidget(info)
        
        # Stats
        stats_group = QGroupBox("Quick Stats")
        stats_layout = QFormLayout()
        stats_layout.addRow("Logged User:", QLabel(self.username))
        stats_layout.addRow("Application Status:", QLabel("Ready"))
        stats_layout.addRow("Models Available:", QLabel(str(len(self.user_manager.get_user_models()))))
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_training_tab(self):
        """Create training tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Data directory selector
        dir_layout = QHBoxLayout()
        dir_label = QLabel("Data Directory:")
        self.data_dir_input = QLineEdit()
        self.data_dir_input.setPlaceholderText("Select directory with audio files")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.select_data_directory)
        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(self.data_dir_input)
        dir_layout.addWidget(browse_btn)
        layout.addLayout(dir_layout)
        
        # Model type selector
        model_layout = QHBoxLayout()
        model_label = QLabel("Model Type:")
        self.model_combo = QComboBox()
        self.model_combo.addItems(['SVM', 'Random Forest'])
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        model_layout.addStretch()
        layout.addLayout(model_layout)
        
        # MFCC settings
        mfcc_layout = QHBoxLayout()
        mfcc_label = QLabel("MFCC Coefficients:")
        self.mfcc_spin = QSpinBox()
        self.mfcc_spin.setValue(13)
        self.mfcc_spin.setRange(10, 40)
        mfcc_layout.addWidget(mfcc_label)
        mfcc_layout.addWidget(self.mfcc_spin)
        mfcc_layout.addStretch()
        layout.addLayout(mfcc_layout)
        
        layout.addSpacing(15)
        
        # Train button
        self.train_btn = QPushButton("🚀 Train Model")
        self.train_btn.setMinimumHeight(50)
        self.train_btn.setFont(QFont('Arial', 12, QFont.Bold))
        self.train_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        self.train_btn.clicked.connect(self.start_training)
        layout.addWidget(self.train_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Output log
        log_label = QLabel("Training Log:")
        layout.addWidget(log_label)
        
        self.train_log = QTextEdit()
        self.train_log.setReadOnly(True)
        self.train_log.setMinimumHeight(200)
        layout.addWidget(self.train_log)
        
        widget.setLayout(layout)
        return widget
    
    def create_prediction_tab(self):
        """Create prediction tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Model selection
        model_layout = QHBoxLayout()
        model_label = QLabel("Select Model:")
        self.model_select = QComboBox()
        self.model_select.addItem("SVM", "svm")
        self.model_select.addItem("Random Forest", "rf")
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_select)
        model_layout.addStretch()
        layout.addLayout(model_layout)
        
        # Audio file selector
        file_layout = QHBoxLayout()
        file_label = QLabel("Audio File:")
        self.audio_file_input = QLineEdit()
        self.audio_file_input.setPlaceholderText("Select audio file to classify")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.select_audio_file)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.audio_file_input)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        layout.addSpacing(15)
        
        # Predict button
        self.predict_btn = QPushButton("🔮 Predict")
        self.predict_btn.setMinimumHeight(50)
        self.predict_btn.setFont(QFont('Arial', 12, QFont.Bold))
        self.predict_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.predict_btn.clicked.connect(self.make_prediction)
        layout.addWidget(self.predict_btn)
        
        # Result display
        result_label = QLabel("Prediction Result:")
        layout.addWidget(result_label)
        
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setMinimumHeight(150)
        self.result_display.setStyleSheet("""
            QTextEdit {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                color: #4CAF50;
            }
        """)
        layout.addWidget(self.result_display)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_visualization_tab(self):
        """Create visualization tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Audio file selector
        file_layout = QHBoxLayout()
        file_label = QLabel("Audio File:")
        self.viz_audio_input = QLineEdit()
        self.viz_audio_input.setPlaceholderText("Select audio file to visualize")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.select_viz_audio_file)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.viz_audio_input)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        # Visualization type selector
        viz_layout = QHBoxLayout()
        viz_label = QLabel("Visualization Type:")
        self.viz_combo = QComboBox()
        self.viz_combo.addItems(['Spectrogram', 'MFCC', 'Waveform'])
        viz_layout.addWidget(viz_label)
        viz_layout.addWidget(self.viz_combo)
        viz_layout.addStretch()
        layout.addLayout(viz_layout)
        
        # Visualize button
        viz_btn = QPushButton("📊 Generate Visualization")
        viz_btn.setMinimumHeight(40)
        viz_btn.setFont(QFont('Arial', 11, QFont.Bold))
        viz_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        viz_btn.clicked.connect(self.generate_visualization)
        layout.addWidget(viz_btn)
        
        # Canvas for matplotlib
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        widget.setLayout(layout)
        return widget
    
    def show_page(self, index):
        """Show specific page"""
        self.content.setCurrentIndex(index)
    
    def select_data_directory(self):
        """Select data directory"""
        directory = QFileDialog.getExistingDirectory(self, "Select Data Directory")
        if directory:
            self.data_dir_input.setText(directory)
    
    def select_audio_file(self):
        """Select audio file for prediction"""
        file, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "WAV Files (*.wav)")
        if file:
            self.audio_file_input.setText(file)
    
    def select_viz_audio_file(self):
        """Select audio file for visualization"""
        file, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "WAV Files (*.wav)")
        if file:
            self.viz_audio_input.setText(file)
    
    def start_training(self):
        """Start model training"""
        data_dir = self.data_dir_input.text().strip()
        
        if not data_dir:
            QMessageBox.warning(self, 'Error', 'Please select a data directory!')
            return
        
        if not Path(data_dir).exists():
            QMessageBox.warning(self, 'Error', 'Directory does not exist!')
            return
        
        model_type = self.model_combo.currentText().lower()
        if model_type == 'random forest':
            model_type = 'random_forest'
        
        # Disable button
        self.train_btn.setEnabled(False)
        self.train_log.clear()
        self.train_log.append("Starting training...\n")
        
        # Start worker
        self.training_worker = TrainingWorker(data_dir, model_type)
        self.training_worker.progress.connect(self.update_progress)
        self.training_worker.finished.connect(self.training_finished)
        self.training_worker.start()
    
    def update_progress(self, value):
        """Update training progress"""
        self.progress_bar.setValue(value)
        self.train_log.append(f"Progress: {value}%")
    
    def training_finished(self, success, message, accuracy=0.0):
        """Handle training completion"""
        self.train_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, 'Success', message)
            self.user_manager.save_model_for_user(self.model_combo.currentText())
        else:
            QMessageBox.critical(self, 'Error', message)
        self.train_log.append(message)
    
    def make_prediction(self):
        """Make prediction on audio file"""
        audio_file = self.audio_file_input.text().strip()
        model_type = self.model_select.currentData()
        
        if not audio_file:
            QMessageBox.warning(self, 'Error', 'Please select an audio file!')
            return
        
        if not Path(audio_file).exists():
            QMessageBox.warning(self, 'Error', 'Audio file does not exist!')
            return
        
        model_path = f'models/{model_type}_model.pkl'
        
        if not Path(model_path).exists():
            QMessageBox.warning(self, 'Prediction Error', 
                f'Model not found!\n\nPlease:\n1. Go to Training tab\n2. Select data directory (data/raw/)\n3. Click Train Model\n4. Try predicting again')
            return
        
        try:
            # Create classifier and explicitly load model
            classifier = UnderwaterSoundClassifier()
            classifier.load_model(model_path)
            
            # Verify model is properly loaded
            if classifier.model is None:
                QMessageBox.warning(self, 'Prediction Error', 
                    'Model is not properly trained.\n\nPlease:\n1. Go to Training tab\n2. Select data directory (data/raw/)\n3. Click Train Model\n4. Try predicting again')
                return
            
            if classifier.scaler is None or not hasattr(classifier.scaler, 'mean_'):
                QMessageBox.warning(self, 'Prediction Error', 
                    'Model is not properly trained.\n\nPlease:\n1. Go to Training tab\n2. Select data directory (data/raw/)\n3. Click Train Model\n4. Try predicting again')
                return
            
            # Make prediction
            prediction = classifier.predict(audio_file)
            
            self.result_display.setText(f"""
🎯 PREDICTION RESULT

File: {Path(audio_file).name}
Model: {self.model_select.currentText()}

Predicted Class: {prediction}

✅ Prediction successful!
            """)
        except Exception as e:
            error_msg = str(e)
            if 'not fitted' in error_msg:
                QMessageBox.critical(self, 'Prediction Error', 
                    'Model is not properly trained.\n\nPlease:\n1. Go to Training tab\n2. Select data directory (data/raw/)\n3. Click Train Model\n4. Try predicting again')
            else:
                QMessageBox.critical(self, 'Prediction Error', error_msg)
    
    def generate_visualization(self):
        """Generate audio visualization"""
        audio_file = self.viz_audio_input.text().strip()
        viz_type = self.viz_combo.currentText()
        
        if not audio_file:
            QMessageBox.warning(self, 'Error', 'Please select an audio file!')
            return
        
        if not Path(audio_file).exists():
            QMessageBox.warning(self, 'Error', 'Audio file does not exist!')
            return
        
        try:
            classifier = UnderwaterSoundClassifier()
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            if viz_type == 'Spectrogram':
                classifier.plot_spectrogram(audio_file, ax=ax)
            elif viz_type == 'MFCC':
                classifier.plot_mfcc(audio_file, ax=ax)
            else:
                # Waveform
                import librosa
                audio, sr = librosa.load(audio_file, sr=16000)
                ax.plot(audio)
                ax.set_title('Waveform')
                ax.set_xlabel('Sample')
                ax.set_ylabel('Amplitude')
            
            self.canvas.draw()
            QMessageBox.information(self, 'Success', f'{viz_type} visualization generated!')
        except Exception as e:
            QMessageBox.critical(self, 'Visualization Error', str(e))
    
    def logout(self):
        """Logout user"""
        reply = QMessageBox.question(self, 'Confirm Logout', 'Are you sure you want to logout?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.user_manager.logout()
            self.close()
    
    def set_style(self):
        """Set application style"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                border-radius: 4px 4px 0 0;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
            QPushButton {
                border-radius: 4px;
            }
            QComboBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)


# For importing
from PyQt5.QtWidgets import QLineEdit
