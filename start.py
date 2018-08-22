# encoding=utf8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import *
import requests
import threading
import time
import subprocess, signal
import os
import sys

i = 0

mainThread = None
toURL = ""
toProxy = []
toChat = ""
toPause = 0
toScreen = 0
toThreads = 10
threads = []

# def clear():
# 	p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
# 	out, err = p.communicate()

# 	for line in out.splitlines():
# 		if 'firefox' in line:
# 			pid = int(line.split(None, 1)[0])
# 			os.kill(pid, signal.SIGKILL)

def run2(proxyList):
	global status_now, toURL, toPause, toScreen
	if toURL.startswith("http://") or toURL.startswith("https://"):
		pass
	else:
		toURL = "http://" + toURL
	for proxy in proxyList:
		print("Proxy: " + proxy)
		proxyIP = proxy.split(":")[0]
		proxyPort = int(proxy.split(":")[1])
		getScreenshot(url = toURL, proxyIP = proxyIP, proxyPort = proxyPort, pause = toPause, toScreen = toScreen)

def run():
	global status_now, toURL, toPause, toProxy, toScreen, toThreads, threads
	def divide(lst,n):
		return [lst[i::n] for i in range(n)]
	proxies = divide(toProxy, toThreads)
	for proxyList in proxies:
		threads.append(threading.Thread(target = run2, args = (proxyList,)).start())

def getScreenshot(url, proxyIP = None, proxyPort = None, pause = 15, toScreen = False):
	global i
	opts = webdriver.FirefoxOptions()
	opts.add_argument("--headless")
	profile = webdriver.FirefoxProfile()

	# proxy = proxyIP + ":" + str(proxyPort)
	if proxyIP != None:
		profile.set_preference("network.socksProxy", proxyIP + ":" + str(proxyPort))
		profile.set_preference("network.proxy.type", 1)
		profile.set_preference("network.proxy.socks", proxyIP)
		profile.set_preference("network.proxy.socks_port", proxyPort)
		profile.set_preference("network.proxy.socks_version", 5)
	profile.update_preferences()

	# proxy = Proxy({
	# 	'socksProxy': proxy,
	# 	'proxyType': ProxyType.MANUAL,
		# 'socks': proxyIP,
		# 'socks_port': proxyPort,
		# 'socks_version': 5
	# })

	try:
		driver = webdriver.Firefox(firefox_profile=profile,
								   firefox_options=opts,
								   executable_path='geckodriver',
								   log_path='geckodriver.log')
	except Exception as e:
		print(e)
		print("Не удалось инициализировать браузер")
		return
	except KeyboardInterrupt as e:
		sys.exit(0)

	driver.implicitly_wait(pause) # seconds
	print("Жду загрузки. " + str(pause) + " сек.")
	print("Открывается url " + url)
	try:
		driver.get(url)
	except Exception as e:
		print(e)
		print("Ошибка открытия страницы. ")
		try:
			driver.close()
			driver.quit()
		except Exception as e:
			return
		finally:
			return
	except KeyboardInterrupt as e:
		sys.exit(0)
	time.sleep(pause)
	try:
		driver.close()
	except Exception as e:
		pass
	except KeyboardInterrupt as e:
		sys.exit(0)

	try:
		driver.quit()
	except Exception as e:
		pass
	except KeyboardInterrupt as e:
		sys.exit(0)

	i = i + 1
	print("Сделано. Всего:" + str(i))

def clearProxyFile():
	open('checked-proxy', 'w').close()

if __name__ == '__main__':
	mainThread = None
	toURL = "https://goo.gl/ZTbT6Z"
	toPause = 20
	toThreads = 8
	prox = [line.replace("\r","").strip('\n') for line in open('checked-proxy.txt')]
	errorsProxy = 0
	for each in prox:
		x = each
		x = x.replace("1", "N").replace("2", "N").replace("3", "N")
		x = x.replace("4", "N").replace("5", "N").replace("6", "N")
		x = x.replace("7", "N").replace("8", "N").replace("9", "N")
		x = x.replace("0", "N").replace("NN", "N").replace("NN", "N").replace("NN", "N")
		if x == "N.N.N.N:N" and each != "N.N.N.N:N":
			toProxy.append(each)
		else:
			errorsProxy = errorsProxy + 1
	clearProxyFile()
	print("Загружено прокси: " + str(len(toProxy)) +". Ошибки в прокси: "+ str(errorsProxy))
	run()