#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

lista = []
nire = ''

def entrada():
	global nire
	nire = input("Informe o Nire da Empresa que deseja pesquisar(11 digitos):")
	if len(nire.lstrip()) != 11 or not nire.isnumeric():
		print("O Nire informado não possui 11 digitos ou não possui apenas digitos")
		entrada()

def acessa_site():
	driver = webdriver.Chrome()
	driver.get('https://www.jucesponline.sp.gov.br/')
	return driver

def pesquisa(driver):
	pesquisa = driver.find_element_by_id('ctl00_cphContent_frmBuscaSimples_txtPalavraChave')
	pesquisa.send_keys(nire)
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
	info = {'Empresa': 2,
		'tipo de empresa': 5,
		'início de atividade': 7,
		'cnpj': 8,
		'nire': 3,
		'data da constituição': 6,
		'inscrição estadual': 9,
		'objeto': 10,
		'capital': 11,
		'logradouro': 12,
		'número': 13,
		'bairro': 14,
		'complemento': 15,
		'município': 16,
		'cep': 17,
		'uf': 18}

	for key, value in info.items():
		try:
			aguarda_id(driver,"dados")
			lista.append({key: driver.find_elements_by_xpath("//*[contains(@id,'ctl00_cphContent_frmPreVisualiza')]")[value].text})
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


