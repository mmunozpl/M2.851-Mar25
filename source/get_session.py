"""
get_session.py
Este módulo contiene la función get_session, que crea y devuelve una sesión
de requests configurada con reintentos y un User-Agent personalizado
"""

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

USER_AGENT: str = 'Mozilla/5.0 (compatible; DataSciencePracticeScraper/1.0)'
REQUEST_TIMEOUT: int = 10  # segundos


def get_session() -> Session:
    """
    Crea y devuelve una sesión de requests configurada con reintentos
    y cabeceras personalizadas

    Returns:
        Session: Objeto requests.Session configurado.
    """
    session: Session = Session()
    session.headers.update({'User-Agent': USER_AGENT})
    retry_strategy = Retry(
        total=3,  # Número total de reintentos
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
        backoff_factor=0.5  # Tiempo incremental entre reintentos
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session
