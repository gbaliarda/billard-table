public class Event implements Comparable<Event> {
    private double t;
    private Particle p1, p2;
    private int p1CollisionCount = 0, p2CollisionCount = 0;

    /**
     * Create a new event representing a collision between
     * particles a and b at time t. If neither a nor b is null, then it represents a pairwise collision between a and b; if both a
     * and b are null, it represents a redraw event; if only b is null, it represents a collision between a and a vertical wall; if
     * only a is null, it represents a collision between b and a horizontal wall.
     * @param t time to collision
     * @param a one particle. If null, then the event represents a collision between `b` and a horizontal wall.
     * @param b another particle. If null, then the event represents a collision between `a` and a vertical wall.
     */
    public Event(double t, Particle a, Particle b) {
        this.t = t;
        this.p1 = a;
        this.p2 = b;
        if (p1 != null)
            this.p1CollisionCount = a.getCollisionCount();
        if (p2 != null)
            this.p2CollisionCount = b.getCollisionCount();
    }

    /**
     * @return time associated with the event.
     */
    public double getTime() {
        return t;
    }

    /**
     * @return first particle, possibly null.
     */
    public Particle getParticle1() {
        return p1;
    }

    /**
     * @return second particle, possibly null.
     */
    public Particle getParticle2() {
        return p2;
    }

    /**
     * @param o
     * @return compare the time associated with this event and x. Return a positive number
     * (greater), negative number (less), or zero (equal) accordingly.
     */
    @Override
    public int compareTo(Event o) {
        int c = 0;
        
        if (this.t > o.t)
            c = 1;
        else if (this.t < o.t)
            c = -1;
        
        return c;
    }

    /**
     * @return true if the event has been invalidated since creation, and false otherwise.
     */
    public boolean wasSuperveningEvent() {
        return (p1 != null && p1CollisionCount != p1.getCollisionCount()) || (p2 != null && p2CollisionCount != p2.getCollisionCount());
    }
}
