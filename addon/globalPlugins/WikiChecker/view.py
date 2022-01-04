#WikiChecker for NVDA.
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.
#Copyright (C) 2021 Antonio Cascales <antonio.cascales@gmail.com>

# We import the necessary modules.
import wx
import gui

from .controller import *

# Displays the main plugin window.
class MainWindow(wx.Dialog):
	# We initialize the window, passing the parent object and its title as arguments.
	def __init__(self, parent, title):
		super(MainWindow, self).__init__(parent, -1, title, size=(1000,700))
		self.results = []
		self.languages = []

		self.panel = wx.Panel(self, wx.ID_ANY)

		sizer = wx.BoxSizer(wx.HORIZONTAL)

		self.availableLanguagesLbl = wx.StaticText(self.panel, wx.ID_ANY, _("&Idiomas disponibles"))

		self.languagesList = wx.Choice(self.panel, wx.ID_ANY, choices=[])

		self.searchTermLbl = wx.StaticText(self.panel, wx.ID_ANY, _("Término a &buscar"))

		self.searchTermCtrl = wx.TextCtrl(self.panel, 101, "", style=wx.TE_PROCESS_ENTER)

		self.availableArticlesLbl = wx.StaticText(self.panel, wx.ID_ANY, _("&Artículos disponibles"))

		self.resultsList = wx.ListBox(self.panel, 102, choices=[], style=wx.LB_SINGLE)

		sizer.Add(self.availableLanguagesLbl, 0, wx.EXPAND)
		sizer.Add(self.languagesList, 0, wx.EXPAND)
		sizer.Add(self.searchTermLbl, 0, wx.EXPAND)
		sizer.Add(self.searchTermCtrl, 0, wx.EXPAND)
		sizer.Add(self.availableArticlesLbl, 0, wx.EXPAND)
		sizer.Add(self.resultsList, 1, wx.EXPAND)

		self.panel.SetSizer(sizer)

		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyEvent)

	# We control the different events that occur.
	def onKeyEvent(self, event):
		if event.GetUnicodeKey() == wx.WXK_RETURN:
			focus = wx.Window.FindFocus().GetId()
			if focus == 101:
				if self.searchTermCtrl.GetValue() == "":
					gui.messageBox(_("El cuadro de búsqueda no puede estar vacío. Debes introducir un término a buscar."), caption=_("¡Error!"), style=wx.ICON_ERROR)
					return
				self.results.clear()
				term = self.searchTermCtrl.GetValue()
				wx.CallAfter(searchInformation, self, term)
			elif focus == 102:
				selectedPageid = self.results[self.resultsList.GetSelection()].getPageid()
				wx.CallAfter(getArticle, self, selectedPageid, self.languages[self.languagesList.GetSelection()])
		elif event.GetUnicodeKey() == wx.WXK_ESCAPE:
			self.searchTermCtrl.Clear()
			self.resultsList.Clear()
			self.Hide()
		else:
			event.Skip()

# Auxiliary function to load the list of available languages correctly in the interface.
	def loadLanguagesList(self):
		 loadLanguages(self)
