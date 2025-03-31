"""
obtener_analisis.py
Este módulo define la función obtener_analisis, que extrae
información de la sección "ANÁLISIS" de la página detallada
de cada anuncio del BOE
"""

from typing import Dict
from bs4 import BeautifulSoup
from source.get_session import get_session

REQUEST_TIMEOUT: int = 3

def obtener_analisis(enlace_html: str) -> Dict[str, str]:
    """
    Extrae datos de la sección "ANÁLISIS" de la página del anuncio

    Args:
        enlace_html (str): URL de la página del anuncio

    Returns:
        Dict[str, str]: Diccionario con campos: Modalidad, Tipo, Procedimiento,
        Ambito_geografico, Materias_CPV y Observaciones
    """
    campos: Dict[str, str] = {
        "Modalidad": "No disponible",
        "Tipo": "No disponible",
        "Procedimiento": "No disponible",
        "Ambito_geografico": "No disponible",
        "Materias_CPV": "No disponible",
        "Observaciones": "No disponible"
    }
    session = get_session()
    try:
        response = session.get(enlace_html, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            return campos
        soup = BeautifulSoup(response.text, 'html.parser')
        analisis_div = soup.find('div', id='analisis')
        if not analisis_div:
            return campos
        dl = analisis_div.find('dl')
        if not dl:
            return campos
        mapping = {
            "Modalidad": "Modalidad",
            "Tipo": "Tipo",
            "Procedimiento": "Procedimiento",
            "Ámbito geográfico": "Ambito_geografico",
            "Materias (CPV)": "Materias_CPV",
            "Observaciones": "Observaciones"
        }
        for dt in dl.find_all('dt'):
            key_text = dt.get_text(strip=True).rstrip(':')
            dd = dt.find_next_sibling('dd')
            if dd:
                value = dd.get_text(" ", strip=True)
                if key_text in mapping:
                    campos[mapping[key_text]] = value
    except Exception as e:
        print(f"Error obteniendo análisis de {enlace_html}: {e}")
    return campos
