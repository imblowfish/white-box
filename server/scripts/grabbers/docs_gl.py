from bs4 import BeautifulSoup
from base_grabber import BaseGrabber

"""
	Модуль парсинга docs.gl
"""

class DocsGLParser(BaseGrabber):
	begin_url = "https://wiki.libsdl.org"
	search_url = "http://docs.gl"
	dir = "../database/docs_gl"
	
	def parse_idents_list(self):
		import requests as req
		page = req.get(self.search_url).text
		if not page:
			return
		soup = BeautifulSoup(page, "html.parser")
		# spans = soup.find_all("span", {"class": "commandcolumn"})
		div = soup.find("div", {"id": "commandlist"})
		childs = div.findChildren("span", recursive=False)
		idents_list = {}
		for child in childs:
			name = child.find("span", {"class": "commandcolumn"}).text
			versions = child.find_all("span", {"class": "versioncolumn"})
			ref = ""
			max_version = 0
			for v in versions:
				a = v.find("a")
				if a:
					doc_version = int(a.text[-1:])
					if doc_version > max_version:
						ref = a["href"]
						max_version = doc_version
			idents_list[name] = f"{self.search_url}/{ref}"
		if not self.save_json(self.dir+"/idents.json", idents_list):
			return
		return idents_list
		
	def parse_page(self, ident_name, url):
		page = self.get_page(url)
		if not page:
			print("Not page")
			return None
		soup = BeautifulSoup(page.content, "html.parser")
		page = soup.find("div", {"id": "khronos"})
		if not self.save_html(self.dir, ident_name, page):
			return False
		return True
		
doc_p = DocsGLParser()
doc_p.parse()