import tkinter as tk
import tkinter.ttk as ttk
from .base_frame import BaseFrame

class LogFrame(BaseFrame):
	"""
		Отображение информации о работе системы
	"""
	stringvar = None
	bg_color = "#3c3836"
	def init_widgets(self):
		self.text = tk.Text(self, wrap=tk.NONE, font=(None, 7), bg = self.bg_color, fg="white")
		yscroll = tk.Scrollbar(self, command=self.text.yview)
		xscroll = tk.Scrollbar(self, command=self.text.xview, orient="horizontal")
		self.text["yscrollcommand"] = yscroll.set
		self.text["xscrollcommand"] = xscroll.set
		self.text.place(relx=0, rely=0, relwidth=0.93, relheight=0.93)
		yscroll.place(relx=0.93, rely=0, relwidth=0.07, relheight=1)
		xscroll.place(relx=0, rely=0.93, relwidth=1, relheight=0.07)
		self.insert("Log...")
	def insert(self, msg):
		self.text.insert(tk.END, msg+'\n')
		self.text.see(tk.END)