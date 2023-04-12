import com.moandjiezana.toml.Toml;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.List;

public class Config {
    private static int tableWidth, tableHeight, ballMass;
    private static double whiteBallX, whiteBallY, ballDiameter;
    private static String staticFile;

    static {
        try {
            Toml toml = new Toml().read(new File("config.toml"));

            tableWidth = toml.getLong("simulation.tableWidth").intValue();
            tableHeight = toml.getLong("simulation.tableHeight").intValue();
            ballMass = toml.getLong("simulation.ballMass").intValue();
            List<Object> whiteBallCords = toml.getList("simulation.whiteBallCoords");
            whiteBallX = (double) whiteBallCords.get(0);
            whiteBallY = (double) whiteBallCords.get(1);
            ballDiameter = toml.getDouble("simulation.ballDiameter");
            staticFile = toml.getString("files.staticInput");
        } catch (Exception e) {
            e.printStackTrace();
        }
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

    public static String getStaticFile() { return staticFile; }
}
