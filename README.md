<!-- <img alt="Static Badge" src="https://img.shields.io/badge/Antonio_Rodriguez-%23bc1224"> -->
<!-- <img alt="Static Badge" src="https://img.shields.io/badge/QA_Engineer_%7C_Antonio_Rodriguez_Farias-%23007bff"> -->
<!-- <img alt="Static Badge" src="https://img.shields.io/badge/QA_Engineer_%7C_Antonio_Rodriguez_Farias-%23007bff"> -->
<!-- <img alt="Static Badge" src="https://img.shields.io/badge/QA_Engineer_%7C_Antonio_Rodriguez_Farias-%2328a745"> -->
<img alt="Static Badge" src="https://img.shields.io/badge/Antonio_Rodriguez_Farias-%2328a745?style=plastic&label=QA%20Engineer&labelColor=%23dc3545">


<h1 align="center"> Python Tests </h1>


### Backend tests:
* An automated endpoint test circuit is created by making the different calls implemented on them, using the <a href="https://docs.python-requests.org/en/latest/index.html"><i>requests</i></a> library.
* Sometimes it connects with <a href="https://firebase.google.com/docs/firestore/quickstart?hl=es-419#python"><i>Cloud Firestore</i></a> to be able to take data as unique identifiers to be able to set them in the next call as an environment variable since the response is empty.
* Being able to delete data created from cloud firestore or using the corresponding endpoint (delete) if applicable.
&nbsp;
### Frontend tests:
* <a href="https://www.selenium.dev/documentation/webdriver/getting_started/"><i>Selenium</i></a> is used as a working framework together with pytest to structure the implemented code
<li>&nbsp; &nbsp; Among the libraries used: </li>
<li>&nbsp; &nbsp; &nbsp; &nbsp; <a href="https://faker.readthedocs.io/en/master/"><i>Faker</i></a>: to generate random data in tests </li>
<li>&nbsp; &nbsp; &nbsp; &nbsp; <a href="https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.desired_capabilities.html"><i>DesiredCapabilities</i></a>: to capture logs </li>
<li>&nbsp; &nbsp; &nbsp; &nbsp; <a href="https://selenium-python.readthedocs.io/getting-started.html"><i>Other</i></a> Selenium libraries </li>
&nbsp;
<li><a href="https://playwright.dev/python/">Playwright</a> used briefly as practice to understand its syntax and operation.</li>

### Continuous testing
* <a href="https://www.jenkins.io/"><i>Jenkins</i></a> is used as a continuous integration tool. Create a freestyle project that includes the development branches, a cronjob with the desired runtimes, and a windows console run that sends to the project directory and runs the script.
