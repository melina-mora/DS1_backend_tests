# DS1 backend tests suite for training/fun purposes

## Installation steps:

### Pre-requisites:
  - Should have pipenv installed.
  - Should have python 3.5 or later.
  - Have MongoDB installed (4.0 or later). Will connect to localhost instance.
  - (optional) Robo 3T to visualize json files.
  
### Steps:
1. Download the whole suite including DB files.
2. Configure pycharm in order to take pipenv interpreter to run tests.
3. In command line run **pipenv shell** to activate virtual environment.
4. In command line run **pipenv sync** to sync all the needed requirements.
5. In **\scripts\mongo_tools_script** run **mongo_tools_script.py** without any parameters.
6. Follow whole wizard installation.
7. Ready to use!

## Usage:

- --env <env> : Before running the test cases specify environment where to run. Example: --env dev
  
  Each test script has it's own set of countries where to run.
  
- --repeat <int> : Will run n number of times a same script. Example: --repeat 5
  
- -n <int> : Specify to run multi threads. Example: -n4
  
- --html=<path to save report>/name.html : specify to save an html file with report of the test cases ran. 
