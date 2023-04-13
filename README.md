# Requirements

- python >= 3.10
  - numpy
  - matplotlib
- java >= 11

# Input Generation

In order to generate random input particles run the following command:

```shell
python generate_particles.py
```

The structure of each line of `static.txt` is:

```
x y vx vy mass radius
```

Where:

- 1st line refers to the white ball.
- 2nd to 7th lines refer to the table holes (fixed particles).
- 8th to 22nd lines refer to the balls in the triangle.

# Configuration

Project configuration can be changed modifying the `config.toml` file:

```toml
[simulation]
tableWidth = 224                # cm
tableHeight = 112               # cm
whiteBallCoords = [56.0, 56.0]  # cm
whiteBallVx = 200.0             # cm/s
ballMass = 165                  # g
ballDiameter = 5.7              # cm

[files]
staticInput = "./static.txt"
```

Note that `whiteBallCoords`, `whiteBallVx` and `ballDiameter` **must** have decimal point.

# Run Simulation

To generate the `.jar` file run the following command:

```shell  
mvn clean package
```

In order to run the simulation run:

```shell
java -jar ./target/billboard-table-1.0-jar-with-dependencies.jar
```

This will generate a file called `output.txt`, whose structure is:

```
time_event_0
particle_1_x, particle_1_y, particle_1_vx, particle_1_vy, particle_1_radius
particle_2_x, particle_2_y, particle_2_vx, particle_2_vy, particle_2_radius
...
particle_N_x, particle_N_y, particle_N_vx, particle_N_vy, particle_N_radius
time_event_1
...
```

# Run Animation

To run the animations based on the simulation output, execute from the root folder:

```shell
python visualization/visuals.py
```

# Authors

- Baliarda Gonzalo - 61490
- Pérez Ezequiel - 61475
