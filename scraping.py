#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 18:19:50 2021

@author: delta
"""

# =============================================================================
# =============================================================================
# PARA DESCARGAR LOS DATOS DESDE LA PAGINA OFICIAL DEL FTSE350 LONDON STOCK EX.
 
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re

paginas = np.arange(1,19) #1 a 18
url_base = "https://www.londonstockexchange.com/indices/ftse-350/constituents/table?page={}"
urls = [ url_base.format(pagina) for pagina in paginas ]

stocks_ = list()
nombres_ = list()

for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    nom_ticker = soup.find_all("td", class_ = r"clickable bold-font-weight instrument-tidm gtm-trackable td-with-link" )
    tickers = list()
    for stock in nom_ticker:
        tickers.append(stock.text)
    stocks_ += tickers
    
    nomb = list()
    for td in soup.find_all('td', {'class': r"clickable instrument-name gtm-trackable td-with-link"}) :
        nomb.append(td.text)
    nombres_ += nomb
    
    
#Para obtener la informacion de los sectores

links = list()
for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    href = soup.find_all('app-link-or-dash')    
    hrefs = list()    
    for i in range(len(href)):
        texte = str(href[i])
        x = re.findall('stock/.*" ' ,texte)
        x[0] = x[0].replace('" ',"")
        hrefs.append(x[0])
    hiper_links = list(set(hrefs))
    links += hiper_links

#Para unir los link y obtener la siguiente pagin---

base = "https://www.londonstockexchange.com/"
termination = "/our-story"
links_sectors = list()
stock_for_reference = list()
for ref in links:
    aux_var = re.findall('/.*/', ref)[0].replace('/','')
    link_creation = base + ref + termination
    links_sectors.append(link_creation)
    stock_for_reference.append(aux_var)
    
#Para obtener los sectores hay que hacer nuevamente web scraping

sectors = list()
for link_sectors in links_sectors:
    page = requests.get(link_sectors)
    soup = BeautifulSoup(page.content, "html.parser")
    nom_sector = soup.find_all("div", class_ = r"bold-font-weight regular-font-size" )[2].text
    sectors.append(nom_sector)
    
#Dictioario para relacionar stocks con sectores!

stocks_sectors = dict(zip(stock_for_reference, sectors))
stocts_companies = dict(zip(stocks_, nombres_))
    

C0 = stock_for_reference # Columna 0, stocks
C1 = [ stocts_companies[stock] for stock in stock_for_reference ]
C2 = sectors # Columna 2, sectores
    
file_ftse350 = pd.DataFrame({'stock':C0, "Company":C1, "Sector":C2})
file_ftse350.to_csv('ftse350_stock_company_sector.csv', index=False)
    
    
    
    
    


