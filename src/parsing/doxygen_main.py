from .doxygen_table import DoxyTable
from .id_table import IDTable
from .doxygen_parser import (
	IndexParser,
	SourceFileParser,
	ClassParser
)
		
from random import *
import subprocess
import shutil

# генерация xml doxygen на основе проекта
def generate_doc(project_path, doc_folder):
	# !!!добавить вывод информации на случай отладки, а также проверку наличия doxygen!!!
	print("generate doxygen documentation")
	folder_name = ""
	#генерация случайного имени директории проекта
	for i in range(0, 15):
		folder_name += chr(randint(97, 122))
	doc_folder += '/'+folder_name
	#генерация документации doxygen
	command = "( type doc & \
				echo GENERATE_XML=YES \
				& echo GENERATE_HTML=NO \
				& echo GENERATE_LATEX=NO \
				& echo RECURSIVE=YES \
				& echo INPUT="+project_path+" \
				& echo OUTPUT_DIRECTORY = "+doc_folder+" ) \
				| "+"doxygen"+" - "
	subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	print("doxygen documentation generating success")
	return doc_folder+"\\xml"
		
# разбор xml вывода doxygen
# разбор ошибок, нигде не проверяется, успешно ли пропарсился проект или нет
def parse(path_to_doc, clear_doc=False):
	print("parse doxygen documentation")
	# создаем таблицу файлов doxygen, настраиваем путь к документации
	doxy_table = DoxyTable(path_to_doc)
	# создаем таблицу идентификаторов
	id_table = IDTable()
	# разбираем файл index.xml
	index_parser = IndexParser(doxy_table, id_table)
	index_parser.parse(path_to_doc+"\index.xml")
	# разбираем файлы с исходным кодом
	source_parser = SourceFileParser(doxy_table, id_table)
	source_parser.parse()
	# разбираем файлы с классами
	class_parser = ClassParser(doxy_table, id_table)
	class_parser.parse()
	# если задано удалить документацию после разбора
	if clear_doc:
		# узнаем имя директории проекта
		pos = path_to_doc.find("xml") - 1
		path_to_doc = path_to_doc[0:pos]
		# удаляем директорию
		shutil.rmtree(path_to_doc)
	# удаляем экземпляры классов разбора и таблицу файлов doxygen
	del index_parser, source_parser, class_parser, doxy_table
	print("doxygen documentation parsing success")
	# возвращаем таблицу идентификаторов
	return id_table
	