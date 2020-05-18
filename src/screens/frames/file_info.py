import tkinter as tk
import tkinter.ttk as ttk
from .base_frame import BaseFrame

class FileInfoFrame(BaseFrame):
	"""
		Фрэйм отображения информации о членах файла
	"""
	info_tree = None # дерево информации о файле
	# виды отношений
	kinds = {
		"Includes": "file", 
		"Included by": "file", 
		"Variables": "variable", 
		"Enums": "enum", 
		"Functions": "function", 
		"Classes": "class"
	}
	includes = None
	included_by = None
	vars = None
	classes = None
	funcs = None
	enums = None
	font_select_color = "#3c3836"
	select_color = "#b6c4db"
	font_color = "#f9f5f7"
	bg_color = "#3c3836"
		
	def init_widgets(self):
		self.info_tree = ttk.Treeview(self, style="Treeview.Heading")
		self.info_tree.heading("#0", text="File info")
		
		yscroll = tk.Scrollbar(self, command=self.info_tree.yview)
		xscroll = tk.Scrollbar(self, command=self.info_tree.xview, orient="horizontal")
		self.info_tree["yscrollcommand"] = yscroll.set
		self.info_tree["xscrollcommand"] = xscroll.set
		
		self.info_tree.tag_configure("selected", background=self.select_color, foreground=self.font_select_color)
		self.info_tree.tag_configure("unselected", background=self.bg_color, foreground=self.font_color)
		
		self.info_tree.place(relx=0, rely=0, relwidth=1, relheight=0.95)
		yscroll.place(relx=0.93, rely=0, relwidth=0.07, relheight=1)
		xscroll.place(relx=0, rely=0.95, relwidth=0.93, relheight=0.05)
		
	def bind_commands(self):
		self.info_tree.bind("<Button-1>", self.select_row)
		self.info_tree.bind("<FocusOut>", lambda e: self.reset_selection())
		
	def select_row(self, event):
		self.reset_selection()
		item_id = self.info_tree.identify("item", event.x, event.y)
		self.info_tree.item(item_id, tags=("selected"))
		
	def reset_selection(self, child=""):
		for child in self.info_tree.get_children(child):
			self.info_tree.item(child, tags=("unselected"))
			self.reset_selection(child)
	
	def show(self, record, id_table):
		self.clear()
		self.init_nodes()
		self.add_parents(record.parents_id, id_table)
		self.add_members(record.members_id, id_table)
		self.reset_selection()
	
	def clear(self):
		if not self.info_tree:
			return
		for node in self.info_tree.get_children():
			self.info_tree.delete(node)
	
	def init_nodes(self):
		self.includes = self.info_tree.insert("", "end", text="Includes", open=True)
		self.included_by = self.info_tree.insert("", "end", text="Included by", open=True)
		self.vars = self.info_tree.insert("", "end", text="Variables", open=True)
		self.enums = self.info_tree.insert("", "end", text="Enums", open=True)
		self.funcs = self.info_tree.insert("", "end", text="Functions", open=True)
		self.classes = self.info_tree.insert("", "end", text="Classes", open=True)
	
	def add_parents(self, parents_id, id_table):
		if not parents_id:
			return
		for id in parents_id:
			parent = id_table.get_record_by_id(id)
			# родителями файла могут быть только другие файлы
			self.info_tree.insert(self.includes, "end", text=parent.name, open=True)
		
	def add_members(self, members_id, id_table):
		if not members_id:
			return
		for id in members_id:
			member = id_table.get_record_by_id(id)
			if member.kind == "file":
				self.info_tree.insert(self.included_by, "end", text=member.name, open=True)
			elif member.kind == "variable":
				self.info_tree.insert(self.vars, "end", text=member.name, open=True)
			elif member.kind == "function":
				self.info_tree.insert(self.funcs, "end", text=member.name, open=True)
			elif member.kind == "enum":
				self.info_tree.insert(self.enums, "end", text=member.name, open=True)
			elif member.kind == "class":
				self.info_tree.insert(self.classes, "end", text=member.name, open=True)
	
	def get_item_info(self, x, y):
		item = self.info_tree.identify("item", x, y)
		name = self.info_tree.item(item, "text")
		parent = self.info_tree.item(self.info_tree.parent(item), "text")
		if len(parent) == 0:
			return None
		return(name, self.kinds[parent])