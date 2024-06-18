<h1 align="center">The Meadow Project-Testing</h1>

![The Meadow Project on different screens]()

[View the live website here - The Meadow Project]()

---
<h2>Contents</h2>







# Introduction

Testing is essential to ensure the website functions correctly, is free from bugs, and allows users to fully utilise all features before its release to the general market. This guarantees a positive user experience (UX) and encourages repeat visits from customers and registered users.

Throughout the development process, I relied on Chrome developer tools to assess page responsiveness across various screen sizes and address any encountered issues. In troubleshooting, I utilised the console to log and monitor JavaScript code, aiding in resolving aspects of the site that did not perform as intended. Additionally, I employed Python development techniques to address backend issues, ensuring seamless functionality across the site. All the test results detailed below are based on the [deployed site]().

---

# Automated Testing

The automated testing implemented in this project complements the manual tests, ensuring that the Python code fulfilled its objectives from the outset. The testing strategy was not aimed at achieving 100% coverage but at supporting and enhancing the manual testing process. To run tests I have used the Django Testing Framework. 

The tests for each app are organized into a tests folder. Note that tests were conducted using the local database, as Heroku does not support automatic testing of its databases. During testing, the Postgres database configuration in settings.py was commented out to facilitate running tests locally.

To run the tests:

* Type "python3 manage.py test" into the terminal.
* To test one app only type "python manage.py test <app name>".
* To understand how comprehensive the test are, generate a coverage report using the command "coverage report".
* To view the coverage report in your web browser, type "coverage html" and open the "index.html" file newly created directory.

During this build, I utilised [Travis](https://www.travis-ci.com/) CI to automatically run tests each time my project was deployed. This ensured I was promptly notified of any test failures caused by new code, allowing me to address issues before they were merged into my main branch. This also meant I did not need to alter my settings.py file to run tests. 

# Manual Testing

# Validators
