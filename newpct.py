#!/usr/bin/env python
#-*- coding: utf-8 -*-

__pychecker__ = 'no-callinit no-classattr'

import mechanize
import os
import re
import sys
import uuid
import xml.parsers.expat
import urllib2


def LocalizarTorrentID(url):
  fichero = 'wget ' + url + ' -O temporal.html'
  os.system(fichero)
  localFile = open('temporal.html', 'r')
  pagina = localFile.read()
  localFile.close()
  os.system('rm temporal.html')
  #print 'Pagina descargada a localizar el Id'
  posicion = pagina.find('http://tumejorjuego.com')
  #print '----------------------------------'
  #print posicion
  #print '----------------------------------'
  id = ''
  if posicion > 0:
    id = pagina[posicion: posicion + 99999999999]
    posicion = id.find(" title=")
    id = id[0:posicion-1]
  return id

def Excepciones(cadena):
   cadena = cadena.replace('Intelligence', 'Intelligence (2014)')
   cadena = cadena.replace('La Caza (The Fall)', 'La Caza')
   cadena = cadena.replace('Resurrection (The Returned)', 'Resurrection')
   cadena = cadena.replace('Vikings', 'Vikingos')
   cadena = cadena.replace('Sillicon Valley', 'Silicon Valley')
   cadena = cadena.replace('The bridge', 'The bridge (2013)')
   cadena = cadena.replace('The Bridge', 'The Bridge (2013)')
   return cadena


class RSSParser(object):
  def __init__(self):
    object.__init__(self)
    self.__element = None
    self.__links = None
    self.__titulos = None
    self.__fechas = None
    self.__anotarFecha = None

  def __start_element(self, name, attrs):
    attrs = (attrs, )
    self.__element.append(name)

  def __end_element(self, name):
    if self.__element[-1] == name:
      self.__element.pop()

  def __char_data(self, data):
    if data.find('[Cap.') != -1 and self.__element[-1] == 'title':
      self.__titulos.append(data)
      self.__anotarFecha = 1
    if self.__element[-1] == 'pubDate' and self.__anotarFecha == 1:
      self.__fechas.append(data)
      self.__anotarFecha = 0
    if 'item' not in self.__element or self.__element[-1] != 'link':
      return
    if data.find('serie') == -1:
      return
    self.__links.append(data)

  def parse(self, data):
    self.__element = list()
    self.__links = list()
    self.__titulos = list()
    self.__fechas = list()
    self.__anotarFecha = 0
    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler = self.__start_element
    p.EndElementHandler = self.__end_element
    p.CharacterDataHandler = self.__char_data
    p.Parse(data)

  def links(self):
    return self.__links

  def elements(self):
    return self.__element

  def Titulos(self):
    return self.__titulos

  def Fechas(self):
    return self.__fechas



class Browser(object):
  def __init__(self):
    object.__init__(self)
    self.__browser = mechanize.Browser()

    self.__browser.open('http://www.newpct1.com/')


  def __identify_login_form(self, form):
    #return 'login' in (x.name for x in form.controls)
    return 'sendLogin' in (x.name for x in form.controls)

  def __log_in(self):
    self.__browser.open('http://www.newpct1.com/entrar/')
    try: # Logging in
      self.__browser.select_form(predicate=self.__identify_login_form)
      self.__browser.form['userName'] = 'uSuArIo'
      self.__browser.form['userPass'] = 'CoNtRaSeÑa'
      self.__browser.submit()
      print 'Logado'
    except mechanize.FormNotFoundError, e:
      print 'Error al logarse'
      print e
      pass # Already logged in

  def download_link(self, url, nombre):
    self.__browser.open(url)

    #print url

    filename = '/ruta-donde-quieres-descargar-los-torrents/torrents/' + nombre + '.torrent'
    fd = open(filename, 'w')
    fd.write(self.__browser.response().read())
    fd.close()

    return True

  def download_RSS_entries(self):
    self.__browser.open('http://feeds.feedburner.com/newpctorrent')
    p = RSSParser()
    p.parse(self.__browser.response().read())
    for link in p.links():
      self.download_link(link)

#comenzamos

if __name__ == '__main__':
  if len(sys.argv) == 0:
    print 'Usage: %s <url> [url] ...'
    sys.exit(1)

  browser = Browser()

  a = mechanize.Browser()
  a.open('http://feeds.feedburner.com/newpctorrent')
  #a.open('http://feeds2.feedburner.com/newpctorrent')

  p = RSSParser()
  p.parse(a.response().read())

  link = list()
  link = p.links()
  titulos = list()
  titulos = p.Titulos()
  fechas = list()
  fechas = p.Fechas()

  fichero = open('/ruta-donde-quieres-dejar-el-fichero/newpct.php', 'w')
  fichero.write('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n')
  fichero.write('<channel>\n')
  fichero.write('<title>NewPct - powered by FeedBurner</title>\n')
  fichero.write('<description>Latest Torrents</description>\n')
  fichero.write('<link>http://www.newpct.com/</link>\n')
  fichero.write('<language>es-es</language>\n')
  fichero.write('<ttl>15</ttl>\n')
  fichero.write('<image>\n')
  fichero.write('\t<title>NewPct - powered by FeedBurner</title>\n')
  fichero.write('\t<url>http://www.newpct.com</url>\n')
  fichero.write('\t<link>http://www.newpct.com</link>\n')
  fichero.write('</image>\n')

  pos = 0
  salir = 0
  debug = 0
  while pos < len(titulos)-1 and debug == 0:
    aux = link[pos]
    urlOriginal = aux
    aux = aux.replace('www.newpct.com','www.newpct1.com').replace('descargar-serie', 'descarga-torrent/serie')  #.replace('/serie/','/descargar-torrent/serie/')
    print aux
    url = LocalizarTorrentID(aux)
    if url == '':
      url = LocalizarTorrentID(urlOriginal)
      if url == '':
        salir = 1
        #debug = 1
        print '------->>>> Error la url esta vacia'


    try:
      titulo = titulos[pos].encode('utf-8')
    except:
      salir = 1
      print '--------------->>>>> Error salvando el enlace en el fichero php'
    if salir == 0:
      posInicio = titulo.find('[Cap.')
      posFin = titulo.find('][Espa')
      if posFin <= 0:
        posFin = titulo.upper().find('][AC')
        if posFin <=0:
          posFin = titulo.find('[Espa')
      titulo = titulo[0:titulo.find('- Temporada')] + '- ' + titulo[posInicio+5:posFin-2] + 'x' + titulo[posFin-2:posFin]
      titulo = Excepciones(titulo)
      #browser.download_link('http://www.pctorrent.com/descargar/index.php?link=descargar/torrent/'+torrentId+'/dummy.html',titulo)
      #browser.download_link('http://tumejorjuego.com/descargar/index.php?link=descargar/torrent/'+torrentId+'/dummy.html',titulo)
      browser.download_link(url, titulo)
      fichero.write('<item>\n')
      fichero.write('\t<title>' + titulo  +'</title>\n')
      fichero.write('\t<category>Series-TV</category>\n')
      fichero.write('\t<link>http://192.168.XXX.XXX/rss/tmp/' + titulo + '.torrent</link>\n')
      fichero.write('\t<pubDate>' + fechas[pos] + '</pubDate>\n')
      fichero.write('</item>\n')
    salir = 0
    pos = pos + 1

  fichero.write('</channel>\n')
  fichero.write('</rss>\n')
  fichero.close()
