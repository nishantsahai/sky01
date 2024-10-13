#@E2E
Feature: BookCart Application Tests

  Background: 
    #Given User navigate to the BookCart Application
    Given User click on the login link

  Scenario: Login should be success
    And User enter the username as "MohanLal"
    And User enter the password as "Mohan@1234"
    When User click on the login button
    Then Login should be success

  @reg @prod
  Scenario Outline: Login should not be success
    And User enter the username as "<username>"
    And User enter the password as "<password>"
    When User click on the login button
    But Login should fail

    @test
    Examples: 
      | username | password    |
      | John     | Johny@123   |
      | koushik  | Passkoushik |

    @prod
    Examples: 
      | username | password  |
      | Maria    | Maria@123 |
