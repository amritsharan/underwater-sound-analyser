"""
Login Screen for Desktop Application
Handles user authentication UI
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTabWidget, QMessageBox,
                             QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPixmap
from desktop.utils.user_manager import user_manager


class LoginScreen(QWidget):
    """Login and Signup screen"""
    
    login_success = pyqtSignal(str)  # Signal emitted when login successful
    
    def __init__(self):
        """Initialize login screen"""
        super().__init__()
        self.user_manager = user_manager
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle('Underwater Sound Classifier - Login')
        self.setGeometry(100, 100, 400, 350)
        self.set_style()
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel('🐋 Underwater Sound Classifier')
        header.setFont(QFont('Arial', 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        subtitle = QLabel('Classify underwater audio with ML')
        subtitle.setFont(QFont('Arial', 10))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666; margin-bottom: 20px;")
        main_layout.addWidget(subtitle)
        
        # Tab widget for login/signup
        self.tabs = QTabWidget()
        
        # Login tab
        login_widget = self.create_login_tab()
        self.tabs.addTab(login_widget, 'Login')
        
        # Signup tab
        signup_widget = self.create_signup_tab()
        self.tabs.addTab(signup_widget, 'Sign Up')
        
        main_layout.addWidget(self.tabs)
        
        self.setLayout(main_layout)
    
    def create_login_tab(self):
        """Create login tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Username input
        username_label = QLabel('Username:')
        username_label.setFont(QFont('Arial', 10))
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText('Enter your username')
        self.login_username.setMinimumHeight(35)
        layout.addWidget(username_label)
        layout.addWidget(self.login_username)
        
        # Password input
        password_label = QLabel('Password:')
        password_label.setFont(QFont('Arial', 10))
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText('Enter your password')
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setMinimumHeight(35)
        layout.addWidget(password_label)
        layout.addWidget(self.login_password)
        
        # Remember me checkbox (decorative)
        layout.addSpacing(10)
        
        # Login button
        login_btn = QPushButton('Login')
        login_btn.setMinimumHeight(40)
        login_btn.setFont(QFont('Arial', 11, QFont.Bold))
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        # Demo account info
        demo_info = QLabel('Demo: username=demo, password=demo123')
        demo_info.setStyleSheet("color: #999; font-size: 9px; margin-top: 10px;")
        demo_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(demo_info)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_signup_tab(self):
        """Create signup tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Username input
        username_label = QLabel('Username:')
        username_label.setFont(QFont('Arial', 10))
        self.signup_username = QLineEdit()
        self.signup_username.setPlaceholderText('Choose a username (3+ characters)')
        self.signup_username.setMinimumHeight(35)
        layout.addWidget(username_label)
        layout.addWidget(self.signup_username)
        
        # Password input
        password_label = QLabel('Password:')
        password_label.setFont(QFont('Arial', 10))
        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText('Choose a password (4+ characters)')
        self.signup_password.setEchoMode(QLineEdit.Password)
        self.signup_password.setMinimumHeight(35)
        layout.addWidget(password_label)
        layout.addWidget(self.signup_password)
        
        # Confirm password
        confirm_label = QLabel('Confirm Password:')
        confirm_label.setFont(QFont('Arial', 10))
        self.signup_confirm = QLineEdit()
        self.signup_confirm.setPlaceholderText('Confirm your password')
        self.signup_confirm.setEchoMode(QLineEdit.Password)
        self.signup_confirm.setMinimumHeight(35)
        layout.addWidget(confirm_label)
        layout.addWidget(self.signup_confirm)
        
        layout.addSpacing(10)
        
        # Signup button
        signup_btn = QPushButton('Create Account')
        signup_btn.setMinimumHeight(40)
        signup_btn.setFont(QFont('Arial', 11, QFont.Bold))
        signup_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        signup_btn.clicked.connect(self.handle_signup)
        layout.addWidget(signup_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def handle_login(self):
        """Handle login button click"""
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password!')
            return
        
        success, message = self.user_manager.login(username, password)
        
        if success:
            QMessageBox.information(self, 'Success', message)
            self.login_success.emit(username)
        else:
            QMessageBox.warning(self, 'Login Failed', message)
    
    def handle_signup(self):
        """Handle signup button click"""
        username = self.signup_username.text().strip()
        password = self.signup_password.text().strip()
        confirm = self.signup_confirm.text().strip()
        
        if not username or not password or not confirm:
            QMessageBox.warning(self, 'Error', 'Please fill all fields!')
            return
        
        if password != confirm:
            QMessageBox.warning(self, 'Error', 'Passwords do not match!')
            return
        
        success, message = self.user_manager.signup(username, password)
        
        if success:
            QMessageBox.information(self, 'Success', message)
            # Switch to login tab
            self.tabs.setCurrentIndex(0)
            # Clear fields
            self.login_username.setText(username)
            self.login_password.clear()
            self.signup_username.clear()
            self.signup_password.clear()
            self.signup_confirm.clear()
        else:
            QMessageBox.warning(self, 'Signup Failed', message)
    
    def set_style(self):
        """Set application style"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial;
            }
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
                outline: none;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 20px;
                margin-right: 2px;
                border-radius: 4px 4px 0 0;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
            QMessageBox {
                background-color: #f5f5f5;
            }
        """)
