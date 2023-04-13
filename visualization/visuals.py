import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

with open("output.txt", 'r') as archivo:
    lineas = archivo.readlines()

diccionario = {}
tiempo_actual = None

for linea in lineas:
    elementos = linea.split()

    if len(elementos) == 1:
        tiempo_actual = float(elementos[0])
        diccionario[tiempo_actual] = []
    else:
        particula = {
            'x': float(elementos[0]),
            'y': float(elementos[1]),
            'velocidad_x': float(elementos[2]),
            'velocidad_y': float(elementos[3]),
            'radio': float(elementos[4])
        }
        diccionario[tiempo_actual].append(particula)

# Función que se ejecuta en cada frame de la animación
def update(frame):
    tiempo = list(diccionario.keys())[frame]
    particulas = diccionario[tiempo]
    x = [p['x'] for p in particulas]
    y = [p['y'] for p in particulas]
    radios = [np.pi*p['radio']*4 for p in particulas]

    ax.clear()
    ax.scatter(x, y, s=radios, edgecolors='k')
    ax.set_xlim([0, 224])
    ax.set_ylim([0, 112])
    ax.set_title(f'Tiempo: {tiempo}')

# Creación de la figura y los ejes
fig, ax = plt.subplots(figsize=(5, 2.5))

# Creación de la animación
anim = animation.FuncAnimation(fig, update, frames=len(diccionario))

# Guardado de la animación como archivo mp4
Writer = animation.writers['ffmpeg']
writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=1800)
anim.save('animacion.mp4', writer=writer)
