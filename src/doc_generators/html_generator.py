import codecs

"""
	Генератор html-страницы с информацией об идентификаторе
"""

class HTMLGenerator:
	output_path = None # путь для генерации
	# шаблон документа
	document="\
	<!DOCTYPE html>\
		<head>\
			<link rel='stylesheet' type='text/css' href='../styles/style.css'>\
			<title>%s</title>\
		</head>\
		<body>\
		</div>\
			<div class='header'>%s</div>\
			<div class='dep_image'>\
			<img src='deps.png'>\
			</div>\
			<div class='members'>%s</div>\
			<div class='mentions'>%s</div>\
		</body>\
	<html>"
	# шаблон записи члена идентификатора
	member_info="<div class='member'>%s</div>"
	# шаблон записей для упоминаний имени идентификатора в других файлах
	mention_info="<div class='mention'>%s</div>"
	
	def __init__(self, gen_path):
		self.output_path = gen_path
	
	def generate_id_info_html(self, record, mentions, id_table):
		"""
			Генерация информации об идентификаторе
		"""
		title = record.name
		members_content = ""
		mentions_content = ""
		if record.members_id:
			# члены идентификатора
			for id in record.members_id:
				member = id_table.get_record_by_id(id)
				members_content += self.member_info % self.record_to_html(member)
		if len(mentions) > 0:
			# упоминания
			mentions_content = self.generate_mentions(mentions)
		page = self.document % (title, self.record_to_html(record), members_content, mentions_content)
		# генерируем
		try:
			file = open(f"{self.output_path}/output.html", "w")
		except:
			print("Generate html open file error")
			return False
		file.write(page)
		file.close()
		return True
		
	def generate_mentions(self, mentions):
		"""
			Создаем строку с упоминаниями идентификатора в других файлах
		"""
		mention_file = "<div class='mention_file'>%s</div>"
		mention_text = "<div class='mention_text'><span class='line_num'>%s </span><span class = 'line_content'>%s</span></div>"
		content = ""
		mention_content = ""
		for key in mentions:
			file_name = mentions[key]["name"]
			content += mention_file % file_name
			for mention in mentions[key]["lines"]:
				content += mention_text%(mention[0], mention[1].replace('<', '&lt;').replace('>', '&gt;'))
			mention_content += self.mention_info % content
			content = ""
		# return self.mention_info % content
		return mention_content
		
	def fix_str(self, str):
		str.replace('<', "lt;")
		str.replace('>', "gt;")
		return str
		
	def record_to_html(self, member):
		"""
			Перевод записи id-таблицы в html
		"""
		str = ""
		if member.kind:
			str += f"<span class='kind'>{member.kind.replace('<', '&lt;').replace('>', '&gt;')} </span>"
		if member.modifier:
			str += f"<span class='modifier'>{member.modifier.replace('<', '&lt;').replace('>', '&gt;')} </span>"
		if member.type:
			str += f"<span class='type'>{member.type.replace('<', '&lt;').replace('>', '&gt;')} </span>"
		str += f"<span class='name'>{member.name.replace('<', '&lt;').replace('>', '&gt;')}</span>"
		if member.args:
			str += f"<span class='args'>{member.args.replace('<', '&lt;').replace('>', '&gt;')}</span>"
		return str
		