#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
#
#  python.py
#  
#  Copyright 2020 Danitxu <danitxu@Anabasa-Games>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

"""
Created on Fri Apr  3 03:33:45 2020

@author: danitxu
"""

from __future__ import print_function

import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import configparser
from unshortenit import UnshortenIt
from urllib.parse import urlparse
from subprocess import call
import configparser

configuracion = configparser.ConfigParser()
terminamos = 0


def sleeper(tiempo):
    
    time.sleep(tiempo)


def carga_configuracion():
    
    global configuracion
    if os.path.isfile('3d-load.cfg'):
        print('Existe archivo de configuración.')
        configuracion = configparser.ConfigParser()
        #        configuracion['Ult.Descargado'] = {'ult.descargado' : 'Nuevo'}
        #        configuracion['Categorias'] = {'clothings' : 'reset', 'environment' : 'reset'}
        #        configuracion['Categorias'] = {}echo
        #        print(configuracion['Ult.Descargado']['ult.descargado'])
        # configuracion['Categorias'] = {}
        # configuracion['TiempoEspera'] = {'tiempo' : 300}
        configuracion.read('3d-load.cfg')
    #        with open("3d-load.cfg","r") as archivo:
    #         for linea in archivo:
    #            print(linea)
    else:
        print('No existe archivo de configuración')
        file = open("3d-load.cfg", "w")
        file.write("configuracion de 3D-Load \n" + os.linesep)
        file.close()

    if os.path.exists("download"):
        pass
    else:
        os.mkdir("download")
    if os.path.exists("extract"):
        pass
    else:
        os.mkdir("extract")
        

def pre_carga():
    
    global configuracion
    print('\n\n Cargando la configuración de 3d-load \n\n')
    
    if os.path.isfile('3d-load.cfg'):
        print(' Existe archivo de configuración.')
        configuracion = configparser.ConfigParser()
        configuracion.read('3d-load.cfg')
    else:
        print(' No existe archivo de configuración')
        file = open("3d-load.cfg", "w")
        file.write("[configuracion de 3D-Load]\n\n" + os.linesep)
        file.close()
    
    if os.path.isfile('listado.ini'):
        fic = open('listado.ini', "r")
        listado = []
        for line in fic:
            listado.append(line)
        fic.close()
    else:
        file = open("listado.ini", "w")
        file.write("[Listado de archivos descargados]\n\n" + os.linesep)
        file.close()
    
    
def carga(page):
    
    global configuracion
    global terminamos
    browser = webdriver.Chrome()
    browser2 = webdriver.Chrome()
    
    web = 'https://3d-load.net/page/' + str(page) + '/'
    print(' \n Accediendo a: ' + web + '\n''')
    browser.get(web)
    assert '3DLOAD' in browser.title
    # sleeper(5)
    
    for a in browser.find_elements_by_class_name('link'):
        links = a.get_attribute('href')
        print(links)
        browser2.get(links)
        # browser2.minimize_window()
        # browser.minimize_window()
        for b in browser2.find_elements_by_class_name('shortcode.button.red.large'):
            alinks = b.get_attribute('href')
            # print(alinks + '\n')
            unshortener = UnshortenIt()
            uri = unshortener.unshorten(alinks)
            print(uri + '\n')
            igual = uri.find("=")
            total = len(uri)
            file_id = uri[igual + 1:total]
            #            print("Descargando: ", file_id +'\n\n')
            o = urlparse(links)
            #                print(o)
            #                print (o.path)
            oPath = o.path
            #            print("len")
            #            print(len(oPath))
            
            oPath = oPath[:len(oPath) - 1]
            #            print(oPath)
            a = 0
            while a != -1:
                a = oPath.find("/")
                oPath = oPath[a + 1:len(oPath)]
                ocat = o.path[1:len(o.path)]
            # print(ocat)
            a = ocat.find("/")
            #            print(a)
            file_name = ocat[a + 1:len(ocat) - 1]
            ocat = ocat[0:a]
            
            #            print(ocat)
            #            print(file_name)
            #            print(file_id)
            
            listado = open('listado.ini', 'r')
            lista = listado.readlines()
            listado.close()
            # print(lista)
            # print(file_name)
            if file_name + '\n' not in lista:
                print(" \n Descargando fichero: " + file_name + '\n')
                os.system('mega-get --ignore-quota-warn ' + file_id + ' ./download/' + file_name)
                print('\nDescomprimiendo en el directorio \'extract\'')
                #                        title2 = oPath.replace('-',' ')
                #                        title2 = title2.title()
                #                        print(title2)
                os.system('unrar x -u "./download/"' + file_name + ' ./extract/')
                print('\nBorrando el archivo \'.rar\'')
                #                        borra = './download/' + title2 + '.rar'
                #                        os.remove (borra)
                try:
                    os.remove('./download/' + file_name)
                except OSError as e:
                    print(e)
                else:
                    print("File is deleted successfully")
                with open('3d-load.cfg', 'w') as archivoconfig:
                    configuracion.write(archivoconfig)
                listado = open("listado.ini", mode="a", encoding="utf-8")
                listado.write(file_name + '\n')
                listado.close()
            else:
                print('si está')
                ultconf = configuracion['Ult.Descargado']['ult.descargado']
                if ultconf == file_name:
                    terminamos = 1
                    break
    browser.close()
    browser2.close()
    

def main(args):
    pre_carga()
    carga_configuracion()
    page = 0
    while terminamos == 0:
        carga(page)
        page = page + 1
    
    return 0


if __name__ == '__main__':
    import sys
    
    sys.exit(main(sys.argv))
