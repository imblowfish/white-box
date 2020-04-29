import requests as req
from bs4 import BeautifulSoup
import json

class SDLWikiParser:
	begin_url = "https://wiki.libsdl.org"
	search_url = "https://wiki.libsdl.org/CategoryAPI"
	def get_page(self, url):
		page = req.get(url)
		if page.status_code != 200:
			print(f"SDLWiki parse {url} error")
			return
		return page
	def parse_idents_list(self):
		page = self.get_page(self.search_url)
		if not page:
			return
		soup = BeautifulSoup(page.content, "html.parser")
		divs = soup.find_all("div", {"class":"searchresults"})
		idents_list = {}
		for div in divs:
			for a in div.find_all("a"):
				name = a.text
				href = a["href"]
				idents_list[name] = self.begin_url+href
		with open("log.json", "w") as file:
			json.dump(idents_list, file)
	def parse_page(self, url):
		page = self.get_page(url)
		if not page:
			return
		soup = BeautifulSoup(page.content, "html.parser")
		page = soup.find("div", {"id": "page"})
		with open("log.html", "w") as file:
			file.write(str(page))
		
sdl_p = SDLWikiParser()
sdl_p.parse_idents_list()
sdl_p.parse_page("https://wiki.libsdl.org/SDL_AssertState?highlight=%28%5CbCategoryEnum%5Cb%29%7C%28SDLEnumTemplate%29")
