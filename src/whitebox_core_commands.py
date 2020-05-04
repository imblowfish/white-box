import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import parsing.directory_parser as dir_par
import parsing.search_module as sm
import parsing.doxygen_main as doxy
from doc_generators.id_info_generator import IDInfoGenerator
from utils.database_downloader import DatabaseDownloader
from utils.server_searcher import ServerSearcher


def run_minibrowser(where_to_look="local", path="../../temp/html/output.html"):
	mini_browser_path = "./utils/minibrowser/"
	subprocess.Popen(["npm", "run", "start", "--prefix", mini_browser_path, where_to_look, path], shell=True)

# список команд, наследуемых WhiteBoxCore
class WhiteBoxCommands:
	out_doc_path = "./temp/docs" # куда генерировать документацию doxygen
	
	def open_project(self, event): # открытие проекта
		# запоминаем предыдущую директорию проекта
		prev_dir = self.project_directory
		# узнаем новую директорию проекта
		self.project_directory =  dir_par.relative_path_to(tk.filedialog.askdirectory())
		if not self.project_directory:
			self.project_directory = prev_dir
			return
		# генерируем документацию проекта
		doc_path = doxy.generate_doc(self.project_directory, self.out_doc_path)
		# получаем таблицу идентификаторов путем разбора документации doxygen
		self.id_table = doxy.parse(doc_path, True)
		self.show_hierarchy()

	def show_hierarchy(self): # отображение иерархии проекта
		# получаем дерево директории
		tree = dir_par.get_dir_tree(self.project_directory)
		# отображаем иерархию
		self.main_win.hierarchy_frame.show(tree)
		# отображаем зависимость файлов
		self.main_win.file_dependency_frame.show(self.id_table.get_records(), self.id_table)

	def hierarchy_click(self, event): # обработка клика по иерархии
		# получаем ссылку на виджет treeview фрейма отображения иерархии
		tree = self.main_win.hierarchy_frame.tree_widget
		# идентифицируем элемент, по которому кликнули
		item = tree.identify("item", event.x, event.y)
		# узнаем его имя
		name = tree.item(item, "text")
		if not len(name):
			return
		# узнаем вид элемента
		record = self.id_table.get_record_by_name(name, copy=True)
		if not record or record.kind != "file":
			return
		# узнаем полный путь до него от корневой директории проекта
		path = dir_par.get_path_from(self.project_directory, name)
		# отображение содержимого файла
		ff = self.main_win.files_frame
		ff.open_file(name, path, self.file_content_click, self.id_table)
		# отображение информации о файле
		fif = self.main_win.file_info_frame
		fif.show(record, self.id_table)

	def file_content_click(self, event, text_tag): # обработка клика по тексту файла
		# вывод информации об идентификаторе
		name = self.main_win.files_frame.get_current().get_word_under(event, text_tag)
		if text_tag == "file":
			# делаем open file
			return
		record = self.id_table.get_record_by_name(name, copy=True)
		if not record:
			# пытаемся найти на серверах
			s_search = ServerSearcher()
			res = s_search.search(name)
			print(res)
			if res[0] != "net":
				run_minibrowser(res[0], res[1])
			else:
				res = messagebox.askyesno("Message", f"Can't find '{name}' on local storage and on server, try to search on internet?")
				if res:
					s_search.search_on_net(name)
			return
		mentions = sm.get_all_pos_in_dir(self.project_directory, name)
		# генерация html-документа с информацией об идентификаторе
		id_info_generator = IDInfoGenerator()
		id_info_generator.generate(record, self.id_table, mentions)
		# открытие html-документа
		run_minibrowser()

	def file_info_click(self, event):
		# отображение окна с информацией об идентификаторе
		item = self.main_win.file_info_frame.get_item_info(event.x, event.y)
		if not item:
			return
		if item[1] == "file":
			# делаем open_file
			return
		record = self.id_table.get_record_by_name_and_kind(item[0], item[1], copy=True)
		mentions = sm.get_all_pos_in_dir(self.project_directory, item[0])
		self.main_win.show_id_info(record, self.id_table, mentions)
		
	def download_database(self):
		dd = DatabaseDownloader()
		res = dd.download(unzip=True)
		if not res[0]:
			messagebox.showerror(f"Error with downloading databas", res[1])
		else:
			messagebox.showinfo("Download result", "Success")
		
		