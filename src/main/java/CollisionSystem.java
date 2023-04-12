import java.util.Iterator;
import java.util.List;
import java.util.PriorityQueue;

public class CollisionSystem {
    private PriorityQueue<Event> pq;
    private List<Particle> particles;
    private int TABLE_HOLES = 6;
    private double t; // in seconds

    public CollisionSystem(List<Particle> particles) {
        this.particles = particles;
        this.pq = new PriorityQueue<Event>();
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

        // Update particles
        boolean didBounce = false;

        Iterator<Particle> it = particles.iterator();

        while (it.hasNext()) {
            Particle p = it.next();

            if (p.isFixed()) continue;
            
            // Update position
            p.setX(p.getX() + p.getVx() * event.getTime());
            p.setY(p.getY() + p.getVy() * event.getTime());
            
            // Update velocity or remove particle
            if (p.equals(event.getParticle1())) {
                if (event.getParticle2() == null)
                    p.bounceX();
                else if (event.getParticle2().isFixed())
                    it.remove();
                else if (!didBounce) {
                    p.bounce(event.getParticle2());
                    didBounce = true;
                }
            } else if (p.equals(event.getParticle2())) {
                if (event.getParticle1() == null)
                    p.bounceY();
                else if (event.getParticle1().isFixed())
                    it.remove();
                else if (!didBounce) {
                    p.bounce(event.getParticle1());
                    didBounce = true;
                }
            }
        }
        
        // Update simulation time
        t += event.getTime();
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

    public boolean hasNextEvent() {
        return this.particles.size() > TABLE_HOLES;
    }
    
}
