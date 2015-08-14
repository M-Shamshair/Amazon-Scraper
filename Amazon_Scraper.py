#Note: This script includes auto bypass method for verfication account if it logins from a new area.
# email: king.ali.1331@gmail.com
"""
Place user text file in same directory
Usage: python amazon_scraper.py 
after run program input user text file which contain account like >> email:password
enter output txt file name after execution
"""
import mechanize
from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup
from optparse import OptionParser
from time import sleep
import datetime
import os
import re
import sys

order_no_id = open('order_ids.txt', 'w+')
not_login = open('not_login.txt','w+')
result = open ('result.txt', 'w+')

def banner():
	print '======================================================'
	print '|		Amazon Multi-Account Order Scraper   |'
	print '======================================================'
	print '| Purpose: To keep the client order history records  |'
	print '| Date:	  24-Feb-2015				     |'	
	print '| Author:  Ali Ahmer aka King Ali		     |'
	print '| email:	  king.ali.1331@gmail.com	     |'
	print '| Note:	  Don,t use for illegal purpose		     |'
	print '======================================================'

def account_info(address_book_info):
	address_book = open('billing_info.txt', 'w+')
	soup = BeautifulSoup(address_book_info)
	print 'Getting Billing Informations...\r\n'
	for order in soup.findAll('ul', {'class': 'displayAddressUL'}):
		for items in order.findAll('li', {'class': 'displayAddressLI displayAddressAddressLine1'}):
			for add1 in items:
				address_book.write(''.join(add1+'\r\n'))		
		for items in order.findAll('li', {'class': 'displayAddressLI displayAddressAddressLine2'}):
			for add2 in items:
				address_book.write(''.join(add2+'\r\n'))
		for items in order.findAll('li', {'class': 'displayAddressLI displayAddressCityStateOrRegionPostalCode'}):
			for s_r_p in items:
				address_book.write(''.join(s_r_p+'\r\n'))
		for items in order.findAll('li', {'class': 'displayAddressLI displayAddressCountryName'}):
			for c_n in items:
				address_book.write(''.join(c_n+'\r\n'))
		for items in order.findAll('li', {'class': 'displayAddressLI displayAddressPhoneNumber'}):
			for p_n in items:
				address_book.write(''.join(p_n+'\r\n'))
	address_book.close()
	result.write('\r\nBilling Information: \r\n')
	result.write('===================\r\n')
	cleaning_format('billing_info.txt')
	result.write('-----------------------------------------------------\r\n')
	
	
def orders_no_details_checking(html):
	product_details = open('product_details.txt', 'w+')
	buyer_details = open('buyer_details.txt', 'w+')
	date_details = open ('date_details.txt', 'w+')
	soup = BeautifulSoup(html)
	print 'Geting Product Details...\r\n'
	for order in soup.findAll('div', {'class': 'a-fixed-left-grid-col a-col-right'}):
		for items in order.findAll('div', {'class': 'a-row'}):
			for title in items.findAll('a', {'class': 'a-link-normal'}):
				for title_text in title:
					product_details.write(''.join(title_text))
			
			for description in items.findAll('span', {'class': 'a-size-small'}):
				for description_text in description:
					product_details.write(''.join(description_text))
					
			for sold_by in items.findAll('span', {'class': 'a-size-small a-color-secondary'}):
				for sold_by_text in sold_by:
					product_details.write(''.join(sold_by_text))
			
			for price in items.findAll('span', {'class': 'a-size-small a-color-price'}):
				for price_text in price:
					product_details.write(''.join(price_text))
			
			for condition in items.findAll('span', {'class': 'a-color-secondary'}):
				for condition_text in condition:
					product_details.write(''.join(condition_text))
	
	print 'Getting Buyer Details....\r\n'
	for order in soup.findAll('div', {'class': 'displayAddressDiv'}):
		for items in order.findAll('ul', {'class': 'displayAddressUL'}):
			for name in items.findAll('li', {'class': 'displayAddressLI displayAddressFullName'}):
				for name_text in name:
					buyer_details.write(''.join(name_text+'\r\n'))
			
			for address in items.findAll('li', {'class': 'displayAddressLI displayAddressAddressLine1'}):
				for address_text in address:
					buyer_details.write(''.join(address_text+'\r\n'))
			
			for city_state_postal_code in items.findAll('li', {'class': 'displayAddressLI displayAddressCityStateOrRegionPostalCode'}):
				for city_state_postal_code_text in city_state_postal_code:
					buyer_details.write(''.join(city_state_postal_code_text+'\r\n'))
			
			for country in items.findAll('li', {'class': 'displayAddressLI displayAddressCountryName'}):
				for country_text in country:
					buyer_details.write(''.join(country_text+'\r\n'))
					
	print 'Getting date information...\r\n'
	for order in soup.findAll('div', {'class': 'a-row a-spacing-none'}):
		for items in order.findAll('span', {'class': 'order-date-invoice-item'}):
			for date_text in items:
				date_details.write(''.join(str(date_text)))
	
	product_details.close()
	buyer_details.close()
	date_details.close()

def cleaning_format(txt_file):
	with open(txt_file, 'r+') as fff:
		for line in fff:
			cleanedLine = line.strip()
			if cleanedLine: #is not empty
				result.write(cleanedLine+'\r\n')
	fff.close()
	
def Getting_orderID(htmls):
	print 'Tracking Order No.s...\r\n'
	soup = BeautifulSoup(htmls)
	for order in soup.findAll("div", {"class": "a-row a-size-mini"}):
		for item in order.findAll("span", {"class": "a-color-secondary value"}):
			for idd in item:
				order_no_id.write(''.join(idd))
##########################Main_Code_Starting_from_here######################################
if __name__ == '__main__':
	banner()
	sleep(1)
	print '\r\n\r\n'
	account_file = raw_input('Enter account file e.g. emails.txt: ')
	try:
		f1 = open(account_file).readlines()
	except:
		print '(!) Error in opening file. Please check file name with extension correctly.'
		sys.exit(1)
	x1 = str(len(f1))
	print 'File Contains '+x1+' Entries.\r\n' 
	firstyear = raw_input('Enter Starting Year to start e.g. 2009: ')
	with open(account_file, 'r+') as ff:
		for words in ff:
			print 'checking...'+words+'\r\n'
			result.write('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\r\n')
			result.write('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\r\n')
			result.write(words+':::::::::::::::::::::::::: \r\n')
			m = re.search(':', words)
			usr = words[:m.start()]
			pwd = words[m.end():]
			pwd = pwd.strip()
			br = mechanize.Browser()
			br.set_handle_robots(False)
			br.addheaders = [("User-agent", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36"),('Accept', 'text/html, application/xml, */*')]
			print 'Attempt to Logging in...'
			resp = br.open("https://www.amazon.com/ap/signin?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&pageId=mas_dev_portal2&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.assoc_handle=mas_dev_portal&openid.return_to=https%3A%2F%2Fdeveloper.amazon.com%2Fap_login.html&language=en_US&openid.pape.max_auth_age=1")
			resp.set_data(re.sub('<!DOCTYPE(.*)>', '', resp.get_data()))      
			br.set_response(resp)
			br.select_form(nr=0)
			br["email"] = usr
			br["password"] = pwd
			logged_in = br.submit()
			xx = logged_in.read()
			error_str1 = "Important Message!"
			error_str2 = "There was a problem with your request"
			if error_str1 in xx:
				print error_str1
				print '\r\n'+'Please Check Account email and password...!\r\n'
				not_login.write(words+'\r\n')
				print 'The account which is not login will save in not_login.txt in same directory. \r\n'
			if error_str2 in logged_in.read():
				print error_str2
				print '\r\n'+'Please Check Account email and password...!\r\n'
				not_login.write(words+'\r\n')
				print 'The account which is not login will save in not_login.txt in same directory. \r\n'
			else:
				print "Successfully Login...!\r\n"
				sleep(2)
				billing_details = br.open("https://www.amazon.com/gp/css/account/address/view.html?ie=UTF8&ref_=ya_manage_address_book_t1")
				billing_details_info = billing_details.read()
				account_info(billing_details_info)
				sleep(2)
				for year in range(int(firstyear),  datetime.datetime.now().year):
					orders_html = br.open("https://www.amazon.com/gp/css/history/orders/view.html?orderFilter=year-%s&startAtIndex=1000" % year)
					print 'Getting Order No.s of '+str(year)+'\r\n'
					orders_details = orders_html.read()
					Getting_orderID(orders_details)
				order_no_id.close()
				orderss = open ('orders.txt', 'w+')
				with open('order_ids.txt', 'r+') as fff:
					for line in fff:
						cleanedLine = line.strip()
						if cleanedLine: #is not empty
							orderss.write(cleanedLine+'\r\n')
				orderss.close()
				fff.close()
				f11 = open('orders.txt').readlines()
				x1 = str(len(f11))
				print 'Total Orders is: '+x1+'\r\n'
				result.write('Total Orders: '+x1+' \r\n')
				print 'Getting Order Details....\r\n'
				ff22 = open('orders.txt', 'r+')
				sleep(2)
				for order_details in ff22:
					print 'Getting Details of Order No. '+str(order_details)+'\r\n'
					order_link = br.open("https://www.amazon.com/gp/your-account/order-details/ref=oh_aui_or_o00_?ie=UTF8&orderID=%s" % order_details)
					order_data = order_link.read()
					orders_no_details_checking(order_data)
					result.write('\r\nProduct Details: \r\n')
					result.write('================\r\n')
					cleaning_format('product_details.txt')
					result.write('-----------------------------------------------------\r\n')
					result.write('\r\nBuyer Details: \r\n')
					result.write('==============\r\n')
					cleaning_format('buyer_details.txt')
					result.write('-----------------------------------------------------\r\n')
					result.write('\r\nDate and Order No.: \r\n')
					result.write('===================\r\n')
					cleaning_format('date_details.txt')
					result.write('-----------------------------------------------------\r\n')
				ff22.close()
			
	print 'Order History of All accounts have been saved in result.txt file...!\r\n'
	print 'Check not_login.txt for invalid login Attempts. \r\n'
	try:
		result.close()
		order_no_id.close()
		not_login.close()
	except:
		pass
	try:
		os.remove('billing_info.txt')
		os.remove('product_details.txt')
		os.remove('buyer_details.txt')
		os.remove('date_details.txt')
	except:
		pass
	try:
		os.remove('order_ids.txt')
		os.remove('orders.txt')
	except:
		pass
	print './ done'