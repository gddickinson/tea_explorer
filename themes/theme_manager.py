"""
Theme System - Modern UI Theming
Provides dark mode, light mode, and custom theme support
"""

from dataclasses import dataclass
from typing import Dict, Any
import json
from pathlib import Path


@dataclass
class ColorScheme:
    """Color scheme for application theme"""
    
    # Background colors
    bg_primary: str
    bg_secondary: str
    bg_tertiary: str
    
    # Foreground/text colors
    fg_primary: str
    fg_secondary: str
    fg_heading: str
    
    # Accent colors
    accent_primary: str
    accent_secondary: str
    accent_success: str
    accent_warning: str
    accent_error: str
    
    # Border and separator colors
    border_color: str
    separator_color: str
    
    # Widget-specific colors
    button_bg: str
    button_fg: str
    button_hover: str
    entry_bg: str
    entry_fg: str
    listbox_bg: str
    listbox_fg: str
    listbox_select_bg: str
    listbox_select_fg: str


# Dark theme color scheme
DARK_THEME = ColorScheme(
    # Backgrounds - dark grays
    bg_primary="#1e1e1e",
    bg_secondary="#2d2d2d",
    bg_tertiary="#3c3c3c",
    
    # Foregrounds - light grays/white
    fg_primary="#ffffff",
    fg_secondary="#b0b0b0",
    fg_heading="#ffffff",
    
    # Accents - vibrant colors
    accent_primary="#4a9eff",      # Blue
    accent_secondary="#9945ff",     # Purple
    accent_success="#00c853",       # Green
    accent_warning="#ffa726",       # Orange
    accent_error="#ff5252",         # Red
    
    # Borders
    border_color="#4a4a4a",
    separator_color="#3a3a3a",
    
    # Widgets
    button_bg="#4a9eff",
    button_fg="#ffffff",
    button_hover="#6bb3ff",
    entry_bg="#2d2d2d",
    entry_fg="#ffffff",
    listbox_bg="#2d2d2d",
    listbox_fg="#ffffff",
    listbox_select_bg="#4a9eff",
    listbox_select_fg="#ffffff",
)


# Light theme color scheme
LIGHT_THEME = ColorScheme(
    # Backgrounds - whites/light grays
    bg_primary="#ffffff",
    bg_secondary="#f5f5f5",
    bg_tertiary="#e0e0e0",
    
    # Foregrounds - dark grays/black
    fg_primary="#212121",
    fg_secondary="#616161",
    fg_heading="#000000",
    
    # Accents - vibrant but slightly muted
    accent_primary="#1976d2",       # Blue
    accent_secondary="#7b1fa2",     # Purple
    accent_success="#388e3c",       # Green
    accent_warning="#f57c00",       # Orange
    accent_error="#d32f2f",         # Red
    
    # Borders
    border_color="#bdbdbd",
    separator_color="#e0e0e0",
    
    # Widgets
    button_bg="#1976d2",
    button_fg="#ffffff",
    button_hover="#1e88e5",
    entry_bg="#ffffff",
    entry_fg="#212121",
    listbox_bg="#ffffff",
    listbox_fg="#212121",
    listbox_select_bg="#1976d2",
    listbox_select_fg="#ffffff",
)


# Tea-inspired theme
TEA_THEME = ColorScheme(
    # Backgrounds - warm earth tones
    bg_primary="#f4f1e8",           # Cream
    bg_secondary="#e8dcc4",         # Light tan
    bg_tertiary="#d4c4a8",          # Tan
    
    # Foregrounds - dark browns
    fg_primary="#3e2723",           # Dark brown
    fg_secondary="#5d4037",         # Medium brown
    fg_heading="#1b0000",           # Almost black
    
    # Accents - tea colors
    accent_primary="#689f38",       # Green tea
    accent_secondary="#8d6e63",     # Oolong
    accent_success="#7cb342",       # Matcha
    accent_warning="#ff6f00",       # Pu-erh
    accent_error="#d32f2f",         # Red tea
    
    # Borders
    border_color="#bcaaa4",
    separator_color="#d7ccc8",
    
    # Widgets
    button_bg="#689f38",
    button_fg="#ffffff",
    button_hover="#7cb342",
    entry_bg="#ffffff",
    entry_fg="#3e2723",
    listbox_bg="#ffffff",
    listbox_fg="#3e2723",
    listbox_select_bg="#689f38",
    listbox_select_fg="#ffffff",
)


class ThemeManager:
    """
    Manages application themes
    Provides theme switching and persistence
    """
    
    THEMES = {
        'dark': DARK_THEME,
        'light': LIGHT_THEME,
        'tea': TEA_THEME,
    }
    
    def __init__(self, config_path: str = 'theme_config.json'):
        """
        Initialize theme manager
        
        Args:
            config_path: Path to theme configuration file
        """
        self.config_path = Path(config_path)
        self.current_theme_name = 'light'
        self.current_theme = LIGHT_THEME
        self.load_preferences()
    
    def get_theme(self, name: str = None) -> ColorScheme:
        """
        Get theme by name
        
        Args:
            name: Theme name, or None for current theme
            
        Returns:
            ColorScheme object
        """
        if name is None:
            return self.current_theme
        return self.THEMES.get(name, LIGHT_THEME)
    
    def set_theme(self, name: str):
        """
        Set current theme
        
        Args:
            name: Theme name
        """
        if name in self.THEMES:
            self.current_theme_name = name
            self.current_theme = self.THEMES[name]
            self.save_preferences()
    
    def get_theme_names(self) -> list:
        """Get list of available theme names"""
        return list(self.THEMES.keys())
    
    def save_preferences(self):
        """Save theme preferences to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump({'theme': self.current_theme_name}, f)
        except Exception as e:
            print(f"Could not save theme preferences: {e}")
    
    def load_preferences(self):
        """Load theme preferences from file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    theme_name = data.get('theme', 'light')
                    self.set_theme(theme_name)
        except Exception as e:
            print(f"Could not load theme preferences: {e}")
    
    def apply_to_widget(self, widget, widget_type: str = 'default'):
        """
        Apply current theme to a widget
        
        Args:
            widget: Tkinter widget
            widget_type: Type of widget (button, entry, listbox, etc.)
        """
        theme = self.current_theme
        
        try:
            if widget_type == 'frame' or widget_type == 'default':
                widget.configure(bg=theme.bg_primary)
            
            elif widget_type == 'label':
                widget.configure(
                    bg=theme.bg_primary,
                    fg=theme.fg_primary
                )
            
            elif widget_type == 'heading':
                widget.configure(
                    bg=theme.bg_primary,
                    fg=theme.fg_heading
                )
            
            elif widget_type == 'button':
                widget.configure(
                    bg=theme.button_bg,
                    fg=theme.button_fg,
                    activebackground=theme.button_hover,
                    activeforeground=theme.button_fg,
                    relief='flat',
                    borderwidth=0,
                    padx=12,
                    pady=6
                )
            
            elif widget_type == 'entry':
                widget.configure(
                    bg=theme.entry_bg,
                    fg=theme.entry_fg,
                    insertbackground=theme.fg_primary,
                    relief='solid',
                    borderwidth=1
                )
            
            elif widget_type == 'listbox':
                widget.configure(
                    bg=theme.listbox_bg,
                    fg=theme.listbox_fg,
                    selectbackground=theme.listbox_select_bg,
                    selectforeground=theme.listbox_select_fg,
                    relief='flat',
                    borderwidth=0
                )
            
            elif widget_type == 'text':
                widget.configure(
                    bg=theme.entry_bg,
                    fg=theme.entry_fg,
                    insertbackground=theme.fg_primary,
                    relief='flat',
                    borderwidth=1
                )
            
        except Exception as e:
            print(f"Could not apply theme to widget: {e}")
    
    def get_style_dict(self) -> Dict[str, Any]:
        """
        Get theme as dictionary for easy access
        
        Returns:
            Dictionary of theme colors
        """
        theme = self.current_theme
        return {
            'bg_primary': theme.bg_primary,
            'bg_secondary': theme.bg_secondary,
            'bg_tertiary': theme.bg_tertiary,
            'fg_primary': theme.fg_primary,
            'fg_secondary': theme.fg_secondary,
            'fg_heading': theme.fg_heading,
            'accent_primary': theme.accent_primary,
            'accent_secondary': theme.accent_secondary,
            'accent_success': theme.accent_success,
            'accent_warning': theme.accent_warning,
            'accent_error': theme.accent_error,
            'border_color': theme.border_color,
            'separator_color': theme.separator_color,
        }


# Global theme manager instance
theme_manager = ThemeManager()


if __name__ == '__main__':
    # Demo usage
    import tkinter as tk
    from tkinter import ttk
    
    root = tk.Tk()
    root.title("Theme Demo")
    root.geometry("600x400")
    
    # Create theme manager
    tm = ThemeManager()
    
    # Theme switcher
    def switch_theme(name):
        tm.set_theme(name)
        update_theme()
    
    def update_theme():
        # Apply theme to all widgets
        tm.apply_to_widget(root, 'frame')
        tm.apply_to_widget(title_label, 'heading')
        tm.apply_to_widget(desc_label, 'label')
        tm.apply_to_widget(entry, 'entry')
        tm.apply_to_widget(listbox, 'listbox')
        for btn in theme_buttons:
            tm.apply_to_widget(btn, 'button')
    
    # UI
    title_label = tk.Label(root, text="Theme System Demo", font=('', 16, 'bold'))
    title_label.pack(pady=10)
    
    desc_label = tk.Label(root, text="Choose a theme:")
    desc_label.pack(pady=5)
    
    # Theme buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    theme_buttons = []
    for theme_name in tm.get_theme_names():
        btn = tk.Button(
            button_frame,
            text=theme_name.title(),
            command=lambda n=theme_name: switch_theme(n)
        )
        btn.pack(side='left', padx=5)
        theme_buttons.append(btn)
    
    # Sample widgets
    entry = tk.Entry(root, width=40)
    entry.insert(0, "Sample text input")
    entry.pack(pady=10)
    
    listbox = tk.Listbox(root, height=10)
    for i in range(5):
        listbox.insert(tk.END, f"List item {i+1}")
    listbox.pack(pady=10, padx=20, fill='both', expand=True)
    
    # Apply initial theme
    update_theme()
    
    root.mainloop()
