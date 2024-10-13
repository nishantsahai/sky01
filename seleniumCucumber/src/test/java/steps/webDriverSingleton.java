package steps;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.remote.RemoteWebDriver;

public class webDriverSingleton {
    private static RemoteWebDriver driver;

    private webDriverSingleton() {
        // Private constructor to prevent instantiation
    }

    public static RemoteWebDriver getDriver() {
        if (driver == null) {
            //System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        	driver = new ChromeDriver();   	
        }
        return driver;
    }

    public static void quitDriver() {
        if (driver != null) {
            driver.quit();
            driver = null;
        }
    }
}
