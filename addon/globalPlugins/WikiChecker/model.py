#WikiChecker for NVDA.
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.
#Copyright (C) 2021 Antonio Cascales <antonio.cascales@gmail.com>

# Stores the information about a result obtained in the query.
class Result():

	# Initializes the Result object, passing it as arguments the title, the snippet and the pageid.
	def __init__(self, title, snippet, pageid):
		self.title = title
		self.snippet = snippet
		self.pageid = pageid

	# Returns the title of the result.
	def getTitle(self):
		return self.title

	# Returns the snippet of the result.
	def getSnippet(self):
		return self.snippet

	# Returns the pageid of the result.
	def getPageid(self):
		return self.pageid

	# Returns the title and snippet of the correctly formatted result for display.
	def __str__(self):
		return self.title + ": " + self.snippet

# Stores information about a specific language from Wikipedia.
class Language():

	# Initializes the Language object, passing it as arguments the abbreviation and the name.
	def __init__(self, abbreviation, name):
		self.abbreviation = abbreviation
		self.name = name

	# Returns the abbreviation of the language.
	def getAbbreviation(self):
		return self.abbreviation

	# Returns the name of the language.
	def getName(self):
		return self.name

	# Returns the abbreviation and name of the language correctly formatted for display.
	def __str__(self):
		return self.abbreviation + ": " + self.name
