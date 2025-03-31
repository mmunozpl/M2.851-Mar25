"""
obtener_extra_texto.py
Este módulo define la función obtener_extra_texto,
que extrae información complementaria (sobre códigos CPV)
de cada página detallada del anuncio del BOE
"""

from typing import Dict
from bs4 import BeautifulSoup
from source.get_session import get_session

REQUEST_TIMEOUT: int = 3

def obtener_extra_texto(enlace_html: str) -> Dict[str, str]:
    """
    Extrae información adicional del bloque de texto
    (normalmente con id "textoxslt") de la página del anuncio

    Args:
        enlace_html (str): URL de la página del anuncio

    Returns:
        Dict[str, str]: Diccionario con el campo "codigos_CPV"
    """
    campos: Dict[str, str] = {
        "Codigos_CPV": "No disponible"
    }
    session = get_session()
    try:
        response = session.get(enlace_html, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            return campos
        soup = BeautifulSoup(response.text, 'html.parser')
        texto_div = soup.find('div', id='textoxslt')
        if not texto_div:
            return campos
        dl = texto_div.find('dl')
        if not dl:
            return campos
        for dt in dl.find_all('dt'):
            key_text = dt.get_text(strip=True)
            dd = dt.find_next_sibling('dd')
            if dd:
                value = dd.get_text(" ", strip=True)
                if "códigos cpv" in key_text.lower():
                    campos["Codigos_CPV"] = value
    except Exception as e:
        print(f"Error obteniendo extra texto de {enlace_html}: {e}")
    return campos
