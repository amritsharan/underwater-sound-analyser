"""
Main Desktop Application Entry Point
Underwater Sound Classifier Desktop App
"""

import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtCore import Qt

from desktop.ui.login import LoginScreen
from desktop.ui.dashboard import Dashboard
from desktop.utils.user_manager import user_manager


class MainApp(QStackedWidget):
    """Main application that switches between login and dashboard"""
    
    def __init__(self):
        """Initialize main app"""
        super().__init__()
        self.setWindowTitle('🐋 Underwater Sound Classifier')
        self.setGeometry(100, 100, 1200, 700)
        
        # Create login screen
        self.login_screen = LoginScreen()
        self.login_screen.login_success.connect(self.show_dashboard)
        self.addWidget(self.login_screen)
        
        # Dashboard placeholder
        self.dashboard = None
        
        # Show login first
        self.setCurrentWidget(self.login_screen)
        self.show()
    
    def show_dashboard(self, username):
        """Show dashboard after successful login"""
        # Create dashboard
        self.dashboard = Dashboard(username)
        self.dashboard.destroyed.connect(self.show_login)
        
        # Hide login
        self.login_screen.hide()
        self.dashboard.show()
    
    def show_login(self):
        """Show login after logout"""
        self.login_screen.show()
        self.login_screen.login_username.clear()
        self.login_screen.login_password.clear()
        self.login_screen.signup_username.clear()
        self.login_screen.signup_password.clear()
        self.login_screen.signup_confirm.clear()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName('Underwater Sound Classifier')
    app.setApplicationVersion('1.0.0')
    
    # Create and show main app
    main_app = MainApp()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
