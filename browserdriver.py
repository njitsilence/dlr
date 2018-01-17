import logging, os
import functools
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from vars_setting import WAITSEC

def show_log(func):

	@functools.wraps(func)
	def wrapper(*arg, **kw):
		logging.debug('The section %s is starting' %(func.__name__))
		res = func(*arg, **kw)
		time.sleep(0.5)
		logging.debug('Thi setion %s is complete'%(func.__name__))
		return res
	return wrapper

class BrowserDriver(object):
	"""docstring for NewWebDriver"""
	def __init__(self, driver_type='Chrome', msg='', status = True, \
		host='localhost', port=5555, is_remote=False, username='', \
		password='', url=''):

		self.msg = msg
		self.status = status
		self.driver_type = driver_type
		self.host = host
		self.port = port
		self.remote = is_remote
		self.username = username
		self.password = password
		self.url = url

	def __enter__(self):
		if not self.remote:
			if self.driver_type == 'Chrome':
				self.options = webdriver.ChromeOptions()
				#self.options.add_argument('headless')
				#self.options.add_argument('isable-gpu')
				#self.options.add_argument('window-size=1200x600')
				self.prefs = {'profile.default_content_settings.popups': 0, \
				'download.default_directory': os.getcwd()}
				self.options.add_experimental_option('prefs', self.prefs)
				try:
					self.driver = webdriver.Chrome(chrome_options=self.options)
				except Exception as e:
					raise
			elif self.driver_type == 'Firefox':
				fp = webdriver.FirefoxProfile()
				fp.set_preference("browser.download.folderList",2)
				fp.set_preference("browser.download.manager.showWhenStarting",False)
				fp.set_preference("browser.download.dir", os.getcwd())
				fp.set_preference("browser.helperApps.neverAsk.saveToDisk", \
				"application/octet-stream")
				try:
					self.driver = webdriver.Firefox(firefox_profile=fp)
				except Exception as e:
					raise
			else:
				logging.error('driver type is incorrect!')
				raise ValueError('driver type is incorrect!')
		else:
			if self.driver_type == 'Chrome':
				self.options = webdriver.ChromeOptions()
				#self.options.add_argument('headless')
				#self.options.add_argument('isable-gpu')
				#self.options.add_argument('window-size=1200x600')
				self.prefs = {'profile.default_content_settings.popups': 0, \
				'download.default_directory': os.getcwd()}
				self.options.add_experimental_option('prefs', self.prefs)
				try:
					self.driver = webdriver.Remote(''.join(['http://',self.host,':',str(self.port),'/wd/hub']),  
    						desired_capabilities=DesiredCapabilities.CHROME,
   							#chrome_options=self.options
   							)
				except Exception as e:
					raise
		return self

	def __exit__(self, exc_ty, exc_val, tb):
		self.driver.quit()

	@show_log
	def logon_check(self, value):

		try:
			self.driver.get(self.url)
			WebDriverWait(self.driver, WAITSEC).until(lambda x: x.find_element_by_xpath("//input[@id='CAMUsername']"))
		except Exception as e:
			logging.error('Logon failed %s' %e)
			raise
		else:
			self.driver.find_element_by_xpath("//input[@id='CAMUsername']").clear()
			self.driver.find_element_by_xpath("//input[@id='CAMUsername']").send_keys(self.username)
			self.driver.find_element_by_xpath("//input[@id='CAMPassword']").clear()
			self.driver.find_element_by_xpath("//input[@id='CAMPassword']").send_keys(self.password)
			self.driver.find_element_by_xpath("//input[@id='cmdOK']").click()

	@show_log
	def sel_rpt_lvl(self, value):

		WebDriverWait(self.driver, WAITSEC).until(lambda x: x.find_element_by_xpath("//option[@dv='"+value+"']"))
		self.driver.find_element_by_xpath("//option[@dv='"+value+"']").click()

	@show_log
	def sel_cty_comp(self, value):

		WebDriverWait(self.driver, WAITSEC).until(lambda x: x.find_element_by_xpath("//option[@dv='"+value+"']"))
		self.driver.find_element_by_xpath("//option[@dv='"+value+"']").click()

	@show_log
	def wk_date_start(self, value):
		start_date_value = '-'.join([str(value.year), str(value.month), str(value.day)])
		element = self.driver.find_element_by_xpath("//input[@class='clsSelectDateEditBox']")
		element.clear()
		element.send_keys(start_date_value)
	
	@show_log
	def wk_date_end(self, value):
		end_date_value = '-'.join([str(value.year), str(value.month), str(value.day)])
		element = self.driver.find_elements_by_xpath("//input[@class='clsSelectDateEditBox']")
		element[1].clear()
		element[1].send_keys(end_date_value)
		
	@show_log
	def sel_rpt_format(self, value):
		self.driver.find_element_by_xpath("//option[@dv='"+value+"']").click()

	@show_log
	def sel_rpt_crit(self, value):
		self.driver.find_element_by_xpath("//option[@dv='"+value+"']").click()
		# wait until the input widget come up
		#time.sleep(15)
		#WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath("//input[@class='clsTextWidget pt']"))

	@show_log
	def sel_acc_emp(self, value):
		if value == 'Account':
			value = 'Account '

		WebDriverWait(self.driver,WAITSEC).until(lambda x:x.find_element_by_xpath("//input[@dv='"+value+"']"))
		self.driver.find_element_by_xpath("//input[@dv='"+value+"']").click()

	@show_log
	def enter_acc(self, value):
		self.driver.find_element_by_xpath("//input[@class='clsTextWidget pt']").send_keys(value)

	@show_log
	def enter_dep(self, value):
		self.driver.find_element_by_xpath("//input[@class='clsTextWidget pt']").send_keys(value)

	@show_log
	def enter_sn(self, value):
		self.driver.find_element_by_xpath("//input[@class='clsTextWidget pt']").send_keys(value)

	@show_log
	def enter_workitem(self, value):
		self.driver.find_element_by_xpath("//input[@class='clsTextWidget pt']").send_keys(value)

	@show_log
	def run_report(self, value):
		self.driver.find_element_by_xpath("//button[starts-with(@name,'finish')]").click()

	def export_report(self, value):

		WebDriverWait(self.driver, WAITSEC).until(lambda x:x.find_element_by_xpath\
			("//span[@lid='HLExportReportResult_NS_']"))
		
		#get current windows handle id
		nowhandle = self.driver.current_window_handle

		#
		self.driver.find_element_by_xpath("//span[@lid='HLExportReportResult_NS_']").click()

		#
		allhandles = self.driver.window_handles
		logging.debug('print all of the handle: %s' %allhandles)

		for handle in allhandles:
			if handle != nowhandle:
				self.driver.switch_to_window(handle)
				WebDriverWait(self.driver, 30).until(lambda x:x.find_element_by_xpath("//td[@class='headerTitle']"))
				logging.debug('waiting for download file...')
				time.sleep(WAITSEC)