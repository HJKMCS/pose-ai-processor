"""
Reusable CustomTkinter UI components.
Pre-styled widgets for consistency.
Easy to customize and reuse.
"""

import customtkinter as ctk
from tkinter import ttk
import constants as C

class StyledButton(ctk.CTkButton):
    """Pre-styled button with consistent appearance."""
    
    def __init__(self, master=None, **kwargs):
        # Set defaults
        if "corner_radius" not in kwargs:
            kwargs["corner_radius"] = 8
        if "height" not in kwargs:
            kwargs["height"] = 40
        if "font" not in kwargs:
            kwargs["font"] = ("Arial", 14, "bold")
        
        super().__init__(master, **kwargs)

class StyledLabel(ctk.CTkLabel):
    """Pre-styled label."""
    
    def __init__(self, master=None, **kwargs):
        if "font" not in kwargs:
            kwargs["font"] = ("Arial", 12)
        
        super().__init__(master, **kwargs)

class ProgressFrame(ctk.CTkFrame):
    """Frame with progress bar and status label."""
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=(10, 5))
        
        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=400,
            mode="determinate"
        )
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)
        
        self.percent_label = ctk.CTkLabel(
            self,
            text="0%",
            font=("Arial", 10, "bold"),
            text_color="gray"
        )
        self.percent_label.pack(pady=(5, 10))
    
    def update_progress(self, percent: float, status: str = ""):
        """Update progress bar and labels."""
        self.progress_bar.set(percent / 100.0)
        self.percent_label.configure(text=f"{percent:.1f}%")
        if status:
            self.status_label.configure(text=status)

class ConfigFrame(ctk.CTkScrollableFrame):
    """Scrollable frame for LM configuration settings."""
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup configuration UI elements."""
        # Model selection
        ctk.CTkLabel(self, text="Model Settings", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.model_entry = ctk.CTkEntry(self, width=300, placeholder_text="Model name")
        self.model_entry.pack(pady=5)
        
        # Temperature
        ctk.CTkLabel(self, text="Temperature (creativity):").pack(pady=(15, 5))
        self.temp_slider = ctk.CTkSlider(self, from_=0, to=2, number_of_steps=20)
        self.temp_slider.pack(pady=5)
        self.temp_slider.set(0.7)
        
        self.temp_label = ctk.CTkLabel(self, text="0.7", font=("Arial", 10))
        self.temp_label.pack()
        
        # Top K
        ctk.CTkLabel(self, text="Top K:").pack(pady=(15, 5))
        self.topk_slider = ctk.CTkSlider(self, from_=1, to=100, number_of_steps=99)
        self.topk_slider.pack(pady=5)
        self.topk_slider.set(40)
        
        self.topk_label = ctk.CTkLabel(self, text="40", font=("Arial", 10))
        self.topk_label.pack()
        
        # Top P
        ctk.CTkLabel(self, text="Top P:").pack(pady=(15, 5))
        self.topp_slider = ctk.CTkSlider(self, from_=0, to=1, number_of_steps=100)
        self.topp_slider.pack(pady=5)
        self.topp_slider.set(0.9)
        
        self.topp_label = ctk.CTkLabel(self, text="0.9", font=("Arial", 10))
        self.topp_label.pack()
        
        # Max Tokens
        ctk.CTkLabel(self, text="Max Tokens:").pack(pady=(15, 5))
        self.maxtokens_slider = ctk.CTkSlider(self, from_=64, to=2048, number_of_steps=20)
        self.maxtokens_slider.pack(pady=5)
        self.maxtokens_slider.set(512)
        
        self.maxtokens_label = ctk.CTkLabel(self, text="512", font=("Arial", 10))
        self.maxtokens_label.pack()
        
        # Penalty Delay
        ctk.CTkLabel(self, text="Penalty Delay (higher = more strict):").pack(pady=(15, 5))
        self.penalty_slider = ctk.CTkSlider(self, from_=0, to=2, number_of_steps=20)
        self.penalty_slider.pack(pady=5)
        self.penalty_slider.set(1.0)
        
        self.penalty_label = ctk.CTkLabel(self, text="1.0", font=("Arial", 10))
        self.penalty_label.pack()
        
        # System Prompt
        ctk.CTkLabel(self, text="System Prompt:", font=("Arial", 14, "bold")).pack(pady=(20, 5))
        self.system_prompt_text = ctk.CTkTextbox(self, width=400, height=150)
        self.system_prompt_text.pack(pady=5)
        self.system_prompt_text.insert("0.0", "You are a posture analysis expert.")
    
    def get_config_values(self) -> dict:
        """Get all configuration values as dictionary."""
        return {
            "model": self.model_entry.get(),
            "temperature": self.temp_slider.get(),
            "top_k": int(self.topk_slider.get()),
            "top_p": self.topp_slider.get(),
            "max_tokens": int(self.maxtokens_slider.get()),
            "penalty_delay": self.penalty_slider.get(),
            "system_prompt": self.system_prompt_text.get("0.0", "end-1c").strip()
        }
    
    def update_labels(self):
        """Update all value labels."""
        self.temp_label.configure(text=f"{self.temp_slider.get():.2f}")
        self.topk_label.configure(text=f"{int(self.topk_slider.get())}")
        self.topp_label.configure(text=f"{self.topp_slider.get():.2f}")
        self.maxtokens_label.configure(text=f"{int(self.maxtokens_slider.get())}")
        self.penalty_label.configure(text=f"{self.penalty_slider.get():.2f}")

class VideoInfoFrame(ctk.CTkFrame):
    """Frame to display video information."""
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.file_label = ctk.CTkLabel(
            self,
            text="No video selected",
            font=("Arial", 12, "bold"),
            wraplength=400
        )
        self.file_label.pack(pady=10)
        
        self.info_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 10),
            text_color="gray"
        )
        self.info_label.pack(pady=5)
    
    def update_info(self, filename: str, info: str = ""):
        """Update video information display."""
        self.file_label.configure(text=filename)
        self.info_label.configure(text=info)

class ResultFrame(ctk.CTkScrollableFrame):
    """Frame to display AI analysis results."""
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.result_text = ctk.CTkTextbox(
            self,
            width=500,
            height=300,
            font=("Consolas", 11)
        )
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def display_result(self, text: str):
        """Display analysis result."""
        self.result_text.delete("0.0", "end")
        self.result_text.insert("0.0", text)