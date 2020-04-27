import tkinter as tk

class BaseFrame(tk.Frame):
	def __init__(self, master, x=0, y=0, width=1, height=1):
		tk.Frame.__init__(self, master)
		self.place(relx=x, rely=y, relwidth=width, relheight=height)
		self.init_widgets()
		self.bind_commands()
	def init_widgets(self):
		pass
	def bind_commands(self):
		pass
	def show(self, *args):
		pass