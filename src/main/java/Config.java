import com.moandjiezana.toml.Toml;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.List;

public class Config {
    private static int tableWidth, tableHeight;
    private static String staticFile, outputFile;

    static {
        try {
            Toml toml = new Toml().read(new File("config.toml"));

            tableWidth = toml.getLong("simulation.tableWidth").intValue();
            tableHeight = toml.getLong("simulation.tableHeight").intValue();
            staticFile = toml.getString("files.staticInput");
            outputFile = toml.getString("files.output");
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

    public static String getStaticFile() { return staticFile; }

    public static String getOutputFile() {
        return outputFile;
    }
}
