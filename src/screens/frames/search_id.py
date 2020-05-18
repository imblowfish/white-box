import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from .base_frame import BaseFrame
from .status_bar import StatusBarFrame

class SearchIDFrame(BaseFrame):
	searcher = None
	run_html = None
	search_res = None
	bg_color = "#3c3836"
	entry_color = "#f9f5f7"
	def init_widgets(self):
		self.entry = tk.Entry(self, bg=self.entry_color, fg="black")
		self.label = tk.Label(self, text="Input ID name and press ENTER:", font=(None, 10), bg=self.bg_color, fg="white")
		self.status = StatusBarFrame(self)
		self.label.place(relx=0, rely=0, relwidth=1, relheight=0.3)
		self.entry.place(relx=0, rely=0.3, relwidth=1, relheight=0.3)
		self.status.place(relx=0, rely=0.6, relheight=0.4)
		
	def bind_commands(self):
		self.entry.bind("<Return>", self.start_search)
		
	def init_searcher(self, searcher):
		self.searcher = searcher
	
	def init_run_html(self, run_html):
		self.run_html = run_html
	
	def start_search(self, event):
		self.status.start()
		id_name = self.entry.get().strip()
		self.search_res = self.searcher.search_id(id_name)
		self.status.stop()
		if self.search_res[0] != "net":
			self.run_html(self.search_res[0], self.search_res[1])
		else:
			res = messagebox.askyesno(
				"Search on net", 
				f"Can't find '{self.entry.get()}' on local storage and on server, try to search on internet?"
			)
			if res:
				self.searcher.open_in_browser(id_name)
		self.master.lift()
		