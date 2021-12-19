#WikiChecker for NVDA.
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.
#Copyright (C) 2021 Antonio Cascales <antonio.cascales@gmail.com>

import globalPluginHandler
import ui
import api
import gui

from scriptHandler import script

from .view import *

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.mainWindow = MainWindow(gui.mainFrame, _("WikiChecker - Ventana Principal"))
		self.mainWindow.loadLanguagesList()
	
	@script(gesture="kb:NVDA+e")
	def script_checkWikiTerm(self, gesture):
		if not self.mainWindow.IsShown():
			gui.mainFrame.prePopup()
			self.mainWindow.Show()
			self.mainWindow.Centre()
			gui.mainFrame.postPopup()
