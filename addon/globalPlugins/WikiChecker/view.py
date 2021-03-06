#WikiChecker for NVDA.
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.
#Copyright (C) 2021 Antonio Cascales <antonio.cascales@gmail.com>

# We import the necessary modules.
import wx
import gui
import addonHandler

from .controller import *

# We call the function in charge of translations.
addonHandler.initTranslation()

# Displays the main plugin window.
class MainWindow(wx.Dialog):
	# We initialize the window, passing the parent object and its title as arguments.
	def __init__(self, parent, title):
		super(MainWindow, self).__init__(parent, -1, title, size=(1000,700))
		self.results = []
		self.languages = []
		self.okLanguages = False

		self.panel = wx.Panel(self, wx.ID_ANY)

		sizer = wx.BoxSizer(wx.VERTICAL)

		# Translators: Label name of the list of available languages.
		self.availableLanguagesLbl = wx.StaticText(self.panel, wx.ID_ANY, _("&Idiomas disponibles"))

		self.languagesList = wx.Choice(self.panel, wx.ID_ANY, choices=[])

		# Translators: Label name of the search edit box.
		self.searchTermLbl = wx.StaticText(self.panel, wx.ID_ANY, _("Término a &buscar"))

		self.searchTermCtrl = wx.TextCtrl(self.panel, 101, "", style=wx.TE_PROCESS_ENTER)

		# Translators: Label name of the 'Search' button.
		self.searchBtn = wx.Button(self.panel, 103, _("Bu&scar"))

		# Translators: Label name of the list of available items.
		self.availableArticlesLbl = wx.StaticText(self.panel, wx.ID_ANY, _("&Artículos disponibles"))

		self.resultsList = wx.ListBox(self.panel, 102, choices=[], style=wx.LB_SINGLE)

		# Translators: Label name of the 'Read Article' button.
		self.readArticleBtn = wx.Button(self.panel, 104, _("&Leer artículo"))

		sizer.Add(self.availableLanguagesLbl, 0, wx.EXPAND)
		sizer.Add(self.languagesList, 0, wx.EXPAND)
		sizer.Add(self.searchTermLbl, 0, wx.EXPAND)
		sizer.Add(self.searchTermCtrl, 0, wx.EXPAND)
		sizer.Add(self.searchBtn, 0, wx.EXPAND)
		sizer.Add(self.availableArticlesLbl, 0, wx.EXPAND)
		sizer.Add(self.resultsList, 1, wx.EXPAND)
		sizer.Add(self.readArticleBtn, 0, wx.EXPAND)

		self.panel.SetSizer(sizer)

		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyEvent)
		self.Bind(wx.EVT_BUTTON, self.onSearchInformation, self.searchBtn)
		self.Bind(wx.EVT_BUTTON, self.onReadArticle, self.readArticleBtn)

	# We control the different events that occur.
	def onKeyEvent(self, event):
		if event.GetUnicodeKey() in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
			focus = wx.Window.FindFocus().GetId()
			if focus == 101:
				self.onSearchInformation(self)
			elif focus == 102:
				self.onReadArticle(self)
		elif event.GetUnicodeKey() == wx.WXK_ESCAPE:
			self.searchTermCtrl.Clear()
			self.resultsList.Clear()
			self.Hide()
		else:
			event.Skip()

# Auxiliary function to load the list of available languages correctly in the interface.
	def loadLanguagesList(self):
		 loadLanguages(self)

# Function that executes the relevant code to make the query in wikipedia.
	def onSearchInformation(self, event):
		if self.searchTermCtrl.GetValue() == "":
			# Translators: Message shown to the user if they have not typed any term to search for in the edit box.
			gui.messageBox(_("El cuadro de búsqueda no puede estar vacío. Debes introducir un término a buscar."),
			# Translators: Title of the error message.
			caption=_("¡Error!"), style=wx.ICON_ERROR)
			return
		if self.languagesList.GetSelection() == -1:
			# Translators: Message shown to the user if they have not selected a language from among the available ones.
			gui.messageBox(_("Debes seleccionar un idioma de entre los disponibles antes de realizar la consulta. En caso de no haber ninguno disponible, comprueba tu conexión a Internet, o reinicia NVDA."),
			# Translators: Title of the error message.
			caption=_("¡Error!"), style=wx.ICON_ERROR)
			return
		self.results.clear()
		term = self.searchTermCtrl.GetValue()
		wx.CallAfter(searchInformation, self, term)

# Function that executes the relevant code to display the chosen article in the browser.
	def onReadArticle(self, event):
		selectedPageid = self.results[self.resultsList.GetSelection()].getPageid()
		wx.CallAfter(getArticle, self, selectedPageid, self.languages[self.languagesList.GetSelection()])
