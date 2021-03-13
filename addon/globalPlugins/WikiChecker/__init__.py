# Complemento wikiChecker para NVDA.
# Autor: Antonio Cascales.
# Fecha: 7 de marzo de 2021.

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

class VentanaPrincipal(wx.Frame):
	def __init__(self, padre, titulo):
		super(VentanaPrincipal, self).__init__(padre, -1, titulo, size=(600,400))
		
		self.panel = wx.Panel(self, wx.ID_ANY)
		
		boxSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.etiquetaBuscarLbl = wx.StaticText(self.panel, wx.ID_ANY, "Término a buscar")
		self.busquedaCtrl = wx.TextCtrl(self.panel, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
		self.busquedaCtrl.Bind(wx.EVT_TEXT_ENTER, self.onBuscar)
		
		self.articulosDisponiblesLbl = wx.StaticText(self.panel, wx.ID_ANY, "Artículos disponibles")
		self.listaResultados = wx.ListBox(self.panel, wx.ID_ANY, choices=[], style=wx.LB_SINGLE)
		self.listaResultados.Bind(wx.EVT_LISTBOX, self.onMostrarArticulo)
		
		self.etiquetaResultadoLbl = wx.StaticText(self.panel, wx.ID_ANY, "Resultado de la búsqueda")
		self.resultadoCtrl = wx.TextCtrl(self.panel, wx.ID_ANY, "", style=wx.TE_MULTILINE|wx.TE_READONLY, size=(300,200))
#		self.resultadoCtrl.Hide()
		
		self.aceptarBtn = wx.Button(self.panel, wx.ID_ANY, "Aceptar")
		self.aceptarBtn.Bind(wx.EVT_BUTTON, self.onBuscar)
		self.cancelarBtn = wx.Button(self.panel, wx.ID_ANY, "Cancelar")
		
		self.panel.SetSizer(boxSizer)
	
	def onBuscar(self, event):
		termino = self.busquedaCtrl.GetValue()
		self.obtenerInformacion(termino)
	
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
	
	def onMostrarArticulo(self, event):
		opcion = self.listaResultados.GetSelection()
		pageid = self.resultados[opcion].getPageid()
		wx.CallAfter(self.obtenerArticulo, pageid)
	
	def obtenerArticulo(self, pageid):
		url = "https://es.wikipedia.org/?curid=" + str(pageid)
		req = request.Request(url, data=None, headers={"User-Agent": "Mozilla/5.0"})
		html = request.urlopen(req)
		datos = html.read().decode("utf-8")
		bs = BeautifulSoup(datos, 'html.parser')
		
		for string in bs.stripped_strings:
			self.resultadoCtrl.AppendText(repr(string))

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
