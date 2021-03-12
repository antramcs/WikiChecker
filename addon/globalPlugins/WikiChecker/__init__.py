# Complemento wikiChecker para NVDA.
# Autor: Antonio Cascales.
# Fecha: 7 de marzo de 2021.

import globalPluginHandler
import scriptHandler

import wx
import json
import re

from urllib import request

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	@scriptHandler.script(gesture="kb:NVDA+e")
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
		self.listaResultados.Bind(wx.EVT_LISTBOX_DCLICK, self.onMostrarArticulo)
		
		self.etiquetaResultadoLbl = wx.StaticText(self.panel, wx.ID_ANY, "Resultado de la búsqueda")
		self.resultadoCtrl = wx.TextCtrl(self.panel, wx.ID_ANY, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
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
		resultados = []
		
		for i in info:
			resultados.append(i["title"])
		
		self.listaResultados.Clear()
		self.listaResultados.AppendItems(resultados)
		self.listaResultados.SetFocus()
	
	def onMostrarArticulo(self, event):
		opcion = self.listaResultados.GetSelection()
		texto = self.listaResultados.GetString(opcion)
		self.resultadoCtrl.SetValue(texto)