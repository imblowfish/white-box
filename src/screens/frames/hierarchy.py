import tkinter as tk
import tkinter.ttk as ttk
from .base_frame import BaseFrame
from .project_tree.project_tree import ProjectTree

# отображение иерархии проекта
class HierarchyFrame(BaseFrame):
	tree_widget = None # виджет treeview для отображения иерархии

	def init_widgets(self): # инициализация виджетов
		style = ttk.Style()
		style.configure("Treeview.Heading", font=(None, 7), align=tk.CENTER)
		# создание treeview
		self.tree_widget = ttk.Treeview(self, style="Treeview.Heading")
		# даем ему название
		self.tree_widget.heading("#0", text="Project hierarchy")
		# размещение
		self.tree_widget.place(relx=0, rely=0, relwidth=1, relheight=1.0)
	
	def show(self, hierarchy): # отображение иерархии проекта
		# очищаем treeview
		self.clear()
		# создаем дерево на основе кортежа hierarchy
		tree = ProjectTree()
		tree.create(hierarchy)
		# заносим каждый узел в treeview
		self.add_nodes(tree.root_elements)

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
