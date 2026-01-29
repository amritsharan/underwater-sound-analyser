"""
User Management System for Desktop App
Handles user login, signup, and session management
"""

import json
import os
from pathlib import Path


class UserManager:
    """Manage user accounts (simple JSON-based storage)"""
    
    def __init__(self):
        """Initialize user manager"""
        self.users_file = Path.home() / '.underwater_classifier' / 'users.json'
        self.users_file.parent.mkdir(exist_ok=True)
        self.current_user = None
        self.load_users()
    
    def load_users(self):
        """Load users from JSON file"""
        if self.users_file.exists():
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def signup(self, username, password):
        """
        Register new user
        
        Parameters:
        -----------
        username : str
            Username to register
        password : str
            Password for account
            
        Returns:
        --------
        tuple : (bool, str)
            (success, message)
        """
        if username in self.users:
            return False, "Username already exists!"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters!"
        
        if len(password) < 4:
            return False, "Password must be at least 4 characters!"
        
        # Store user (plain text - no real auth needed)
        self.users[username] = {
            'password': password,
            'created': str(Path.cwd()),
            'models': []
        }
        
        self.save_users()
        return True, f"Account created successfully! Welcome {username}!"
    
    def login(self, username, password):
        """
        Login user
        
        Parameters:
        -----------
        username : str
            Username
        password : str
            Password
            
        Returns:
        --------
        tuple : (bool, str)
            (success, message)
        """
        if username not in self.users:
            return False, "Username not found!"
        
        if self.users[username]['password'] != password:
            return False, "Incorrect password!"
        
        self.current_user = username
        return True, f"Welcome back, {username}!"
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get current logged-in user"""
        return self.current_user
    
    def save_model_for_user(self, model_name):
        """Save model name for current user"""
        if self.current_user:
            if model_name not in self.users[self.current_user]['models']:
                self.users[self.current_user]['models'].append(model_name)
                self.save_users()
    
    def get_user_models(self):
        """Get all models for current user"""
        if self.current_user:
            return self.users[self.current_user].get('models', [])
        return []


# Global user manager instance
user_manager = UserManager()
