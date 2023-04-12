import com.moandjiezana.toml.Toml;

import java.io.FileInputStream;
import java.io.InputStream;
import java.util.List;

public class Config {
    private static int tableWidth, tableHeight, ballMass;
    private static double whiteBallX, whiteBallY, ballDiameter;

    static {
        Toml toml = new Toml().read(Config.class.getResourceAsStream("config.toml"));

        tableWidth = toml.getLong("simulation.tableWidth").intValue();
        tableHeight = toml.getLong("simulation.tableHeight").intValue();
        ballMass = toml.getLong("simulation.ballMass").intValue();
        List<Object> whiteBallCords = toml.getList("simulation.whiteBallX");
        whiteBallX = (double) whiteBallCords.get(0);
        whiteBallY = (double) whiteBallCords.get(1);
        ballDiameter = toml.getDouble("simulation.ballDiameter");
    }

    public static int getTableWidth() {
        return tableWidth;
    }

    public static int getTableHeight() {
        return tableHeight;
    }

    public static int getBallMass() {
        return ballMass;
    }

    public static double getWhiteBallX() {
        return whiteBallX;
    }

    public static double getWhiteBallY() {
        return whiteBallY;
    }

    public static double getBallDiameter() {
        return ballDiameter;
    }
}
