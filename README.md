# Bot for searching and sending job applications

This is an application for searching for, and sending, job applications via StackOverflow.
It is developed using Python, and used Selenium to emulate a web browser. 
Note that this bot violates the terms and conditions of StackOverflow,
and thus should be use at your own risk. Because of this, please use it
with the predefined parameters, as to not overload their servers.

## Table of contents 
- [The Goal](#the-goal)
- [Installation](#installation)
- [User Guide](#user-guide)
    
## The Goal

The main objective of this project is to increase the chances of landing a job. Searching for, and sending, job applications
is usually a slow and tedious process. As a programmer, looking for programming jobs, I thought I would spare myself this pain.
Today, I feel like I should share this project so that anyone looking for a programming job could utilise this as well.

In any case, there are a few things worth noting:
 1) this bot works only for StackOverflow, and even than there are many job applications which it can not handle. 
 for example, many job applications redirect to an external page, which is not handled by this bot;
 2) this bot violates the terms of conditions of StackOverflow. Since StackOverflow is a website with a community that I respect 
 a lot, I ask you to use it carefully, and to not overload their servers.
 

## Installation

This application requires the download of:

1) Chromedriver - the driver that is used by selenium - download via [chromedriver](http://chromedriver.chromium.org/).
Please remember to add chromedriver to your path, or to a folder which already exists in the path (for example the python directory)

To actually install this app on your local machine, execute the following steps:
1) create and navigate to a directory of your choice, for example:
    ``` 
    mkdir jobsBot && cd jobsBot
    ```
2) start the git environment:
    ```sh
    git init .
    ```
3) clone this repository:
    ```sh 
    git clone https://github.com/rafaelmarques7/JobsBot.git
    ```
4) navigate to the newly created folder: 
    ```sh 
    cd jobsBot
    ```
 5) install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```
 6) update the configs.json file: add your name, email, location, phone number, cover letter, add your CV to /docs, and select
 a list of keywords (for example Python, JavaScript, etc.), and locations (for example Berlin, France, etc.)
     ```json
     {
      "candidate_name": "Your Name",
      "candidate_location": "Your location",
      "candidate_email": "Your email",
      "candidate_phone_number": "Your phone number (use country indicative)",
      "keywords": ["list", "of", "keywords"],
      "locations": ["list", "of", "cities", "and/or", "countries"],
      "taboo_rel_path": "docs/taboo.txt",
      "applied_rel_path": "docs/applied.txt",
      "targets_rel_path": "docs/targets.txt",
      "cv_rel_path": "docs/cv.txt",
      "letter": "Write your introduction letter here. Use \n to create newline for paragraph spacing."
    }  
     ```
 7) you can now execute the bot by running:
    ```sh
    python jobs_infty.py
    ```
    
    
## User Guide

This program works in the following way:
1) It creates a webdriver using Selenium and Google Chrome. This driver is created upon the initialisation of a
StackJobs class object.
2) It creates an URL for the StackOverflow jobs website, based on the configs (location and keywords) (/jobs/utils.py/yield_base_url). 
Note that the maximum experience level is set to MidLevel.
    
    2.1) It traverses each of these URL's and collects the target jobs urls - which are stored to /docs/targets.txt
3) It will navigate to each of the target job page, and apply to it, by uploading your basic information and curriculum (/jobs/StackJobs.py/apply_auto).
4) It stores the information about the application on (/docs/applied.txt in case of success and /docs/taboo.txt in case of success and failure)
as to not repeat these applications.
5) After some applications, the server will eventually detect the program, notice its a bot, and add a Captcha to the webpage. In this case,
the program must stop the execution, and restart later. 
6) If the program was run using jobs_infty.py, the program sleeps for an hour after being detected, and automatically restarts after. 
If it is executed using jobs_cli.py, it must be restarted manually.
