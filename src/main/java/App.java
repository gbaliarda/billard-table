import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.stream.Stream;

public class App {
    public static void main( String[] args ) {
        try (Stream<String> stream = Files.lines(Paths.get(Config.getStaticFile()))) {
            List<Particle> particles = new ArrayList<>();
            stream.forEach(line -> {
                String[] values = line.split(" ");
                double[] doubles = new double[values.length];
                for (int i = 0; i < values.length; i++) {
                    doubles[i] = Double.parseDouble(values[i]);
                }
                double x = doubles[0];
                double y = doubles[1];
                double vx = doubles[2];
                double vy = doubles[3];
                double mass = doubles[4];
                double radius = doubles[5];
                Particle p = new Particle(x, y, vx, vy, mass, radius, mass == 0);
                particles.add(p);
            });
            updateOutputFile("output.txt", particles, 0);
            CollisionSystem collisionSystem = new CollisionSystem(particles);
            while (collisionSystem.hasNextEvent()) {
                collisionSystem.nextEvent();
                updateOutputFile("output.txt", particles, collisionSystem.getTime());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void updateOutputFile(String fileName, List<Particle> particles, double time) throws IOException, IOException {
        File file = new File(fileName);
        FileWriter fileWriter = new FileWriter(file, true);

        StringBuilder stringBuilder = new StringBuilder();

        stringBuilder.append(time).append("\n");

        particles.forEach(particle -> stringBuilder.append(String.format(Locale.US ,"%f %f %f %f %f\n", particle.getX(), particle.getY(), particle.getVx(), particle.getVy(), particle.getRadius())));

        fileWriter.write(stringBuilder.toString());
        fileWriter.close();
    }
}
