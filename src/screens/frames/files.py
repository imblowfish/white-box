import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import codecs
from .base_frame import BaseFrame
from .color.color_scheme import file_content_color_scheme as color_scheme

# отображение текста файла
class FileContentFrame(BaseFrame):
	text = None # виджет отображения текста
	file_path = None # путь до файла
	def __init__(self, master, file_path, command, x=0, y=0, width=1, height=1):
		self.file_path = file_path
		super().__init__(master, x, y, width, height)
	def init_widgets(self):
		self.text = tk.Text(self, wrap=tk.NONE)
		self.text.insert(tk.END, self.file_path) 
		self.text.place(relx=0, rely=0, relwidth=1, relheight=1)
	def bind_commands(self):
		for key in color_scheme:
			self.text.tag_config(key, foreground=color_scheme[key])
			self.text.tag_bind(key, "<Button-1>", lambda e: command(e, key))
	def show(self):
		try:
			file = codecs.open(self.file_path, "r", "utf_8_sig")
		except:
			messagebox.showerror("Open file error", f"Can't open file {self.file_path}")
			return False
		self.text.delete(1.0, tk.END)
		for line in file:
			# отображение содержимого файла с подсветкой синтаксиса
			self.text.insert(tk.END, line)
		file.close()
		return True
		
# отображение открываемых пользователем файлов
class FilesFrame(BaseFrame):
	notebook = None
	def init_widgets(self):
		self.notebook = ttk.Notebook(self)
		self.notebook.place(relx=0, rely=0, relwidth=1, relheight=1)
	# добавление нового файла в notebook
	def open_file(self, file_name, file_path, command):
		frame = FileContentFrame(self.notebook, file_path, command)
		if not frame.show():
			return
		self.notebook.add(frame, text=file_name)
		self.notebook.select(frame)