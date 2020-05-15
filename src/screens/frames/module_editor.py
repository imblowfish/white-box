import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import codecs
import os
import json
from .base_frame import BaseFrame
from doc_generators.module_generator import ModuleGenerator

class ModuleTextFrame(BaseFrame):
	text = None
	def init_widgets(self):
		self.text = tk.Text(self, font=(None, 8))
		self.text.place(relx=0, rely=0, relwidth=1, relheight=1)


class ModuleEditor(BaseFrame):
	saved = True
	modules = None
	module_file_path = "./temp/module.json"
	now_selected = None
	
	def init_widgets(self):
		self.module_text_frame = ModuleTextFrame(self)
		self.module_tree = ttk.Treeview(self)
		self.module_tree.heading("#0", text="Modules")
		self.add_button = tk.Button(self, text="Add", command=lambda: self.add_in_module(self.module_text_frame.text.get("1.0", tk.END)))
		yscroll = tk.Scrollbar(self, command=self.module_tree.yview)
		xscroll = tk.Scrollbar(self, command=self.module_tree.xview, orient="horizontal")
		self.module_tree["yscrollcommand"] = yscroll.set
		self.module_tree["xscrollcommand"] = xscroll.set
		self.module_tree.place(relx=0, rely=0, relwidth=0.5, relheight=0.95)
		yscroll.place(relx=0.5, rely=0, relwidth=0.07, relheight=1)
		xscroll.place(relx=0, rely=0.95, relwidth=0.5, relheight=0.05)
		self.module_text_frame.place(relx=0.57, relwidth=0.43, relheight=0.9)
		self.add_button.place(relx=0.57, rely=0.9, relwidth=0.43, relheight=0.1)
		self.init_menu()
		
	def init_menu(self):
		self.menu_bar = tk.Menu(self)
		self.master["menu"] = self.menu_bar
		self.menu_bar.add_command(label="Add module", command=self.add_module)
		self.menu_bar.add_command(label="Delete element", command=self.delete_element)
		self.menu_bar.add_command(label="Edit element", command=self.edit_element)
		self.menu_bar.add_command(label="Export modules", command=self.export_modules)
		
	def bind_commands(self):
		self.module_tree.bind("<Button-1>", self.select_module)
		def after_close():
			self.save_modules()
			self.master.destroy()
		self.bind("<Destroy>", lambda e: after_close())
		
	def select_module(self, event):
		if not self.modules:
			self.now_selected = None
			return
		item = self.module_tree.identify("item", event.x, event.y)
		name = self.module_tree.item(item, "text")
		tags = self.module_tree.item(item)["tags"]
		if not len(name):
			return
		if not len(tags):
			self.now_selected = None
			return
		if tags[0] == "block_content":
			# отображаем содержимое блока
			win = tk.Toplevel()
			win.wm_title("Block content")
			win.geometry("300x200")
			text = tk.Text(win, font=(None, 8))
			text.place(relx=0, rely=0, relwidth=1, relheight=1)
			text.insert(tk.END, name)
			self.now_selected = None
			return
		# if tags[0] == "description_text":
			# return
		self.now_selected = (name, tags[0], item)
		
	def add_module(self):
		win = tk.Toplevel()
		win.wm_title("Add module")
		win.geometry("300x200")
		win.resizable(False, False)
		text = tk.Entry(win)
		descr = tk.Text(win)
		button = tk.Button(win, text="Add")
		text.place(relx=0, rely=0, relwidth=1, relheight=0.1)
		descr.place(relx=0, rely=0.1, relwidth=1, relheight=0.7)
		button.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
		win.grab_set()
		def add(text, descr, win):
			self.add_new_module(text.get(), descr.get("1.0", tk.END))
			win.destroy()
		button.bind("<Button-1>", lambda e: add(text, descr, win))
		
	def add_new_module(self, module_name, description):
		if not len(module_name):
			return
		if not self.modules:
			self.modules = {}
		if module_name in self.modules.keys():
			print("Already exist")
			return
		self.modules[module_name] = {
			"description": description,
			"block": []
		}
		self.saved = True
		self.redraw_tree()
		
	def add_in_module(self, text):
		if not self.modules:
			print("Modules empty, please add")
			return
		if not self.now_selected:
			return
		if self.now_selected[1] != "module_name":
			return
		# ищем выбранный модуль
		self.modules[self.now_selected[0]]["block"].append(text)
		self.redraw_tree()
		
	def delete_element(self):
		if not self.now_selected:
			return
		print("Delete")
		parent = self.module_tree.parent(self.now_selected[2])
		parent_name = self.module_tree.item(parent, "text")
		if not len(parent_name):
			del self.modules[self.now_selected[0]]
		else:
			tag = self.now_selected[1]
			if tag == "description":
				self.modules[parent_name]["description"] = {}
			elif tag == "block":
				for child in self.module_tree.get_children(self.now_selected[2]):
					idx = -1
					print(self.modules[parent_name][tag])
					for i, block in enumerate(self.modules[parent_name][tag]):
						if self.module_tree.item(child, "text") == block:
							del self.modules[parent_name][tag][i]
							break
			else:
				return
		self.redraw_tree()
	
	def edit_element(self):
		if not self.now_selected:
			return
		if self.now_selected[1] != "module_name":
			return
		win = tk.Toplevel()
		win.wm_title("Edit module")
		win.geometry("300x200")
		win.resizable(False, False)
		text = tk.Entry(win)
		text.insert(tk.END, self.now_selected[0])
		descr = tk.Text(win)
		descr.insert(tk.END, self.modules[self.now_selected[0]]["description"])
		button = tk.Button(win, text="Edit")
		text.place(relx=0, rely=0, relwidth=1, relheight=0.1)
		descr.place(relx=0, rely=0.1, relwidth=1, relheight=0.7)
		button.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
		win.grab_set()
		def edit(module_name, text, descr):
			old_key_blocks = self.modules[module_name]["block"].copy()
			del self.modules[module_name]
			self.modules[text.get()] = {
				"description": descr.get("1.0", tk.END),
				"block": old_key_blocks
			}
			win.destroy()
			self.redraw_tree()
		button.bind("<Button-1>", lambda e: edit(self.now_selected[0], text, descr))
	
	def save_modules(self):
		if not self.modules:
			print("Nothing to save")
			return
		if not os.path.exists(self.module_file_path):
			print("Create json_file")
			with open(self.module_file_path, "w") as file:
				pass
		print("Save")
		try:
			json_file = open(self.module_file_path, "w")
			print(self.modules)
			json.dump(self.modules, json_file)
			json_file.close()
		except:
			print("Error with file saving")
		
	def export_modules(self):
		if not self.modules:
			return
		print("Export")
		m_exporter = ModuleGenerator()
		m_exporter.generate(self.modules)
		
	def show(self, text=None):
		# если нет, ничего не отображаем, если есть, парсим
		if text:
			self.module_text_frame.text.insert(tk.END, text)
		# поиск временного файла модулей проекта
		# if os.path.exists(self.module_file_path):
			# os.remove(self.module_file_path)
		if not os.path.exists(self.module_file_path):
			with open(self.module_file_path, "w") as file:
				pass
		# читаем модули из файла
		self.modules = self.parse_json()
		if not self.modules:
			return
		self.redraw_tree()
			
	def parse_json(self):
		try:
			json_file = open(self.module_file_path, "r")
			data = json.load(json_file)
			json_file.close()
		except:
			print("Error with file open")
			return
		return data
		
	def redraw_tree(self):
		for node in self.module_tree.get_children():
			self.module_tree.delete(node)
		for key in self.modules.keys():
			module_node = self.module_tree.insert("", "end", text=key, open=True)
			self.module_tree.item(module_node, tags=("module_name"))
			self.draw_module(module_node, self.modules[key])
			
	def draw_module(self, module_node, module):
		descr = module["description"]
		node = self.module_tree.insert(module_node, "end", text="description", open=True)
		self.module_tree.item(node, tags=("description"))
		child = self.module_tree.insert(node, "end", text=descr, open=False)
		self.module_tree.item(child, tags=("description_text"))
		for i, val in enumerate(module["block"]):
			node = self.module_tree.insert(module_node, "end", text=f"Block {i+1}", open=True)
			self.module_tree.item(node, tags=("block"))
			content = self.module_tree.insert(node, "end", text=val, open=True)
			self.module_tree.item(content, tags=("block_content"))
			
			