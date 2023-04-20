import java.util.Iterator;
import java.util.List;
import java.util.Objects;
import java.util.PriorityQueue;

public class CollisionSystem {
    private final PriorityQueue<Event> pq;
    private final List<Particle> particles;
    private final int TABLE_HOLES = 6;
    private double t; // in seconds

    public CollisionSystem(List<Particle> particles) {
        this.particles = particles;
        this.pq = new PriorityQueue<>();
    }

    public void nextEvent() {
        // Add all future events (collisions) to the priority queue
        for(Particle p : particles) {
            if (p.isFixed()) continue;
            pq.add(nextParticleEvent(p));
        }

        // Get the next event (least time until occurence)
        Event event = pq.poll();

        while (event.wasSuperveningEvent())
            event = pq.poll();

        for (Particle p : particles) {
            if (p.isFixed()) continue;

            // Update position
            p.setX(p.getX() + p.getVx() * event.getTime());
            p.setY(p.getY() + p.getVy() * event.getTime());
        }

        Particle p1 = event.getParticle1();
        Particle p2 = event.getParticle2();

        // Update velocity or remove particle
        if (p1 == null)
            p2.bounceY();
        else if (p2 == null)
            p1.bounceX();
        else if (p1.isFixed()) {
            particles.remove(p2);
            p2.incCollisionCount();
        }
        else if (p2.isFixed()) {
            particles.remove(p1);
            p1.incCollisionCount();
        }
        else
            p1.bounce(p2);
        
        // Update simulation time
        t += event.getTime();

        logEvent(event);
    }

    private Event nextParticleEvent(Particle p) {
        Event minEvent = null;
        double tc;

        // Compute all tc's of collisions with another particle
        for(Particle particle: particles) {
            if (p.equals(particle)) continue;

            tc = p.collides(particle);
            if (minEvent == null || minEvent.getTime() > tc)
                minEvent = new Event(tc, p, particle);
        }

        // Compute tc of collision with vertical wall
        tc = p.collidesX();
        // minEvent can't be null here because particles contains at least TABLE_HOLES fixed particles
        if (minEvent.getTime() > tc)
            minEvent = new Event(tc, p, null);

        // Compute tc of collision with horizontal wall
        tc = p.collidesY();
        if (minEvent.getTime() > tc)
            minEvent = new Event(tc, null, p);

        return minEvent;
    }

    private void logEvent(Event event) {
        if (!Config.isVerbose())
            return;

        Particle p1 = event.getParticle1();
        Particle p2 = event.getParticle2();

        System.out.printf("Time: %.2f\n", t);

        System.out.printf("Particles left: %d ; ", particles.size() - TABLE_HOLES);

        System.out.print("[ ");
        for (Particle p : particles)
            if (!p.isFixed())
                System.out.printf("%s ",  p.getColor());
        System.out.print("]\n");

        System.out.printf("%s bounces with %s at ~(%.2f, %.2f)\n",
                p1 == null ? "HWall" : (p1.isFixed() ? "HOLE" : p1.getColor().toUpperCase()),
                p2 == null ? "VWall" : (p2.isFixed() ? "HOLE" : p2.getColor().toUpperCase()),
                p1 == null ? p2.getX() : p1.getX(),
                p1 == null ? p2.getY() : p1.getY()
        );

//        if (p1 != null && p2 != null)
//            System.out.printf("Distance between centers: %.2f\n", Math.sqrt(
//                    Math.pow(p1.getX() - p2.getX(), 2) + Math.pow(p1.getY() - p2.getY(), 2)
//            ));

        System.out.println();
    }

    public boolean hasNextEvent() {
        return this.particles.size() > TABLE_HOLES;
    }

    public double getTime() { return t;}
}
