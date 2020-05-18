import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import parsing.doxygen_main as doxy
import parsing.directory_parser as dir_par
import parsing.search_module as sm
from doc_generators.id_info_generator import IDInfoGenerator
from utils.server_searcher import ServerSearcher
from utils.database_downloader import DatabaseDownloader
from screens.frames.file_dependencies import FileDependenciesFrame

class WhiteBoxCommands:
	"""
		список команд, наследуемых WhiteBoxCore
	"""
	out_doc_path = "./temp/docs" # куда генерировать документацию doxygen
	html_viewer_path = "./utils/minibrowser/"
	default_id_info_path = "../../temp/html/output.html"
	
	def get_id_table(self):
		"""
			Получение таблицы идентификаторов из вывода doxygen
		"""
		self.main_win.log("Generate documentation...")
		# генерируем документацию проекта
		doc_path = doxy.generate_doc(self.project_directory, self.out_doc_path)
		if not doc_path:
			messagebox.showerror(
				"Generate documentation error", 
				"Can't generate doxygen documentation"
			)
			return
		# проверяет папку с документацией на пустоту
		
		self.main_win.log("Documentation generation success")
		# получаем таблицу идентификаторов путем разбора документации doxygen
		self.main_win.log("Parse identifiers")
		self.id_table = doxy.parse(doc_path, True)
		if not self.id_table:
			self.main_win.log("ID Table is None")
			return False
		if self.id_table.empty():
			self.main_win.log("ID Table is empty")
			return False
		return True

	def show_hierarchy(self):
		"""
			отображение иерархии проекта
		"""
		# получаем дерево директории
		self.main_win.log("Parse directory tree")
		tree = dir_par.dir_tree(self.project_directory)
		self.main_win.log("Show hierarchy")
		# отображаем иерархию
		self.main_win.hierarchy_frame.show(tree)
		self.main_win.log("Show files dependencies")
		# отображаем зависимость файлов
		self.main_win.file_dependency_frame.show(self.id_table.get_records(), self.id_table)
		
	def show_file(self, name, path, record):
		"""
			Отображени содержимого файла
		"""
		self.main_win.log(f"Determine path to the file {name}...")
		# если нет пути до файла, значит файл не принадлежит проекта, ищем в других местах
		if not path:
			self.search_id(name)
			return
		# иначе отображаем
		self.main_win.log(f"Render file {name}")
		self.main_win.files_frame.open_file(
			name, 
			path, 
			self.file_content_click, 
			self.file_content_right_click,
			self.id_table
		)
		self.main_win.log(f"Show file info")
		if record:
			self.main_win.file_info_frame.show(record, self.id_table)
		
	def search_id(self, name):
		"""
			Поиск идентификатора
		"""
		self.main_win.log(f"Search {name} on local database and server...")
		# пытаемся найти на серверах
		s_search = ServerSearcher()
		res = s_search.search_id(name)
		# если в результате поиска нашли на сервере
		if res[0] != "net":
			self.main_win.log(f"Found success")
			self.main_win.log(f"Run html viewer...")
			self.run_html_viewer(res[0], res[1])
		else:
			# иначе спрашиваем, будет ли пользователь искать в интернете?
			self.main_win.log(f"Found failed")
			res = messagebox.askyesno(
				"Search on net", 
				f"Can't find '{name}' on local storage and on server, try to search on internet?"
			)
			# если да, открываем браузер
			if res:
				self.main_win.log(f"Run browser...")
				s_search.open_in_browser(name)

	def show_id_info(self, record, mentions):
		"""
			Отображение информации об идентификаторе
		"""
		# генерируем html-документ
		id_info_generator = IDInfoGenerator()
		self.main_win.log(f"Generate html for {record.name}...")
		id_info_generator.generate(record, self.id_table, mentions)
		self.main_win.log(f"Run html viewer...")
		# отображаем
		self.run_html_viewer()
		
	def remove_spaces(self, str):
		str = str.replace(" ", "")
		str = str.replace("\n", "")
		str = str.replace("\t", "")
		str = str.replace("\r", "")
		return str

	# UTILITY COMMANDS
	def run_html_viewer(self, where_to_look="local", path=default_id_info_path):
		"""
			Запуск визуализатора html в дочернем процессе
		"""
		self.main_win.start_statusbar()
		try:
			subprocess.Popen(["npm", "run", "start", "--prefix", self.html_viewer_path, where_to_look, path], shell=True)
		except:
			self.main_win.log(f"Creating subprocess error")
			messagebox.showerror(
				"Run HTML Viewer Error", 
				"Can't create subprocess"
			)
		self.main_win.stop_statusbar()
		
	def download_database(self):
		"""
			Загрузка БД с сервера
		"""
		self.main_win.start_statusbar()
		self.main_win.log(f"Try to download database from server...")
		dd = DatabaseDownloader()
		# после скачивания будем сразу разархивировать, поэтому unzip True
		res = dd.download(unzip=True)
		self.main_win.stop_statusbar()
		if not res[0]:
			self.main_win.log(f"Download error {res[1]}")
			messagebox.showerror(f"Error with downloading databas", res[1])
		else:
			self.main_win.log(f"Download success")
			messagebox.showinfo("Download result", "Success")
	
	# CLICK COMMANDS
	def open_project_click(self, event):
		"""
			открытие проекта
		"""
		# запоминаем предыдущую директорию проекта
		prev_dir = self.project_directory
		# узнаем новую директорию проекта
		self.project_directory =  dir_par.relative_path_to( tk.filedialog.askdirectory() )
		self.main_win.start_statusbar()
		if not self.project_directory:
			self.project_directory = prev_dir
			return
		self.main_win.log(f"Open project in directory {self.project_directory}...")
		if not self.get_id_table():
			messagebox.showerror(
				"Doxygen parsing error", 
				"Can't get id table, maybe unsupported language"
			)
			return
		self.show_hierarchy()
		self.main_win.stop_statusbar()
		
	def open_file_click(self, event):
		"""
			Клик по пункту меню открыть файл
		"""
		# узнаем у пользователя, какой файл открыть
		file_path = dir_par.relative_path_to( tk.filedialog.askopenfilename() )
		if not file_path:
			return
		self.main_win.start_statusbar()
		self.main_win.log(f"Open file {file_path}...")
		self.main_win.stop_statusbar()
		self.show_file(file_path, file_path, None)
	
	def maximize_file_dependencies(self, event):
		"""
			Увеличение визуализации зависимостей файлов проекта
		"""
		if not self.id_table:
			return
		win = tk.Toplevel(self.main_win.master)
		win.wm_title("File dependencies")
		win.geometry("500x300")
		frame = FileDependenciesFrame(win)
		frame.zoom_btn.pack_forget()
		frame.show(self.id_table.get_records(), self.id_table)
	
	def hierarchy_click(self, event):
		"""
			обработка клика по иерархии
		"""
		# идентифицируем элемент, по которому кликнули
		name = self.main_win.hierarchy_frame.get_name(event)
		if not len(name):
			return
		# узнаем вид элемента
		record = self.id_table.get_record_by_name_and_kind(name, "file", copy=True)
		if not record:
			return
		# узнаем полный путь до него от корневой директории проекта
		path = dir_par.path_from_dir_to_file(self.project_directory, name)
		self.show_file(name, path, record)
		
	def files_tab_click(self, event):
		if not self.id_table:
			return
		ff = self.main_win.files_frame
		name = ff.get_tab_name(event)
		# print(name)
		if not name:
			return
		record = self.id_table.get_record_by_name_and_kind(name, "file", copy=True)
		fif = self.main_win.file_info_frame
		fif.show(record, self.id_table)
		
	def file_content_click(self, event, text_tag):
		"""
			обработка клика по тексту файла
		"""
		name = self.remove_spaces( self.main_win.files_frame.get_current().get_word_under(event, text_tag) )
		if not len(name):
			return
		if not self.id_table:
			self.search_id(name)
			return
		record = self.id_table.get_record_by_name(name, copy=True)
		path = dir_par.path_from_dir_to_file(self.project_directory, name)
		if not record:
			print("Can't find record")
			self.search_id(name)
			return
		if not record.parents_id and record.kind == "file":
			# делаем open file
			if path:
				self.show_file(name, path, record)
			else:
				self.search_id(name)
			return
		if record.kind == "file":
			path = dir_par.path_from_dir_to_file(self.project_directory, name)
			self.show_file(name, path, record)
			return
		mentions = sm.get_all_pos_in_dir(self.project_directory, name)
		self.show_id_info(record, mentions)
		
	def file_info_click(self, event):
		"""
			отображение окна с информацией об идентификаторе
		"""
		name, kind = self.main_win.file_info_frame.get_item_info(event.x, event.y)
		name = self.remove_spaces(name)
		if not name:
			return
		if not len(name):
			return
		record = self.id_table.get_record_by_name_and_kind(name, kind, copy=True)
		if kind == "file":
			# делаем open_file
			path = dir_par.path_from_dir_to_file(self.project_directory, name)
			self.show_file(name, path, record)
			return
		mentions = sm.get_all_pos_in_dir(self.project_directory, name)
		self.show_id_info(record, mentions)
		
	def file_content_right_click(self, event):
		"""
			Отображение popup меню при правом клике по содержимому файла
		"""
		popup = tk.Menu(self.main_win.master, tearoff=0)
		text = self.main_win.files_frame.get_selected_text()
		if text:
			popup.add_command(label="Add to module", command=lambda :self.add_to_module(text))
		popup.add_command(label="Search...", command=lambda :self.main_win.search_id(ServerSearcher(), self.run_html_viewer))
		popup.tk_popup(event.x_root, event.y_root, 0)
	
	def add_to_module(self, text):
		"""
			Добавление блока текста в модуль
		"""
		self.main_win.text_in_module_adding(text)
	
		
	
	
		
	
		
		