#WikiChecker for NVDA.
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.
#Copyright (C) 2021 Antonio Cascales <antonio.cascales@gmail.com>

import globalPluginHandler
import ui
import api
import textInfos
import gui

from scriptHandler import script

import wx
import json
import re
import sys, os

from threading import Thread

import webbrowser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
	del sys.modules['html']
except:
	pass

from bs4 import BeautifulSoup

from urllib import request

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	@script(gesture="kb:NVDA+e")
	def script_checkWikiTerm(self, gesture):
		ventanaPrincipal = VentanaPrincipal(None, "WikiChecker - Ventana Principal")
		ventanaPrincipal.Show()

class VentanaPrincipal(wx.Dialog):
	def __init__(self, padre, titulo):
		super(VentanaPrincipal, self).__init__(padre, -1, titulo, size=(1000,700))
		
		self.panel = wx.Panel(self, wx.ID_ANY)
		
		boxSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.etiquetaBuscarLbl = wx.StaticText(self.panel, wx.ID_ANY, "Término a buscar")
		self.busquedaCtrl = wx.TextCtrl(self.panel, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
		self.Bind(wx.EVT_TEXT_ENTER, self.onBuscar, self.busquedaCtrl)
		
		self.articulosDisponiblesLbl = wx.StaticText(self.panel, wx.ID_ANY, "Artículos disponibles")
		self.listaResultados = wx.ListBox(self.panel, wx.ID_ANY, choices=[], style=wx.LB_SINGLE)
		self.listaResultados.Bind(wx.EVT_LISTBOX, self.onBuscarItem)
		
		self.areaTexto = wx.TextCtrl(self.panel, wx.ID_ANY, "", style= wx.TE_MULTILINE | wx.TE_READONLY)
		
		self.aceptarBtn = wx.Button(self.panel, wx.ID_OK, "Aceptar")
		
		self.cancelarBtn = wx.Button(self.panel, wx.ID_CANCEL, "Cancelar")
		
		self.panel.SetSizer(boxSizer)
	
	def onBuscar(self, event):
		termino = self.busquedaCtrl.GetValue()
		self.obtenerInformacion(termino)
		event.Skip()
	
	def eliminarEtiquetas(self, texto):
		return re.sub(r'<[^>]*?>', '', texto)
	
	def obtenerInformacion(self, termino):
		req = request.Request("https://es.wikipedia.org/w/api.php?action=query&list=search&srprop=snippet&format=json&origin=*&utf8=&srsearch=" + termino, data=None, headers={"User-Agent": "Mozilla/5.0"})
		html = request.urlopen(req)
		datos = html.read().decode("utf-8")
		diccionario = json.loads(datos)
		info = diccionario["query"]["search"]
		self.resultados = []
		self.listaResultados.Clear()
		
		for i in info:
			resultado = Resultado(i["title"], self.eliminarEtiquetas(i["snippet"]), i["pageid"])
			self.resultados.append(resultado)
			self.listaResultados.AppendItems(resultado.__str__())
		
		self.listaResultados.SetFocus()
	
	def onBuscarItem(self, event):
		opcion = self.listaResultados.GetSelection()
		pageid = self.resultados[opcion].getPageid()
		
		wx.CallAfter(self.obtenerArticulo, pageid)
	
	def obtenerArticulo(self, pageid):
		hilo = HiloConsulta(self, pageid)
		hilo.start()

class Resultado():
	def __init__(self, title, snippet, pageid):
		self.title = title
		self.snippet = snippet
		self.pageid = pageid
	
	def getTitle(self):
		return self.title
	
	def getSnippet(self):
		return self.snippet
	
	def getPageid(self):
		return self.pageid
	
	def __str__(self):
		return self.title + ": " + self.snippet

class HiloConsulta(Thread):
	def __init__(self, padre, pageid):
		super(HiloConsulta, self).__init__()
		
		self.daemon = True
		self.padre = padre
		self.pageid = pageid
	
	def run(self):
#		self.padre.areaTexto.Clear()
#		
		url = "https://es.wikipedia.org/?curid=" + str(self.pageid)
#		req = request.Request(url, data=None, headers={"User-Agent": "Mozilla/5.0"})
#		html = request.urlopen(req)
#		datos = html.read().decode("utf-8")
#		
#		self.padre.areaTexto.write(self.padre.eliminarEtiquetas(datos))
		webbrowser.open(url)
