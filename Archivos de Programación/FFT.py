import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import scipy.io.wavfile as wav

eps = 1e-8 #Valor pequeño para evitar indeterminación de la función logaritmo

# Función para calcular el espectro de frecuencia utilizando la FFT
def calcular_espectro(audio, fs, N):
    
    num_segmentos = len(audio) // N #segmentos en los que se dividirá el audio en función de N
    espectro_total = np.zeros(N//2 + 1) #crea un arreglo de ceros para almacenar el espectro acumulado

    for i in range(num_segmentos):
        inicio = i * N
        fin = inicio + N
        
        # Aplicar ventana de Hanning al segmento de audio
        ventana = np.hanning(N)
        segmento_ventaneado = audio[inicio:fin] * ventana

        # Calcular la FFT del segmento
        espectro = np.fft.fft(segmento_ventaneado, N)
        magnitud_espectro = np.abs(espectro)[:N//2 + 1]

        # Agregar al espectro total
        espectro_total += magnitud_espectro

    # Salimos del ciclo
    # Promediar el espectro acumulado
    espectro_total /= num_segmentos

    # Convertir a dBFS 
    magnitud_espectro_db = 20 * np.log10(espectro_total+eps)

    # Calcular los ejes de frecuencia
    f = np.arange(0, fs/2 + fs/N, fs/N)

    return f, magnitud_espectro_db


# Iterar sobre los archivos .wav
def iterar_archivos(carpeta_audio, fs, N, carpeta_fig_espectros,carpeta_data):
    # Crear un DataFrame para almacenar los datos de frecuencia y amplitud
    df_espectro = pd.DataFrame()

    # Bandas de tercio de octava
    bandas_tercio_octava = [20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000]
    
    # Obtener las frecuencias límite de cada banda de tercio de octava
    #frecuencias_limite = [banda * (2 ** (1/6)) for banda in bandas_tercio_octava]
    
    lower_limits = [17.8, 22.4, 28.2, 35.5, 44.7, 56.2, 70.7, 89.1, 112, 141, 178, 224, 282, 355, 447, 562, 708, 891, 1122, 1413, 1778, 2239, 2818, 3548, 4467, 5623, 7079, 8913, 11220, 14130]  # Valores de límite inferior para cada banda
    upper_limits = [22.4, 28.2, 35.5, 44.7, 56.2, 70.7, 89.1, 112, 141, 178, 224, 282, 355, 447, 562, 708, 891, 1122, 1413, 1778, 2239, 2818, 3548, 4467, 5623, 7079, 8913, 11220, 14130, 17780]  # Valores de límite superior para cada banda    

    # Crear un DataFrame vacío para almacenar los valores de amplitud promedio en 1/3 octava
    df_amplitudes = pd.DataFrame(columns=["Frecuencia"] + bandas_tercio_octava)

    # Obtener la lista de archivos .wav en la carpeta en el mismo orden en que están en la carpeta
    archivos_wav = sorted(glob.glob(os.path.join(carpeta_audio, "*.wav")), key=os.path.getmtime)
    
    for archivo_wav in archivos_wav:
        
        # Ruta completa del archivo de audio
        ruta_archivo = os.path.join(carpeta_audio, archivo_wav)
        nombre_archivo = os.path.splitext(os.path.basename(archivo_wav))[0] #obtiene el nombre del archivo sin extension

        # Leer el archivo de audio
        _,audio = wav.read(ruta_archivo)

        # Obtener el espectro de frecuencia
        f, magnitud_espectro_db = calcular_espectro(audio, fs, N)
        
        # Normalizar a 0 dB
        magnitud_espectro_db -= np.max(magnitud_espectro_db)

        # Agregar los datos al DataFrame de espectro
        df_espectro[archivo_wav.replace('.wav', '')] = magnitud_espectro_db

        # Ruta de la figura de espectro
        ruta_figura = os.path.join(carpeta_fig_espectros, archivo_wav.replace('.wav','.pdf').split('/')[-1])

        # Graficar el espectro de frecuencia
        plt.figure(figsize=(12, 6))
        plt.semilogx(f, magnitud_espectro_db)
        plt.xlim(20,20000)
        plt.ylim(-80,6)
        plt.xticks([20, 100, 500, 1000, 10000], ['20','100', '500', '1K', '10K'])
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Amplitud (dBFS)')
        plt.title('Espectro de Frecuencia {}'.format(nombre_archivo))
        plt.grid(True)

        # Guardar la figura en la ruta especificada
        plt.savefig(ruta_figura, format="pdf")
        plt.close()

        # Calcular los promedios de amplitud para cada banda de tercio de octava
        amplitudes_promedio = []
        for i in range(len(bandas_tercio_octava)):
            #lower_limit = frecuencias_limite[i] / (2 ** (1/6))
            #upper_limit = frecuencias_limite[i] * (2 ** (1/6))
            lower_limit = lower_limits[i]
            upper_limit = upper_limits[i]
            
            indices_banda = np.where((f >= lower_limit) & (f < upper_limit))[0]

            #amplitud_promedio = 10 * np.log10(np.mean((10 ** (magnitud_espectro_db[indices_banda]/10))) + eps)
            
            suma_energetica = 10 * np.log10(np.sum(10 ** (magnitud_espectro_db[indices_banda]/10)))

            amplitudes_promedio.append(suma_energetica)
            
        # Agregar los datos al DataFrame de amplitudes promedio
        df_amplitudes.loc[len(df_amplitudes)] = [nombre_archivo] + amplitudes_promedio
        
        # Reemplazar los valores vacíos por eps
        df_amplitudes.fillna(eps, inplace=True)

    # Agregar los datos de frecuencia al DataFrame de espectro
    df_espectro.insert(0, "Frecuencia", f)

    # Guardar el DataFrame de espectro en un archivo CSV
    df_espectro.to_csv(carpeta_data+"/Espectro FFT.csv", index=False)

    # Transponer el DataFrame para tener las frecuencias y valores de amplitud como columnas
    df_amplitudes_transpuesto = df_amplitudes.transpose()

    # Guardar el DataFrame transpuesto en un archivo CSV
    df_amplitudes_transpuesto.to_csv(carpeta_data+"/Espectro Tercios.csv", header=None)    

