#WikiChecker for NVDA.
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.
#Copyright (C) 2021 Antonio Cascales <antonio.cascales@gmail.com>

# We import the modules necessary for proper operation.
import json
import re
import sys, os
import wx
import languageHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
	del sys.modules['html']
except:
	pass

from threading import Thread, Lock
from bs4 import BeautifulSoup
from urllib import request, parse
from .model import *

# Generates a new thread with which to display the selected Wikipedia article.
class DoANewCheck(Thread):
	# We initialize the thread, passing it the parent object, the pageid and the language necessary for the check.
	def __init__(self, parent, pageid, language):
		super(DoANewCheck, self).__init__()
		self.parent = parent
		self.pageid = pageid
		self.language = language

	# We format the destination URL and display the article on Wikipedia.
	def run(self):
		url = "https://" + self.language + ".wikipedia.org/?curid=" + str(self.pageid)
		wx.LaunchDefaultBrowser(url)

# Generate a new thread that retrieves the available languages from Wikipedia.
class DoLanguageCheck(Thread):
	# We initialize the thread, passing the parent object as an argument.
	def __init__(self, parent):
		super(DoLanguageCheck, self).__init__()
		self.parent = parent

	# We get the list of available languages. We check it from the Spanish version, for reasons of simplicity for the developer.
	def run(self):
		try:
			req = request.Request("https://es.wikipedia.org/wiki/Wikipedia:Lista_completa_de_Wikipedias", data=None, headers={"User-Agent": "Mozilla/5.0"})
			html = request.urlopen(req)
			data = html.read().decode("utf-8")
		except:
			print("Error retrieving list of languages from Wikipedia.")

		bs = BeautifulSoup(data, 'html.parser')
		rows = bs.find_all('tr')

		for i in range(1, len(rows)):
			cells = rows[i].find_all('td')
			abbreviation = cells[0].a.string
			name = cells[1].a.string
			self.parent.languages.append(abbreviation)
			self.parent.languagesList.Append(name)

# Remove the HTML tags from the text passed as an argument.
def removeTags(text):
	return re.sub(r'<[^>]*?>', '', text)

def loadLanguages(parent):
	check = DoLanguageCheck(parent)
	check.start()

def searchInformation(parent, term):
	selectedLanguage = parent.languages[parent.languagesList.GetSelection()]
	url = "https://" + selectedLanguage + ".wikipedia.org/w/api.php?action=query&list=search&srprop=snippet&format=json&origin=*&utf8=&srsearch=" + request.quote(term)
	try:
		req = request.Request(url, data=None, headers={"User-Agent": "Mozilla/5.0"})
		html = request.urlopen(req)
		data = html.read().decode("utf-8")
	except:
		print("Error obteniendo los artículos disponibles.")

	diccionario = json.loads(data)
	info = diccionario["query"]["search"]
	parent.resultsList.Clear()
	for i in info:
		result = Result(i["title"], removeTags(i["snippet"]), i["pageid"])
		parent.results.append(result)
		parent.resultsList.AppendItems(str(result))
	parent.resultsList.SetFocus()

def getArticle(parent, pageid, language):
	check = DoANewCheck(parent, pageid, language)
	check.start()

def setDefaultLanguage(parent):
	defaultLanguage = languageHandler.getLanguage().split('_')[0]
	position = parent.languages.index(defaultLanguage)
	parent.languagesList.SetSelection(position)
