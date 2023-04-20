import numpy as np
import tomllib

# Configuration
with open("config.toml", "rb") as f:
  config = tomllib.load(f)
  STATIC_FILE = config["files"]["staticInput"]
  BALL_MASS = config["simulation"]["ballMass"]
  BALL_DIAMETER = config["simulation"]["ballDiameter"]
  WHITEBALL_VX = config["simulation"]["whiteBallVx"]
  WHITEBALL_COORDS = config["simulation"]["whiteBallCoords"]
  TABLE_WIDTH = config["simulation"]["tableWidth"]
  TABLE_HEIGHT = config["simulation"]["tableHeight"]

# X, Y, vx, vy, mass, radius
def generate_static_file():
    with open(STATIC_FILE, "w") as f:
        # White Ball
        f.write(f"{WHITEBALL_COORDS[0]} {WHITEBALL_COORDS[1]} {WHITEBALL_VX} 0 {BALL_MASS} {BALL_DIAMETER/2} white\n")

        # Fixed balls (table holes)
        f.write(f"0 0 0 0 0 {BALL_DIAMETER} gray\n")
        f.write(f"{TABLE_WIDTH / 2} 0 0 0 0 {BALL_DIAMETER} gray\n")
        f.write(f"{TABLE_WIDTH} 0 0 0 0 {BALL_DIAMETER} gray\n")
        f.write(f"0 {TABLE_HEIGHT} 0 0 0 {BALL_DIAMETER} gray\n")
        f.write(f"{TABLE_WIDTH / 2} {TABLE_HEIGHT} 0 0 0 {BALL_DIAMETER} gray\n")
        f.write(f"{TABLE_WIDTH} {TABLE_HEIGHT} 0 0 0 {BALL_DIAMETER} gray\n")
        
        # Triangle balls
        colors = ['yellow', 'blue', 'red', 'purple', 'orange', 'green',
                   'maroon', 'black', 'yellow', 'blue', 'red', 'purple', 'orange',
                   'green', 'maroon']
        color_index = 0

        positions_x = [TABLE_WIDTH - TABLE_HEIGHT / 2]
        # Columnas
        for i in range(5):
          # Siempre initial_y es el y de la bola de mas arriba del triangulo, este y inicial es fijo
          initial_y = TABLE_HEIGHT / 2 + i * BALL_DIAMETER / 2
          # Tomo el maximo X para despues calcular el nuevo X de la columna que sigue
          max_x = max(positions_x)
          # Para cada bola obtengo uno de los x que genere y genero la bola en determinada posicion en Y, seteando luego la proxima Y
          for _ in range(i + 1):
            x = positions_x.pop(0)
            f.write(f"{x} {initial_y} 0 0 {BALL_MASS} {BALL_DIAMETER / 2} {colors[color_index]}\n")
            color_index += 1
            eps = np.random.uniform(0.02, 0.03)
            initial_y = initial_y - BALL_DIAMETER  - eps

          # Genero los X para la proxima columna, a aprtir del maximo
          for _ in range(i + 2):
             eps = np.random.uniform(0.02, 0.03)
             positions_x.append(max_x + eps + BALL_DIAMETER)


        
        # # Columnas
        # for i in range(5):
        #   # Para la x tomo la posicion de la bola de mas a la izquierda, le sumo cutas i columnas de diametro con su error 
        #   # Notar que uso BALL_DIAMETER y no el radio porque la distancia centro a centro es 2 veces el radio
        #   initial_x = TABLE_WIDTH - TABLE_HEIGHT / 2 + i * (BALL_DIAMETER + eps)
        #   # Para la primera y tomo la de arriba en diagonal de la columna y voy bajando
        #   # Notar que uso el radio esta vez porque en el triangulo va subiendo, quizas agregar eps aca?
        #   initial_y = TABLE_HEIGHT / 2 + i * BALL_DIAMETER / 2
        #   for _ in range(i + 1):
        #     f.write(f"{initial_x} {initial_y} 0 0 {BALL_MASS} {BALL_DIAMETER / 2} {colors[color_index]}\n")
        #     color_index += 1
        #     initial_y = initial_y - BALL_DIAMETER  - eps
            
             
            

if __name__ == "__main__":
    generate_static_file()
