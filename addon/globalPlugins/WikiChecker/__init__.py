#WikiChecker for NVDA.
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.
#Copyright (C) 2021 Antonio Cascales <antonio.cascales@gmail.com>

# We import the modules necessary for the operation of the plugin.
import globalPluginHandler
import ui
import api
import gui
import languageHandler
import globalVars
import config
import core
import addonHandler

from scriptHandler import script

from .view import *

# We call the function in charge of translations.
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()

		if globalVars.appArgs.secure or config.isAppX:
			return

		# Translators: Name of the plugin's main window.
		self.mainWindow = MainWindow(gui.mainFrame, _("WikiChecker - Ventana Principal"))
		if hasattr(globalVars, 'wikiChecker'):
			self.postStartupHandler()
		core.postNvdaStartup.register(self.postStartupHandler)
		globalVars.wikiChecker = None

		# We created an option within the Tools submenu of the NVDA menu, so that the user can call it from there.
		self.menu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.wikiMenu = self.menu.Append(wx.ID_ANY, "&WikiChecker")
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onStart, self.wikiMenu)

	@script(gesture=None,
	# Translators: Description of the plugin.
	description=_("Busca los artículos relacionados con el término introducido en Wikipedia."),
	# Translators: Plugin category name.
	category=_("WikiChecker"))
	def script_checkWikiTerm(self, gesture):
		if len(self.mainWindow.languages)==0:
			self.mainWindow.loadLanguagesList()
		elif self.mainWindow.okLanguages:
			if not self.mainWindow.IsShown():
				gui.mainFrame.prePopup()
				self.mainWindow.Show()
				self.mainWindow.searchTermCtrl.SetFocus()
				self.mainWindow.resultsList.Enabled = False
				self.mainWindow.resultsList.SetItems([])
				self.mainWindow.readArticleBtn.Enabled = False
				self.mainWindow.CenterOnScreen()
				gui.mainFrame.postPopup()
		else:
			# Translators: Message shown to the user if it is not possible to load the languages ​​available in wikipedia.
			msg = \
_("""No se pudieron cargar los idiomas del complemento. Vuelve a intentarlo en unos segundos.

Si el problema persiste comprueba tu conexión a Internet, o reinicia NVDA.""")
			ui.message(msg)

	def postStartupHandler(self):
		self.mainWindow.loadLanguagesList()

	def onStart(self, event):
		self.script_checkWikiTerm(None)

	def terminate(self):
		core.postNvdaStartup.unregister(self.postStartupHandler)

		self.menu.Remove(self.wikiMenu.Id)
		self.wikiMenu.Destroy()
		self.wikiMenu = None
