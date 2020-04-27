import tkinter as tk
import tkinter.ttk as ttk
from .base_frame import BaseFrame

class FileInfoFrame(BaseFrame):
	info_tree = None # дерево информации о файле
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
		
	def init_widgets(self):
		style = ttk.Style()
		style.configure("Treeview.Heading", font=(None, 7), align=tk.CENTER)
		self.info_tree = ttk.Treeview(self, style="Treeview.Heading")
		self.info_tree.heading("#0", text="File info")
		self.info_tree.place(relx=0, rely=0, relwidth=1, relheight=1)
	
	def show(self, record, id_table):
		self.clear()
		self.init_nodes()
		self.add_parents(record.parents_id, id_table)
		self.add_members(record.members_id, id_table)
	
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