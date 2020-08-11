#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

lista = []
empresa = ''

def entrada():
	global empresa
	empresa = input("Informe o Nome da Empresa que deseja pesquisar:")
	if len(empresa.lstrip()) <= 2:
		print("Informe um Nome com mais de 2 caracteres")
		entrada()


def acessa_site():
	driver = webdriver.Chrome()
	driver.get('https://www.jucesponline.sp.gov.br/')
	return driver

def pesquisa(driver):
	pesquisa = driver.find_element_by_id('ctl00_cphContent_frmBuscaSimples_txtPalavraChave')
	pesquisa.send_keys(empresa)
	pesquisa.send_keys(Keys.ENTER)

def preenche_captcha(driver):
	try:
		time.sleep(1)
		captcha = driver.find_element_by_name('ctl00$cphContent$gdvResultadoBusca$CaptchaControl1')
		captcha_value = input("Digite o Captcha apresentado no browser: (Caso o Captcha tenha sido preenchido no browser digite ENTER)")
		captcha.send_keys(captcha_value)
		captcha.send_keys(Keys.ENTER)
		time.sleep(1)
		try:
			driver.find_element_by_name('ctl00$cphContent$gdvResultadoBusca$CaptchaControl1')
			preenche_captcha(driver)
		except:
			return 1
	except:
		return 1

def coleta_informacoes(driver):
	try:
		#time.sleep(2)
		aguarda_id(driver,"ctl00_cphContent_gdvResultadoBusca_gdvContent")
		tabela = driver.find_element_by_id('ctl00_cphContent_gdvResultadoBusca_gdvContent')
		table_rows = tabela.find_elements_by_css_selector('tr')
		for tr in range(1,len(table_rows)):
			empresa = table_rows[tr].find_elements_by_css_selector('td')[1].text
			nire = table_rows[tr].find_elements_by_css_selector('td')[0].text.strip()
			municipio = table_rows[tr].find_elements_by_css_selector('td')[2].text
			lista.append({"Empresa": empresa, "NIRE": nire, "Município": municipio})
	except:
		return 1

def aguarda_id(driver,element_id):
	wait = WebDriverWait(driver, 10)
	wait.until(expected_conditions.presence_of_element_located((By.ID, element_id)))

entrada()
driver = acessa_site()
pesquisa(driver)
preenche_captcha(driver)
coleta_informacoes(driver)
print(lista)

input("Digite Enter para fechar o Browser")
driver.quit()