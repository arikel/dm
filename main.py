#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
	import psyco
	psyco.full()
except:
	print("No psyco found")

import pygame
from config import *
from offset import *

from gui import *

# level img : 560 * 400


#-------------------------------------------------------------------
# Image loaders
#-------------------------------------------------------------------

class TileLoader(object):
	def __init__(self, name, mirrored = True):
		self.name = name
		self.mirror = mirrored
		self.prefix = "graphics/tiles/" + name + "/"
		
		self.img = {}
		
		codeList = povOffsetList
			
		for code in codeList:
			if self.mirror and "-" in code:
				imgPath = self.prefix + code[1:] + ".png"
			else:
				imgPath = self.prefix + code + ".png"
			try:
				self.img[code] = pygame.image.load(imgPath)
			except:
				continue
				#print "Image not found for %s %s, path was %s" % (code, name, imgPath)
			
			if self.mirror and code in self.img and "-" in code:
				self.img[code] = pygame.transform.flip(self.img[code], 1, 0)
		
	def getImage(self, code):
		if code not in self.img:
			return None
		return self.img[code]
	
	def getOffset(self, code):
		if code not in povOffsetDic:
			return (0,0)
		offset = povOffsetDic[code]
		return offset

class AnimatedTileLoader(object):
	def __init__(self, name, nbFrames, mirrored = True):
		self.name = name
		self.mirror = mirrored
		self.prefix = "graphics/tiles/" + name + "/"
		
		self.img = {}
		
		codeList = povOffsetList
			
		for code in codeList:
			
			for n in range(nbFrames):
				#print "making code for animated tile : %s from list becomes %s" % (code, code + "-" + str(n))
				newcode = code + "_" + str(n)
				if "-" in code and self.mirror:
					imgPath = self.prefix + newcode[1:] + ".png"
				else:
					imgPath = self.prefix + newcode + ".png"
				try:
					self.img[newcode] = pygame.image.load(imgPath)
				except:
					if "door" in self.name:
						if self.mirror and "-" in code:
							imgPath = "graphics/tiles/gate/" + code[1:] + ".png"
						else:
							imgPath = "graphics/tiles/gate/" + code + ".png"
						self.img[newcode] = pygame.image.load(imgPath)
					
				if self.mirror and newcode in self.img and "-" in newcode:
					self.img[newcode] = pygame.transform.flip(self.img[newcode], 1, 0)
	
	def getImage(self, code, frame=0):
		code += "_" + str(frame)
		if code not in self.img:
			return None
		return self.img[code]
	
	def getOffset(self, code):
		if code not in povOffsetDic:
			return (0,0)
		offset = povOffsetDic[code]
		return offset



class ItemLoader(object):
	def __init__(self, name):
		self.name = name
		self.prefix = "graphics/tiles/" + name + "/"
		
		self.img = {}
		
		for code in ["00", "01", "02", "03", "04", "05"]:
			imgPath = self.prefix + code + ".png"
			try:
				self.img[code] = pygame.image.load(imgPath)
			except:
				print "Image not found for %s %s" % (code, name)
	
	def getImage(self, code, flipped = False):
		code = "0" + str(code[1])
		if code not in self.img:
			return None
		if flipped:
			return pygame.transform.flip(self.img[code], 1, 0)
		else:
			return self.img[code]
			
	
	def getOffset(self, code):
		if code not in itemOffsetDic:
			return (0,0)
		offset = itemOffsetDic[code]
		return offset

	

	
ImgDB = {}
ImgDB["bg1"] = pygame.image.load("graphics/tiles/bg1.png")
ImgDB["bg2"] = pygame.image.load("graphics/tiles/bg2.png")	
#-------------------------------------------------------------------
# Main
#-------------------------------------------------------------------
class Game(object):
	def __init__(self):
		
		self.screen = pygame.display.set_mode((800,600))
		
		self.level = Level("data/level/testLevel.txt")
		self.playerX = 2
		self.playerY = 2
		self.playerDirection = "S"
		
		self.turnLeftDic = {"N":"W", "W":"S", "S":"E", "E":"N"}
		self.turnRightDic = {"N":"E", "W":"N", "S":"W", "E":"S"}
		self.turnBackDic = {"N":"S", "W":"E", "S":"N", "E":"W"}
		self.itemOrderDic = {
			"N": ("NW", "NE", "SW", "SE"),
			"E": ("NE", "SE", "NW", "SW"),
			"S": ("SE", "SW", "NE", "NW"),
			"W": ("SW", "NW", "SE", "NE")
		}
		
		self.levelImg = pygame.surface.Surface((560,400))
		self.lastBg = "bg1"
			
		self.imgLoader = {}
		self.imgLoader["wall"] = TileLoader("wallparts")
		self.imgLoader["wall2"] = TileLoader("wallparts2")
		self.imgLoader["door"] = AnimatedTileLoader("door", 5)
		self.imgLoader["niche"] = TileLoader("niche")
		self.imgLoader["gate"] = TileLoader("gate")
		self.imgLoader["switch"] = TileLoader("switch", False)
		self.imgLoader["box"] = ItemLoader("box")
		
		self.clickZone = {}
		self.clickZone["rightSwitch"] = pygame.Rect((435,260), (25,22))
		self.clickZone["floor_ul"] = pygame.Rect((116,413), (110,30))
		self.clickZone["floor_ur"] = pygame.Rect((316,413), (110,30))
		self.clickZone["floor_dl"] = pygame.Rect((60,460), (170,30))
		self.clickZone["floor_dr"] = pygame.Rect((310,460), (170,30))
		
		self.clickZone["throw_l"] = pygame.Rect((0,94), (270,250))
		self.clickZone["throw_r"] = pygame.Rect((281,94), (270,250))
		
		
		self.level.tiles[3][3].makeItem("box", "NE")
		self.level.tiles[3][3].makeItem("box", "SE")
		self.level.tiles[3][3].makeItem("box", "NW")
		self.level.tiles[3][3].makeItem("box", "SW")
		
		self.level.tiles[3][4].makeItem("box", "NE")
		self.level.tiles[3][4].makeItem("box", "SE")
		self.level.tiles[3][4].makeItem("box", "NW")
		self.level.tiles[3][4].makeItem("box", "SW")
		
		#self.level.tiles[0][1].addElement("niche", "E")
		#self.level.tiles[1][0].addElement("niche", "S")
		
		
		self.handItem = None
		
		self.party = PlayerParty()
		'''
		p = Player("halk", 0)
		self.party.addPlayer(p)
		p.setCarac("hp", 5)
		self.party.setLeader(0)
		
		p = Player("boris", 1)
		self.party.addPlayer(p)
		p.setCarac("hp", 25)
		'''
		self.gui = GameGui(self)
		
		self.running = True
		self.run()
		
		
	def addPlayer(self, playerName):
		rank = len(self.party.players)
		player = Player(playerName, rank)
		
		self.party.addPlayer(player)
		
	#-------------------------------------------------------------------
	# drawing functions
	#-------------------------------------------------------------------
	
	def getTileGenre(self, x, y):
		if self.level.isInLevel(x, y):
			genre = self.level.tiles[x][y].genre
			if genre == "wall":
				if ( (x+y)%2 == 0 ):
					genre = "wall2"
		else:
			genre = "wall"
		return genre
	
	#-------------------------------------------------------------------
	# Wall tile
	#-------------------------------------------------------------------
	def drawWallTile(self, rel_x, rel_y, x, y):
		tile = self.level.getTile(x, y)
		dirFacing = self.turnBackDic[self.playerDirection]
		dirLSide = self.turnRightDic[self.playerDirection]
		dirRSide = self.turnLeftDic[self.playerDirection]
		if rel_x<0:
			dirSide = dirLSide
		elif rel_x>0:
			dirSide = dirRSide
		else:
			dirSide = None
		
		if tile:
			if dirSide:
				self.drawWallSide(rel_x, rel_y, x, y)
				self.drawElement(rel_x, rel_y, x, y, dirSide)
			self.drawWallFace(rel_x, rel_y, x, y)
			self.drawElement(rel_x, rel_y, x, y, dirFacing)
		else:
			self.drawWallSide(rel_x, rel_y, x, y)
			self.drawWallFace(rel_x, rel_y, x, y)
			
	#-------------------------------------------------------------------
	# wall side
	def drawWallSide(self, rel_x, rel_y, x, y):
		code = str(rel_x) + str(rel_y) + "side"
		if code not in povOffsetDic:
			return
		if rel_x>0:
			dirFacing = self.turnLeftDic[self.playerDirection]
		elif rel_x < 0:
			dirFacing = self.turnRightDic[self.playerDirection]
		
		else:
			# if x == 0, tile is in front, and no side is visible
			return
		
		genre = self.getTileGenre(x, y)
		if genre == "door":
			img = self.imgLoader[genre].getImage(code, self.level.getTile(x,y).frame)
		else:
			img = self.imgLoader[genre].getImage(code)
		if not img:
			#print "couldn't get image in genre : %s for code %s" % (genre, code)
			return
		offsetx, offsety, w, h = povOffsetDic[code]
		self.levelImg.blit(img, (offsetx, offsety))
	
	#-------------------------------------------------------------------
	# wall face
	def drawWallFace(self, rel_x, rel_y, x, y):
		code = str(rel_x) + str(rel_y)
		if code not in povOffsetDic:
			#print "code not found for wall face %s, %s, code was %s" % (rel_x, rel_y, code)
			return
		#print "drawing wall face for %s %s %s %s" % (rel_x, rel_y, x, y)
		
		dirFacing = self.turnBackDic[self.playerDirection]
		genre = self.getTileGenre(x, y)
		if genre == "door" and "door" not in self.imgLoader:
			return
		if genre == "door":
			img = self.imgLoader[genre].getImage(code, self.level.getTile(x,y).frame)
		else:
			img = self.imgLoader[genre].getImage(code)
		
		if not img:return
		#else:
		#	print "wall face not found for %s %s" % (rel_x, rel_y)
		#print "found wall face to draw : %s / %s" % (rel_x, rel_y)
		offsetx, offsety, w, h = povOffsetDic[code]
		self.levelImg.blit(img, (offsetx, offsety))
		
		
	#-------------------------------------------------------------------
	# Door tile
	#-------------------------------------------------------------------
	def drawDoorTile(self, rel_x, rel_y, x, y):
		if "door" not in self.imgLoader:
			return
		tile = self.level.getTile(x, y)
		dirFacing = self.turnBackDic[self.playerDirection]
		dirLSide = self.turnRightDic[self.playerDirection]
		dirRSide = self.turnLeftDic[self.playerDirection]
		if rel_x<0:
			dirSide = dirLSide
		elif rel_x>0:
			dirSide = dirRSide
		else:
			dirSide = None
		
		if tile:
			if dirSide:
				self.drawDoorSide(rel_x, rel_y, x, y)
				self.drawElement(rel_x, rel_y, x, y, dirSide)
			self.drawDoorFace(rel_x, rel_y, x, y)
			self.drawElement(rel_x, rel_y, x, y, dirFacing)
		else:
			self.drawDoorSide(rel_x, rel_y, x, y)
			self.drawDoorFace(rel_x, rel_y, x, y)
			
	#-------------------------------------------------------------------
	# door side
	def drawDoorSide(self, rel_x, rel_y, x, y):
		code = str(rel_x) + str(rel_y) + "side"
		
		if code not in povOffsetDic:
			return
		if rel_x>0:
			dirFacing = self.turnLeftDic[self.playerDirection]
		elif rel_x < 0:
			dirFacing = self.turnRightDic[self.playerDirection]
		
		else:
			# if x == 0, tile is in front, and no side is visible
			return
		
		genre = self.getTileGenre(x, y)
		img = self.imgLoader[genre].getImage(code, self.level.getTile(x,y).frame)
		
		if not img:
			print "couldn't get image in genre : %s for code %s" % (genre, code)
			return
		offsetx, offsety, w, h = povOffsetDic[code]
		self.levelImg.blit(img, (offsetx, offsety))
	
	#-------------------------------------------------------------------
	# door face
	def drawDoorFace(self, rel_x, rel_y, x, y):
		code = str(rel_x) + str(rel_y)
		if code not in povOffsetDic:
			return
		
		dirFacing = self.turnLeftDic[self.turnLeftDic[self.playerDirection]]
		genre = self.getTileGenre(x, y)
		img = self.imgLoader[genre].getImage(code, self.level.getTile(x,y).frame)
		
		offsetx, offsety, w, h = povOffsetDic[code]
		self.levelImg.blit(img, (offsetx, offsety))
	
	
		
	#-------------------------------------------------------------------
	# Tile
	def drawTile(self, rel_x, rel_y, x, y):
		tile = self.level.getTile(x, y)
		if tile:
			if tile.genre == "wall":
				self.drawWallTile(rel_x, rel_y, x, y)
				return
			elif tile.genre == "floor":
				slots = self.itemOrderDic[self.playerDirection]
				for slot in slots:
					self.drawItems(rel_x, rel_y, x, y, slot)
					self.drawThrownItems(rel_x, rel_y, x, y, slot)
			
			elif tile.genre == "door":
				slots = self.itemOrderDic[self.playerDirection]
				self.drawItems(rel_x, rel_y, x, y, slots[0])
				self.drawThrownItems(rel_x, rel_y, x, y, slots[0])
				self.drawItems(rel_x, rel_y, x, y, slots[1])
				self.drawThrownItems(rel_x, rel_y, x, y, slots[1])
				
				self.drawDoorTile(rel_x, rel_y, x, y)
				
				self.drawItems(rel_x, rel_y, x, y, slots[2])
				self.drawThrownItems(rel_x, rel_y, x, y, slots[2])
				self.drawItems(rel_x, rel_y, x, y, slots[3])
				self.drawThrownItems(rel_x, rel_y, x, y, slots[3])
		
		else:
			self.drawWallTile(rel_x, rel_y, x, y)
			return
		
	#-------------------------------------------------------------------
	# WallElement
	def drawElement(self, rel_x, rel_y, x, y, slot):
		
		tile = self.level.tiles[x][y]
		
		if slot not in tile.elemSlots:
			return

		for elem in tile.elemSlots[slot]:
			
			genre = elem.genre
				
			if genre not in self.imgLoader:
				return
			
			code = str(rel_x) + str(rel_y)
			
			# if element is not facing the player, it's on a side
			if slot != self.turnRightDic[self.turnRightDic[self.playerDirection]]:
				code =  code + "side"
				
				facing = False
			else:
				facing = True
			
			# if element faces the right of the player, the image is flipped
			if rel_x>0:
				imgflipped = True
			else:
				imgflipped = False
			
			if code not in povOffsetDic:
				code = code.replace("side", "")
				if code not in povOffsetDic:
					#print "code %s not found for %s" % (code, genre)
					return
			offsetx, offsety, w, h = povOffsetDic[code]
			
			# get the image to blit
			img = self.imgLoader[genre].getImage(code)
			if img:
				self.levelImg.blit(img, (offsetx,offsety))
				
			#else:
			#	print "image not found for %s with code %s" % (genre, code)
	
	def getRelSlotPosCode(self, slot):
		"""gets the relative position of the slot in its tile,
		according to the player orientation"""
		slots = self.itemOrderDic[self.playerDirection]
		if slot == slots[0]:
			return "ul"
		elif slot == slots[1]:
			return "ur"
		elif slot == slots[2]:
			return "dl"
		elif slot == slots[3]:
			return "dr"
		return None
	#-------------------------------------------------------------------
	# items
	def drawItems(self, rel_x, rel_y, x, y, slot):
		#if not self.level.isInLevel(x, y):
		#	return
		tile = self.level.getTile(x, y)
		if slot not in tile.itemSlots:
			return
		
		offsetcode = str(rel_x) + str(rel_y)
		suff = self.getRelSlotPosCode(slot)
		if not suff:
			return
		offsetcode += suff
		
		imgcode = str(abs(rel_x)) + str(rel_y)
		flipped = False
		if rel_x > 0:
			flipped = True
			imgcode += "2"
		
		for item in tile.itemSlots[slot]:
			#print "drawing item %s, name = %s" % (item, item.name)
			img = self.imgLoader[item.name].getImage(imgcode, flipped)
			if not img:
				#print "item image not found for code %s" % (code)
				continue
				
			if offsetcode not in itemOffsetDic:continue
			
			if len(itemOffsetDic[offsetcode])!=2:continue
			
			sx, sy = itemOffsetDic[offsetcode]
			imgh = img.get_height()
			imgw = img.get_width()
			iorder = self.itemOrderDic[self.playerDirection]
			
			if rel_x >= 0:
				if slot == iorder[1] or slot == iorder[3]:
					img = pygame.transform.flip(img, 1,0)
					
			self.levelImg.blit(img, (sx, sy-imgh))
	
	
	def drawThrownItems(self, rel_x, rel_y, x, y, slot):
		#if not self.level.isInLevel(x, y):
		#	return
		tile = self.level.getTile(x, y)
		if not tile:
			return
		
		for thrownItem in self.level.thrownItems:
			if thrownItem.x == x and thrownItem.y == y and thrownItem.slot == slot:
				#print "Found item %s to draw in %s / %s, slot %s" % (thrownItem.item.name, x, y, slot)
				offsetcode = str(rel_x) + str(rel_y)
				suff = self.getRelSlotPosCode(slot)
				if not suff:
					return
				offsetcode += suff
				
				imgcode = str(abs(rel_x)) + str(rel_y)
				flipped = False
				if rel_x > 0:
					flipped = True
					imgcode += "2"
		
				img = self.imgLoader[thrownItem.item.name].getImage(imgcode, flipped)
				if not img:
					#print "item image not found for code %s" % (code)
					continue
					
				if offsetcode not in itemOffsetDic:
					#print "offsetcode %s not found for thrownitem %s" % (offsetcode, thrownItem.item.name)
					continue
				
				if len(itemOffsetDic[offsetcode])!=2:
					#print "no offset valid for thrown"
					continue
				
				sx, sy = itemOffsetDic[offsetcode]
				imgh = img.get_height()
				imgw = img.get_width()
				iorder = self.itemOrderDic[self.playerDirection]
				dy = 300/(1.0+rel_y)
				if rel_x >= 0:
					if slot == iorder[1] or slot == iorder[3]:
						img = pygame.transform.flip(img, 1,0)
						
				self.levelImg.blit(img, (sx, sy-imgh-dy))
			#else:
				#if x == thrownItem.x and y == thrownItem.y:
					#print "throwItem not visible now : %s %s %s %s, pos is : %s %s %s" % (thrownItem.item.name, thrownItem.x, thrownItem.y, thrownItem.slot, x, y, slot)
			
	#-------------------------------------------------------------------
	# floor switching
	def toggleBg(self):
		if self.lastBg == "bg1":
			self.lastBg = "bg2"
		else:
			self.lastBg = "bg1"
	
	
	#-------------------------------------------------------------------
	# level map
	def drawLevelPlan(self):
		size = 16
		for x in range(self.level.X):
			for y in range(self.level.Y):
				if self.level.isOpen(x, y):
					pygame.draw.rect(self.screen, (120,120,120), (x*16, y*16, 16,16))
				else:
					pygame.draw.rect(self.screen, (50,50,50), (x*16, y*16, 16,16))
				if self.playerX == x and self.playerY == y:
					pygame.draw.rect(self.screen, (255,120,120), (x*16+5, y*16+5, 6,6))
					if self.playerDirection == "N":
						pygame.draw.rect(self.screen, (255,255,255), (x*16+5, y*16, 6,6))
					if self.playerDirection == "S":
						pygame.draw.rect(self.screen, (255,255,255), (x*16+5, y*16+10, 6,6))
					if self.playerDirection == "E":
						pygame.draw.rect(self.screen, (255,255,255), (x*16+10, y*16+5, 6,6))
					if self.playerDirection == "W":
						pygame.draw.rect(self.screen, (255,255,255), (x*16, y*16+5, 6,6))
	
	#-------------------------------------------------------------------
	# background (roof and floor)
	def drawBg(self):
		self.levelImg.blit(ImgDB[self.lastBg], (0,0))
		
	#-------------------------------------------------------------------
	# update self.levelImg
	def updateView(self):
		#self.levelImg.fill((0,0,0))
		
		self.drawBg()
		
		fwd, right = self.getPlayerMoves()
		
		for code in povOffsetList:
			if "-" in code:
				rel_x = -int(code[1])
				rel_y = int(code[2])
			else:
				rel_x = int(code[0])
				rel_y = int(code[1])
			
			x = self.playerX + rel_x*right[0] + rel_y*right[1]
			y = self.playerY + rel_x*fwd[0] + rel_y*fwd[1]
			self.drawTile(rel_x, rel_y, x, y)
		self.drawTile(0, 0, self.playerX, self.playerY)	
		self.screen.blit(self.levelImg, (0,94))
		
		#self.drawLevelPlan()
	
	#-------------------------------------------------------------------
	# player move functions
	#-------------------------------------------------------------------
	
	def getPlayerMoves(self):
		if self.playerDirection == "N":
			fwd = (0, -1)
			right = (1,0)
			
		if self.playerDirection == "S":
			fwd = (0, 1)
			right = (-1,0)
		
		if self.playerDirection =="E":
			fwd = (1, 0)
			right = (0,1)
			
		if self.playerDirection == "W":
			fwd = (-1, 0)
			right = (0,-1)
			
		return (fwd, right)
		
	def onMoveForward(self):
		fwd, right = self.getPlayerMoves()
		x, y = self.playerX+fwd[0], self.playerY+fwd[1]
		if self.level.isOpen(x, y):
			self.playerX = x
			self.playerY = y
			self.toggleBg()
			#print "moving forward : pos = %s/%s" % (x, y)
		else:
			SoundDB["bump"].stop()
			SoundDB["bump"].play()
			#print "you hit a wall %s/%s forward" % (x,y)
			
	def onMoveBackward(self):
		fwd, right = self.getPlayerMoves()
		x, y = self.playerX-fwd[0], self.playerY-fwd[1]
		if self.level.isOpen(x, y):
			self.playerX = x
			self.playerY = y
			self.toggleBg()
			#print "moving backward : pos = %s/%s" % (x, y)
		else:
			SoundDB["bump"].stop()
			SoundDB["bump"].play()
			#print "you hit a wall %s/%s backward" % (x,y)
	
	def onMoveLeft(self):
		fwd, right = self.getPlayerMoves()
		x, y = self.playerX-right[0], self.playerY-right[1]
		if self.level.isOpen(x, y):
			self.playerX = x
			self.playerY = y
			self.toggleBg()
			#print "moving left : pos = %s/%s" % (x, y)
		else:
			SoundDB["bump"].stop()
			SoundDB["bump"].play()
			#print "you hit a wall %s/%s left" % (x,y)
	
	def onMoveRight(self):
		fwd, right = self.getPlayerMoves()
		x, y = self.playerX+right[0], self.playerY+right[1]
		if self.level.isOpen(x, y):
			self.playerX = x
			self.playerY = y
			self.toggleBg()
			#print "moving right : pos = %s/%s" % (x, y)
		else:
			SoundDB["bump"].stop()
			SoundDB["bump"].play()
			#print "you hit a wall %s/%s right" % (x,y)
	
	def onTurnLeft(self):
		self.playerDirection = self.turnLeftDic[self.playerDirection]
		self.toggleBg()
		#print "player turned left, now going to %s" % (self.playerDirection)
		
	def onTurnRight(self):
		self.playerDirection = self.turnRightDic[self.playerDirection]
		self.toggleBg()
		#print "player turned right, now going to %s" % (self.playerDirection)
	
	#-------------------------------------------------------------------
	# events
	#-------------------------------------------------------------------
	
	def onLeftClick(self):
		#print "click left."
		x, y = pygame.mouse.get_pos()
		#print "Mouse screen pos : %s %s" % (x, y)
		for k, v in self.clickZone.items():
			if v.collidepoint(x, y):
				#print "Zone clicked : %s" % (k)
				
				if k == "rightSwitch":
					self.onClickRightSwitch()
				elif k == "floor_ul":
					self.onClickFloorUL()
				elif k == "floor_ur":
					self.onClickFloorUR()
				elif k == "floor_dl":
					self.onClickFloorDL()
				elif k == "floor_dr":
					self.onClickFloorDR()
				elif k =="throw_l":
					self.onClickThrowLeft()
				elif k =="throw_r":
					self.onClickThrowRight()
					
			else:
				pass
				#print "missed : %s, %s is out of %s" % (x, y, str(v))
	
	def onClickRightSwitch(self):
		fx,fy = self.playerX+self.getPlayerMoves()[0][0], self.playerY+self.getPlayerMoves()[0][1]
		tile = self.level.getTile(fx, fy)
		if tile:
			genre = tile.genre
			#print "click right switch on tile %s" % (genre)
			if genre == "door":
				if tile.state == "closed" or tile.state=="closing":
					tile.state = "opening"
					self.level.addToUpdate(fx, fy)
					#print "starting to open door in %s, %s" % (fx, fy)
				elif tile.state == "open" or tile.state == "opening":
					tile.state = "closing"
					self.level.addToUpdate(fx, fy)
					#print "starting to close door in %s, %s" % (fx, fy)
	
	def onClickFloor(self, code):
		if code == "UL":
			ulDir = self.itemOrderDic[self.playerDirection][2]
			fx,fy = self.playerX+self.getPlayerMoves()[0][0], self.playerY+self.getPlayerMoves()[0][1]
		elif code == "UR":
			ulDir = self.itemOrderDic[self.playerDirection][3]
			fx,fy = self.playerX+self.getPlayerMoves()[0][0], self.playerY+self.getPlayerMoves()[0][1]
		elif code == "DL":
			ulDir = self.itemOrderDic[self.playerDirection][0]
			fx, fy = self.playerX, self.playerY
		elif code == "DR":
			ulDir = self.itemOrderDic[self.playerDirection][1]
			fx, fy = self.playerX, self.playerY
		else:
			return
		
		#fx,fy = self.playerX+self.getPlayerMoves()[0][0], self.playerY+self.getPlayerMoves()[0][1]
		tile = self.level.getTile(fx, fy)
		if not tile:
			return
		if tile.genre == "wall":
			# walls don't have items on their floor
			return
		
		if tile.hasItem(ulDir):
			if not self.handItem:
				self.handItem = tile.itemSlots[ulDir][-1]
				#print "Item now in hand : %s" % (self.handItem)
				tile.removeItem(ulDir)
			else:
				tile.addItem(self.handItem, ulDir)
				#print "Dropped item %s on top of others" % (self.handItem)
				self.handItem = None
				
		else:
			if self.handItem:
				tile.addItem(self.handItem, ulDir)
				#print "Dropped item %s" % (self.handItem)
				self.handItem = None
	
	def onClickFloorUL(self):
		self.onClickFloor("UL")
	def onClickFloorUR(self):
		self.onClickFloor("UR")
	def onClickFloorDL(self):
		self.onClickFloor("DL")
	def onClickFloorDR(self):
		self.onClickFloor("DR")
	
	def onClickThrowLeft(self):
		if self.handItem:
			s = {"N":"SW", "E":"NW", "S":"NE", "W":"SE"}
			dx = {"N":0, "E":1, "S":0, "W":-1}
			dy = {"N":-1, "E":0, "S":1, "W":0}
			x = self.playerX+dx[self.playerDirection]
			y = self.playerY+dy[self.playerDirection]
			tile = self.level.getTile(x, y)
			if tile:
				# don't throw stuff on the wall!
				if tile.genre == "wall":
					return
				#else:
					#print "j'ai pas un mur, j'ai un %s, je lance!" % (tile.genre)
			#else:
				#print "tile %s %s not found to throw" % (x, y)
			self.level.addThrownItem(self.handItem, x, y, s[self.playerDirection], self.playerDirection)
			SoundDB["swipe"].play()
			self.handItem = None
			
	def onClickThrowRight(self):
		if self.handItem:
			s = {"N":"SE", "E":"SW", "S":"NW", "W":"NE"}
			dx = {"N":0, "E":1, "S":0, "W":-1}
			dy = {"N":-1, "E":0, "S":1, "W":0}
			x = self.playerX+dx[self.playerDirection]
			y = self.playerY+dy[self.playerDirection]
			tile = self.level.getTile(x, y)
			if tile:
				# don't throw stuff on the wall!
				if tile.genre == "wall":
					return
				#else:
				#	print "j'ai pas un mur, j'ai un %s, je lance!" % (tile.genre)
			#else:
			#	print "tile %s %s not found to throw" % (x, y)
			self.level.addThrownItem(self.handItem, x, y, s[self.playerDirection], self.playerDirection)
			SoundDB["swipe"].play()
			self.handItem = None
	
	def onRightClick(self):
		print pygame.mouse.get_pos()
		#print "click right."
	
	
	#-------------------------------------------------------------------
	# main game loop
	#-------------------------------------------------------------------					
	def run(self):
		self.frames = 0
		pygame.init()
		# display handling	
		self.updateView()
		pygame.display.flip()
		
		self.startTime = pygame.time.get_ticks()
		
		while(self.running):
			self.update()
		
		totalTime = pygame.time.get_ticks() - self.startTime
		fps = self.frames / (totalTime/1000.0)
		print "Total time : %s seconds, FPS : %s" % (totalTime/1000.0, fps)
		pygame.quit()
		
		
	def update(self):
		t = pygame.time.get_ticks()
		x, y = pygame.mouse.get_pos()
		# events handling
			
		fwd, right = self.getPlayerMoves()
			
		events = pygame.event.get()
		
		self.gui.handleEvents(events)
		
		if not self.gui.displaySheet:
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.running = False
					
					# player movements
					if event.key == KEY_FORWARD:
						self.onMoveForward()
					
					if event.key == KEY_BACKWARD:
						self.onMoveBackward()
						
					if event.key == KEY_LEFT:
						self.onMoveLeft()
							
					if event.key == KEY_RIGHT:
						self.onMoveRight()
							
					if event.key == KEY_TURN_RIGHT:
						self.onTurnRight()
						
					if event.key == KEY_TURN_LEFT:
						self.onTurnLeft()
					
					if event.key == pygame.K_SPACE:
						self.addPlayer("halk")
						self.gui.updateParty()
		
		# dunjeon handling
		for tile in self.level.tilesToUpdate:
			self.level.getTile(tile[0], tile[1]).update(t)
		for item in self.level.thrownItems:
			item.update(t)
			
		# display handling
		self.screen.fill((50,50,50))
		self.updateView()
		
		
		self.gui.blit(self.screen)
		
		if self.handItem:
			#img = self.imgLoader[self.handItem.name].getImage("01")
			img = iconLoader.getImg(self.handItem.name)
			if img:
				imgw, imgh = img.get_width(), img.get_height()
				self.screen.blit(img, (x-imgw/2, y-imgh/2))
			
		pygame.display.flip()
		
		self.frames +=1

if __name__=="__main__":
	g = Game()
