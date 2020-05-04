class HTMLGenerator:
	output_path = None

	document="\
	<!DOCTYPE html>\
	<head>\
	<link rel='stylesheet' type='text/css' href='../styles/style.css'>\
	<title>%s</title>\
	</head>\
	<body>\
	<div class='dep_image'>\
	<img src='deps.png'>\
	</div>\
	<div class='header'>%s</div>\
	<div class='members'>%s</div>\
	<div class='mentions'>%s</div>\
	</body>\
	<html>"
	member_info="<div class='member'>%s</div>"
	mention_info="<div class='mention'>%s</div>"
	
	def __init__(self, gen_path):
		self.output_path = gen_path
	
	def generate_id_info_html(self, record, mentions, id_table):
		title = record.name
		members_content = ""
		mentions_content = ""
		if record.members_id:
			# члены идентификатора
			for id in record.members_id:
				member = id_table.get_record_by_id(id)
				members_content += self.member_info % self.to_html(member)
		if len(mentions) > 0:
			# упоминания
			mentions_content = self.generate_mentions(mentions)
			# запись в файл
		page = self.document % (title, str(record), members_content, mentions_content)
		# page = self.document % (title, content)
		file = open(f"{self.output_path}/output.html", "w")
		file.write(page)
		file.close()
		return True
		
	def generate_mentions(self, mentions):
		mention_file = "<div class='mention_file'>%s</div>"
		mention_text = "<div class='mention_text'><span class='line_num'>%s </span><span class = 'line_content'>%s</span></div>"
		content = ""
		for key in mentions:
			file_name = mentions[key]["name"]
			content += mention_file % file_name
			for mention in mentions[key]["lines"]:
				content += mention_text%(mention[0], mention[1])
		return self.mention_info % content
		
	def to_html(self, member):
		str = ""
		if member.kind:
			str += f"<span class='kind'>{member.kind} </span>"
		if member.modifier:
			str += f"<span class='modifier'>{member.modifier} </span>"
		if member.type:
			str += f"<span class='type'>{member.type} </span>"
		str += f"<span class='name'>{member.name}</span>"
		if member.args:
			str += f"<span class='args'>{member.args}</span>"
		return str
		