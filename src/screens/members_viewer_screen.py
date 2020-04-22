import tkinter as tk
import tkinter.ttk as ttk

# возможно тут стоит не только отображать членов, но и родительские элементы, а также базовые классы, если такие есть

class MembersViewerScreen:
	def show(self, members, command):
		self.root = tk.Tk()
		self.members = ttk.Treeview(self.root)
		included_by = self.members.insert("", "end", text="Included by")
		classes = self.members.insert("", "end", text="Classes")
		variables = self.members.insert("", "end", text="Variables", open=True)
		functions = self.members.insert("", "end", text="Functions", open=True)
		enums = self.members.insert("", "end", text="Enums")
		for member in members:
			if member.kind == "file":
				self.members.insert(included_by, "end", text=member.name, open=True)
			elif member.kind == "class":
				self.members.insert(classes, "end", text=member.name, open=True)
			elif member.kind == "function":
				self.members.insert(functions, "end", text=member.name, open=True)
			elif member.kind == "var":
				self.members.insert(variables, "end", text=member.name, open=True)
			elif member.kind == "enum":
				self.members.insert(enums, "end", text=member.name, open=True)
		self.members.bind("<Button-1>", command)
		self.members.pack()
		self.root.mainloop()