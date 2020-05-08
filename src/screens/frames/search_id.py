import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from .base_frame import BaseFrame
from .status_bar import StatusBarFrame

class SearchIDFrame(BaseFrame):
	searcher = None
	run_html = None
	search_res = None
	
	def init_widgets(self):
		self.entry = tk.Entry(self)
		self.btn = tk.Button(self, text="Search...")
		self.stringvar = tk.StringVar()
		self.label = tk.Label(self, text="...", anchor="nw", justify=tk.LEFT, textvariable=self.stringvar)
		self.status = StatusBarFrame(self)
		self.entry.place(relx=0, rely=0, relwidth=1, relheight=0.3)
		self.status.place(relx=0, rely=0.3, relheight=0.4)
		self.label.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)
		
	def bind_commands(self):
		self.entry.bind("<Return>", self.start_search)
		
	def init_searcher(self, searcher):
		self.searcher = searcher
	
	def init_run_html(self, run_html):
		self.run_html = run_html
	
	def start_search(self, event):
		self.status.start()
		self.stringvar.set("Start searching...")
		id_name = self.entry.get().strip()
		self.search_res = self.searcher.search_id(id_name)
		self.status.stop()
		if self.search_res[0] != "net":
			self.stringvar.set(f"Found on {res[0]}, run html viewer...")
			self.run_html(self.search_res[0], self.search_res[1])
			# self.btn.configure(state=tk.NORMAL)
		else:
			res = messagebox.askyesno(
				"Search on net", 
				f"Can't find '{self.entry.get()}' on local storage and on server, try to search on internet?"
			)
			if res:
				self.stringvar.set(f"Run browser...")
				self.searcher.open_in_browser(id_name)
				self.stringvar.set(f"Browser was runned")
			else:
				self.stringvar.set(f"Searching was reset")
		self.master.lift()
		