#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import Image
import os
# level img : 560 * 400


#-----------------------------------------------------------------------
# ImageHandler
#-----------------------------------------------------------------------
class ImageHandler(object):
	def __init__(self, filename="auto.png"):
		self.setFile(filename)
	
	def setFile(self, filename):
		self.filename = filename
		self.img = None
		if self.filename:
			self.img = Image.open(self.filename)
	
	#-------------------------------------------------------------------
	# get image info
	#-------------------------------------------------------------------
	def get_width(self):
		if self.img:
			return self.get_size()[0]
		return None
		
	def get_height(self):
		if self.img:
			return self.get_size()[1]
		return None
		
			
	def get_size(self):
		if self.img:
			return self.img.size
		return None
			
	def get_format(self):
		if self.img:
			return self.img.format
		return None
		
	def get_mode(self):
		if self.img:
			return self.img.mode
		return None
	
	def get_pixel(self, x, y):
		if self.img:
			return self.img.getpixel((x, y))
		return None
	
	def get_bounds(self):
		"""returns x, y, w, and h of the visible part of the image"""
		if not self.img:return None
		xmin = 560
		xmax = 0
		ymin = 400
		ymax = 0
		for x in range(self.get_size()[0]):
			for y in range(self.get_size()[1]):
				pixel = self.get_pixel(x, y)
				if pixel[3]>0:
					if x>xmax:xmax = x
					if x<xmin:xmin = x
					if y>ymax:ymax = y
					if y<ymin:ymin = y
		return (xmin, ymin, xmax-xmin+1, ymax-ymin+1)
	#-------------------------------------------------------------------
	# image manipulation
	#-------------------------------------------------------------------
	def subsurface(self, x, y, w, h):
		"""returns a PIL image"""
		return self.img.crop((x, y, x+w, y+h))
	
	def makePygameSurface(self):
		"""returns image as a pygame surface"""
		if not self.img:return
		return pygame.image.fromstring(self.img.tostring(), (560,400), "RGB")
		
	def show(self):
		"""uses pygame to display the image"""
		if not self.img:return
		screen = pygame.display.set_mode((800,600))
		screen.blit(self.makePygameSurface(), (0,0))
		pygame.display.flip()
		
	def crop(self, x, y, w, h):
		self.img = self.subsurface(x, y, w, h)
		
	def save(self, filename):
		self.img.save(filename)
	
	
	
#-----------------------------------------------------------------------
# some hard data we'll need soon
#-----------------------------------------------------------------------	
povOffsetDic = {}

povOffsetDic["02"] = (145, 95, 270, 186)
povOffsetDic["03"] = (183, 125, 194, 133)
povOffsetDic["13"] = (377, 125, 183, 133)
povOffsetDic["12"] = (415, 95, 145, 186)
povOffsetDic["12side"] = (377, 96, 38, 185)
povOffsetDic["10side"] = (505, 0, 55, 368)
povOffsetDic["11side"] = (415, 26, 90, 309)
povOffsetDic["01"] = (55, 25, 450, 310)
povOffsetDic["11"] = (505, 25, 55, 310)
povOffsetDic["23side"] = (505, 128, 55, 128)
povOffsetDic["13side"] = (355, 125, 22, 133)


for k, v in povOffsetDic.items():
	# building left version of facing and side tiles
	if int(k[0])!=0:
		newcode = "-" + k
		newx = 560-v[0]-v[2]
		povOffsetDic[newcode] = (newx, v[1], v[2], v[3])

povOffsetList = [
	"23side", "-23side", "13side", "-13side", "13", "-13", "03",
	"12side", "-12side", "12", "-12", "02", "11side", "-11side", "11", "-11", "01", "10side", "-10side"
]

#-----------------------------------------------------------------------
# PovrayHandler
#-----------------------------------------------------------------------
class PovrayHandler(object):
	def __init__(self, povBaseFile="dmScene.pov", iniBaseFile=None):
		self.setPovBase(povBaseFile)
		self.clear()
		self.light = 2.0
		self.fogDistance = 0.0
		self.coordRectDic = {}
		
	def clear(self):
		self.povData = ""
		
		
	def add(self, cmd):
		self.povData = self.povData + cmd
	
	def setPovBase(self, filename):
		#self.povBaseFile = filename
		#self.povBase = open(filename).read()
		self.povBase = "#include \"dmScene.pov\"\n\n"
		
	def makePovFile(self, name='test.pov'):
		content = self.povBase + self.povData
		f = open(name, "w")
		f.write(content)
		f.close()
		print("Saved pov file to %s" % (name))
		
	#-------------------------------------------------------------------
	# generic scene settings
	#-------------------------------------------------------------------
	
	def setLight(self, n):
		self.light = n
		
	def setFogDistance(self, n):
		self.fogDistance = n
		
	def addBg(self):
		cmd = "makeBg()\n"
		self.add(cmd)
		
	def addCamera(self, eyeY=1.2):
		cmd = "makeCamera(%s)\n" % (eyeY)
		self.add(cmd)
		
	def addLight(self, light = None):
		if not light:
			light = self.light
		cmd = "makeLight(" + str(light) + ")\n"
		self.add(cmd)
		
	def setLight(self, light):
		self.light = light
		
	def addFog(self, fog = None):
		if not fog:
			fog = self.fogDistance
		cmd = "makeFog(" + str(fog) + ")\n"
		self.add(cmd)
		
	#-------------------------------------------------------------------
	# scene elements
	#-------------------------------------------------------------------
		
	def addBox(self, x, y):
		cmd = "makeBox(" + str(x) + ", " + str(y) + ")\n"
		self.add(cmd)
		
	def addFace(self, x, y):
		cmd = "makeFace(" + str(x) + ", " + str(y) + ")\n"
		self.add(cmd)
		
	def addSide(self, x, y):
		cmd = "makeSide(" + str(x) + ", " + str(y) + ")\n"
		self.add(cmd)
		
	def addObjectFace(self, name = "aritest", objectPath="aritest.txt", x=0.0, y=1.0):
		name = "aritest"
		if objectPath:
			cmd = "#declare " + name + " = #include \"" + objectPath + "\";\n"
		cmd += "object { " + name + " translate <BOX_SIZE*" + str(x)+ ", 0, BOX_SIZE*" + str(y) + "+BOX_SIZE/2> }\n"
		self.add(cmd)
		
	def addObjectSide(self, name = "aritest", objectPath="aritest.txt", x=0.0, y=1.0):
		name = "aritest"
		if objectPath:
			cmd = "#declare " + name + " = #include \"" + objectPath + "\";\n"
		cmd += "object { " + name + " rotate <0,90,0> translate <BOX_SIZE*" + str(x)+ "+2, 0, BOX_SIZE*" + str(y) + "+BOX_SIZE> }\n"
		self.add(cmd)
		
	def addObjectBoxFace(self, name = "aritest", objectPath="aritest.txt", x=0.0, y=1.0):
		name = "aritest"
		if objectPath:
			cmd = "#declare " + name + " = #include \"" + objectPath + "\";\n"
		cmd += "object { " + name + " translate <BOX_SIZE*" + str(x)+ "+2, 0, BOX_SIZE*" + str(y) + "+BOX_SIZE> }\n"
		self.add(cmd)
		
	def addObjectBoxSide(self, name = "aritest", objectPath="aritest.txt", x=0.0, y=1.0):
		name = "aritest"
		if objectPath:
			cmd = "#declare " + name + " = #include \"" + objectPath + "\";\n"
		cmd += "object { " + name + " rotate <0,90,0> translate <BOX_SIZE*" + str(x)+ "+2, 0, BOX_SIZE*" + str(y) + "+BOX_SIZE> }\n"
		self.add(cmd)
		
		
	#-------------------------------------------------------------------
	# render
	#-------------------------------------------------------------------
	def render(self, filename="auto.png", pause = False):
		if ".png" not in filename:
			filename = filename + ".png"
		
		self.makePovFile('test.pov')
		cmd = "povray test.pov +W560 +H400 +O%s +UA -V -GA +WL0 " % (filename)
		if pause:
			cmd += "+P"
		os.system(cmd)

	
	#-------------------------------------------------------------------
	# mass rendering
	#-------------------------------------------------------------------
	def buildTileFaceWall(self, coords):
		X, Y = coords[0], coords[1]
		self.clear()
		self.addCamera()
		self.setLight(2.0-(Y/4.0))
		self.addLight(self.light)
		self.addFog(self.fogDistance)
		self.addFace(-X,Y)
		self.render("auto.png")
		img = ImageHandler("auto.png")
		bounds = img.get_bounds()
		if bounds[2]>0:
			x, y, w, h = bounds[0], bounds[1], bounds[2], bounds[3]
			code = str(X) + str(Y)
			self.coordRectDic[code] = (x, y, w, h)
			print "Found bounds : %s %s %s %s" % (x, y, w, h)
			img.img = img.subsurface(x, y, w, h)
			name = str(X) + str(Y) + ".png"
			img.save(name)
		
	def buildTileSideWall(self, coords):
		X, Y = coords[0], coords[1]
		if X == 0:
			return
		self.clear()
		self.addCamera()
		self.setLight(2.0-(Y/4.0))
		self.addLight(self.light)
		self.addFog(self.fogDistance)
		self.addSide(-X,Y)
		self.render("auto.png")
		img = ImageHandler("auto.png")
		bounds = img.get_bounds()
		if bounds[2]>0:
			x, y, w, h = bounds[0], bounds[1], bounds[2], bounds[3]
			code = str(X) + str(Y) + "side"
			self.coordRectDic[code] = (x, y, w, h)
			img.img = img.subsurface(x, y, w, h)
			name = str(X) + str(Y) + "side.png"
			img.save(name)
	
	def buildSetWall(self):
		"""builds the complete set of images for walls"""
		for tile in boxCoordList:
			self.buildTileFaceWall(tile)
			self.buildTileSideWall(tile)
			print "built tile %s" % (str(tile))
	
	def buildSetDoorWoodClosed(self):
		for tile in boxCoordList:
			X, Y = tile[0], tile[1]
			
			
			code = str(X) + str(Y)
			code2 = code + "2"
			codeSide = code + "side"
			codeSide2 = code + "side2"
			
			if codeSide in povOffsetDic:
				x, y, w, h = povOffsetDic[codeSide]
				self.clear()
				self.addCamera()
				self.setLight(2.0-(Y/4.0))
				self.addLight()
				self.add("makeDoorWoodClosedSideBox(%s,%s)\n" % (-X, Y))
				
				self.render("auto.png")
				img = ImageHandler("auto.png")
				
				img.img = img.subsurface(x, y, w, h)
				name = str(X) + str(Y) + "side.png"
				img.save(name)
			
			if codeSide2 in povOffsetDic:
				x, y, w, h = povOffsetDic[codeSide2]
				self.clear()
				self.addCamera()
				self.setLight(2.0-(Y/4.0))
				self.addLight()
				self.add("makeDoorWoodClosedSideBox(%s,%s)\n" % (X, Y))
				
				self.render("auto.png")
				img = ImageHandler("auto.png")
				
				img.img = img.subsurface(x, y, w, h)
				name = str(X) + str(Y) + "side2.png"
				img.save(name)
				
			if code2 in povOffsetDic:
				x, y, w, h = povOffsetDic[code2]
				self.clear()
				self.addCamera()
				self.setLight(2.0-(Y/4.0))
				self.addLight()
				self.add("makeDoorWoodClosedBox(%s,%s)\n" % (X, Y))
				
				self.render("auto.png")
				img = ImageHandler("auto.png")

				img.img = img.subsurface(x, y, w, h)
				name = code2 + ".png"
				img.save(name)
				
			if code in povOffsetDic:
				x, y, w, h = povOffsetDic[code]
				self.clear()
				self.addCamera()
				self.setLight(2.0-(Y/4.0))
				self.addLight()
				self.add("makeDoorWoodClosedBox(%s,%s)\n" % (-X, Y))
				
				self.render("auto.png")
				img = ImageHandler("auto.png")

				img.img = img.subsurface(x, y, w, h)
				name = code + ".png"
				img.save(name)
			
	def buildSetNiche(self):
		for tile in boxCoordList:
			X, Y = tile[0], tile[1]
			
			
			code = str(X) + str(Y)
			code2 = code + "2"
			codeSide = code + "side"
			codeSide2 = code + "side2"
			
			if codeSide in povOffsetDic:
				x, y, w, h = povOffsetDic[codeSide]
				self.clear()
				self.addCamera()
				self.setLight(2.0-(Y/4.0))
				self.addLight()
				self.add("makeNicheSide(%s,%s)\n" % (-X, Y))
				
				self.render("auto.png")
				img = ImageHandler("auto.png")
				
				img.img = img.subsurface(x, y, w, h)
				name = str(X) + str(Y) + "side.png"
				img.save(name)
			
			if codeSide2 in povOffsetDic:
				x, y, w, h = povOffsetDic[codeSide2]
				self.clear()
				self.addCamera()
				self.setLight(2.0-(Y/4.0))
				self.addLight()
				self.add("makeNicheSide(%s,%s)\n" % (X, Y))
				
				self.render("auto.png")
				img = ImageHandler("auto.png")
				
				img.img = img.subsurface(x, y, w, h)
				name = str(X) + str(Y) + "side2.png"
				img.save(name)
				
			if code2 in povOffsetDic:
				x, y, w, h = povOffsetDic[code2]
				self.clear()
				self.addCamera()
				self.setLight(2.0-(Y/4.0))
				self.addLight()
				self.add("makeNiche(%s,%s)\n" % (X, Y))
				
				self.render("auto.png")
				img = ImageHandler("auto.png")

				img.img = img.subsurface(x, y, w, h)
				name = code2 + ".png"
				img.save(name)
				
			if code in povOffsetDic:
				x, y, w, h = povOffsetDic[code]
				self.clear()
				self.addCamera()
				self.setLight(2.0-(Y/4.0))
				self.addLight()
				self.add("makeNiche(%s,%s)\n" % (-X, Y))
				
				self.render("auto.png")
				img = ImageHandler("auto.png")

				img.img = img.subsurface(x, y, w, h)
				name = code + ".png"
				img.save(name)
	
	def buildSetCmd(self, cmd, mirror = True):
		for tile in boxCoordList:
			X, Y = tile[0], tile[1]
			
			code = str(X) + str(Y)
			code2 = code + "2"
			codeSide = code + "side"
			codeSide2 = code + "side2"
			
			if codeSide in povOffsetDic:
				x, y, w, h = povOffsetDic[codeSide]
				self.clear()
				self.addCamera()
				self.setLight(2.0-(Y/4.0))
				self.addLight()
				self.add("%s(%s,%s)\n" % (cmd, -X, Y))
				
				self.render("auto.png")
				img = ImageHandler("auto.png")
				
				img.img = img.subsurface(x, y, w, h)
				name = str(X) + str(Y) + "side.png"
				img.save(name)
			
			if codeSide2 in povOffsetDic and mirror==False:
				x, y, w, h = povOffsetDic[codeSide2]
				self.clear()
				self.addCamera()
				self.setLight(2.0-(Y/4.0))
				self.addLight()
				self.add("%sSide(%s,%s)\n" % (cmd, X, Y))
				
				self.render("auto.png")
				img = ImageHandler("auto.png")
				
				img.img = img.subsurface(x, y, w, h)
				name = str(X) + str(Y) + "side2.png"
				img.save(name)
				
			if code2 in povOffsetDic and mirror == False:
				x, y, w, h = povOffsetDic[code2]
				self.clear()
				self.addCamera()
				self.setLight(2.0-(Y/4.0))
				self.addLight()
				self.add("%sSide(%s,%s)\n" % (cmd, X, Y))
				
				self.render("auto.png")
				img = ImageHandler("auto.png")

				img.img = img.subsurface(x, y, w, h)
				name = code2 + ".png"
				img.save(name)
				
			if code in povOffsetDic:
				x, y, w, h = povOffsetDic[code]
				self.clear()
				self.addCamera()
				self.setLight(2.0-(Y/4.0))
				self.addLight()
				self.add("%s(%s,%s)\n" % (cmd, -X, Y))
				
				self.render("auto.png")
				img = ImageHandler("auto.png")

				img.img = img.subsurface(x, y, w, h)
				name = code + ".png"
				img.save(name)
	
	def buildItemSet(self, itemCmd):
		for i in range(6):
			code = "0" + str(i)
			self.clear()
			self.addCamera()
			self.setLight(2.0-(i/4.0))
			self.addLight()
			self.add("%s(%s,%s)\n" % (itemCmd, 0, i+1))
			
			self.render("auto.png")
			img = ImageHandler("auto.png")
			x, y, w, h = img.get_bounds()
			img.img = img.subsurface(x, y, w, h)
			name = code + ".png"
			img.save(name)


itemSpotDic = {}
itemSpotDic["152"] = (333, 237, 130, 7)
itemSpotDic["242"] = (467, 244, 93, 10)
itemSpotDic["132"] = (356, 254, 204, 15)
itemSpotDic["012"] = (55, 296, 450, 65)
itemSpotDic["112"] = (415, 296, 145, 65)
itemSpotDic["032"] = (184, 254, 192, 15)
itemSpotDic["052"] = (219, 237, 122, 7)
itemSpotDic["02"] = (146, 269, 268, 27)
itemSpotDic["03"] = (184, 254, 192, 15)
itemSpotDic["00"] = (0, 361, 560, 39)
itemSpotDic["01"] = (55, 296, 450, 65)
itemSpotDic["04"] = (205, 244, 150, 10)
itemSpotDic["05"] = (219, 237, 122, 7)
itemSpotDic["232"] = (509, 254, 51, 12)
itemSpotDic["24"] = (0, 244, 93, 10)
itemSpotDic["142"] = (342, 244, 163, 10)
itemSpotDic["25"] = (0, 237, 122, 7)
itemSpotDic["002"] = (0, 361, 560, 39)
itemSpotDic["122"] = (377, 269, 183, 27)
itemSpotDic["022"] = (146, 269, 268, 27)
itemSpotDic["102"] = (507, 361, 53, 38)
itemSpotDic["042"] = (205, 244, 150, 10)
itemSpotDic["11"] = (0, 296, 145, 65)
itemSpotDic["10"] = (0, 361, 53, 38)
itemSpotDic["13"] = (0, 254, 204, 15)
itemSpotDic["12"] = (0, 269, 183, 27)
itemSpotDic["15"] = (97, 237, 130, 7)
itemSpotDic["14"] = (55, 244, 163, 10)
itemSpotDic["23"] = (0, 254, 51, 12)
itemSpotDic["35"] = (0, 237, 17, 3)
itemSpotDic["352"] = (543, 237, 17, 3)
itemSpotDic["252"] = (438, 237, 122, 7)

if __name__=="__main__":
	p = PovrayHandler()
	
	
	
	# door export
	for code in povOffsetDic:
		if "-" in code:
			continue
		
		if "-" in code:
			X = -int(code[1])
			Z = int(code[2])
		else:
			X = int(code[0])
			Z = int(code[1])
		
		p.clear()
		p.addCamera(1.2)
		p.addLight(2.0-Z/3.0)
		if "side" in code:
			#cmd = "makeDoorWoodClosedSideBox(%s, %s)\n" % (X,Z)
			cmd = "makeNicheSide(%s, %s)\n" % (X, Z)
		else:
			#cmd = "makeDoorWoodClosedBox(%s, %s)\n" % (X,Z)
			cmd = "makeNiche(%s, %s)\n" % (X, Z)
			
		p.add(cmd)
		p.render("test.png")
		imgHandler = ImageHandler("test.png")
		x, y, w, h = povOffsetDic[code]
		
		imgHandler.img = imgHandler.subsurface(x, y, w, h)
		name = str(code) + ".png"
		imgHandler.save(name)
	
	'''
	# wallparts export (with offset calculation)
	
	for code in ["23", "13", "03", "22", "12", "02", "21", "11", "01", "10"]:
		X = int(code[0])
		Z = int(code[1])
		
		p.clear()
		p.addCamera(1.2)
		p.addLight(2.0-Z/3.0)
		p.addFace(X, Z)
		p.render("test.png")
		imgHandler = ImageHandler("test.png")
		x, y, w, h = imgHandler.get_bounds()
		if w>0:
			imgHandler.img = imgHandler.subsurface(x, y, w, h)
			p.coordRectDic[code] = (x, y, w, h)
			name = str(code) + ".png"
			imgHandler.save(name)
		if X == 0:continue
		
		p.clear()
		p.addCamera(1.2)
		p.addLight(2.0-Z/4.0)
		p.addSide(X, Z)
		p.render("test.png")
		imgHandler = ImageHandler("test.png")
		x, y, w, h = imgHandler.get_bounds()
		if w>0:
			imgHandler.img = imgHandler.subsurface(x, y, w, h)
			p.coordRectDic[code+"side"] = (x, y, w, h)
			name = str(code) + "side.png"
			imgHandler.save(name)
	print "Done"
	for i in p.coordRectDic:
		print "povOffsetDic[\"%s\"] = %s" % (i, p.coordRectDic[i])
	
	'''
	
	
	
	
