import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter import messagebox
import codecs
from .base_frame import BaseFrame
from .color.color_scheme import file_content_color_scheme as color_scheme
from .color.color_scheme import file_content_select_bg as select_bg
from .tokenizer.tokenizer import Tokenizer
from math import *
import re

"""
	Модуль для отображения файлов содержимого файлов проекта
"""

class FileContentFrame(BaseFrame):
	"""
		Класс отображения содержимого файлов
	"""
	text = None # виджет отображения текста
	file_path = None # путь до файла
	file_name = None
	selection_pos = "1.0"
	search_color = "white"
	bg_color = "#3c3836"
	
	def __init__(self, master, file_name, file_path, command, right_command, x=0, y=0, width=1, height=1):
		# устанавливаем имя файла
		self.file_name = file_name
		# записываем путь до него
		self.file_path = file_path
		super().__init__(master, x, y, width, height)
		# устанавливаем тег select, если пользователь будет кликать мышкой по идентификатору
		self.text.tag_config("select", background=select_bg)
		# инициализируем остальные теги по цветовой схеме
		for key in color_scheme:
			self.text.tag_config(key, foreground=color_scheme[key])
			def make_lambda(k):
				return lambda e: command(e, k)
			if key == "line" or key == "default":
				continue
			self.text.tag_bind(key, "<Double-Button-1>", make_lambda(key))
			self.text.tag_bind(key, "<Enter>", self.on_enter)
			self.text.tag_bind(key, "<Leave>", self.on_leave)
		self.text.bind("<Control-MouseWheel>", self.resize)
		self.text.bind("<Button-3>", right_command)
			
	def init_widgets(self):
		# создаем текстовый виджет, а также скроллбары
		self.font = tkFont.Font(family=None, size=8)
		self.text = tk.Text(self, wrap=tk.NONE, font=self.font, cursor="arrow", bg=self.bg_color)
		
		y_scroll = tk.Scrollbar(self, command=self.text.yview)
		x_scroll = tk.Scrollbar(self, orient="horizontal", command=self.text.xview)
		
		self.text.tag_config("search", background = self.search_color)
		
		self.text["yscrollcommand"] = y_scroll.set
		self.text["xscrollcommand"] = x_scroll.set
		self.text.place(relx=0, rely=0, relwidth=0.97, relheight=0.97)
		y_scroll.place(relx=0.97, relwidth=0.03, relheight=1)
		x_scroll.place(relx=0, rely=0.97, relwidth=1, relheight=0.03)
	
	def on_enter(self, event):
		"""
			При проходе мышки над идентификатором
		"""
		# проходим по каждому тегу в текстовом виджете
		for tag in self.text.tag_names():
			# если тег по-умолчанию или комментарий, игнорируем
			if tag == "default" or "comment" in tag:
				continue
			# иначе, получаем нач и кон позиции слова
			interval = self.get_interval_under(event, tag)
			# устанавливаем тег выделения
			if interval:
				self.text.tag_add("select", interval[0], interval[1])
		
	def on_leave(self, event):
		# убираем тег выделения, когда мышь выходит из фокуса слова
		self.text.tag_remove("select", "1.0", "end")
	
	def resize(self, event):
		"""
			Масштабирование содержимого виджета Text
		"""
		font_size = int(self.font.cget("size")) + event.delta / fabs(event.delta)
		if font_size <= 0:
			font_size = 1
		self.font["size"] = int(font_size)
		return "break"
	
	def show(self, id_table):
		"""
			Отображение содержимого файла
		"""
		try:
			# пытаемся открыть по кодировке знакового utf-8
			file = codecs.open(self.file_path, "r", "utf_8_sig")
		except:
			messagebox.showerror("Open file error", f"Can't open file {self.file_path}")
			return False
		# запускаем виджет
		self.text.config(state=tk.NORMAL)
		# очищаем содержимое
		self.text.delete(1.0, tk.END)
		try:
			# пытаемся вывести содержимое и подсвечиваем синтаксис
			self.highlight(file, id_table)
		except:
			try:
				# если не получается, дает codecs автоматически определить кодировку
				file = codecs.open(self.file_path, "r")
			except:
				messagebox.showerror("Open file error", f"Can't open file {self.file_path}")
				return False
			# если успех, проделываем тоже самое
			self.text.config(state=tk.NORMAL)
			self.text.delete(1.0, tk.END)
			try:
				self.highlight(file, id_table)
			except:
				messagebox.showerror("Codec error", f"Can't open file {self.file_path}")
				return False
		file.close()
		# отключаем виджет текста для исключения вмешательства пользователя
		self.text.config(state=tk.DISABLED)
		return True
	
	def highlight(self, file, id_table):
		"""
			Подсветка синтаксиса в файле
		"""
		# инициализируем токенизатор
		tokenizer = Tokenizer()
		# перменная для накопления значения токена
		t_value = ""
		# и для хранения его типа
		t_type = None
		# проходим файл построчно
		for num, line in enumerate(file):
			# вставляем в начало строки номер строки
			self.text.insert(tk.END, "%+4s%2s"%(num, ""), "line")
			i = 0
			while i < len(line):
				# накапливаем значение токена
				t_value += line[i]
				# узнаем тип токена
				now_type = tokenizer.get_token_type(t_value)
				# если None, или конец строки
				if not now_type or i+1 == len(line):
					# проверяем, был ли токен до этого чему-то равен
					if t_type:
						# если да, и не конец строки
						if i+1 < len(line):
							# уменьшаем i, т.к. захватили лишний символ
							i -= 1
							# обрезаем значение токена, убирая лишний захваченный символ
							t_value = t_value[:-1]
						# уточняем тип токена по таблице идентификаторов
						t_type = self.specify(t_value, t_type, tokenizer, id_table)
						# добавляем в виджет с t_type в качестве тега
						self.text.insert(tk.END, t_value, t_type)
					else:
						# иначе добавляем неизвестный токен
						self.text.insert(tk.END, t_value, "default")
					t_value = ""
				# обновляем тип токена
				t_type = now_type
				# переходим к след. символу
				i += 1
	
	def specify(self, value, type, tokenizer, id_table):
		"""
			Уточнение типа токена
		"""
		# проверка на ключевое слово
		if tokenizer.is_keyword(value):
			return "keyword"
		# если идентификатор и есть таблица идентификаторов
		if type == "id" and id_table:
			# принадлежит ли токен текущему файлу?
			if id_table.has_record_in_file(self.file_name, value):
				return "id"
			# принадлежит ли вообще токен проекту?
			elif id_table.has_record(value):
				return "another_file_id"
			# значит неизвестный токен
			return "unknown_id"	
		# если не id или нет таблицы, просто возвращаем без уточнения типа
		return type
	
	def get_interval_under(self, event, tag):
		"""
			Получение интервала слова под позицией мыши
		"""
		index = self.text.index("@%s,%s" % (event.x, event.y))
		tag_indices = list(self.text.tag_ranges(tag))
		for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
			if self.text.compare(start, '<=', index) and self.text.compare(index, '<', end):
				return (start, end)
		return None
	
	def get_word_under(self, event, tag):
		"""
			Получение слова под позицией мыши
		"""
		index = self.text.index("@%s,%s" % (event.x, event.y))
		tag_indices = list(self.text.tag_ranges(tag))
		for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
			if self.text.compare(start, '<=', index) and self.text.compare(index, '<', end):
				return self.text.get(start, end)
		return None
		
	def search(self, pattern):
		"""
			Поиск паттерна в файле
		"""
		# очищаем тег выделения найденного паттерна в виджете
		self.text.tag_remove("search", "1.0", "end")
		# устанавливаем начальную позицию и конечную для поиска
		start = self.selection_pos
		end = self.text.index(tk.END)
		# получаем содержимого текстового виджета
		string = self.text.get(start, end)
		# если есть содержимое
		if string:
			# производим поиск
			last_end = "1.0"
			match = re.search(pattern, string)
			# если нашли
			if match:
				# получаем индексы начала и конца
				m_start = self.text.index("%s+%dc"%(start, match.start()))
				m_end = self.text.index("%s+%dc" % (start, match.end()))
				# выделяем тегом результата поиска
				self.text.tag_add("search", m_start, m_end)
				# устаналиваем позицию начала поиска сразу после слова, чтобы в след раз начать искать уже после него
				self.selection_pos = m_end
				# перемещаемся на позицию в виджеет
				self.text.see(m_start)
				return True
			else:
				# если не нашли, в след. раз поиск будет опять идти с начала
				self.selection_pos = "1.0"
		return False
		
	def selected_text(self):
		"""
			Получение выделенного текста из виджета
		"""
		try:
			text = self.text.selection_get()
		except:
			return None
		return text

class FilesFrame(BaseFrame):
	"""
		Класс фрэйма отображения открываемых пользователем файлов
	"""
	notebook = None # контейнер для фрэймов под каждый файл
	frames = None # фрэймы для каждого файла
	search_text = None # паттерн для поиска
	now_frame = None # фрэйм текущего файла
	font_color = "#f9f5f7"
	bg_color = "#bda993"
	
	def init_widgets(self):
		self["background"] = self.bg_color
		style = ttk.Style(self)
		style.configure("TNotebook", background=self.bg_color, foreground=self.font_color)
		self.notebook = ttk.Notebook(self, style="TNotebook")
		self.search_text = tk.StringVar()
		self.search_entry = tk.Entry(self, textvariable=self.search_text, bg="white", fg="black")
		self.search_entry.place(relx=0, rely=0, relwidth=0.5, relheight=0.03)
		self.notebook.place(relx=0, rely=0.03, relwidth=1, relheight=0.97)
		self.notebook.bind("<Button-3>", self.notebook_right_click)
		self.frames = []
	
	def bind_commands(self):
		# по Enter будет идти поиск
		self.search_entry.bind("<Return>", self.start_search)
		
	def start_search(self, event):
		"""
			Начало поиска в результате нажатия Enter
		"""
		# узнаем фрэйм текущего файла
		frame = self.get_current()
		if not frame:
			return
		# смотрим, нашли или нет
		res = frame.search(self.search_text.get())
		if not res:
			# если не нашли, выводим результат безуспешного поиска
			label = tk.Label(self, justify=tk.LEFT, text="No results...", bg="#bda993", foreground="#fb4934", anchor="nw")
			label.place(relx=0.5, rely=0, relwidth=0.4, relheight=0.03)
			self.after(1000, label.place_forget)			
	
	def notebook_right_click(self, event):
		"""
			Вывод popup меню по правому клику на notebook
		"""
		# меню для закрытия вкладки, всех вкладок
		if not len(self.notebook.tabs()):
			return
		popup = tk.Menu(self, tearoff=0)
		popup.add_command(label="Close tab", command=self.close_tab)
		popup.add_command(label="Close all tabs", command=self.close_all_tabs)
		popup.tk_popup(event.x_root, event.y_root, 0)
		
	def close_tab(self):
		"""
			Закрытие вкладки
		"""
		# удалем из списка фрэймов текущий выбранный элемент
		del self.frames[self.notebook.index("current")] 
		# удаляем из notebook
		self.notebook.forget(self.notebook.select())
		
	def close_all_tabs(self):
		"""
			Закрытие всех вкладок
		"""
		self.frames = []
		for tab in self.notebook.tabs():
			self.notebook.forget(tab)
			
	def open_file(self, file_name, file_path, content_click, right_content_click, id_table):
		"""
			открытие файла
		"""
		# проверяем, есть ли данный файл в notebook
		tab_names = [self.notebook.tab(i, "text") for i in self.notebook.tabs()]
		if file_name in tab_names:
			return
		# создаем новый фрэйм содержимого файла
		frame = FileContentFrame(self.notebook, file_name, file_path, content_click, right_content_click)
		# отображаем содержимое файла
		if not frame.show(id_table):
			return
		# добавляем фрэйм в notebook
		self.notebook.add(frame, text=file_name)
		# выбираем текущим
		self.notebook.select(frame)
		# добавляем в список фрэймов
		self.frames.append(frame)
	
	def get_tab_name(self, event):
		"""
			Получение имени вкладки по клику
		"""
		if not len(self.notebook.tabs()):
			return
		clicked_tab = self.notebook.tk.call(self.notebook._w, "identify", "tab", event.x, event.y)
		if type(clicked_tab) == str:
			return
		return self.notebook.tab(clicked_tab, "text")
		
	def get_selected_text(self):
		"""
			Получение выделенного текста в фрэйме содержимого файла
		"""
		frame = self.get_current()
		return frame.selected_text()
	
	def get_current(self):
		"""
			Получение фрэйма текущего файла
		"""
		if not len(self.notebook.tabs()):
			return
		return self.frames[ self.notebook.index("current") ]