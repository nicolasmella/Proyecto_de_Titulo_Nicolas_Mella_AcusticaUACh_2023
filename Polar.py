import csv
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')

# Leer los datos de la planilla
def polar(archivo_csv,carpeta_fig_polares):
    bandas_tercio_octava = []
    amplitudes_por_banda = []

    with open(archivo_csv, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la primera fila (encabezados)
        
        for row in reader:
            # Leer la banda de tercio de octava
            banda_tercio_octava = float(row[0])
            bandas_tercio_octava.append(banda_tercio_octava)
            
            # Leer las amplitudes para cada posición angular en esa banda
            amplitudes_angular = [float(val) for val in row[1:]]
            amplitudes_por_banda.append(amplitudes_angular)

    # Convertir a matrices numpy
    bandas_tercio_octava = np.array(bandas_tercio_octava)
    amplitudes_por_banda = np.array(amplitudes_por_banda)
    
    # Normalizar las amplitudes por banda de frecuencia
    for i in range(len(amplitudes_por_banda)):
        amplitudes = amplitudes_por_banda[i]
            
        # Calcular el máximo de amplitud en esa banda
        max_amplitud = np.max(amplitudes)
            
        # Normalizar las amplitudes por el máximo
        amplitudes_por_banda[i] = amplitudes - max_amplitud

    # Calcular la cantidad de grupos de 4 bandas
    num_grupos = len(bandas_tercio_octava) // 3

    
    # Crear los gráficos por grupos de 3 bandas
    for i in range(num_grupos):
        inicio = (i * 3)
        fin = ((i + 1) * 3)
        
        # Obtener las bandas y amplitudes del grupo actual
        bandas_grupo = bandas_tercio_octava[inicio:fin]
        amplitudes_grupo = amplitudes_por_banda[inicio:fin]

        # Ajustar los límites de amplitud y las marcas de graduación
        limite_superior = 6
        limite_inferior = -42

        # Crear la gráfica polar para el grupo actual
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='polar')

        # Configurar los ángulos para cada posición angular
        angulos_rad = np.linspace(0, 2*np.pi, len(amplitudes_grupo[0]), endpoint=False)

        # Agregar el primer valor de ángulo al final del arreglo de ángulos
        angulos_rad = np.append(angulos_rad, angulos_rad[0])
        
        # Configurar el desplazamiento angular para que el ángulo 0 esté en la parte superior
        ax.set_theta_offset(np.pi/2)
        
        # Invertir la graduación de los ángulos para que crezca en sentido horario
        ax.set_theta_direction(-1)

        # Graficar las amplitudes para cada banda del grupo
        for j in range(len(bandas_grupo)):
            amplitudes = amplitudes_grupo[j]

            # Agregar el primer valor de amplitud al final del arreglo de amplitudes
            amplitudes = np.append(amplitudes, amplitudes[0])
            
            amplitudes = np.asarray([a if a > limite_inferior else limite_inferior for a in amplitudes])
            
            ax.plot(angulos_rad, amplitudes, linewidth=1.2, linestyle='-')
        
        # Configurar los ángulos en grados y agregar marcas de graduación cada 30 grados
        ax.set_xticks(np.deg2rad(np.arange(0, 360, 30)))
        ax.set_xticklabels([f"{int(theta_deg)}°" for theta_deg in np.arange(0, 360, 30)])
        
        # Calcular los valores de las marcas de graduación en dB
        marcas_graduacion = np.array([0, -6,-12,-18, -24, -30,-36])

        # Configurar los límites y las marcas de graduación en el eje radial
        ax.set_rlim(limite_inferior, limite_superior)
        ax.set_yticks(marcas_graduacion)
        ax.set_yticklabels([f"{int(val)} dB" for val in marcas_graduacion])

        # Ajustar el tamaño de letra de los ángulos
        ax.tick_params(axis='x', labelsize=8)

    # Ajustar el tamaño de letra de las marcas de graduación
        ax.tick_params(axis='y', labelsize=6)

        # Configurar los márgenes del gráfico para dejar espacio para la leyenda
        fig.subplots_adjust(bottom=0.2)
    
        # Configurar el título y leyenda
        ax.set_title("Patrón Polar de Radiación (1/3 Octava)")
        frecuencias_legenda = [f"{int(banda_tercio_octava)} Hz" for banda_tercio_octava in bandas_grupo]
        
        ax.legend(frecuencias_legenda, loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=len(bandas_tercio_octava))

        # Guardar la gráfica
        plt.savefig(carpeta_fig_polares+"/Fig_" + str(i+1) + ".pdf", format="pdf")
        plt.close()



