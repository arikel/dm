#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from level import *
from gui import *

#-----------------------------------------------------------------------
# image loader
class ImgLoader(object):
	def __init__(self):
		self.tileImg = {}
		self.imgList = ["door", "floor", "key", "mummy", "new",
			"next", "niche", "open", "prev", "resize", "save", "wall"]
		self.size = 20
		self.reload()
		
	def setSize(self, n):
		if n != self.size:
			self.size = n
			self.reload()
	
	def reload(self):
		for img in self.imgList:
			path = "graphics/editor/" + img + ".png"
			self.tileImg[img] = pygame.image.load(path)
			self.tileImg[img] = pygame.transform.scale(self.tileImg[img], (self.size, self.size))
			
	def getImg(self, name):
		if name not in self.tileImg:
			return None
		return self.tileImg[name]
	
	def getImage(self, name):
		return self.getImg(name)

class TileSelector(object):
	def __init__(self, editor):
		self.editor = editor
		self.state = "closed"
		self.genres = ["wall", "floor", "door"]
		
		self.triggerbutton = Button(600,10,"graphics/editor/wall.png")
		self.triggerbutton.bind(self.toggle)
		self.buttons = []
		for i, n in enumerate(self.genres):
			b = Button(600,10+(i+1)*35,"graphics/editor/" + n + ".png", n)
			b.bind(self.editor.selectGenre, n)
			self.buttons.append(b)
		
	def toggle(self):
		
		if self.state == "open":
			self.close()
		else:
			self.open()
		print "Selector toggled, state = %s" % (self.state)
		
	def open(self):
		self.state = "open"
		for i, n in enumerate(self.genres):
			b = self.buttons[i]
			b.bind(self.editor.selectGenre, n)
		
	def close(self):
		self.state = "closed"
	
	def handleEvents(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if self.triggerbutton.hover:
						self.triggerbutton.onClick()
					for b in self.buttons:
						if b.hover:
							b.onClick()
							self.close()
	
	def blit(self, screen):
		self.triggerbutton.blit(screen)
		if self.state == "open":
			for b in self.buttons:
				b.blit(screen)
	
class TileElementSelector(TileSelector):
	def __init__(self, editor):
		self.editor = editor
		self.state = "closed"
		self.genres = ["niche"]
		
		self.triggerbutton = Button(640,10,"graphics/editor/niche.png")
		self.triggerbutton.bind(self.toggle)
		self.buttons = []
		for i, n in enumerate(self.genres):
			b = Button(640,10+(i+1)*35,"graphics/editor/" + n + ".png", n)
			b.bind(self.editor.selectGenre, n)
			self.buttons.append(b)
			
	

#-----------------------------------------------------------------------
# The main editor class
#-----------------------------------------------------------------------
 
class LevelEditor(object):
	def __init__(self, filename=None):
		self.screen = pygame.display.set_mode((800,600))
		self.screen_w = self.screen.get_width()
		self.screen_h = self.screen.get_height()
		
		self.imgLoader = ImgLoader()
		# size of a tile, in pixels, for the editor level image
		self.setTileSize(25)
		
		self.turnLeftDic = {"N":"W", "W":"S", "S":"E", "E":"N"}
		self.turnRightDic = {"N":"E", "W":"N", "S":"W", "E":"S"}
		self.turnBackDic = {"N":"S", "W":"E", "S":"N", "E":"W"}
		
		
		
		# dragging
		self.off_x = 0
		self.off_y = 0
		
		self.drag_x = 0
		self.drag_y = 0
		self.dragging = False
		
		# drawing
		self.drawing = False
		
		self.buttons = {}
		
		# resizing
		self.resizing = False
		self.resizeGuide = Button(0,0,"graphics/editor/resize.png")
		self.resizeGuide.bind(self.startResize)
		self.buttons["resize"] = self.resizeGuide
		
		
		
		self.guiStep = 30
		i = 0
		self.b_new = Button(5+i*self.guiStep,5,"graphics/editor/new.png", "new")
		self.b_new.bind(self.onClickNew)
		self.buttons["new"]= self.b_new
		i += 1
		self.b_open = Button(5+i*self.guiStep,5,"graphics/editor/open.png", "open")
		self.b_open.bind(self.onClickOpen)
		self.buttons["open"] = self.b_open
		i += 1
		self.b_save = Button(5+i*self.guiStep,5,"graphics/editor/save.png", "save")
		self.buttons["save"] = self.b_save
		i += 1
		
		
		
		self.labelcoord = Label(10,580, "ok", "coord")
		self.buttons["coord"] = self.labelcoord
		
		self.labeltitle = Label(80,580, "title", "title")
		self.buttons["title"] = self.labeltitle
		
		self.levelListVisible = False
		
		
		self.selectedGenre = "wall"
		self.selectedDirection = "N"
		
		self.tileSelector = TileSelector(self)
		self.elemSelector = TileElementSelector(self)
		self.tileList = ["wall", "floor", "door"]
		self.elemList = ["niche"]
		
		# level image
		if filename:
			self.load(filename)
		else:
			self.filename = None
			self.level = None
			
		self.makeLevelImage()
		
		
		
	def load(self, filename):
		self.filename = filename
		self.level = Level("data/level/" + self.filename)
		self.b_save.bind(self.save, self.filename)
		self.labeltitle.setText(self.filename)
		self.cleanOpenLevelButtons()
		
	def save(self, filename):
		if not filename:
			return
		self.filename = filename
		self.level.save("data/level/" + self.filename)
	
	def openLevel(self, filename):
		self.load(filename)
		self.makeLevelImage()
	
	def onClickOpen(self):
		if self.levelListVisible:
			self.cleanOpenLevelButtons()
		else:
			self.makeOpenLevelButtons()
	
	def onClickNew(self):
		self.level.new("new.txt")
		self.filename = "new.txt"
		self.b_save.bind(self.save, self.filename)
		self.labeltitle.setText(self.filename)
		self.cleanOpenLevelButtons()
		self.makeLevelImage()
	
	def makeOpenLevelButtons(self):
		levels = os.listdir("data/level")
		dy = 40
		for i, level in enumerate(levels):
			b = Label(5, dy+i*25, level, level)
			name = "open_" + level
			b.bind(self.openLevel, level)
			self.buttons[name] = b
		self.levelListVisible = True
		
	def cleanOpenLevelButtons(self):
		for b in self.buttons.keys():
			if "open_" in b:
				del self.buttons[b]
		self.levelListVisible = False
		
	def selectGenre(self, genre):
		self.selectedGenre = genre
		
	def toggleSelectedGenre(self):
		if self.selectedGenre == "wall":
			self.selectedGenre = "door"
		elif self.selectedGenre == "floor":
			self.selectedGenre = "door"
		elif self.selectedGenre == "door":
			self.selectedGenre = "wall"
		print "selecting %s to draw" % (self.selectedGenre)
		
	def zoomIn(self):
		if self.size < 50:
			self.size += 5
			self.imgLoader.setSize(self.size)
			self.makeLevelImage()
			
	def zoomOut(self):
		if self.size > 5:
			self.size -= 5
			self.imgLoader.setSize(self.size)
			self.makeLevelImage()
	
	#-------------------------------------------------------------------
	# level resizing
	'''
	def extendLevelX(self, n):
		if not self.level:return
		self.level.extendX(n)
		self.makeLevelImage()
		
	def extendLevelY(self, n):
		if not self.level:return
		self.level.extendY(n)
		self.makeLevelImage()
		
	def reduceLevelX(self, n):
		if not self.level:return
		self.level.reduceX(n)
		self.makeLevelImage()
		
	def reduceLevelY(self, n):
		if not self.level:return
		self.level.reduceY(n)
		self.makeLevelImage()
	'''
	def setLevelSize(self, X, Y):
		if X<=0 or Y<=0:return
		if X==self.level.X and Y==self.level.Y:return
		
		if X>self.level.X:
			dx = X - self.level.X
			self.level.extendX(dx)
		elif X<self.level.X:
			dx = self.level.X - X
			self.level.reduceX(dx)
		if Y>self.level.Y:
			dy = Y - self.level.Y
			self.level.extendY(dy)
		elif Y<self.level.Y:
			dy = self.level.Y - Y
			self.level.reduceY(dy)
		self.makeLevelImage()
	
	#-------------------------------------------------------------------
	# level image
	def makeLevelImage(self):
		if not self.level:return
		self.img = pygame.surface.Surface((self.size*self.level.X, self.size*self.level.Y))
		self.img.fill((174,174,174))
		
		for x in range(self.level.X):
			for y in range(self.level.Y):
				self.drawTile(x, y)
	
	#-------------------------------------------------------------------
	# setTile
	def setTile(self, x, y, genre):
		if self.level.isInLevel(x, y):
			tile = self.level.getTile(x, y)
			if genre != tile.genre:
				self.level.tiles[x][y] = makeTile(self.level, x, y, genre)
				self.drawTile(x, y)
	
	def setTileElement(self, x, y, genre, slot):
		if self.level.isInLevel(x, y):
			tile = self.level.getTile(x, y)
			tile.addElement(genre, slot)
			self.drawTile(x, y)
	
	
	def setTileSize(self, size):
		self.size = size
		self.imgLoader.setSize(self.size)
	
	def drawTile(self, x, y):
		if not self.level.isInLevel(x, y):
			return
		tile = self.level.getTile(x, y)
		genre = tile.genre
		#print "calling drawTile for genre %s" % (genre)
		if genre == "floor":
			self.img.blit(self.imgLoader.getImg("floor"), (x*self.size, y*self.size))
			
		elif genre == "wall":
			self.img.blit(self.imgLoader.getImg("wall"), (x*self.size, y*self.size))
			#print "drawTile : wall drawn, tile slots = %s" % (tile.elemSlots)
			for slot in tile.elemSlots:
				#print "drawTile found slot %s" % (slot)
				for elem in tile.elemSlots[slot]:
					self.drawElement(x, y, elem.genre, slot)
					#print "Drawn element %s slot %s for tile %s %s" % (elem.genre, slot, x, y)
					
		elif genre == "door":
			if self.level.getTile(x-1, y):
				if self.level.getTile(x-1, y).genre == "floor":
					img = pygame.transform.rotate(self.imgLoader.getImg("door"), 90)
					
				else:
					img = self.imgLoader.getImg("door")
				self.img.blit(img, (x*self.size, y*self.size))
			else:
				self.img.blit(self.tileImg.getImg("wall"), (x*self.size, y*self.size))
	
	def drawElement(self, x, y, genre, slot):
		#print "drawElement called"
		img = self.imgLoader.getImg(genre)
		rot = 0
		if slot == "E": rot = -90
		if slot == "W": rot = 90
		if slot == "S": rot = 180
		img = pygame.transform.rotate(img, rot)
		self.img.blit(img, (x*self.size, y*self.size))
	
	def onLeftClick(self):
		
		for b in self.buttons.values():
			if b.hover:
				b.onClick()
				return
		
		self.startDraw(self.selectedGenre)
			
	def onRightClick(self):
		self.startDraw("floor")
		
	def onSpace(self):
		self.toggleSelectedGenre()
		
	#-------------------------------------------------------------------
	# dragging
	def startDrag(self):
		self.dragging = True
		x, y = pygame.mouse.get_pos()
		self.drag_x = x-self.off_x
		self.drag_y = y-self.off_y
		
	def stopDrag(self):
		self.dragging = False
	
	def dragUpdate(self):
		if not self.dragging:
			return
		
		x, y = pygame.mouse.get_pos()
		dx, dy = x-self.drag_x, y-self.drag_y
		self.off_x = dx
		self.off_y = dy
		
	#-------------------------------------------------------------------
	# drawing	
	def startDraw(self, genre):
		self.drawing = genre
		#print "starting to draw %s tiles" % (genre)
		
	def drawUpdate(self):
		if self.drawing:
			x, y = pygame.mouse.get_pos()
			if y<35:
				# no drawing when mouse on top button bar
				return
			x, y = x-self.off_x, y-self.off_y
			X, Y = x/self.size, y/self.size
			tile = self.level.getTile(X, Y)
			if not tile:
				#print "drawing %s tiles, but %s, %s not found" % (self.drawing, X, Y)
				return
			
			if self.drawing == "niche":
				tile.addElement("niche", self.selectedDirection)
				self.drawTile(X, Y)
				return
				
			if tile.genre != self.drawing:
				self.setTile(X, Y, self.drawing)
				
	def stopDraw(self):
		#print "stopping %s tiles drawing" % (self.drawing)
		self.drawing = False
	
	
	#-------------------------------------------------------------------
	# resizing
	
	def startResize(self):
		self.resizing = True
		x, y = pygame.mouse.get_pos()
		self.drag_x = x-self.off_x
		self.drag_y = y-self.off_y
	
	def resizeUpdate(self):
		if not self.resizing:return
		#print "resizing right now!"
		X, Y = self.getMouseTilePos()
		if X != self.level.X or Y != self.level.Y:
			self.setLevelSize(X, Y)
		
	def stopResize(self):
		self.resizing = False
	
	def getMouseTilePos(self):
		x, y = pygame.mouse.get_pos()
		x, y = x-self.off_x, y-self.off_y
		X, Y = x/self.size, y/self.size
		return X, Y
	
	#-------------------------------------------------------------------
	# update
	def update(self):
		self.dragUpdate()
		self.drawUpdate()
		self.resizeUpdate()
		
		events = pygame.event.get()
		self.tileSelector.handleEvents(events)
		self.elemSelector.handleEvents(events)
		
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False
				
				elif event.key == pygame.K_LEFT:
					self.selectedDirection = self.turnLeftDic[self.selectedDirection]
					
				elif event.key == pygame.K_RIGHT:
					self.selectedDirection = self.turnRightDic[self.selectedDirection]
					
				elif event.key == pygame.K_UP:
					self.level.reduceY(1)
					self.makeLevelImage()
					
				elif event.key == pygame.K_DOWN:
					self.level.extendY(1)
					self.makeLevelImage()
				
				elif event.key == pygame.K_SPACE:
					self.onSpace()
			
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.onLeftClick()
				elif event.button == 3:
					self.onRightClick()
				elif event.button == 2:
					self.startDrag()
				elif event.button == 4:
					self.zoomIn()
				elif event.button == 5:
					self.zoomOut()
					
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1 or event.button == 3:
					if self.drawing:
						self.stopDraw()
					if self.resizing:
						self.stopResize()
						
				elif event.button == 2:
					self.stopDrag()
	#-------------------------------------------------------------------
	# blit
	def blit(self):
		x, y = self.getMouseTilePos()
		mx, my = pygame.mouse.get_pos()
		
		# the level image
		self.screen.blit(self.img, (self.off_x,self.off_y))
		
		self.resizeGuide.topleft = (self.off_x+(self.level.X)*self.size, self.off_y+(self.level.Y)*self.size)
		
		
		if self.level.isInLevel(x, y):
			self.labelcoord.setText("%s / %s" % (x, y))
			if not self.drawing:
				img = self.imgLoader.getImg(self.selectedGenre)
				rot = 0
				if self.selectedGenre in self.elemList:
					if self.selectedDirection == "E" : rot = -90
					if self.selectedDirection == "W" : rot = 90
					if self.selectedDirection == "S" : rot = 180
				img = pygame.transform.rotate(img, rot)
				
				img.set_alpha(120)
				self.screen.blit(img, (x*self.size + self.off_x, y*self.size + self.off_y))
			
		#else:
		#	pygame.mouse.set_visible(True)

		# GUI
		pygame.draw.rect(self.screen, (0,0,0), (0,0,800,35))
		
		for b in self.buttons:
			self.buttons[b].blit(self.screen)
		
		self.tileSelector.blit(self.screen)
		self.elemSelector.blit(self.screen)
		
	#-------------------------------------------------------------------
	# run
	def run(self):
		self.running = True
		while self.running:
			self.screen.fill((50,50,50))
			self.update()
			self.blit()
			pygame.display.flip()
		pygame.quit()
		
if __name__=="__main__":
	editor = LevelEditor("new.txt")
	editor.run()
		
