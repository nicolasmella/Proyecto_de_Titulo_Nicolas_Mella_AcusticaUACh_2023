import os
import glob
from PyPDF2 import PdfMerger

def unirpdf(carpeta_contenedora, nombre_archivo):
    # Obtener la lista de archivos .pdf en el mismo orden en que están en la carpeta
    archivos_pdf = sorted(glob.glob(os.path.join(carpeta_contenedora, "*.pdf")), key=os.path.getmtime)
    
    # Crear un objeto PdfMerger
    fusionador = PdfMerger()

    # Recorrer los archivos PDF y agregarlos al fusionador
    for archivo in archivos_pdf:
        ruta_archivo = os.path.join(carpeta_contenedora, archivo)
        fusionador.append(ruta_archivo)

    # Ruta y nombre de archivo deseados para el archivo fusionado
    carpeta_destino = carpeta_contenedora

    # Ruta y nombre de archivo de salida
    archivo_salida =  carpeta_destino + '/' + nombre_archivo + ".pdf"

    # Fusionar los archivos y guardar el resultado en el archivo de salida
    fusionador.write(archivo_salida)

    # Cerrar el fusionador
    fusionador.close()

    # Eliminar los archivos individuales PDF
    for archivo in archivos_pdf:
        ruta_archivo = os.path.join(carpeta_contenedora, archivo)
        os.remove(ruta_archivo)
