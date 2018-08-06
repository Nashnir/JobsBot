""" JobsBot - The heart of the app relies here

This is the main class of the program.
It defines the JobsBot class, which is responsible for searching for, and sending, job applications.

Main class functions:
    - get_targets() - updates the list of job applications which are possible applications;
    - apply_auto() - sends the job applications;


USAGE:

# import the bot
from jobs.StackJobs import JobsBot

# define verbosity
v = 0                                           # not very verbose
v = 1                                           # more verbosity

# create the bot
sj_bot = JobsBot(verbose=v)                     # creates the bot object, passes verbosity argument. default is 0

# find jobs which match your parameters
sj_job.get_targets(should_update=True)          # always use should_update=True on the first usage
                                                # next usages will ignore already found targets, and be much faster

# apply to jobs
sj_job.apply_auto()                             # sends the job applications.
                                                # This will eventually be discovered by StackOverflow,
                                                # upon which the process must restart.

"""

import time
import random
from jobs.utils import *
from selenium import webdriver
from jobs.logger import getLogger


class JobsBot(object):
    """ JobsBot is responsible for searching for, and sending, job applications.

    Main class functions:
        - get_targets() - updates the list of job applications which are possible applications;
        - apply_auto() - sends the job applications;

    """

    def __init__(self, verbose=0):
        """ initiates the bot by loading config variables, and driver """
        self.init_logger(verbose)
        self.init_docs()
        self.driver = webdriver.Chrome()

    def init_logger(self, verbose):
        """ Initiates the logger """
        logging_lvl = "INFO" if verbose == 1 else "WARNING"
        self.logger = getLogger(lvl=logging_lvl)
        self.logger.info("loading config variables")

    def init_docs(self):
        """ Loads the configurations, together with the relevant paths. """
        self.configs = get_configs()
        self.taboo_path = get_path_from_rel(self.configs["taboo_rel_path"])
        self.applied_path = get_path_from_rel(self.configs["applied_rel_path"])
        self.targets_path = get_path_from_rel(self.configs["targets_rel_path"])
        self.cvr_path = get_path_from_rel(self.configs["cv_rel_path"])

    def nav_to(self, url, sleep_time=2):
        """ navigates toa given page and waits for a predefined time """
        self.driver.get(url)
        time.sleep(sleep_time)

    def get_targets(self, should_update=True):
        """ 1) Loads the targets from file;
            2) Scrapes targets from page, for each link;
            3) Stops after encountering an already existing target;
            4) Overwrites targets file - preservers the old targets
        """
        self.logger.info("Loading targets...")
        targets_existing = load_txt_to_list(self.targets_path)
        if should_update:
            keywords, locations = self.configs["keywords"], self.configs["locations"]
            for base_url in yield_base_url(keywords, locations):
                self.logger.info("Loading targets from: {}".format(base_url))
                targets_new = self.get_all_targets(base_url, targets_existing)
                targets_existing.extend(targets_new)
            self.logger.info("Finished loading targets.")
            overwrite_file(self.targets_path, targets_existing)
        self.targets = set(targets_existing)

    def get_all_targets(self, url, targets_base, sleep_time=2):
        """ Gets all job offer links from a particular query - visits all relevant pages """
        targets = []
        while True:
            self.nav_to(url)
            continue_searching = self.get_targets_from_page(targets, targets_base)
            if not continue_searching:
                self.logger.warning("encountered an already existing target. will not continue")
                return targets
            url = self.check_next_page()
            if not url:
                break
            time.sleep(sleep_time)
        return targets

    def get_targets_from_page(self, targets, targets_base):
        """ gets all job offer links from the current page. adds to targets list """
        for num in range(1, 26):
            xpath = '//*[@id="mainbar"]/div[2]/div/div[{}]/div[3]/h2/a'.format(num)
            target_elems = self.driver.find_elements_by_xpath(xpath)
            if len(target_elems) == 0:
                continue
            new_target = str(target_elems[0].get_attribute("href"))
            if new_target in targets_base:
                return False
            targets.append(new_target)
        return True

    def check_next_page(self):
        """ checks if next page exists. returns the page url if so. returns False otherwise """
        next_elems = self.driver.find_elements_by_link_text("nextchevron_right")
        if len(next_elems) == 0:
            return False
        else:
            url = next_elems[0].get_attribute("href")
            return url

    def apply_to(self, url):
        """ navigates to target page, verifies if application is possible, uploads info, and clicks apply job """
        self.nav_to(url)
        company_name = self.get_company_name()
        can_apply = self.nav_to_apply()
        if not can_apply:
            return False
        self.upload_all()
        self.click_apply()
        try:
            alert = self.driver.switch_to_alert()
            alert.accept()
        except:
            pass
        #add_to_taboo(self.applied_path, url)
        # self.logger.critical("successfully applied to: {}".format(company_name))
        return True

    def get_company_name(self):
        xpath_name = '//*[@id="content"]/header/div[2]/div/a'
        name_elems = self.driver.find_elements_by_xpath(xpath_name)
        name_company = name_elems[0].text
        return name_company

    def click_apply(self):
        """ clicks on the 'apply' button """
        css_apply = "#content > div.j-full-page-apply.wmx6.m-auto.px48.py24.ba.bc-black-2.my24 > form > div.grid.gs12.ai-center > div:nth-child(1) > input"
        self.driver.find_element_by_css_selector(css_apply).click()
        time.sleep(2)

    def nav_to_apply(self):
        """ navigates to application page, is possible, and returns True. Returns False, is not possible """
        xpath_apply = '//*[@id="content"]/header/div[3]/div[1]/a'
        apply_el = self.driver.find_element_by_xpath(xpath_apply)
        is_external = apply_el.get_attribute("target")
        if is_external:
            return False
        apply_el.click()
        return True

    def upload_all(self, sleep_time=20):
        """ Handles the update of Curriculum, base information, and motivation letter. Sleeps after"""
        self.logger.info("Uploading necessary information")
        self.upload_cv()
        self.upload_base_info()
        self.upload_letter()
        time.sleep(sleep_time)              # requires long sleep time, so the CV can be uploaded and scanned for virus

    def upload_base_info(self):
        """ Clears the text area of name, location, email and phone number, and uploads this info """
        self.driver.find_element_by_id("CandidateName").clear()
        self.driver.find_element_by_id("CandidateName").send_keys(self.configs["candidate_name"])
        self.driver.find_element_by_id("CandidateLocation").clear()
        self.driver.find_element_by_id("CandidateLocation").send_keys(self.configs["candidate_location"])
        self.driver.find_element_by_id("CandidateEmail").clear()
        self.driver.find_element_by_id("CandidateEmail").send_keys(self.configs["candidate_email"])
        self.driver.find_element_by_id("CandidatePhoneNumber").clear()
        self.driver.find_element_by_id("CandidatePhoneNumber").send_keys(self.configs["candidate_phone_number"])

    def upload_letter(self):
        """ Cleans and uploads the motivation letter """
        xpath_text = '//*[@id="CoverLetter"]'
        text_el = self.driver.find_element_by_xpath(xpath_text)
        text_el.clear()
        self.driver.execute_script("arguments[0].value = arguments[1]", text_el, self.configs["letter"])

    def upload_cv(self):
        """ Uploads the Curriculum """
        xpath_dd = '//*[@id="uploader-wrapper"]/div/p[2]/a/input'
        self.driver.find_element_by_xpath(xpath_dd).send_keys(self.cvr_path)

    def apply_safe(self, url):
        try:
            success = self.apply_to(url)
            append_to_file(self.applied_path, url)
            self.logger.critical("Succesfully applied to {}".format(url))
            return success
        except:
            self.logger.error("There was an error applying to {}. continuing.".format(url))
            return False

    def apply_auto(self):
        self.logger.info("Starting main cycle - applying to jobs")
        num_errors = 0
        self.get_targets()                                      # Loads targets from file, and updates them. targets available at self.targets (set)
        taboos = set(load_txt_to_list(self.taboo_path))         # Loads taboo urls to set
        urls = self.targets.difference(taboos)                  # disjunction of targets and taboos
        for index, url in enumerate(urls):
            self.logger.warning("Running application number {} out of {}".format(index, len(urls)))
            self.logger.warning("Will try to apply to {}".format(url))
            append_to_file(self.taboo_path, url)                # extend taboo file
            success = self.apply_safe(url)                      # apply safely
            num_errors = 0 if success else num_errors + 1
            sleep_time = random.randint(50, 80) if success else random.randint(10, 40)
            time.sleep(sleep_time)
            if num_errors > 10:
                self.logger.error("Got too many consecutive errors. Will stop now.")
                return
        self.driver.quit()
        self.logger.info("Finished execution on the end. Good luck with the interviews. Bye now.")

