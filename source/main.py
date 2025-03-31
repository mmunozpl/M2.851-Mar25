"""
main.py
Módulo principal que recorre el período definido, extrae los anuncios
diarios del BOE y genera un DataFrame que se guarda en un archivo CSV
dentro del directorio CSV
"""

import os
import time
from datetime import datetime, timedelta
import pandas as pd
from source.obtener_anuncios import obtener_anuncios

REQUEST_DELAY: int = 3  # segundos

def main() -> None:
    """
    Función para extraer los datos diarios del BOE y generar el CSV final
    """
    # Se define el período: del 1 de enero de 2014 al 31 de diciembre de 2024
    start_date = datetime(2014, 1, 1)
    end_date = datetime(2024, 12, 31)
    todos_anuncios = []
    current_date = start_date

    while current_date <= end_date:
        fecha_str = current_date.strftime("%Y/%m/%d")
        lista = obtener_anuncios(fecha_str)
        print(f"Obtenidos {len(lista)} anuncios del BOE del día {fecha_str}")
        todos_anuncios.extend(lista)
        current_date += timedelta(days=1)
        time.sleep(REQUEST_DELAY)

    df = pd.DataFrame(todos_anuncios)

    # Reordenar columnas
    column_order = [
        "Institucion",
        "Organismo responsable",
        "Expediente",
        "Fecha",
        "Modalidad",
        "Tipo",
        "Objeto",
        "Procedimiento",
        "Ambito_geografico",
        "Materias_CPV",
        "Codigos_CPV",
        "Observaciones",
        "Enlace HTML"
    ]
    existing_cols = [col for col in column_order if col in df.columns]
    df = df[existing_cols]

    # Comprobación directorio CSV y grabado del dataset
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "CSV")
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, "licitaciones_contrataciones_BOE_2014_2024.csv")
    df.to_csv(output_filename, index=False)
    print(f"Dataset guardado en {output_filename}")
    print("Tamaño de dataset:",df.shape)
    print(df.head(15))

if __name__ == '__main__':
    main()
