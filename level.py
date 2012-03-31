#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from player import *

pygame.mixer.init()
SoundDB = {}
SoundDB["bump"] = pygame.mixer.Sound("sounds/party_bump.wav")
SoundDB["door"] = pygame.mixer.Sound("sounds/dungeon_door.wav")
SoundDB["thud"] = pygame.mixer.Sound("sounds/dungeon_thud.wav")
SoundDB["swipe"] = pygame.mixer.Sound("sounds/attack_swipe.wav")

WALL_ELEMENTS = ["niche", "fountain", "lock", "vim", "button", "torch_holder"]
FLOOR_ELEMENTS = ["pit", "hidden_pit", "trigger", "hidden_trigger"]

ALL_ITEMS = ["box"]

#-------------------------------------------------------------------
# Item
#-------------------------------------------------------------------

class ThrownItem(object):
	def __init__(self, item, level, x, y, slot, direction, step=500, moves=5):
		self.item = item
		self.x = x
		self.y = y
		self._level = level
		self.slot = slot
		self.direction = direction
		self.step = step
		self.moves = moves
		self.nextUpdate = pygame.time.get_ticks() + self.step
		
	def update(self, t=None):
		if not t:
			t = pygame.time.get_ticks()
		if t>= self.nextUpdate:
			if self.moves>0:
				x, y, slot = self.getNextPos()
				#if self._level.getTile(x, y).genre == "floor":
				if self._level.getTile(x, y)._open:
					#TODO : add test for hitting monster or player
					self.x = x
					self.y = y
					self.slot = slot
					self.nextUpdate = t + self.step
					self.moves -=1

				else:
					#TODO : add possible effect on wall or through door
					self._level.tiles[self.x][self.y].addItem(self.item, self.slot)
					self._level.removeThrownItem(self)
					self.moves = 0
					SoundDB["thud"].play()
			else:
				self._level.tiles[self.x][self.y].addItem(self.item, self.slot)
				self._level.removeThrownItem(self)
				SoundDB["thud"].play()
		
	def getNextPos(self):
		if self.direction == "N":
			if self.slot == "NW":
				x = self.x
				y = self.y - 1
				slot = "SW"
			elif self.slot == "NE":
				x = self.x
				y = self.y - 1
				slot = "SE"
			elif self.slot == "SW":
				x = self.x
				y = self.y
				slot = "NW"
			elif self.slot == "SE":
				x = self.x
				y = self.y
				slot = "NE"
		if self.direction == "S":
			if self.slot == "NW":
				x = self.x
				y = self.y
				slot = "SW"
			elif self.slot == "NE":
				x = self.x
				y = self.y
				slot = "SE"
			elif self.slot == "SW":
				x = self.x
				y = self.y + 1
				slot = "NW"
			elif self.slot == "SE":
				x = self.x
				y = self.y + 1
				slot = "NE"
		if self.direction == "W":
			if self.slot == "NW":
				x = self.x - 1
				y = self.y
				slot = "NE"
			elif self.slot == "NE":
				x = self.x
				y = self.y
				slot = "NW"
			elif self.slot == "SW":
				x = self.x - 1
				y = self.y
				slot = "SE"
			elif self.slot == "SE":
				x = self.x
				y = self.y
				slot = "SW"
		if self.direction == "E":
			if self.slot == "NW":
				x = self.x
				y = self.y
				slot = "NE"
			elif self.slot == "NE":
				x = self.x + 1
				y = self.y
				slot = "NW"
			elif self.slot == "SW":
				x = self.x
				y = self.y
				slot = "SE"
			elif self.slot == "SE":
				x = self.x + 1
				y = self.y
				slot = "SW"
		return (x, y, slot)
		
#-------------------------------------------------------------------
# Tile
#-------------------------------------------------------------------
class Tile(object):
	def __init__(self, _level, x, y, _open=True):
		self._level = _level
		self._open = _open
		self.x = x
		self.y = y
		self.elemSlots = {}
		self.itemSlots = {}
		
		self.genre = "floor" # wall, door, hole
		self.frame = -1 # if self.frame >= 0 , tile has animation
		self.nbFrames = 1
		self.state = "sleep"
		
	#-------------------------------------------------------------------
	# items
	def addItem(self, item, slotName="NE"):
		#print "Adding item : %s for slot %s" % (item, slotName)
		if slotName not in self.itemSlots:
			self.itemSlots[slotName] = []
		self.itemSlots[slotName].append(item)
	
	def makeItem(self, itemName, slotName="NE"):
		#print "making item : %s for slot %s" % (itemName, slotName)
		if slotName not in self.itemSlots:
			self.itemSlots[slotName] = []
		self.itemSlots[slotName].append(Item(itemName))
	
	def removeItem(self, slotName):
		if self.hasItem(slotName):
			return self.itemSlots[slotName].pop(-1)
		return False
		
	def hasItem(self, slotName):
		if slotName not in self.itemSlots:
			return False
		#print "slotName %s found, value = %s" % (slotName, self.itemSlots[slotName])
		if len(self.itemSlots[slotName])>0:
			return True
		return False
	
	#-------------------------------------------------------------------
	# elements	
	def addElement(self, elementName, slot):
		#print "Adding element : %s for slot %s" % (elementName, slot)
		if slot not in self.elemSlots:
			self.elemSlots[slot] = []
		#self.elemSlots[slot].append(elementName)
		
		# don't add a same element twice on the same slot
		else:
			for elem in self.elemSlots[slot]:
				if elem.genre == elementName:
					return
		if elementName == "niche" and self.genre == "floor":
			#print "can't add niche to floor"
			return
		self.elemSlots[slot].append(TileElement(elementName, slot))
		
	def removeElement(self, slot):
		if slot in self.slots:
			if len(self.slots[slot]>0):
				self.slots[slot].pop(-1)
			if len(self.slots[slot])==0:
				del self.slots[slot]

	def hasElement(self):
		if len(self.elemSlots)>0:
			return True
		return False
	
	def update(self, t):
		pass

	def getSaveData(self):
		data = ""
		if self.hasElement():
			for slot in self.elemSlots:
				for elem in self.elemSlots[slot]:
					elemtxt = "tileElement, %s, %s = %s, %s\n" % (self.x, self.y, elem.genre, elem.slot)
					data += elemtxt
		return data

#-------------------------------------------------------------------
# DoorTile
#-------------------------------------------------------------------
class DoorTile(Tile):
	def __init__(self, _level, x, y, _open=False):
		self._level = _level
		self._open = _open
		self.x = x
		self.y = y
		self.elemSlots = {}
		self.itemSlots = {}
		self.genre = "door"
		self.frame = 0 #tile has animation
		self.nbFrames = 5
		self.state = "closed" # 
		self.nextUpdate = 0
		self.step = 300
		
		opposite = {"N":"S", "E":"W", "S":"N","W":"E"}
		for k in opposite:
			self.addElement("switch", k)
		
	def update(self, t):
		if t>= self.nextUpdate:
			if self.state == "opening":
				self.frame += 1
				if self.frame >= self.nbFrames:
					self.frame = self.nbFrames - 1
					self.state = "open"
					self._level.removeToUpdate(self.x, self.y)
				else:
					#SoundDB["door"].stop()
					SoundDB["door"].play()
			if self.state == "closing":
				self.frame -= 1
				if self.frame < 0:
					self.frame = 0
					self.state = "closed"
					self._level.removeToUpdate(self.x, self.y)
				else:
					#SoundDB["door"].stop()
					SoundDB["door"].play()
			
			if self.frame >=3:
				self._open = True
			else:
				self._open = False
			
			self.nextUpdate = t + self.step
	
#-------------------------------------------------------------------
# TileElement : special objects on tiles
#-------------------------------------------------------------------
class TileElement(object):
	def __init__(self, genre, slot):
		self.genre = genre
		self.slot = slot
		self.items =  []
		self.acceptedItems = []
		
	def addItem(self, item):
		if item.genre in self.acceptedItems:
			self.items.append(item)
	
	def removeItem(self):
		if len(self.items):
			return self.items.pop(-1)
		return None
		
	def onAction(self, action = None):
		if not action:return
		cmd = action["action"]
		print "Action %s received" % (cmd)
	
def makeFloorTile(level, x, y):
	return Tile(level, x, y)
	
def makeWallTile(level, x, y):
	tile = Tile(level, x, y, False)
	tile.genre = "wall"
	return tile

def makeDoorTile(level, x, y):
	tile = DoorTile(level, x, y)
	return tile

def makeNicheTile(level, x, y, direction="N"):
	tile = Tile(level, x, y, False)
	tile.genre = "wall"
	tile.direction = direction
	tile.addElement("niche", tile.direction)
	return tile
	
def makeTile(level, x, y, genre):
	if genre == "floor":
		return makeFloorTile(level, x, y)
	elif genre == "wall":
		return makeWallTile(level, x, y)
	elif genre == "door":
		return makeDoorTile(level, x, y)
	else:
		return None
		
	

#-------------------------------------------------------------------
# Level
#-------------------------------------------------------------------
class Level(object):
	def __init__(self, filename = None):
		# codes used in saved data
		self.dataCode = {}
		self.dataCode["floor"] = "0"
		self.dataCode["wall"] = "1"
		self.dataCode["door"] = "d"
		
		self.tilesToUpdate = []
		self.thrownItems = []
		
		self.filename = filename
		if self.filename:
			self.load(self.filename)
		
	def makeTileFromCode(self, code, x, y):
		if code == "d":
			genre = "door"
		elif code == "0":
			genre = "floor"
		elif code == "1":
			genre = "wall"
		return makeTile(self, x, y, genre)
		
	def extendX(self, n):# add column to level map
		for i in range(n):
			col = []
			for y in range(self.Y):
				col.append(makeWallTile(self, self.X+i, y))
			self.tiles.append(col)
		self.X += n
	
	def extendY(self, n):# add line to level map
		for x in range(self.X):
			for i in range(n):
				self.tiles[x].append(makeWallTile(self, x, self.Y+i))
		self.Y += n
	
	def reduceX(self, n):# remove column from level map
		for i in range(n):
			self.tiles.pop(-1)
		self.X -= n
	
	def reduceY(self, n):# remove line from level map
		for x in range(self.X):
			for i in range(n):
				self.tiles[x].pop(-1)
		self.Y -= n
	
	def new(self, filename, x=30, y=20):
		self.filename
		self.X = x
		self.Y = y
		print "creating new level x = %s, y = %s" % (self.X, self.Y)
		
		self.tiles = []
		
		for x in range(self.X):
			tilesCol = []
			for y in range(self.Y):
				#print "adding tile %s %s" % (x, y)
				tileCode = "1"
				tilesCol.append(makeWallTile(self, x, y))
			self.tiles.append(tilesCol)
	
	#-------------------------------------------------------------------
	# load
	def load(self, levelFile):
		content = open(levelFile).read()
		lines = content.split("\n")
		
		for line in lines:
			if len(line.split("=")) != 2:
				#print "invalid line found %s" % (line)
				continue
			k, v = line.split("=")
			
			if k.strip() == "x":
				self.X = int(v.strip())
			elif k.strip() == "y":
				self.Y = int(v.strip())
			elif k.strip() == "tilecode":
				tilecode = v.strip()
				i = 0
				if len(tilecode) == self.X*self.Y:
					self.tiles = []
					for x in range(self.X):
						tileCols = []
						for y in range(self.Y):
							code = tilecode[y*self.X+x]
							tileCols.append(self.makeTileFromCode(code, x, y))
							i += 1
						self.tiles.append(tileCols)
				#print "loaded tiles ok"
			
			elif len(k.split(","))==3:
				elems = k.split(",")
				code, x, y = elems[0].strip(), int(elems[1].strip()), int(elems[2].strip())
				if code == "tileElement":
					genre, direction = v.split(",")
					genre = genre.strip()
					direction = direction.strip()
					self.tiles[x][y].addElement(genre, direction)
				elif code == "item":
					pass
				
	
	
	#-------------------------------------------------------------------
	# save	
	def getSaveData(self):
		data = ""
		data += "x = %s\n" % self.X
		data += "y = %s\n" % self.Y
		
		data += "tilecode = "
		for y in range(self.Y):
			for x in range(self.X):
				data = data + self.dataCode[self.tiles[x][y].genre]
			#data += "\n"
		data += "\n"
		
		for x in range(self.X):
			for y in range(self.Y):
				tiledata = self.tiles[x][y].getSaveData()
				if tiledata:
					data += tiledata
		return data
	
	
	def save(self, filename):
		f = open(filename, "w")
		f.write(self.getSaveData())
		f.close()
		print "Level file saved as : %s" % (filename)
		
	def isInLevel(self, x, y):
		if not 0<=x<self.X:
			return False
		if not 0<=y<self.Y:
			return False
		return True
		
	def getTile(self, x, y):
		if not self.isInLevel(x, y):
			return None
		return self.tiles[x][y]
		
	def isOpen(self, x, y):
		if not self.isInLevel(x, y):
			return False
		
		if self.tiles[x][y]._open:
			return True
		return False
		
	def addToUpdate(self, x, y):
		if not self.isInLevel(x, y):
			return False
		if ((x, y) not in self.tilesToUpdate):
			self.tilesToUpdate.append((x, y))
			
	def removeToUpdate(self, x, y):
		if ((x, y) in self.tilesToUpdate):
			self.tilesToUpdate.remove((x, y))
	
	def addItem(self, item, x, y, slot):
		if not self.isInLevel(x, y):
			return
		tile = self.getTile(x, y)
		if not tile:
			return
		tile.addItem(item, slot)
		
	def removeItem(self, x, y, slot):
		if not self.isInLevel(x, y):
			return
		tile = self.getTile(x, y)
		if not tile:
			return
		tile.removeItem(slot)
		
	def addThrownItem(self, item, x, y, slot, direction):
		thrownItem = ThrownItem(item, self, x, y, slot, direction)
		self.thrownItems.append(thrownItem)
		
	def removeThrownItem(self, thrownItem):
		if thrownItem in self.thrownItems:
			self.thrownItems.remove(thrownItem)
