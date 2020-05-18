import tkinter as tk
import tkinter.ttk as ttk
from .base_frame import BaseFrame
from .project_tree.project_tree import ProjectTree

# отображение иерархии проекта
class HierarchyFrame(BaseFrame):
	tree_widget = None # виджет treeview для отображения иерархии
	font_select_color = "#3c3836"
	select_color = "#f9f5f7"
	font_color = "#f9f5f7"
	bg_color = "#3c3836"

	def init_widgets(self): # инициализация виджетов
		style = ttk.Style(self)
		style.theme_use("clam")
		style.configure("Treeview.Heading", font=(None, 8), align=tk.CENTER, background=self.bg_color, fieldbackground=self.bg_color, foreground=self.font_color)
		# создание treeview
		self.tree_widget = ttk.Treeview(self, style="Treeview.Heading")
		# даем ему название
		self.tree_widget.heading("#0", text="Project hierarchy")
		
		yscroll = tk.Scrollbar(self, command=self.tree_widget.yview)
		xscroll = tk.Scrollbar(self, command=self.tree_widget.xview, orient="horizontal")
		self.tree_widget["yscrollcommand"] = yscroll.set
		self.tree_widget["xscrollcommand"] = xscroll.set
        
		self.tree_widget.tag_configure("selected", background=self.select_color, foreground=self.font_select_color)
		self.tree_widget.tag_configure("unselected", background=self.bg_color, foreground=self.font_color)

		# размещение
		self.tree_widget.place(relx=0, rely=0, relwidth=1, relheight=0.95)
		yscroll.place(relx=0.93, rely=0, relwidth=0.07, relheight=1)
		xscroll.place(relx=0, rely=0.95, relwidth=0.93, relheight=0.05)
	
	def bind_commands(self):
		self.tree_widget.bind("<Button-1>", self.select_row)
		self.tree_widget.bind("<FocusOut>", lambda e: self.reset_selection())
		
	def select_row(self, event):
		self.reset_selection()
		item_id = self.tree_widget.identify("item", event.x, event.y)
		self.tree_widget.item(item_id, tags=("selected"))
		
	def reset_selection(self, child=""):
		for child in self.tree_widget.get_children(child):
			self.tree_widget.item(child, tags=("unselected"))
			self.reset_selection(child)
	
	def get_name(self, event):
		return self.tree_widget.item(self.tree_widget.identify("item", event.x, event.y), "text")
	
	def show(self, hierarchy): # отображение иерархии проекта
		# очищаем treeview
		self.clear()
		# создаем дерево на основе кортежа hierarchy
		tree = ProjectTree()
		tree.create(hierarchy)
		# заносим каждый узел в treeview
		self.add_nodes(tree.root_elements)
		self.reset_selection()

	def clear(self): # очистка treeview
		if not self.tree_widget:
			return
		for node in self.tree_widget.get_children():
			self.tree_widget.delete(node)
			
	def add_nodes(self, nodes, parent=""): # добавление нодов в treeview 
		if not nodes:
			return
		for node in nodes:
			next_parent = self.tree_widget.insert(parent, "end", text=node.name, open=True)
			if not node.child_elements:
				continue
			self.add_nodes(node.child_elements, next_parent)
