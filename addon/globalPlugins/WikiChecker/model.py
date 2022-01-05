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
