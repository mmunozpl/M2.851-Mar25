# Practica1-M2851-Mar25
Tipología y ciclo de vida de los datos Práctica 1 UOC Mar2025

# BOE Data Scraper

Scraper en Python para extraer anuncios de licitaciones y contrataciones diarias publicadas en el BOE (Boletín Oficial del Estado) a lo largo de un período definido de 10 años (2014-2024). El proceso se organiza de forma modular en varios archivos y el dataset se guarda en el directorio `CSV`

## Estructura del Proyecto

```
. 
├── CSV
│   ├── LICENSE_dataset.txt 
│   └── licitaciones_contrataciones_BOE_2014_2024.csv # CSV generado tras la ejecución
├── LICENSE.txt 
├── LICENSE_dataset.txt 
├── README.md 
├── requirements.txt 
└── source 
    ├── get_session.py 
    ├── obtener_analisis.py 
    ├── obtener_extra_texto.py 
    ├── obtener_anuncios.py 
    └── main.py
```

  
## Descripción del Código

El proceso se organiza en cuatro apartados:

- **Extracción y procesamiento de los anuncios diarios – función `obtener_anuncios`**  
  - Convierte la fecha de entrada al formato deseado ("dd/mm/aaaa")
  - Solicita la página diaria del BOE y, en caso de error (como 404), salta ese día sin interrumpir el flujo
  - Recorre el contenido de la página para actualizar la "Institucion" (cada `<h4>`) y extraer, para cada anuncio (elemento `<li>` con clase `dispo`), datos básicos: organismo responsable, objeto, expediente, enlace HTML y un valor inicial para "Tipo" (según el texto del anuncio)
  - Llama a las funciones `obtener_analisis` y `obtener_extra_texto` para complementar el anuncio con información adicional  
  - **Validación del campo "Tipo"**: Antes de actualizar el campo "Tipo" con los datos obtenidos de "ANÁLISIS", se valida que el valor extraído sea exactamente "Licitación" o "Contratación". Sólo en ese caso se sobrescribe el valor inicial, garantizando que el campo "Tipo" contenga únicamente uno de esos dos valores

- **Extracción de la sección “ANÁLISIS” – función `obtener_analisis`**  
  - Solicita la página detallada del anuncio y, mediante BeautifulSoup, busca el div con id `analisis`  
  - Extrae los datos contenidos en el elemento `<dl>` (usando `<dt>` y `<dd>`) para atributos como Modalidad, Tipo, Procedimiento, Ámbito geográfico, Materias (CPV) y Observaciones
  - Utiliza un diccionario para mapear los textos de `<dt>` a las claves deseadas, asignando "No disponible" en caso de ausencia

- **Extracción de información adicional del bloque de texto – función `obtener_extra_texto`**  
  - Solicita nuevamente la misma página del anuncio, buscando en el div (normalmente con id `textoxslt`) otro bloque de metadatos
  - Extrae el valor de "códigos cpv" y lo asigna a la clave `Codigos_CPV`

- **Recorrido del período y generación del DataFrame – módulo `main.py`**  
  - Define un rango de fechas (por ejemplo, del 1 de enero de 2014 al 31 de diciembre de 2024) y recorre día a día
  - Llama a `obtener_anuncios` para extraer los datos diarios y acumula todos los anuncios
  - Aplica un delay entre solicitudes para no saturar el servidor
  - Crea un DataFrame con pandas y guarda el resultado en un archivo CSV dentro del directorio `CSV`
  - El dataset tiene los siguientes atributos
    - **Institucion**. Nombre de la entidad u organismo que publica el anuncio, extraído de los encabezados () de la página del BOE
    - **Organismo responsable**. Indica la parte responsable del anuncio, obtenido mediante una expresión regular que identifica la parte del texto que sigue a "de"
    - **Expediente**. Código o identificador del contrato o anuncio, que facilita la identificación y seguimiento del proceso
    - **Fecha**. La fecha de publicación del anuncio en formato dd/mm/aaaa, obtenida a partir de la fecha que aparece en la URL del día correspondiente
    - **Tipo**. Clasificación del anuncio, que indica si se trata de una "Licitación" o "Contratación", según el texto del anuncio
    - **Objeto**. Descripción breve del objeto del contrato, indicando qué se pretende contratar o licitar
    - **Procedimiento**. Detalles sobre el procedimiento de contratación, extraídos de la sección de análisis
    - **Ambito_geografico**. Información sobre el ámbito geográfico al que se dirige el anuncio, por ejemplo, una comunidad autónoma o región
    - **Materias_CPV**. Datos sobre las materias, basados en el código CPV y la descripción asociada, que permite clasificar el tipo de obra o servicio
    - **Codigos_CPV**. Campo complementario que contiene otros códigos CPV asociados al anuncio, extraídos de la sección de texto
    - **Observaciones**. Comentarios adicionales que pueden incluir notas o detalles relevantes sobre el anuncio
    - **Enlace HTML**. URL que dirige a la página completa y  detallada del anuncio, desde donde se han extraído los datos enriquecidos

## Buenas Prácticas y Consideraciones Éticas

- **Persistencia de Conexión**. Se utiliza una sesión de `requests` con cabeceras personalizadas para mejorar la eficiencia
- **Timeout y Reintentos**. Cada solicitud tiene un timeout configurado y se implementan reintentos para gestionar errores específicos
- **Delay entre Solicitudes**. Se introduce un delay para evitar saturar el servidor del BOE, respetando así las políticas de uso
- **Manejo de Errores**. Se capturan y gestionan errores y excepciones, permitiendo que el proceso continúe sin interrumpirse
- **Modularidad**. El código está organizado en módulos separados por función, lo que facilita el mantenimiento y la revisión

## Requisitos

- Python 3.9  
- Las siguientes librerías (puedes instalarlas con `pip install -r requirements.txt`):
  - requests == 2.31.0
  - urllib3 == 2.2.3
  - beautifulsoup4 == 4.12.3
  - pandas == 2.0.3

## Uso

Para ejecutar el scraper, navega al directorio `source` y ejecuta:

```bash
python main.py
```
