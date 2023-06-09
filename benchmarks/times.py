import toml
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import math

def main() -> None:
  # Load config
  with open("config.toml", "r") as f:
    config = toml.load(f)

  initialPositions = config["benchmarks"]["initialPositions"]
  rounds = config["benchmarks"]["rounds"]
  whiteBallYRange = config["benchmarks"]["whiteBallYRange"]
  step = (whiteBallYRange[1] - whiteBallYRange[0]) / (initialPositions - 1)

  times = {}
  
  for i in range(initialPositions):
    # Update white ball `y` coordinate
    current_y = whiteBallYRange[0] + step * i
    config["simulation"]["whiteBallCoords"] = [config["simulation"]["whiteBallCoords"][0], current_y]

    print("Running simulation with white ball at [", config["simulation"]["whiteBallCoords"][0], ", ", current_y, "]")

    with open("config.toml", "w") as f:
      toml.dump(config, f)

    # Save the times of each round for the current `y`
    times[current_y] = {}

    for j in range(rounds):    
      # Create particles
      subprocess.run(["python", "generate_particles.py"])

      # Run simulation
      subprocess.run(["java", "-jar", "./target/billard-table-1.0-jar-with-dependencies.jar"])

      # Save event times
      with open(config["files"]["output"], 'r') as file:
        lines = file.readlines()
      
      times[current_y][j] = []
      
      for line in lines:
        data = line.split()

        if len(data) == 1:
          time = float(data[0])

          if time > 500:
            times[current_y][j] = None # outlier
            break

          times[current_y][j].append(time)

  # Plot mean time until completion
  plot_end_times(times, rounds)

  # Plot mean time between events
  plot_times_between_events(times, rounds)
  
  # Probability Density Function of events along time
  plot_event_density(times, rounds)


def plot_end_times(times: dict[float, dict[int, float]], rounds: int):
  # `y` coordinates of the white ball
  x_values = []
  # Average end times for each `y`
  y_values = []
  errors = []

  for y in times.keys():
    x_values.append(y)

    # End times of each round for the current `y`
    end_times = []

    for j in range(rounds):
      if times[y][j] != None: # discard outliers
        end_times.append(times[y][j][-1])

    avg_end_time = np.mean(end_times)
    std_end_time = np.std(end_times)

    y_values.append(avg_end_time)
    errors.append(std_end_time / math.sqrt(len(end_times))) # use the Standard Error of the Mean (SEM)

    # print()
    # print(f"Time to complete at {y=} = {avg_end_time} +- {std_end_time}")
    # print(f"End times: {[t for t in end_times]}")

  plt.bar(x_values, y_values, yerr=errors, capsize=5)

  plt.xlabel("Coordenada `y` bola blanca (cm)", fontsize=18)
  plt.ylabel("Tiempo de finalización (s)", fontsize=18)

  plt.grid()
  plt.tight_layout()
  
  plt.savefig("out/end_times.png")

  plt.close()


def plot_times_between_events(times: dict[float, dict[int, float]], rounds: int):
  # `y` coordinates of the white ball
  x_values = []
  # Average end times for each `y`
  y_values = []
  errors = []

  for y in times.keys():
    x_values.append(y)
    time_spans = []

    for j in range(rounds):
      if times[y][j] != None: # discard outliers
        # Get the time span between each pair of events
        aux = [times[y][j][i + 1] - times[y][j][i] for i in range(len(times[y][j]) - 1)]
        time_spans += aux
    
    avg_time_span = np.mean(time_spans)
    std_time_span = np.std(time_spans)

    y_values.append(avg_time_span)
    errors.append(std_time_span / math.sqrt(len(time_spans))) # use the Standard Error of the Mean (SEM)
  
    # Plot the PDF of the times between events
    bins = np.array([1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100])
    counts = []

    for i in range(1, len(bins)):
      # Get the number of events in the current round that are less than or equal to the current bin
      event_count = len([ts for ts in time_spans if ts <= bins[i] and ts > bins[i - 1]])
      counts.append(event_count)
    
    # Plot the Probability Density Function of the times between events
    density = counts / (sum(counts) * np.diff(bins))
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    plt.loglog(bin_centers, density, "-", label=f"y={y}", alpha=0.8)

  plt.xlabel('Tiempo entre eventos (s)', fontsize=18)
  plt.ylabel('Densidad de probabilidad de eventos', fontsize=18)
  plt.grid()
  plt.legend()
  plt.savefig(f"out/time_events_density.png")
  plt.close()

  # Plot mean time between events
  plt.bar(x_values, y_values, yerr=errors, capsize=5)

  plt.xlabel("Coordenada `y` bola blanca (cm)", fontsize=20)
  plt.ylabel("Tiempo entre eventos (s)", fontsize=20)

  plt.grid()
  plt.tight_layout()

  plt.savefig("out/mean_time_events.png")
  plt.close()

  # Plot frequency of events (use STD to get the error)
  plt.bar(x_values, [1/y for y in y_values], yerr=[1/(e * math.sqrt(len(time_spans))) for e in errors], capsize=5)

  plt.xlabel("Coordenada `y` bola blanca (cm)", fontsize=20)
  plt.ylabel("Frecuencia de eventos (1/s)", fontsize=20)

  plt.grid()
  plt.tight_layout()
  
  plt.savefig("out/mean_freqs_events.png")
  plt.close()
  

def plot_event_density(times: dict[float, dict[int, float]], rounds: int):
  bins = np.array([0, 2, 4, 6, 8, 10, 15, 20, 40, 60, 80])

  _, ax = plt.subplots(figsize=(16, 6))

  # Go through all the `y` values of the white ball, and draw a histogram for each one
  for y in times.keys():
    # data = []
    # errors = []
    counts = []

    # Get the number of times less than or equal to each bin
    for i in range(1, len(bins)):
      events_in_bin = []

      for j in range(rounds):
        if times[y][j] != None: # discard outliers
          # Get the number of events in the current round that are less than or equal to the current bin
          event_amt = len([t for t in times[y][j] if t <= bins[i] and t > bins[i - 1]])
          events_in_bin.append(event_amt)
      
      # Add random events to the data, to populate the bins according to the number of events in each bin
      event_count = int(round(np.mean(events_in_bin), 0))
      counts.append(event_count)
      # data += [bins[i] - 1] * event_count
      # errors.append(np.std(events_in_bin))

    # Plot a histogram
    # _, bins, _ = ax.hist(data, bins=bins, edgecolor='black')

    # Plot the histogram as a Probability Density Function
    density = counts / (sum(counts) * np.diff(bins))
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    ax.plot(bin_centers, density, "-", label=f"y={y}", alpha=0.8)

  xticks = [0, 5, 10, 15, 20, 60, 80]
  xticklabels = ['0', '5', '10', '', '20', '60', '80']
  ax.set_xticks(xticks, xticklabels)

  # Set the x-axis label
  ax.set_xlabel('Tiempo (s)', fontsize=20)

  # Set the y-axis label
  ax.set_ylabel('Densidad de probabilidad de eventos', fontsize=18)
  # ax.set_ylim(0, 200)

  # Enable grid and labels
  ax.grid()
  ax.legend()

  # Save the plot
  plt.savefig(f"out/event_density.png")

  plt.close()


if __name__ == "__main__":
  main()
