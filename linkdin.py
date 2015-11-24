import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
class LinkDinScrap():


	def __init__(self):
		lenght_of_args = len(sys.argv)
		arugement_list = sys.argv
		self.startUrl = arugement_list[1]
		self.driver = webdriver.Firefox()

		self.callMethods()


	def callMethods(self):
		self.declareXpaths()
		self.openUrl()
		self.fetchData()
		self.writeToFile()
		self.driver.close()

	def fetchData(self):
		self.fetchBasicInfo()
		self.fetchMainData()
		self.fetchEducation()
		self.fetchExperience()

	def declareXpaths(self):
		self.Name = "//h1[@id='name']"
		self.headline = "//p[@class='headline title']"
		self.locality = "//span[@class='locality']"
		self.field = "//dd[@class='descriptor']"
		self.currentCompany = "//span[@class='org']/a"
		self.previosComapnies = "//table[@class='extra-info']/tbody/tr[2]//a"
		self.education = "//table[@class='extra-info']/tbody/tr[3]//a"
		self.summary = "//section[@id='summary']/div/p"
		self.connections = "//div[@class='member-connections']/strong"

		self.skills = "//li[@class='skill' or @class='skill extra']/a/span"
		self.languages = "//li[@class='language']//h4"

		self.EducationMain = "//ul[@class='schools']/li"
		self.subEducationUniName = "//header/h4/a"
		self.subEducationCourseName = "//header/h5[@class='item-subtitle']"
		self.subEducationYears = "//div/span/time"

	def openUrl(self):
		print "Opening Webpage -> ",self.startUrl
		self.driver.get(self.startUrl)
		print "Web Page Open Completed"

	def filterString(self,stringf):
		stringf = str(stringf.encode('ascii', 'ignore'))
		stringf = stringf.replace(',',' ')
		return stringf

	def fetchBasicInfo(self):
		driver = self.driver
		print "************************************************************"
		print "Extracting Name..."
		self.nameOfUser = self.filterString(driver.find_element_by_xpath(self.Name).text)

		print "Name Fetched ->",self.nameOfUser

		print "************************************************************"

		print "Extracting headline...."
		self.userHeadline = self.filterString(driver.find_element_by_xpath(self.headline).text)
		print "Headline Fetched -> ",self.userHeadline


		print "************************************************************"


		print "Extracting Locality...."
		self.userLocality = self.filterString(driver.find_element_by_xpath(self.locality).text)
		print "Locality Fetched -> ",self.userLocality

		print "************************************************************"

		print "Extracting Field...."
		self.userField = self.filterString(driver.find_element_by_xpath(self.field).text)
		print "Field Fetched -> ",self.userField

		print "************************************************************"

		print "Extracting Current Company..."
		self.userCurrentCompany = self.filterString(driver.find_element_by_xpath(self.currentCompany).text)
		print "Current Company Fetched -> ",self.userCurrentCompany

		print "************************************************************"

		print "Extracting Previous Company..."
		self.userPreviousCompanyList = driver.find_elements_by_xpath(self.previosComapnies)
		self.userPreviousCompany = ""
		for content in self.userPreviousCompanyList:
			self.userPreviousCompany = "%s | %s"%(self.userPreviousCompany,self.filterString(content.text))
		print "Prevois Company Fetched  ->",self.userPreviousCompany

		print "************************************************************"

		print "Extracting User Main Education...."
		self.userMainEducation = self.filterString(driver.find_element_by_xpath(self.education).text)
		print "User Main Education Fetched -> ",self.userMainEducation

		print "************************************************************"


		print "Summary of User ....."
		self.userSummary = self.filterString(driver.find_element_by_xpath(self.summary).text)
		print "User Summary Fetched -> ",self.userSummary
		print "************************************************************"
		print "User Total Connections...."
		self.userConnections = self.filterString(driver.find_element_by_xpath(self.connections).text)
		print "User Total Connections Fetched -> ",self.userConnections

	def fetchMainData(self):
		driver = self.driver
		try:driver.find_element_by_xpath("//li[@class='skill see-more']/label").click()
		except:pass
		time.sleep(2)
		print "Extracting User Skills..."
		self.userskills = driver.find_elements_by_xpath(self.skills)
		self.userskillsStr = ""
		for content in self.userskills:
			self.userskillsStr = "%s | %s"%(self.userskillsStr,self.filterString(content.text))
		print "User skilss Fetched  ->",self.userskillsStr
		

		print "************************************************************"

		print "Languages Knows"
		self.languagesKnow = driver.find_elements_by_xpath(self.languages)
		self.userLanguagesKnow = ""
		for content in self.languagesKnow:
			self.userLanguagesKnow = "%s | %s"%(self.userLanguagesKnow,self.filterString(content.text))

		print "User Languages Know Fetched -> ",self.userLanguagesKnow
		print "************************************************************"

	def fetchEducation(self):
		driver = self.driver

		print "************************************************************"
		print "Fetching School Information  ...."
		listOfEducations = driver.find_elements_by_xpath(self.EducationMain)
		self.educationList = []
		for educationContent in listOfEducations:
			educationContent = self.filterString(educationContent.text)
			educationContent = educationContent.split("\n")
			makeDict = { 'school':educationContent[0],'course':educationContent[1],'year':educationContent[2] }
			self.educationList.append(makeDict)
		print "School Course Information Fetched -> ",self.educationList
		self.educationList = str(json.dumps(self.educationList))
		print "************************************************************"



	def fetchExperience(self):
		driver = self.driver
		print "************************************************************"
		print "Fetching Experience ....."
		listOfExpericne = driver.find_elements_by_xpath("//li[@class='position']")
		self.experinceList = []
		for experienceContent in listOfExpericne:
			experienceContent =  self.filterString(experienceContent.text)
			experienceContent = experienceContent.split("\n")
			makeDict = {'position':experienceContent[0],'company':experienceContent[1],'experince':experienceContent[2]}
			self.experinceList.append(makeDict)
		print "Experince Information Fetched ->",self.experinceList
		self.experinceList = str(json.dumps(self.experinceList))
		print "*************************************************************"


	def writeToFile(self):
		fileNamePrefix = self.nameOfUser
		fileNamePrefix = fileNamePrefix.replace(" ","_")
		fileName = "%s.csv"%(fileNamePrefix)
		f = open(fileName,"w")
		fields = ['Name','headline','Locality','Field','CurrentCompany','PreviousCompany','Main Education','Summary','Total Connections','User Skills','Language Speaks','Education','Experince']
		for tabName in fields:
			f.write(tabName)
			f.write(',')
		f.write('\n')
		f.write(self.nameOfUser)
		f.write(',')
		f.write(self.userHeadline)
		f.write(',')
		f.write(self.userLocality)
		f.write(',')
		f.write(self.userField)
		f.write(',')
		f.write(self.userCurrentCompany)
		f.write(',')
		f.write(self.userPreviousCompany)
		f.write(',')
		f.write(self.userMainEducation)
		f.write(',')
		f.write(self.userSummary)
		f.write(',')
		f.write(self.userConnections)
		f.write(',')
		f.write(self.userskillsStr)
		f.write(',')
		f.write(self.userLanguagesKnow)
		f.write(',')
		f.write(self.educationList)
		f.write(',')
		f.write(self.experinceList)
		f.close()



if __name__ == '__main__':
	obj = LinkDinScrap()
