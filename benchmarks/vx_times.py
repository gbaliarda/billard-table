import toml
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import math

def main() -> None:
  # Load config
  with open("config.toml", "r") as f:
    config = toml.load(f)

  initialVelocities = config["benchmarks"]["initialVelocities"]
  rounds = config["benchmarks"]["rounds"]
  whiteBallVxRange = config["benchmarks"]["whiteBallVxRange"]
  step = (whiteBallVxRange[1] - whiteBallVxRange[0]) / (initialVelocities - 1)

  times = {}
  
  for i in range(initialVelocities):
    # Update white ball `vx` velocity
    current_vx = whiteBallVxRange[0] + step * i
    config["simulation"]["whiteBallVx"] = float(current_vx)

    print(f"Running simulation with white ball at vx = {current_vx}")

    with open("config.toml", "w") as f:
      toml.dump(config, f)

    # Save the times of each round for the current `vx`
    times[current_vx] = {}

    for j in range(rounds):    
      # Create particles
      subprocess.run(["python", "generate_particles.py"])

      # Run simulation
      subprocess.run(["java", "-jar", "./target/billard-table-1.0-jar-with-dependencies.jar"])

      # Save event times
      with open(config["files"]["output"], 'r') as file:
        lines = file.readlines()
      
      times[current_vx][j] = []
      
      for line in lines:
        data = line.split()

        if len(data) == 1:
          time = float(data[0])

          if time > 500:
            times[current_vx][j] = None # outlier
            break
          
          times[current_vx][j].append(time)

  # Plot mean time until completion
  plot_end_times(times, rounds)

  # Reset config
  config["simulation"]["whiteBallVx"] = float(200)

  with open("config.toml", "w") as f:
    toml.dump(config, f)


def plot_end_times(times: dict[float, dict[int, float]], rounds: int):
  # `vx` velocities of the white ball
  x_values = []
  # Average end times for each `vx`
  y_values = []
  errors = []

  for vx in times.keys():
    x_values.append(vx)

    # End times of each round for the current `vx`

    end_times = []

    for j in range(rounds):
      if times[vx][j] != None: # discard outliers
        end_times.append(times[vx][j][-1])

    avg_end_time = np.mean(end_times)
    std_end_time = np.std(end_times)

    print()
    print(f"Time to complete at {vx=} = {avg_end_time} +- {std_end_time}")
    print(f"End times: {[t for t in end_times]}")

    y_values.append(avg_end_time)
    errors.append(std_end_time / math.sqrt(len(end_times))) # use the Standard Error of the Mean (SEM)

  plt.bar(x_values, y_values, width=15, yerr=errors, capsize=5)

  plt.xlabel("Rapidez horizontal bola blanca (cm/s)", fontsize=18)
  plt.ylabel("Tiempo de finalización (s)", fontsize=18)

  plt.grid()
  plt.tight_layout()
  plt.savefig("out/end_times_vx.png")

  plt.close()


if __name__ == "__main__":
  main()
