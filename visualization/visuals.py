import numpy as np
import matplotlib.pyplot as plt

# Leer el archivo de texto y extraer los datos
data = np.loadtxt('output.txt', skiprows=1, usecols=(0, 1, 2, 3, 4))

# Extraer el tiempo de la primera línea
# tiempo = data[0]

# Extraer los datos de las partículas
particulas = data[0:]

# Extraer las posiciones de las partículas
posiciones = particulas[:, :2]

# Extraer los radios de las partículas
radios = particulas[:, -1]
print(radios)

# Crear un gráfico de dispersión con las posiciones de las partículas
fig, ax = plt.subplots()
ax.scatter(posiciones[:, 0], posiciones[:, 1], s=np.pi * (2*radios)**2, alpha=0.5)

# Configurar los ejes del gráfico
ax.set_xlim([0, 224])
ax.set_ylim([0, 112])
ax.set_aspect('equal')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Particulas en el tiempo t')

# Mostrar el gráfico
plt.show()
