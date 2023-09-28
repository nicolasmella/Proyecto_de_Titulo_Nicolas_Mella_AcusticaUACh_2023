import tkinter as tk
from tkinter import ttk
import sys
import serial
import sounddevice as sd
import soundfile as sf
import time
import threading
from tkinter import filedialog
import os
from tkinter import font
from tkinter import messagebox
import emoji
import subprocess



import FFT as myfft

import Polar as polar

import Unir_PDF as unirpdf







#Establecer la conexión serial con el dispositivo Arduino
#En sistema operativo windows se debe verificar el puerto COM correspondiente al dispositivo
ser = serial.Serial('/dev/tty.usbserial-0001', 9600) 


# Llamar al comando 'caffeinate' para mantener el sistema despierto
caffeinate_process = subprocess.Popen(['caffeinate'])




#Predefine variables
fs = None
N = None
presicion = None
measurement_running = True 
eps = 1e-8 #Valor pequeño para evitar indeterminación de la función logaritmo








#Crea pantalla de visualización de la consola
class ConsoleDisplay:
    def __init__(self, master):
        self.text_area = tk.Text(master, height=5, width=40)
        self.text_area.pack(padx=10, pady=10)

    def write(self, message):
        self.text_area.insert(tk.END, message)
        self.text_area.see(tk.END)
        
    def clear(self):
        self.text_area.delete('1.0', tk.END)

    def flush(self):
        pass



def clear_console():
    console_display.clear()


#Funcion para reproducir ruido rosa para calibrar nivel
def reproducir_ruido():
    archivo_audio = "PINK NOISE.wav"
    audio_data, sample_rate = sf.read(archivo_audio)
    sd.play(audio_data, sample_rate, blocking=True, latency='low')
    sd.wait()

#Funcion para abrir manual de usuario
def abrir_manual_de_usuario():
    manual_de_usuario_pdf = 'ruta_al_manual_de_usuario'
    subprocess.run(['open', manual_de_usuario_pdf])











#Funciones para control del motor

#SENTIDO DE GIRO
def sentido_giro(sentido):
    if sentido == "horario":
        ser.write(b'horario\n') #Enviar la señal "horario" al arduino
    if sentido == "antihorario":
        ser.write(b'antihorario\n') #Enviar la señal "antihorario" al arduino

#MOVER 5 GRADOS
def mov_5_deg():
    ser.write(b'5deg\n') #Enviar la señal 5deg al arduino

#MOVER 10 GRADOS
def mov_10_deg():
    ser.write(b'10deg\n') #Enviar la señal 10deg al arduino

#MOVER 20 GRADOS
def mov_20_deg():
    ser.write(b'20deg\n') #Enviar la señal 20deg al arduino

#MOVER 30 GRADOS
def mov_30_deg():
    ser.write(b'30deg\n') #Enviar la señal 30deg al arduino

#MOVER 45 GRADOS
def mov_45_deg():
    ser.write(b'45deg\n') #Enviar la señal 45deg al arduino
    
#MOVER 90 GRADOS
def mov_90_deg():
    ser.write(b'90deg\n') #Enviar la señal 45deg al arduino
    
#MOVER 180 GRADOS
def mov_180_deg():
    ser.write(b'180deg\n') #Enviar la señal 45deg al arduino
    
#MOVER 360 GRADOS
def mov_360_deg():
    ser.write(b'360deg\n') #Enviar la señal 45deg al arduino

#VOLVER A LA POSICION INICIAL
def mov_reversa():
    ser.write(b'origen\n') #Enviar la señal origen al arduino














# Función para abrir un cuadro de diálogo y seleccionar una ruta de directorio
def select_directory():
    carpeta_principal = filedialog.askdirectory()
    if carpeta_principal:
        save_entry.delete(0, tk.END)
        save_entry.insert(0, carpeta_principal)
    
    # Crear una carpeta llamada "Data" para guardar los datos de espectros en .csv
    carpeta_data = os.path.join(carpeta_principal, 'Data')
    if not os.path.exists(carpeta_data):
        os.makedirs(carpeta_data)
    
    # Crear una carpeta llamada "Fig Espectros" para guardar los graficos de espectro
    carpeta_fig_espectros = os.path.join(carpeta_principal, 'Fig Espectros')
    if not os.path.exists(carpeta_fig_espectros):
        os.makedirs(carpeta_fig_espectros)
        
    # Crear una carpeta llamada "Fig Polares" para guardar las figuras de patrones polares
    carpeta_fig_polares = os.path.join(carpeta_principal, 'Fig Polares')
    if not os.path.exists(carpeta_fig_polares):
        os.makedirs(carpeta_fig_polares)









#FUNCIONES PARA MEDICION

def start_measurement():
    measurement_thread = threading.Thread(target=start_measurement_thread)
    measurement_thread.setDaemon(True)
    measurement_thread.start()
    




#Hilo de MEDICION
def start_measurement_thread():
    global measurement_running
    measurement_running = True
    
    clear_console()
    
    time.sleep(1)
    
    print("Parámetros Seleccionados:")
    selected_fs = int(combo_fs.get().split()[0])
    print("Frecuencia de muestreo:", selected_fs, "Hz")
    selected_N = int(combo_N.get())
    print("Tamaño FFT:", selected_N)
    selected_grados = int(combo_grados.get().split()[0].replace("°", ""))
    print("Precisión:", selected_grados, "grados")
    
    if selected_grados == 5:
        print(emoji.emojize("Tiempo aprox. de medición: 12 minutos :timer_clock:"))
    
    # Asignar los valores seleccionados a las variables correspondientes
    fs = selected_fs
    N = selected_N
    presicion = selected_grados
    total_grabaciones = 360 // presicion
    
    # Abrir el archivo de audio de ruido rosa
    archivo = 'PINK NOISE.wav'
    audio_data, _ = sf.read(archivo, dtype='float32')

    time.sleep (3)

    print(emoji.emojize("\n Iniciando medición... :play_button:"))
    
    time.sleep (3)
    
    #MEDIR
    

    # BUCLE DE MEDICIÓN
    for i in range(total_grabaciones):
        
        if not measurement_running: #Comprueba si el codigo se está ejecutando
            print(emoji.emojize("\n Medicion detenida :red_square:"))
            break
    
        # Obtener el dispositivo de audio seleccionado
        selected_device = device_combobox.get()

        # Configurar el dispositivo de audio seleccionado
        sd.default.device = selected_device
        
        # Obtener la ruta ingresada por el usuario para guardar los archivos
        carpeta_principal = save_entry.get()
        
        # Crear la carpeta "Recording" en la ruta seleccionada (si no existe)
        carpeta_audio = os.path.join(carpeta_principal, "Recording")
        os.makedirs(carpeta_audio, exist_ok=True)
        
        # Crear la carpeta "Data" en la ruta seleccionada (si no existe)
        carpeta_data = os.path.join(carpeta_principal, "Data")
        os.makedirs(carpeta_data, exist_ok=True)
        
        # Crear la carpeta "Fig Espectros" en la ruta seleccionada (si no existe)
        carpeta_fig_espectros = os.path.join(carpeta_principal, "Fig Espectros")
        os.makedirs(carpeta_fig_espectros, exist_ok=True)
        
        # Crear la carpeta "Fig Polares" en la ruta seleccionada (si no existe)
        carpeta_fig_polares = os.path.join(carpeta_principal, "Fig Polares")
        os.makedirs(carpeta_fig_polares, exist_ok=True)
        
        # Verificar si se ha ingresado una ruta válida
        if carpeta_principal:
            # Iniciar la grabación y reproducción simultáneas
            print(emoji.emojize(f"\n Midiendo {i*presicion}°... :speaker_high_volume: :microphone:"))
            recording = sd.playrec(audio_data, fs, channels=1, blocking=True, latency='low')
            # Esperar hasta que la reproducción y grabación hayan finalizado
            sd.wait()
            # Guardar la grabación como un nuevo archivo de audio
            filename_out = os.path.join(carpeta_audio,f"{i*presicion}°.wav")
            sf.write(filename_out, recording, fs)
            
            print(emoji.emojize(f"\n Medición {i*presicion}°... :OK_button: :check_mark_button:"))

            clear_console()
            
            time.sleep (1)
            
            if not measurement_running: #Comprueba si el codigo se está ejecutando
                print(emoji.emojize("\n Medicion detenida :red_square:"))
                break
                
            if presicion == 5:
                ser.write(b'horario\n') #Enviar la señal "horario" al arduino
                mov_5_deg() #mover
                time.sleep(2)
                
            if presicion == 10:
                ser.write(b'horario\n') #Enviar la señal "horario" al arduino
                mov_10_deg() #mover
                time.sleep(3)
                
            if presicion == 20:
                ser.write(b'horario\n') #Enviar la señal "horario" al arduino
                mov_20_deg() #mover
                time.sleep(3)
            
            if presicion == 30:
                ser.write(b'horario\n') #Enviar la señal "horario" al arduino
                mov_30_deg() #mover
                time.sleep(3)
                
            if presicion == 45:
                ser.write(b'horario\n') #Enviar la señal "horario" al arduino
                mov_45_deg() #mover
                time.sleep(4)
    
    
    if measurement_running: #Comprueba si el codigo se está ejecutando
        mov_reversa()        

        #LLAMA FUNCION FFT 
        time.sleep(1)
        print(emoji.emojize("\n Calculando FFT ... :laptop:"))
        time.sleep (2) 
        myfft.iterar_archivos(carpeta_audio,fs,N,carpeta_fig_espectros,carpeta_data)
        time.sleep(1)
        unirpdf.unirpdf(carpeta_fig_espectros,"Espectro FFT")
        print(emoji.emojize("\n FFT :laptop: :OK_button: :check_mark_button:"))
        
        time.sleep(2)
        
        clear_console()
        
        #LLAMA A LA FUNCION POLAR
        time.sleep(1)
        print(emoji.emojize("\n Graficando polares ... :pencil:"))
        time.sleep(2)
        polar.polar(carpeta_data+"/Espectro Tercios.csv",carpeta_fig_polares)
        time.sleep(1)
        unirpdf.unirpdf(carpeta_fig_polares,"Patrones Polares")
        print(emoji.emojize("\n Gráficos Polares :OK_button: :check_mark_button:"))
        
        clear_console()
        
        time.sleep(2)
        
        #MEDICION FINALIZADA CON EXITO
        print(emoji.emojize("\n Medición finalizada con éxito :check_mark_button: :smiling_face_with_sunglasses:"))        
    
    
#FUNCION PARA DETENER EL HILO DE MEDICIÓN
def stop_measurement():
    global measurement_running
    measurement_running = False
    


















# Función para salir de la aplicación
def exit_application():
    if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
        window.destroy()  # Cerrar la ventana y finalizar la aplicación
        # Al finalizar, terminar el proceso 'caffeinate' para permitir que el sistema vuelva a dormir
        caffeinate_process.terminate()
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# Crear la ventana principal
window = tk.Tk()
window.title("Polar 2023")

# Establecer el icono
window.iconphoto(True, tk.PhotoImage(file='ICONO2.png'))






# Crear una nueva fuente con el tamaño especificado
fuente = tk.font.Font(family="Roboto Black", size=20)

# Aplicar la nueva fuente a todos los elementos de la ventana
window.option_add("*Font", fuente)



# Crear la sección "Control manual"
control_manual = tk.LabelFrame(window, text="Control manual", padx=10, pady=10)
control_manual.pack(padx=10, pady=10)



# Crea las variables para los botones de opción de selección de sentido de giro
sentido = tk.StringVar()
sentido.set("horario")  # Selecciona "horario" por defecto

#Crea botones para seleccionar sentido de giro
imagen_horario = tk.PhotoImage(file="horario.png")
imagen_antihorario = tk.PhotoImage(file="antihorario.png")

boton_horario = tk.Radiobutton(control_manual, image=imagen_horario, variable=sentido, value="horario", command=lambda: sentido_giro(sentido.get()))
boton_antihorario = tk.Radiobutton(control_manual, image=imagen_antihorario, variable=sentido, value="antihorario", command=lambda: sentido_giro(sentido.get()))
boton_horario.grid(row=0, column=1, padx=5, pady=5)
boton_antihorario.grid(row=0, column=4, padx=5, pady=5)

boton_5deg = tk.Button(control_manual, text="5°", command=mov_5_deg, width=5, height=2)
boton_5deg.grid(row=1, column=0, padx=5, pady=5)

boton_10deg = tk.Button(control_manual, text="10°", command=mov_10_deg, width=5, height=2)
boton_10deg.grid(row=1, column=1, padx=5, pady=5)

boton_45deg = tk.Button(control_manual, text="45°", command=mov_45_deg, width=5, height=2)
boton_45deg.grid(row=1, column=2, padx=5, pady=5)

boton_90deg = tk.Button(control_manual, text="90°", command=mov_90_deg, width=5, height=2)
boton_90deg.grid(row=1, column=3, padx=5, pady=5)

boton_180deg = tk.Button(control_manual, text="180°", command=mov_180_deg, width=5, height=2)
boton_180deg.grid(row=1, column=4, padx=5, pady=5)

boton_360deg = tk.Button(control_manual, text="360°", command=mov_360_deg, width=5, height=2)
boton_360deg.grid(row=1, column=5, padx=5, pady=5)


# Crear la sección Medicion de directividad
seccion_medir = tk.LabelFrame(window, text="Medición de Directividad", padx=10, pady=10)
seccion_medir.pack(padx=10, pady=10)

# Etiqueta y combobox para seleccionar el dispositivo de audio
device_label = tk.Label(seccion_medir, text="Dispositivo de Audio:")
device_label.pack()
devices = sd.query_devices()
device_combobox = ttk.Combobox(seccion_medir, values=[device["name"] for device in devices])
device_combobox.pack()

# Etiqueta y campo de entrada para la ruta de guardado
save_label = tk.Label(seccion_medir, text="Ruta de Guardado:")
save_label.pack()
save_entry = tk.Entry(seccion_medir, width=40)
save_entry.pack()

# Botón para seleccionar la ruta de directorio
select_button = tk.Button(seccion_medir, text="Seleccionar Ruta", command=select_directory)
select_button.pack()





# Título y selección para la frecuencia de muestreo (fs)
label_fs = tk.Label(seccion_medir, text="Frecuencia de muestreo (fs)")
label_fs.pack(side=tk.LEFT, padx=5)

options_fs = ["44100 Hz", "48000 Hz", "96000 Hz"]
combo_fs = ttk.Combobox(seccion_medir, values=options_fs, width=8, justify="center")
combo_fs.current(0)
combo_fs.pack(side=tk.LEFT, padx=5)

# Título y selección para el tamaño de FFT (N)
label_N = tk.Label(seccion_medir, text="Tamaño FFT (N)")
label_N.pack(side=tk.LEFT, padx=5)

options_N = ["512", "1024", "2048", "4096", "8192", "16384"]
combo_N = ttk.Combobox(seccion_medir, values=options_N, width=5, justify="center")
combo_N.current(0)
combo_N.pack(side=tk.LEFT, padx=5)

# Título y selección para la precisión
label_grados = tk.Label(seccion_medir, text="Precisión")
label_grados.pack(side=tk.LEFT, padx=5)

options_grados = ["5°", "10°", "20°", "30°", "45°"]
combo_grados = ttk.Combobox(seccion_medir, values=options_grados, width=4, justify="center")
combo_grados.current(0)
combo_grados.pack(side=tk.LEFT, padx=5)


#IMAGENES PLAY Y STOP

imagen_play = tk.PhotoImage(file="PLAY.png")
imagen_stop = tk.PhotoImage(file="STOP.png")
imagen_reset = tk.PhotoImage(file="RESET.png")
imagen_ruido = tk.PhotoImage(file="RUIDO.png")


# Boton iniciar medición
start_button = tk.Button(seccion_medir, image=imagen_play, command=start_measurement)
start_button.pack(side=tk.LEFT, padx=5)

#BOTÓN STOP
stop_button = tk.Button(seccion_medir, image=imagen_stop, command=stop_measurement)
stop_button.pack(side=tk.LEFT, padx=5)

#BOTÓN reset
reset_button = tk.Button(seccion_medir, image=imagen_reset, command=clear_console)
reset_button.pack(side=tk.LEFT, padx=5)

#BOTÓN reset
ruido_button = tk.Button(seccion_medir, image=imagen_ruido, command=reproducir_ruido)
ruido_button.pack(side=tk.LEFT, padx=5)



seccion_consola = tk.LabelFrame(window, padx=10, pady=10)
seccion_consola.pack(padx=10, pady=10)

# Crear el objeto de visualización de la consola
console_display = ConsoleDisplay(seccion_consola)
# Redirigir sys.stdout al objeto de visualización
sys.stdout = console_display







# Crear la sección "SALIR"
seccion_salir = tk.LabelFrame(window, padx=5, pady=5)
seccion_salir.pack(padx=10, pady=10)

#Boton de AYUDA
boton_instrucciones = tk.Button(seccion_salir, text="Ayuda", command=abrir_manual_de_usuario)
boton_instrucciones.pack(pady=10)

# Botón de "Salir"
exit_button = tk.Button(seccion_salir, text="Salir", command=exit_application)
exit_button.pack()










# Maximizar la ventana
window.state('zoomed')

# Iniciar el bucle principal de la ventana
window.mainloop()

