import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter import messagebox
import codecs
from .base_frame import BaseFrame
from .color.color_scheme import file_content_color_scheme as color_scheme
from .color.color_scheme import file_content_select_bg as select_bg
from .tokenizer.tokenizer import Tokenizer
from math import *
import re

# отображение текста файла
class FileContentFrame(BaseFrame):
	text = None # виджет отображения текста
	file_path = None # путь до файла
	file_name = None
	selection_pos = "1.0"
	search_color = "#9ed9ae"
	
	def __init__(self, master, file_name, file_path, command, right_command, x=0, y=0, width=1, height=1):
		self.file_name = file_name
		self.file_path = file_path
		super().__init__(master, x, y, width, height)
		self.text.tag_config("select", background=select_bg)
		for key in color_scheme:
			self.text.tag_config(key, foreground=color_scheme[key])
			def make_lambda(k):
				return lambda e: command(e, k)
			if key == "line" or key == "default":
				continue
			self.text.tag_bind(key, "<Double-Button-1>", make_lambda(key))
			self.text.tag_bind(key, "<Enter>", self.on_enter)
			self.text.tag_bind(key, "<Leave>", self.on_leave)
		self.text.bind("<Control-MouseWheel>", self.resize)
		self.text.bind("<Button-3>", right_command)
			
	def init_widgets(self):
		self.font = tkFont.Font(family=None, size=8)
		self.text = tk.Text(self, wrap=tk.NONE, font=self.font, cursor="arrow")
		
		y_scroll = tk.Scrollbar(self, command=self.text.yview)
		x_scroll = tk.Scrollbar(self, orient="horizontal", command=self.text.xview)
		
		self.text.tag_config("search", background = self.search_color)
		
		self.text["yscrollcommand"] = y_scroll.set
		self.text["xscrollcommand"] = x_scroll.set
		self.text.place(relx=0, rely=0, relwidth=0.97, relheight=0.97)
		y_scroll.place(relx=0.97, relwidth=0.03, relheight=1)
		x_scroll.place(relx=0, rely=0.97, relwidth=1, relheight=0.03)
	
	def on_enter(self, event):
		for tag in self.text.tag_names():
			if tag == "default" or "comment" in tag:
				continue
			interval = self.get_interval_under(event, tag)
			if interval:
				self.text.tag_add("select", interval[0], interval[1])
		
	def on_leave(self, event):
		self.text.tag_remove("select", "1.0", "end")
	
	def resize(self, event):
		font_size = int(self.font.cget("size")) + event.delta / fabs(event.delta)
		if font_size <= 0:
			font_size = 1
		self.font["size"] = int(font_size)
		return "break"
	
	def show(self, id_table):
		try:
			file = codecs.open(self.file_path, "r", "utf_8_sig")
			# file = codecs.open(file_path, "r", "utf_8_sig", errors="ignore")
			# file = codecs.open(self.file_path, "r")
		except:
			messagebox.showerror("Open file error", f"Can't open file {self.file_path}")
			return False
		self.text.config(state=tk.NORMAL)
		self.text.delete(1.0, tk.END)
		try:
			self.highlight(file, id_table)
		except:
			try:
				file = codecs.open(self.file_path, "r")
				# file = codecs.open(file_path, "r", "utf_8_sig", errors="ignore")
				# file = codecs.open(self.file_path, "r")
			except:
				messagebox.showerror("Open file error", f"Can't open file {self.file_path}")
				return False
			self.text.config(state=tk.NORMAL)
			self.text.delete(1.0, tk.END)
			try:
				self.highlight(file, id_table)
			except:
				messagebox.showerror("Codec error", f"Can't open file {self.file_path}")
				return False
		file.close()
		self.text.config(state=tk.DISABLED)
		return True
	
	def highlight(self, file, id_table):
		tokenizer = Tokenizer()
		t_value = ""
		t_type = None
		
		for num, line in enumerate(file):
			self.text.insert(tk.END, "%+4s%2s"%(num, ""), "line")
			i = 0
			while i < len(line):
				t_value += line[i]
				now_type = tokenizer.get_token_type(t_value)
				if not now_type or i+1 == len(line):
					if t_type:
						if i+1 < len(line):
							i -= 1
							t_value = t_value[:-1]
						t_type = self.specify(t_value, t_type, tokenizer, id_table)
						self.text.insert(tk.END, t_value, t_type)
					else:
						self.text.insert(tk.END, t_value, "default")
					t_value = ""
				t_type = now_type
				i += 1
	
	def specify(self, value, type, tokenizer, id_table):
		if tokenizer.is_keyword(value):
			return "keyword"
		if type == "id" and id_table:
			if id_table.has_record_in_file(self.file_name, value):
				return "id"
			elif id_table.has_record(value):
				return "another_file_id"
			return "unknown_id"	
		return type
	
	def get_interval_under(self, event, tag):
		index = self.text.index("@%s,%s" % (event.x, event.y))
		tag_indices = list(self.text.tag_ranges(tag))
		for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
			if self.text.compare(start, '<=', index) and self.text.compare(index, '<', end):
				return (start, end)
		return None
	
	def get_word_under(self, event, tag):
		index = self.text.index("@%s,%s" % (event.x, event.y))
		tag_indices = list(self.text.tag_ranges(tag))
		for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
			if self.text.compare(start, '<=', index) and self.text.compare(index, '<', end):
				return self.text.get(start, end)
		return None
		
	def search(self, pattern):
		self.text.tag_remove("search", "1.0", "end")
		start = self.selection_pos
		end = self.text.index(tk.END)
		string = self.text.get(start, end)
		if string:
			last_end = "1.0"
			match = re.search(pattern, string)
			if match:
				m_start = self.text.index("%s+%dc"%(start, match.start()))
				m_end = self.text.index("%s+%dc" % (start, match.end()))
				self.text.tag_add("search", m_start, m_end)
				self.selection_pos = m_end
				self.text.see(m_start)
				return True
			else:
				self.selection_pos = "1.0"
		return False
		
	def selected_text(self):
		try:
			text = self.text.selection_get()
		except:
			return None
		return text

# отображение открываемых пользователем файлов
class FilesFrame(BaseFrame):
	notebook = None
	frames = None
	search_text = None
	now_frame = None
	def init_widgets(self):
		self.notebook = ttk.Notebook(self)
		self.search_text = tk.StringVar()
		self.search_entry = tk.Entry(self, textvariable=self.search_text)
		self.search_entry.place(relx=0, rely=0, relwidth=0.5, relheight=0.03)
		self.notebook.place(relx=0, rely=0.03, relwidth=1, relheight=0.97)
		self.notebook.bind("<Button-3>", self.notebook_right_click)
		self.frames = []
	
	def bind_commands(self):
		self.search_entry.bind("<Return>", self.start_search)
		
	def start_search(self, event):
		frame = self.get_current()
		if not frame:
			return
		res = frame.search(self.search_text.get())
		if not res:
			label = tk.Label(self, justify=tk.LEFT, text="No results...", foreground="#c22e21", anchor="nw")
			label.place(relx=0.5, rely=0, relwidth=0.4, relheight=0.03)
			self.after(1000, label.place_forget)			
	
	def notebook_right_click(self, event):
		if not len(self.notebook.tabs()):
			return
		popup = tk.Menu(self, tearoff=0)
		popup.add_command(label="Close tab", command=self.close_tab)
		popup.add_command(label="Close all tabs", command=self.close_all_tabs)
		popup.tk_popup(event.x_root, event.y_root, 0)
		
	def close_tab(self):
		del self.frames[self.notebook.index("current")] 
		self.notebook.forget(self.notebook.select())
		
	def close_all_tabs(self):
		self.frames = []
		for tab in self.notebook.tabs():
			self.notebook.forget(tab)
			
	def open_file(self, file_name, file_path, content_click, right_content_click, id_table):
		for i in self.notebook.tabs():
			if self.notebook.tab(i, "text") == file_name:
				self.notebook.select(i)
				return
		tab_names = [self.notebook.tab(i, "text") for i in self.notebook.tabs()]
		if file_name in tab_names:
			return
		frame = FileContentFrame(self.notebook, file_name, file_path, content_click, right_content_click)
		if not frame.show(id_table):
			return
		self.notebook.add(frame, text=file_name)
		self.notebook.select(frame)
		self.frames.append(frame)
	
	def get_tab_name(self, event):
		if not len(self.notebook.tabs()):
			return
		clicked_tab = self.notebook.tk.call(self.notebook._w, "identify", "tab", event.x, event.y)
		if type(clicked_tab) == str:
			return
		return self.notebook.tab(clicked_tab, "text")
		
	def get_selected_text(self):
		frame = self.get_current()
		return frame.selected_text()
	
	def get_current(self):
		if not len(self.notebook.tabs()):
			return
		return self.frames[ self.notebook.index("current") ]