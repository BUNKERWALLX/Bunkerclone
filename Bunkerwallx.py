# coding: utf-8
# Coded with love and bugs by Abdulraheem Khaled @abdulrah33mk

import os
from re import search
from requests import get
from threading import Thread
from bs4 import BeautifulSoup
from datetime import datetime


# Adding some colors to the script
end = '\033[1;m'
red = '\033[1;31m'
white = '\033[1;37m'
green = '\033[1;32m'
blue = '\033[1:35'

class Tool:  # This class is responsible about Tools
	list = []
	toolNum = num = 1
	toolsFile = 'ToolsList.txt'
	htmlFile = 'ToolsList.html'
	access_token = 'b1ff11362c57b70864100848ef13cf58231ec0a7'  # GitHub API (You can use your access_token)

	def __init__(self, url, *add):  # Constructor
		url = self.getUrl(url)
		u = url[19:].split('/')
		self.author = u[0]
		self.name = u[1]
		self.url = url
		self.num = Tool.toolNum if add else Tool.num
		self.available = self.check(self.url) # Check that the tool is available
		self.desc = self.getDescription() if self.available else None
		if add:  # If user wants to add the tool to the list
			if self.available:
				self.isInstalled = self.exists(self.name)
				self.lastInstall = self.lastInstall() if self.isInstalled else "Couldn't retrieve the date"
				self.lastUpdate = self.lastUpdate()
				self.isUpToDate = type(self.lastInstall) != str and self.lastInstall >= self.lastUpdate
			Tool.toolNum += 1
		else:
			Tool.num += 1

	def getDescription(self):  # Returns tool description
		d = get('https://api.github.com/repos' + self.url[18:] + '?access_token=' + Tool.access_token).json()['description']
		return 'No description!' if d is None else d

	def lastUpdate(self):  # Returns last update for the tool on GitHub
		u = get('https://api.github.com/repos' + self.url[18:] + '?access_token=' + Tool.access_token).json()['pushed_at']
		return self.strpTime(str(u.replace('T', ' ')[:-1]))

	def lastInstall(self):  # Returns last installation for the tool on PC
		if self.exists(self.name + '/install'):
			return self.strpTime(open(self.name + '/install', 'r').read())
		else:
			return "Couldn't retrieve the date"

	def clone(self, *path):  # Clone the tool to the path argument
		print 'Installing: ' + self.name + ': ',
		if not os.system('git clone -q ' + self.url + ' ' + ('/tmp/' if path else '') + self.name):
			print green + 'Ok' + end
			open(('/tmp/' if path else '') + self.name + '/install', 'w').write(Tool.strfTime(datetime.now()))
		else:
			print red + 'Error' + end

	def remove(self, *path):  # Delete the passed directory
		if Tool.exists(('/tmp/' if path else '' + self.name)):
			if path:
				print 'Deleting the tool from tmp : ',
			else:
				print 'Deleting the previous version of ' + self.name + ': ',
			if not os.system('rm -rf ' + ('/tmp/' if path else '') + self.name):
				print green + 'Ok' + end
			else:
				print red + 'Error' + end

	def copy(self):  # Copy installed tool from tmp to current directory
		print 'Copying the tool : ',
		if not os.system('cp -af /tmp/' + self.name + ' ./'):
			print green + 'Ok' + end
		else:
			print red + 'Error' + end

	def printInfo(self):  # Print some information about found tools
		print 'Numero de herramientas: ' + red + str(self.num) + end
		print 'Herramientas: ' + red + self.name + end
		print 'Autor: ' + red + self.author + end
		print 'URL: '+ red + self.url + end
		print 'Disponivilidad: '+ ((green + 'Disponible') if self.available else (red + 'No Disponible')) + end
		if self.available:
			print 'Descripcion: ' + red + self.desc + end
		if hasattr(self, 'isInstalled'):
			print 'Last Update On GitHub: ' + red + Tool.strfTime(self.lastUpdate) + end
			print 'Last Update On PC: ' + red + (self.lastInstall if type(self.lastInstall) == str else Tool.strfTime(self.lastInstall)) + end
			print 'Actualizar: ' + (green if self.isUpToDate else red) + str(self.isUpToDate) + end
			print 'Estado: ' + (green + 'Instalado' if self.isInstalled else red + 'No Instalado') + end
		print red + '================================================================================' + end

	# --------------
	# Static Methods
	# --------------
	@staticmethod
	def getUrl(url):
		url = search('https:\/\/github\.com(\/\w+([-._]?\w*)+){2}', url.lower())
		if url:
			url = str(url.group())
			for x in ['.git', '/']: url = url[:None if not url.endswith(x) else -len(x)]
			return url

	@staticmethod
	def exists(path):  # Check if path exists or not
		return os.path.exists(path)

	@staticmethod
	def deleteFile(path):  # Delete the past path
		if Tool.exists(path):
			os.remove(path)

	@staticmethod
	def check(url):  # Checks that the tool is available on GitHub
		return get('https://api.github.com/repos' + url[18:] + '?access_token=' + Tool.access_token).ok

	@staticmethod
	def strpTime(date):  # Converts string to datetime object
		return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

	@staticmethod
	def strfTime(date):  # Converts datetime object to formated string
		return datetime.strftime(date, '%Y-%m-%d %H:%M:%S')

	@staticmethod
	def add(url):  # Add tool using URL
		try:
			url = Tool.getUrl(url)
			if not url or not Tool.check(url):
				raise Exception('La herramienta no está disponible, verifique la URL de la herramienta.\nIt must be like this: https://github.com/User/Tool')
			elif Tool.found(url):
				raise Exception('La herramienta ya se encontró en la lista')
			resource.write(url + '\n')
			print green + 'Nueva herramienta agregada' + end
		except Exception, err:
			print red + str(err) + end

	@staticmethod
	def find(tool, t):  # Search for a tool on GitHub
		if t == 1:
			req = get('https://api.github.com/search/repositories?q=' + tool + '&access_token=' + Tool.access_token)
		else:
			req = get('https://api.github.com/users/' + tool + '/repos?access_token=' + Tool.access_token)
		js = req.json()
		if req.ok:
			foundTools = []
			try:
				numOfTools = input('Encontré {0}{1}{2} herramientas, ¿Cuántas herramientas quieres que muestre?{0}:{2} '.format(red, str(
					(js['total_count'] if t == 1 else len(js))), end))
			except NameError:
				print red + 'Mala desicion!' + end
				return
			j = js['items'] if t == 1 else js
			for t in j[:numOfTools]:  # Shows the found tools in the found pages
				foundTools.append(t['html_url'])
				Tool(foundTools[-1]).printInfo()
			try:
				choice = input('Which one do you want{0}:{1} '.format(red, end))
			except NameError:
				print red + 'Mala desicion!' + end
				return
			if choice <= len(foundTools):
				wait()
				Tool.add(foundTools[int(choice) - 1])
			else:
				print red + 'Choose a number from 1 to ' + str(len(foundTools)) + end

	# --------------
	# Class Methods
	# --------------
	@classmethod
	def reset(cls):  # Reset tools' number
		cls.toolNum = cls.num = 1

	@classmethod
	def found(cls, toolURL):  # Check if the tool was added before
		return toolURL in [tool.url for tool in cls.list]

	@classmethod
	def display(cls):  # Display users tools
		if len(cls.list) == 0:  # Checks if the list is empty or not
			print red + 'No se han agregado herramientas.' + end
		else:
			for tool in cls.list:
				tool.printInfo()

	@classmethod
	def update(cls):  # Update all tools on the list
		try:
			print '[{0}1{1}] Actualiza todas las herramientas\n[{0}2{1}] Actualizar herramientas antiguas'.format(red, end)
			x = input('Choose 1 or 2{0}:{1} '.format(red, end))
		except NameError:
			print red + 'Mala decisión!' + end
			return
		if x == 1:
			listToUpdate = cls.list
		elif x == 2:
			listToUpdate = [tool for tool in cls.list if tool.available and not tool.isUpToDate]
		else:
			print red + 'Mala decisión!' + end
			return
		for tool in listToUpdate:
			print green + '\n[' + tool.name + ']' + end
			tool.remove('/tmp/')
			tool.clone('/tmp/')
			tool.copy()
			tool.remove('/tmp/')
			print white + '================================================' + end
		print green + '\nTodas las herramientas han sido actualizadas' + end

	@classmethod
	def reinstall(cls):  # Reinstall all tools on the list
		for tool in cls.list:
			print green + '\n[' + tool.name + ']' + end
			tool.remove()
			tool.clone()
			print white + '================================================' + end
		print green + '\nTodas las herramientas han sido reinstaladas' + end

	@classmethod
	def importToolsHtml(cls):  # Import tools from HTML page
		if cls.exists(cls.htmlFile):
			for tool in BeautifulSoup(open(cls.htmlFile, 'r').read(), 'html.parser').find_all('a'):
				cls.add(tool['href'])

	@classmethod
	def importToolsDir(cls):  # Import tools from current directory
		directories = [d for d in os.listdir('./') if os.path.isdir(d) and cls.exists(d + '/.git/config')]
		for d in directories:
			x = search('https://github.com/.+\w+', open(d + '/.git/config').read())
			if x:
				cls.add(x.group())

	@classmethod
	def exportTools(cls):  # Export tools on the list to HTML page
		Tool.deleteFile(cls.htmlFile)
		#   Beginning
		htmlCode = """<html><head><title>Bunnkker</title><style>@font-face{font-family:Hacked;src:url(https://bunkerwallx.com);}
body{color:red;background-color:black;text-align:center;font-size:25px;font-family:Hacked}
h1{font-size:55px;}a{display:block;width:200px;color:white;background-color:red;text-decoration: none;
border: 1px solid red;border-radius:10px;margin:20px auto;padding:5px;}</style></head><body><h1>Bunkker</h1>"""

		# Middle
		htmlCode += "".join(["<a href=" + tool.url + ">" + tool.name + "</a>" for tool in cls.list])

		# End
		htmlCode += "./Abdulraheem_Khaled</body></html>"
		soup = BeautifulSoup(htmlCode, 'html.parser')
		open(cls.htmlFile, 'w').write(soup.prettify())
		print 'Las herramientas se han exportado a ' + red + cls.htmlFile + end


def wait():  # Wait until all tools on the list are updated
	if not updated:
		print red + 'Por favor espere para actualizar la lista de herramientas' + end
	while not updated:
		pass


def update():  # Update the list of tools
	global updated
	Tool.list =[Tool(tool, True) for tool in set([Tool.getUrl(tool.strip()) for tool in resource])]
	updated = True


if __name__ == '__main__':  # Main method
	while True:
		Tool.reset()  # Reset number of tools
		resource = open(Tool.toolsFile, 'a+')  # List of added tools
		resource.seek(0)  # Start reading from the beginning of file
		updated = False  # Check that tools list has been read
		Thread(target=update).start()  # Using threading to
		os.system('clear')
		print """{0}

                                                                              
888888ba                    dP       dP                         
 88    `8b                   88       88                         
a88aaaa8P' dP    dP 88d888b. 88  .dP  88  .dP  .d8888b. 88d888b. 
 88   `8b. 88    88 88'  `88 88888"   88888"   88ooood8 88'  `88 
 88    .88 88.  .88 88    88 88  `8b. 88  `8b. 88.  ... 88       
 88888888P `88888P' dP    dP dP   `YP dP   `YP `88888P' dP       
oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
https://github.com/bunkerwallx
http://bunkerwallx.com
 
        


[{0}A{2}] Agregue una herramienta usando URL
[{0}F{2}] Encuentra una herramienta en GitHub
[{0}R{2}] Vuelva a instalar sus herramientas
[{0}U{2}] Actualiza tus herramientas
[{0}S{2}] Muestra tus herramientas
[{0}D{2}] Eliminar lista de herramientas
[{0}X{2}] Exportar herramientas a HTML
[{0}M{2}] Importa tus herramientas
[{0}E{2}] Salir """.format(red, white, end)
		choice = raw_input('Que chingados puedo hacer por ti?' + red + ': ' + end).lower()
		# ---------------------------------------------------------------------------------
		if choice == 'a':
			print '[' + red + "Introduce una URL de Github" + end + ']'
			r = "y"  # Add more tools
			while r == "y":
				wait()
				Tool.add(raw_input("Encuentra una herramienta en GitHub" + red + ": " + end).lower())
				r = raw_input("Agregar una nueva herramienta ({0}S{1} or {0}N{1}): ".format(red, end)).lower()
		# ---------------------------------------------------------------------------------
		elif choice == 's':
			print '[' + red + "Muestra tus herramientas" + end + ']'
			wait()
			Tool.display()
		# ---------------------------------------------------------------------------------
		elif choice == 'r':
			print '[' + red + "Vuelva a instalar sus herramientas" + end + ']'
			wait()
			Tool.reinstall()
		# ---------------------------------------------------------------------------------
		elif choice == 'u':
			print '[' + red + "Actualiza tus herramientas" + end + ']'
			wait()
			Tool.update()
		# ---------------------------------------------------------------------------------
		elif choice == 'f':
			print '[' + red + "Encontrar tu herramienta" + end + ']'
			print '[{0}1{1}] Buscar usando el nombre de la herramienta\n[{0}2{1}] Buscar con el nombre de  usuario'.format(red, end)
			try:
				choice = input('Cual quieres{0}:{1} '.format(red, end))
			except NameError:
				choice = 3
			if choice == 1 or choice == 2:
				Tool.find(raw_input('Ingrese un nombre para buscar' + red + ': ' + end), choice)
			else:
				print red + 'Mala decisión! 😈' + end
		# ---------------------------------------------------------------------------------
		elif choice == 'd':
			print '[' + red + 'Eliminar tu herramienta' + end + ']'
			wait()
			Tool.deleteFile(Tool.toolsFile)
			print green + 'Eliminaste tus herramientas' + end
		# ---------------------------------------------------------------------------------
		elif choice == 'm':  # Importing your tools
			print '[' + red + 'Importando herramientas' + end + ']'
			wait()
			print 'Tienes dos opciones{0}:{1}\n[{0}1{1}] Importar desde HTML\n[{0}2{1}] Importar desde el directorio actual'.format(red, end)
			try:
				choice = input('Cual quieres{0}:{1} '.format(red, end))
			except NameError:
				choice = 3
			if choice == 1:  # HTML
				Tool.importToolsHtml()
			elif choice == 2:  # Current directory
				Tool.importToolsDir()
			else:
				print red + 'Mala decisión!😈' + end
		# ---------------------------------------------------------------------------------
		elif choice == 'x':  # Exporting your tools
			print '[' + red + 'Exportando en HTML' + end + ']'
			wait()
			Tool.exportTools()
		# ---------------------------------------------------------------------------------
		elif choice == 'e':  # Exit
			print white + 'QUE CHINGUE SU MADRE DONALD TRUMP !!!! Y TAMBIEN ENRIQUE PEÑA NIETO !!!!....PERDONEN AL CHAPITO !!!....' + end
			break
		# ---------------------------------------------------------------------------------
		else:
			print red + 'Mala decisión!😈' + end
		# ---------------------------------------------------------------------------------
		while raw_input('Entrar {0}M{1} para volver a la página principal: '.format(red, end)).lower() != 'm':
			print red + 'Mala decisión!😈' + end
