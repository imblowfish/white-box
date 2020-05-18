import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import shutil

class ModuleGenerator:
	stylepath="./conf/modulestyle.css"
	document="\
	<!DOCTYPE html>\
		<head>\
			<link rel='stylesheet' type='text/css' href='modulestyle.css'>\
			<title>Modules</title>\
		</head>\
		<body>\
			<div class='modules'>%s</div>\
		</body>\
	<html>"
	module_template="\
	<div class='module_name'>%s</div>\
	<div class='description'>%s</div>\
	<div class='blocks'>%s</div>\
	"
	block_template="\
	<div class='block_name'>%s</div>\
	<div class='block_content'>%s</div>\
	"
	
	def generate(self, modules):
		# выбираем путь, куда экспортировать
		export_dir =  tk.filedialog.askdirectory()
		if not export_dir:
			return
		modules_content = ""
		for name in modules.keys():
			# узнаю все блоки
			blocks_content = ""
			for i, val in enumerate(modules[name]["block"]):
				blocks_content += self.block_template % (f"Block {i+1}", val)
			# записываю имя и описание
			modules_content += self.module_template % (name, modules[name]["description"], blocks_content)
		content = self.document % (modules_content)
		try:
			file = open(f"{export_dir}/project_modules.html", "w")
			file.write(content)
			file.close()
		except:
			print("Error with exporting modules")
			return
		shutil.copyfile(self.stylepath, f"{export_dir}/modulestyle.css")
		messagebox.showinfo("Modules export", "Success")