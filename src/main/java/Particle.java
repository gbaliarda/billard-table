import java.util.Objects;

public class Particle {
    private double x, y, vx, vy, mass, radius;
    private int collisionCount;
    private final String color;

    public Particle(double x, double y, double vx, double vy, double mass, double radius, String color) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.mass = mass;
        this.radius = radius;
        this.collisionCount = 0;
        this.color = color;
    }

    /**
     * @return duration of time until the invoking particle collides with a vertical wall,
     * assuming it follows a straight-line trajectory. If the particle never collides with a vertical wall, return infinity.
     */
    public double collidesX() {
        double tc = Double.MAX_VALUE;

        if (vx > 0)
            tc = (Config.getTableWidth() - radius - x) / vx;
        else if (vx < 0)
            tc = (0 + radius - x) / vx; // left wall is at x = 0
        
        return tc;
    }

    /**
     * @return duration of time until the invoking particle collides with a horizontal wall,
     * assuming it follows a straight-line trajectory. If the particle never collides with a horizontal wall, return infinity.
     */
    public double collidesY() {
        double tc = Double.MAX_VALUE;

        if (vy > 0)
            tc = (Config.getTableHeight() - radius - y) / vy;
        else if (vy < 0)
            tc = (0 + radius - y) / vy; // bottom wall is at y = 0
        
        return tc;
    }

    /**
     * @param b any other Particle
     * @return duration of time until the invoking particle collides with particle
     * b, assuming both follow straight-line trajectories. If the two particles never collide, return a negative value.
     */
    public double collides(Particle b) {
        double tc = Double.MAX_VALUE;

        double[] dr = {b.getX() - this.x, b.getY() - this.y};
        double[] dv = {b.getVx() - this.vx, b.getVy() - this.vy};

        double dv_dr = dotProduct(dv, dr);

        if (dv_dr >= 0)
            return tc;
    
        double dv_dv = dotProduct(dv, dv);
        double sigma = this.radius + b.getRadius();

        double d = Math.pow(dv_dr, 2) - dv_dv*(dotProduct(dr, dr) - Math.pow(sigma, 2));
    
        if (d < 0)
            return tc;
            
        tc = -(dv_dr + Math.sqrt(d)) / dv_dv;
    
        return tc;
    }

    private double dotProduct(double[] a, double[] b) {
        double dp = 0;

        for (int i = 0; i < a.length; i++)
            dp += a[i] * b[i];

        return dp;
    }

    /**
     *  update the invoking particle to simulate it bouncing off a vertical wall.
     */
    public void bounceX() {
        this.vx *= -1;
        this.collisionCount++;
    }

    /**
     * update the invoking particle to simulate it bouncing off a horizontal wall
     */
    public void bounceY() {
        this.vy *= -1;
        this.collisionCount++;
    }

    /**
     * update both particles to simulate them bouncing off each other
     * @param b any other Particle
     */
    public void bounce(Particle b) {
        double[] dr = {b.getX() - this.x, b.getY() - this.y};
        double[] dv = {b.getVx() - this.vx, b.getVy() - this.vy};

        double sigma = this.radius + b.getRadius();

        double j = (2 * this.mass * b.getMass() * dotProduct(dv, dr))
                    / (sigma * (this.mass + b.getMass()));
                    
        double jx = (j * dr[0]) / sigma;
        double jy = (j * dr[1]) / sigma;

        this.vx = vx + jx / this.mass;
        this.vy = vy + jy / this.mass;

        b.setVx(b.getVx() - jx / b.getMass());
        b.setVy(b.getVy() - jy / b.getMass());

        this.collisionCount++;
    }

    /**
     * @return total number of collisions involving this particle.
     */
    public int getCollisionCount() {
        return collisionCount;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public double getVx() {
        return vx;
    }
    
    public double getVy() {
        return vy;
    }

    public double getRadius() {
        return radius;
    }

    public double getMass() {
        return mass;
    }

    public boolean isFixed() {
        return mass == 0;
    }

    public String getColor() {
        return color;
    }

    public void setVx(double vx) {
        this.vx = vx;
    }

    public void setVy(double vy) {
        this.vy = vy;
    }

    public void setX(double x) {
        this.x = x;
    }

    public void setY(double y) {
        this.y = y;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Particle particle = (Particle) o;
        return Double.compare(particle.x, x) == 0 && Double.compare(particle.y, y) == 0;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }
}
