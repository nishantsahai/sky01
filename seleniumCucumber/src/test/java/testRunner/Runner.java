package testRunner;

import cucumber.api.CucumberOptions;
import cucumber.api.SnippetType;
import cucumber.api.testng.AbstractTestNGCucumberTests;

@CucumberOptions(
			features = {"src/test/java/features/login.feature", "src/test/java/features/addToCart.feature"},
			dryRun = false,
			snippets = SnippetType.CAMELCASE,
			monochrome = true,
			glue = {"steps", "hooks"},
			plugin = {"pretty", "html:cucumberReport.html", "json:reports/report.json", "junit:reports/report.xml"}
//			tags = {"@reg, @smoke"}
//			tags = {"@test"}
		)

public class Runner extends AbstractTestNGCucumberTests{

}
