#class="uk-table table table-bordered text-center table table-hover table-striped  display dataTable no-footer"
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import time
import re
import os
import sys
from selenium.webdriver.support.ui import WebDriverWait
import MySQLdb
import logging
import datetime
from scrapy.selector import Selector
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
from email import encoders
from email.mime.base import MIMEBase
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from optparse import OptionParser
from selenium.webdriver.common.by import By



loggers = {}
def myLogger(name):
	log_path = os.path.abspath('logs/')
	try:
		os.mkdir(log_path)
	except:
		pass

	global loggers
	path = 'logs/nps_rpa_%s_%s.log'

	if loggers.get(name):
		return loggers.get(name)
	else:
		logger = logging.getLogger(name)
		logger.setLevel(logging.DEBUG)
		now = datetime.datetime.now()
		handler = logging.FileHandler(path %(name, now.strftime("%Y-%m-%d")))
		formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)d - %(funcName)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		logger.addHandler(handler)
		loggers.update(dict(name=logger))
		return logger


process_logger = myLogger('process')

def log_exception(driver, custome_exc, exc, GP_ID, images_list):
	process_logger.debug(custome_exc)
	process_logger.debug(exc)
	process_logger.debug('Failure GPID :: %s' %str(GP_ID))
	failure.append(GP_ID)
	failure_image_list.extend(images_list)
	failure_ids_list.append(GP_ID)
	driver.get(materials_url)
	driver.refresh()
	driver.implicitly_wait(5)
	time.sleep(2)

def start_nps_process():
	#process_logger.debug('NPS RPA Process has started.')
	display, driver = open_driver()
	login_status, message = login_nps(driver, display)
	#if login_status: 
	#return message
	driver.implicitly_wait(5)
	process_logger.debug('Login Successful')
	sel = Selector(text=driver.page_source)
	import pdb;pdb.set_trace()
	from datetime import date
	today = date.today()
	x =  today.strftime("%m-%d-%Y")
	del_path = '/home/headrun/Documents/ann/myntra_POD/upload_document/del_path/'
	path = '/home/headrun/Documents/ann/myntra_POD/upload_document'
	driver.find_element_by_xpath('//div[@id="datepicker"]//input[@id="fromDate"]').click()
	driver.find_element_by_xpath('//div[@id="datepicker"]//input[@id="fromDate"]').clear()
	driver.find_element_by_xpath('//div[@id="datepicker"]//input[@id="fromDate"]').send_keys(x)
	driver.find_element_by_xpath('//div//button[@id="tableData"]').click()
	time.sleep(10)
	driver.find_element_by_xpath('//a[contains(text(),"Download CSV")]').click()
	import csv
	path = os.getcwd()
	for root, dirs, files in os.walk(path):
		for dir_file in files:
			 if '.csv' in dir_file:
				import pdb;pdb.set_trace()
			 	_file = path+'/'+dir_file
				command = 'mv "%s" "%s"' % (_file, del_path)
			 	os.system(command)
				
			 for root, dirs, files in os.walk(del_path):
				for dir_file in files:
					if '.csv' in dir_file:
						mail = send_mail()
					
							
def send_mail():

		#import pdb;pdb.set_trace()
		del_path = '/home/headrun/Documents/ann/myntra_POD/upload_document/del_path/'
		receivers_list = ["minal@mieone.com", "suraj@headrun.com"]
		sender, receivers  = "minal@headrun.com", ",".join(receivers_list)
		msg = MIMEMultipart("alternative")
		msg['Subject'] = "PFA the csv file for NPS %s" % str(datetime.datetime.now().date())
		line = "<p>Hi All,</p><p>Please find the attached CSV's of NPS feedback.</p>"
		end_line = "<p>Thanks,<br/>Minal Mittal</p>"
		import pdb;pdb.set_trace()
		path = os.getcwd()+'/'+"del_path/"
		
		for root, dirs, files in os.walk(path):
			for dir_file in files:
				now = time.strftime('%d-%m-%Y')
				if '.csv' in dir_file:
					#import pdb;pdb.set_trace()
					csv_file  = dir_file
					print csv_file
					#import pdb;pdb.set_trace()
					
					import csv
					csv_path = path + csv_file
					#data = pd.read_csv(csv_path)
					msg['From'] = sender
					msg['To'] = receivers

					part = MIMEBase('application', "octet-stream")
					#give full path name
					part.set_payload(open(csv_path, "rb").read())
					encoders.encode_base64(part)
					csv_file_main = str(datetime.datetime.now().date())  + '_' + csv_file
					part.add_header('Content-Disposition', 'attachment', filename=csv_file_main)
					mail_text = MIMEText(''.join(line+end_line),part)
					#msg.attach(''.join(line+end_line),part)
					s = smtplib.SMTP('smtp.gmail.com:587')
					s.ehlo()
					s.starttls()
					s.login(sender, 'Nicagoes14$')
					print "Mail Sent!"
					s.sendmail(sender, receivers_list, msg.as_string())
					s.quit()
					os.remove(csv_file)
					
					

def open_driver():
	display = "something"
	options = webdriver.ChromeOptions()
	driver = webdriver.Chrome()
	return display, driver

def close_driver(display, driver):
	display.stop()
	driver.quit()


def login_nps(driver, display):
	import pdb;pdb.set_trace()
	login_url = "https://warehouse-feedback-collection.firebaseapp.com/"
	login_status = 0
		#import pdb;pdb.set_trace()
	driver.get(login_url)
	time.sleep(5)
	process_logger.debug('Login URL: %s has loaded into webdriver.' %str(login_url))
	time.sleep(5)
	wait_driver = WebDriverWait(driver, 5)
	return login_status, {'message': 'Login Successful', 'status': True}

if __name__ == '__main__':


	try:start_nps_process()
	except: import pdb;pdb.set_trace()