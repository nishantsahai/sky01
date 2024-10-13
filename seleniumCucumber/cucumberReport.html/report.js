$(document).ready(function() {var formatter = new CucumberHTML.DOMFormatter($('.cucumber-report'));formatter.uri("src\\test\\java\\features\\addToCart.feature");
formatter.feature({
  "name": "Add books to the cart",
  "description": "",
  "keyword": "Feature"
});
formatter.scenarioOutline({
  "name": "Adding book to the cart",
  "description": "",
  "keyword": "Scenario Outline",
  "tags": [
    {
      "name": "@smoke"
    }
  ]
});
formatter.step({
  "name": "User enter the username as \"\u003cusername\u003e\"",
  "keyword": "And "
});
formatter.step({
  "name": "User enter the password as \"\u003cpassword\u003e\"",
  "keyword": "And "
});
formatter.step({
  "name": "User click on the login button",
  "keyword": "And "
});
formatter.step({
  "name": "User search a book \"\u003cbook\u003e\"",
  "keyword": "And "
});
formatter.step({
  "name": "User add books to the cart",
  "keyword": "When "
});
formatter.step({
  "name": "The cart badge should get updated",
  "keyword": "Then "
});
formatter.examples({
  "name": "",
  "description": "",
  "keyword": "Examples",
  "rows": [
    {
      "cells": [
        "username",
        "password",
        "book"
      ]
    },
    {
      "cells": [
        "MohanLal",
        "Mohan@1234",
        "Birthday girl"
      ]
    }
  ]
});
formatter.background({
  "name": "",
  "description": "",
  "keyword": "Background"
});
formatter.before({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User click on the login link",
  "keyword": "Given "
});
formatter.match({
  "location": "LoginSteps.userClickOnTheLoginLink()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.scenario({
  "name": "Adding book to the cart",
  "description": "",
  "keyword": "Scenario Outline",
  "tags": [
    {
      "name": "@smoke"
    }
  ]
});
formatter.step({
  "name": "User enter the username as \"MohanLal\"",
  "keyword": "And "
});
formatter.match({
  "location": "LoginSteps.userEnterTheUsernameAs(String)"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User enter the password as \"Mohan@1234\"",
  "keyword": "And "
});
formatter.match({
  "location": "LoginSteps.userEnterThePasswordAs(String)"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User click on the login button",
  "keyword": "And "
});
formatter.match({
  "location": "LoginSteps.userClickOnTheLoginButton()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User search a book \"Birthday girl\"",
  "keyword": "And "
});
formatter.match({
  "location": "AddToCartSteps.userSearchABook(String)"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User add books to the cart",
  "keyword": "When "
});
formatter.match({
  "location": "AddToCartSteps.userAddBooksToTheCart()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "The cart badge should get updated",
  "keyword": "Then "
});
formatter.match({
  "location": "AddToCartSteps.theCartBadgeShouldGetUpdated()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.embedding("image/png", "embedded0.png");
formatter.after({
  "status": "passed"
});
formatter.uri("src\\test\\java\\features\\login.feature");
formatter.feature({
  "name": "BookCart Application Tests",
  "description": "",
  "keyword": "Feature"
});
formatter.background({
  "name": "",
  "description": "",
  "keyword": "Background"
});
formatter.before({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User click on the login link",
  "keyword": "Given "
});
formatter.match({
  "location": "LoginSteps.userClickOnTheLoginLink()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.scenario({
  "name": "Login should be success",
  "description": "",
  "keyword": "Scenario"
});
formatter.step({
  "name": "User enter the username as \"MohanLal\"",
  "keyword": "And "
});
formatter.match({
  "location": "LoginSteps.userEnterTheUsernameAs(String)"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User enter the password as \"Mohan@1234\"",
  "keyword": "And "
});
formatter.match({
  "location": "LoginSteps.userEnterThePasswordAs(String)"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User click on the login button",
  "keyword": "When "
});
formatter.match({
  "location": "LoginSteps.userClickOnTheLoginButton()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "Login should be success",
  "keyword": "Then "
});
formatter.match({
  "location": "LoginSteps.loginShouldBeSuccess()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.embedding("image/png", "embedded1.png");
formatter.after({
  "status": "passed"
});
formatter.scenarioOutline({
  "name": "Login should not be success",
  "description": "",
  "keyword": "Scenario Outline",
  "tags": [
    {
      "name": "@reg"
    },
    {
      "name": "@prod"
    }
  ]
});
formatter.step({
  "name": "User enter the username as \"\u003cusername\u003e\"",
  "keyword": "And "
});
formatter.step({
  "name": "User enter the password as \"\u003cpassword\u003e\"",
  "keyword": "And "
});
formatter.step({
  "name": "User click on the login button",
  "keyword": "When "
});
formatter.step({
  "name": "Login should fail",
  "keyword": "But "
});
formatter.examples({
  "name": "",
  "description": "",
  "keyword": "Examples",
  "rows": [
    {
      "cells": [
        "username",
        "password"
      ]
    },
    {
      "cells": [
        "John",
        "Johny@123"
      ]
    },
    {
      "cells": [
        "koushik",
        "Passkoushik"
      ]
    }
  ],
  "tags": [
    {
      "name": "@test"
    }
  ]
});
formatter.background({
  "name": "",
  "description": "",
  "keyword": "Background"
});
formatter.before({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User click on the login link",
  "keyword": "Given "
});
formatter.match({
  "location": "LoginSteps.userClickOnTheLoginLink()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.scenario({
  "name": "Login should not be success",
  "description": "",
  "keyword": "Scenario Outline",
  "tags": [
    {
      "name": "@reg"
    },
    {
      "name": "@prod"
    },
    {
      "name": "@test"
    }
  ]
});
formatter.step({
  "name": "User enter the username as \"John\"",
  "keyword": "And "
});
formatter.match({
  "location": "LoginSteps.userEnterTheUsernameAs(String)"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User enter the password as \"Johny@123\"",
  "keyword": "And "
});
formatter.match({
  "location": "LoginSteps.userEnterThePasswordAs(String)"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User click on the login button",
  "keyword": "When "
});
formatter.match({
  "location": "LoginSteps.userClickOnTheLoginButton()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "Login should fail",
  "keyword": "But "
});
formatter.match({
  "location": "LoginSteps.loginShouldFail()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.embedding("image/png", "embedded2.png");
formatter.after({
  "status": "passed"
});
formatter.background({
  "name": "",
  "description": "",
  "keyword": "Background"
});
formatter.before({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User click on the login link",
  "keyword": "Given "
});
formatter.match({
  "location": "LoginSteps.userClickOnTheLoginLink()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.scenario({
  "name": "Login should not be success",
  "description": "",
  "keyword": "Scenario Outline",
  "tags": [
    {
      "name": "@reg"
    },
    {
      "name": "@prod"
    },
    {
      "name": "@test"
    }
  ]
});
formatter.step({
  "name": "User enter the username as \"koushik\"",
  "keyword": "And "
});
formatter.match({
  "location": "LoginSteps.userEnterTheUsernameAs(String)"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User enter the password as \"Passkoushik\"",
  "keyword": "And "
});
formatter.match({
  "location": "LoginSteps.userEnterThePasswordAs(String)"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User click on the login button",
  "keyword": "When "
});
formatter.match({
  "location": "LoginSteps.userClickOnTheLoginButton()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "Login should fail",
  "keyword": "But "
});
formatter.match({
  "location": "LoginSteps.loginShouldFail()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.embedding("image/png", "embedded3.png");
formatter.after({
  "status": "passed"
});
formatter.examples({
  "name": "",
  "description": "",
  "keyword": "Examples",
  "rows": [
    {
      "cells": [
        "username",
        "password"
      ]
    },
    {
      "cells": [
        "Maria",
        "Maria@123"
      ]
    }
  ],
  "tags": [
    {
      "name": "@prod"
    }
  ]
});
formatter.background({
  "name": "",
  "description": "",
  "keyword": "Background"
});
formatter.before({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User click on the login link",
  "keyword": "Given "
});
formatter.match({
  "location": "LoginSteps.userClickOnTheLoginLink()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.scenario({
  "name": "Login should not be success",
  "description": "",
  "keyword": "Scenario Outline",
  "tags": [
    {
      "name": "@reg"
    },
    {
      "name": "@prod"
    },
    {
      "name": "@prod"
    }
  ]
});
formatter.step({
  "name": "User enter the username as \"Maria\"",
  "keyword": "And "
});
formatter.match({
  "location": "LoginSteps.userEnterTheUsernameAs(String)"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User enter the password as \"Maria@123\"",
  "keyword": "And "
});
formatter.match({
  "location": "LoginSteps.userEnterThePasswordAs(String)"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "User click on the login button",
  "keyword": "When "
});
formatter.match({
  "location": "LoginSteps.userClickOnTheLoginButton()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.beforestep({
  "status": "passed"
});
formatter.step({
  "name": "Login should fail",
  "keyword": "But "
});
formatter.match({
  "location": "LoginSteps.loginShouldFail()"
});
formatter.result({
  "status": "passed"
});
formatter.afterstep({
  "status": "passed"
});
formatter.embedding("image/png", "embedded4.png");
formatter.after({
  "status": "passed"
});
});