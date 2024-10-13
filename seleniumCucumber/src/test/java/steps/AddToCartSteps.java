package steps;

import java.time.Duration;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;


public class AddToCartSteps {

	WebDriver driver = webDriverSingleton.getDriver(); 
	WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
	
	@Given("User search a book {string}")
	public void userSearchABook(String book) {
		driver.findElement(By.cssSelector("input[type='search']")).sendKeys(book);
		//driver.findElement(By.cssSelector("input[type='search']")).sendKeys(Keys.ENTER);
		driver.findElement(By.cssSelector("div#mat-autocomplete-0>mat-option>span")).click();
		try {
			Thread.sleep(2000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	@When("User add books to the cart")
	public void userAddBooksToTheCart() {
		WebElement addButton = driver.findElement(By.xpath("//span[text()[normalize-space()='Add to Cart']]"));
		wait.until(ExpectedConditions.visibilityOf(addButton)).click();
		try {
			Thread.sleep(2000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	@Then("The cart badge should get updated")
	public void theCartBadgeShouldGetUpdated() throws InterruptedException {
		driver.findElement(By.xpath("(//span[@class='mat-mdc-button-touch-target'])[3]")).click();
		Thread.sleep(2000);
		String text = driver.findElement(By.linkText("Birthday Girl")).getText();
		//String text = driver.findElement(By.xpath("(//span[@class='mat-mdc-button-touch-target'])[3]")).getText();
		//Assert.assertEquals(Integer.parseInt(text) > 0, true);
		Assert.assertEquals(text, "Birthday Girl");
		try {
			Thread.sleep(2000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
//		webDriverSingleton.quitDriver();
	}
	
}
