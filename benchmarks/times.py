import toml
import subprocess
import numpy as np
import matplotlib.pyplot as plt

def main() -> None:
  # Load config
  with open("config.toml", "r") as f:
    config = toml.load(f)

  initialPositions = config["benchmarks"]["initialPositions"]
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

    for j in range(config["benchmarks"]["rounds"]):    
      # Create particles
      subprocess.run(["python", "generate_particles.py"])

      # Run simulation
      subprocess.run(["java", "-jar", "./target/billboard-table-1.0-jar-with-dependencies.jar"])

      # Save event times
      with open(config["files"]["output"], 'r') as file:
        lines = file.readlines()
      
      times[current_y][j] = []
      
      for line in lines:
        data = line.split()

        if len(data) == 1:
          time = float(data[0])
          times[current_y][j].append(time)

  # Plot mean time between events
  plot_end_times(times, step, config)

  # TODO: plot mean time until completion
  
  # Plot histogram (number of events in each time bin)
  plot_histogram(times, config["benchmarks"]["rounds"])


def plot_end_times(times: dict[float, dict[int, float]], step: float, config: dict):
  # `y` coordinates of the white ball
  x_values = [y for y in times.keys()]
  # Average end times for each `y`
  y_values = []
  errors = []

  for i in range(config["benchmarks"]["initialPositions"]):
    y = config["benchmarks"]["whiteBallYRange"][0] + step * i

    # End times of each round for the current `y`
    end_times = [times[y][j][-1] for j in range(config["benchmarks"]["rounds"])]

    avg_end_time = np.mean(end_times)
    std_end_time = np.std(end_times)

    y_values.append(avg_end_time)
    errors.append(std_end_time)

    # print()
    # print(f"Time to complete at {y=} = {avg_end_time} +- {std_end_time}")
    # print(f"End times: {[t for t in end_times]}")

  plt.bar(x_values, y_values, yerr=errors, capsize=5)

  plt.xlabel("Coordenada `y` bola blanca (cm)", fontsize=18)
  plt.ylabel("Tiempo de finalización (s)", fontsize=18)

  plt.savefig("out/end_times.png")

  plt.close()


def plot_histogram(times: dict[float, dict[int, float]], rounds: int):
  bins = [0, 5, 10, 15, 20, 40, 60, 80, 100, 300]

  # Go through all the `y` values of the white ball, and draw a histogram for each one
  for y in times.keys():
    data = []
    errors = []

    # Get the number of times less than or equal to each bin
    for i in range(1, len(bins)):
      events_in_bin = []

      for j in range(rounds):
        # Get the number of events in the current round that are less than or equal to the current bin
        event_amt = len([t for t in times[y][j] if t <= bins[i] and t > bins[i - 1]])
        events_in_bin.append(event_amt)
      
      # Add random events to the data, to populate the bins according to the number of events in each bin
      data += [bins[i] - 1] * int(round(np.mean(events_in_bin), 0))
      errors.append(np.std(events_in_bin))

    # Create a histogram
    _, ax = plt.subplots(figsize=(16, 6))
    n, bins, _ = ax.hist(data, bins=bins, edgecolor='black')

    # Add error bars (std) to the histogram
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    bin_widths = bins[1:] - bins[:-1]
    ax.errorbar(bin_centers, n, yerr=errors, xerr=bin_widths/2, fmt='none', ecolor='black', capsize=5)

    xticks = [0, 5, 10, 15, 20, 60, 100, 300]
    xticklabels = ['0', '', '10', '', '20', '60', '100', '300']
    ax.set_xticks(xticks, xticklabels)

    # Set the x-axis label
    ax.set_xlabel('Tiempo (s)', fontsize=20)

    # Set the y-axis label
    ax.set_ylabel('Eventos', fontsize=20)
    ax.set_ylim(0, 200)

    # Show the plot
    plt.savefig(f"out/hist_{y}.png")

    plt.close()


if __name__ == "__main__":
  main()
