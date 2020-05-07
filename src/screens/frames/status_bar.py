import tkinter as tk
import tkinter.ttk as ttk
from .base_frame import BaseFrame

class StatusBarFrame(BaseFrame):
	def init_widgets(self):
		self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
		self.progress_bar.place(relx=0, rely=0, relwidth=1, relheight=1)
		
	def start(self):
		self.progress_bar.start()
		self.progress_bar.update_idletasks()
	def stop(self):
		self.progress_bar.stop()
	