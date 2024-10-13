package hooks;

import java.time.Duration;

import org.openqa.selenium.OutputType;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriver.Options;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.support.ui.WebDriverWait;

import cucumber.api.Scenario;
import cucumber.api.java.After;
import cucumber.api.java.AfterStep;
import cucumber.api.java.Before;
import cucumber.api.java.BeforeStep;
import steps.webDriverSingleton;

public class hook {
	
	RemoteWebDriver driver = webDriverSingleton.getDriver();
	WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
	
	@Before
	public void beofreScenario(Scenario scenario) throws InterruptedException {
		System.out.println("Scenario name : "+ scenario.getName());
		String URL = "https://bookcart.azurewebsites.net/";
		driver.get(URL);
		Options manage = driver.manage();
		driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
		manage.window().maximize();
		Thread.sleep(2000);		
	}
	
	@After
	public void afterScenario(Scenario scenario) {
		boolean status = scenario.isFailed();
		System.out.println("Is Failed? - "+ status);
		if(!status) {
			byte[] screenshotAs = driver.getScreenshotAs(OutputType.BYTES);
			scenario.embed(screenshotAs, "image/png");
		}
		webDriverSingleton.quitDriver();
	}
	
	@BeforeStep
	public void beforeStep() {
		
	}
	
	@AfterStep
	public void afterStep() {
		
	}

}
