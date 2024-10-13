package steps;

import java.time.Duration;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriver.Options;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;

import cucumber.api.java.en.And;
import cucumber.api.java.en.But;
import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;

public class LoginSteps {

	WebDriver driver = webDriverSingleton.getDriver(); 
	WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

//	@Given("User navigate to the BookCart Application")
//	public void userNavigateToTheBookCartApplication() throws InterruptedException {
//		//User navigate to the BookCart Application
//		System.out.println("Testing this line");
//		//driver = new ChromeDriver();
//		String URL = "https://bookcart.azurewebsites.net/";
//		driver.get(URL);
//		Options manage = driver.manage();
//		driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
//		manage.window().maximize();
//		Thread.sleep(2000);
//	}

	@Given("User click on the login link")
	public void userClickOnTheLoginLink() throws InterruptedException {
		driver.findElement(By.xpath("//span[text()=' Login ']")).click();	
		Thread.sleep(2000);
	}

	@And("User enter the username as {string}")
	public void userEnterTheUsernameAs(String username) throws InterruptedException {
		driver.findElement(By.cssSelector("input[placeholder='Username']")).sendKeys(username);	
		Thread.sleep(2000);
	}

	@And("User enter the password as {string}")
	public void userEnterThePasswordAs(String password) throws InterruptedException {
		driver.findElement(By.cssSelector("input[placeholder='Password']")).sendKeys(password);	
		Thread.sleep(2000);
	}

	@When("User click on the login button")
	public void userClickOnTheLoginButton() throws InterruptedException {
		driver.findElement(By.xpath("//span[text()='Login']")).click();
		Thread.sleep(2000);
	}

	@Then("Login should be success")
	public void loginShouldBeSuccess() throws InterruptedException {
		WebElement userName = driver.findElement(By.xpath("//span[text()=' MohanLal']"));
		String loginUser  = wait.until(ExpectedConditions.visibilityOf(userName)).getText();
		Assert.assertEquals("MohanLal", loginUser);
		Thread.sleep(5000);
//		webDriverSingleton.quitDriver();
	}

	@But("Login should fail")
	public void loginShouldFail() throws InterruptedException {
		String loginText = driver.findElement(By.xpath("//mat-error[text()='Username or Password is incorrect.']")).getText();
		Assert.assertEquals("Username or Password is incorrect.", loginText);
		Thread.sleep(5000);
//		webDriverSingleton.quitDriver();	
	}


}
