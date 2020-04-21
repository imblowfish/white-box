from parsing import (
	doxygen_worker_main as dox_w,
	source_worker_main as s_w,
	
)

# лишний класс, стоит убрать

class Analyzer:
	def __init__(self):
		pass
	def get_id_table(self, project_directory):
		# генерация документации doxygen
		
		# разбор документации doxygen
		return dox_w.parse("./docs/imap/xml")
		# добавить разбор каждого файла по отдельности
		
		# return dox_w.parse("./docs/imap/xml")
		