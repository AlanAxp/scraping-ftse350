# Web Scraping

Código que implementa la técnica de *web scraping* para extraer la información de las compañias que se encuentran en la bolsa de valores de Londres, directamente de la [página oficial](https://www.londonstockexchange.com/)


### Para ejecutar el codigo

Instalar la libreria BeautifulSoup

```bash
pip install beautifulsoup4
```

Correr el código con python 

```bash
python3 scraping.py
```

Se obtiene un archivo `.csv` con los datos de los stocks y nombres de las 350 compañias.
