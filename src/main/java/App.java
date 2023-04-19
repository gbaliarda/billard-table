import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.stream.Stream;

public class App {
    public static void main( String[] args ) {
        Path filePath = Paths.get(Config.getOutputFile());

        try {
            // Create any non-existent directories in th output path
            Files.createDirectories(filePath.getParent());
            // Delete old output file
            Files.deleteIfExists(filePath);
        } catch (IOException e) {
            e.printStackTrace();
        }

        try (Stream<String> stream = Files.lines(Paths.get(Config.getStaticFile()))) {
            List<Particle> particles = new ArrayList<>();

            // Load static inputs
            stream.forEach(line -> {
                String[] values = line.split(" ");
                double[] doubles = new double[values.length];
                String color = "black";
                for (int i = 0; i < values.length; i++) {
                    if (i == values.length - 1)
                        color = values[i];
                    else
                        doubles[i] = Double.parseDouble(values[i]);
                }
                double x = doubles[0];
                double y = doubles[1];
                double vx = doubles[2];
                double vy = doubles[3];
                double mass = doubles[4];
                double radius = doubles[5];
                Particle p = new Particle(x, y, vx, vy, mass, radius, color);
                particles.add(p);
            });

            updateOutputFile(particles, 0);

            CollisionSystem collisionSystem = new CollisionSystem(particles);

            // Run the simulation
            while (collisionSystem.hasNextEvent()) {
                collisionSystem.nextEvent();
                updateOutputFile(particles, collisionSystem.getTime());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void updateOutputFile(List<Particle> particles, double time) throws IOException {
        File file = new File(Config.getOutputFile());
        FileWriter fileWriter = new FileWriter(file, true);

        StringBuilder stringBuilder = new StringBuilder();

        stringBuilder.append(time).append("\n");

        particles.forEach(particle -> stringBuilder.append(String.format(Locale.US ,"%f %f %f %f %f %s\n", particle.getX(), particle.getY(), particle.getVx(), particle.getVy(), particle.getRadius(), particle.getColor())));

        fileWriter.write(stringBuilder.toString());
        fileWriter.close();
    }
}
