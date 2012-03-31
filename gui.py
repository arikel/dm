#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import os
from level import *
from player import *

pygame.font.init()
FONT = pygame.font.Font("fonts/Verdana.ttf", 12)

#-----------------------------------------------------------------------
# gui functions
#-----------------------------------------------------------------------

def wordWrap(msg, longueur, font=FONT):
	msg = msg.replace("\n", " ")
	wordsToAdd = msg.strip().split(" ")
	#print "words to add : %s" % (wordsToAdd)
	lines = []
	currentLine = ""
	lastGoodLine = ""
	for word in wordsToAdd:
		currentLine += " " + word
		if font.size(currentLine)[0]>= longueur:
			lastGoodLine = lastGoodLine.strip()
			lines.append(lastGoodLine)
			currentLine = word
			
		else:
			lastGoodLine = currentLine
	lines.append(lastGoodLine)
	return lines

#-----------------------------------------------------------------------
# generic widgets
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
# Button
class Button(pygame.Rect):
	def __init__(self, x, y, imgPath, name="button", dx=0, dy=0):
		self.name = name
		self.img = pygame.image.load(imgPath)
		w = self.img.get_width()
		h = self.img.get_height()
		self.func = None
		self.params = None
		pygame.Rect.__init__(self, x, y, w, h)
		self.dx = dx
		self.dy = dy
		
	def setOffset(self, dx, dy):
		self.dx = dx
		self.dy = dy
	
	def is_hover(self):
		x, y = pygame.mouse.get_pos()
		return self.collidepoint(x-self.dx, y-self.dy)
	hover = property(is_hover)
		
	def blit(self, screen):
		screen.blit(self.img, self)
		
	def bind(self, func, params=[]):
		self.func = func
		self.params = params	
		
	def onClick(self):
		#print "button clicked"
		if self.func:
			#print "command sent"
			print "function %s found, params are %s" % (self.func, self.params)
			if self.params:
				self.func(self.params)
			else:
				self.func()
		else:
			print "button %s doesn't have any function binded" % (self.name)

#-----------------------------------------------------------------------
# Label
class Label(Button):
	def __init__(self, x, y, text, name = "label", color = (255,0,0,255), dx=0, dy=0):
		self.name = name
		self.text = text
		self.color = color
		self.img = FONT.render(text, False, color, (0,255,0,255))
		w, h = self.img.get_width(), self.img.get_height()
		pygame.Rect.__init__(self, x, y, w, h)
		pygame.draw.rect(self.img, self.color, (0,0,w,h),1)
		self.setText(text)
		
		self.func = None
		self.params = None
		self.setOffset(dx, dy)
		
	def setText(self, text):
		self.text = text
		self.textimg = FONT.render(self.text, False, (20,20,20), (200,200,200,255))
		self.w, self.h = self.textimg.get_width(), self.textimg.get_height()
		self.img = pygame.surface.Surface((self.w, self.h))
		self.img.fill((0,0,0))
		self.img.blit(self.textimg, (0,0))

	def setOffset(self, dx, dy):
		self.dx = dx
		self.dy = dy
		
#-----------------------------------------------------------------------
# game widgets
#-----------------------------------------------------------------------

class VBar(pygame.Rect):
	def __init__(self, val, maxval, x, y, w, h, color = (255,0,0)):
		self.maxval = maxval
		self.val = val
		self.color = color
		pygame.Rect.__init__(self, (x, y), (w, h))
		
	def setPos(self, x, y):
		self.x = x
		self.y = y
		
	def blit(self, screen):
		h = float(self.h) * (float(self.val)/float(self.maxval))
		pygame.draw.rect(screen, self.color, (self.x, self.y-h, self.w, h-1))
		
class HBar(pygame.Rect):
	def __init__(self, val, maxval, x, y, w, h, color = (255,0,0)):
		self.maxval = maxval
		self.val = val
		self.color = color
		pygame.Rect.__init__(self, (x, y), (w, h))
		
	def setPos(self, x, y):
		self.x = x
		self.y = y
		
	def blit(self, screen):
		w = float(self.w) * (float(self.val)/float(self.maxval))
		pygame.draw.rect(screen, self.color, (self.x, self.y, w, self.h))
		

class IconImageLoader(object):
	def __init__(self):
		self.img = {}
		for f in os.listdir("graphics/icons/"):
			name = f.replace(".png", "")
			self.loadImg(name)
		
	def loadImg(self, name):
		path = "graphics/icons/" + name + ".png"
		img = pygame.image.load(path)
		self.img[name] = img
		
	def getImg(self, name):
		if name in self.img:
			return self.img[name]
		return None

class PortraitLoader(object):
	def __init__(self):
		self.img = {}
		for f in os.listdir("graphics/portraits/"):
			name = f.replace(".png", "")
			self.loadImg(name)
		
	def loadImg(self, name):
		path = "graphics/portraits/" + name + ".png"
		img = pygame.image.load(path)
		self.img[name] = img
		
	def getImg(self, name):
		if name in self.img:
			return self.img[name]
		return None
		
iconLoader = IconImageLoader()
portraitLoader = PortraitLoader()


#-----------------------------------------------------------------------
# Button
class ItemSlotButton(pygame.Rect):
	def __init__(self, x, y, name="button", genre="generic", baseImg = None, dx=0, dy=0):
		self.name = name
		w, h = 32, 32
		self.func = None
		self.params = None
		pygame.Rect.__init__(self, x, y, w, h)
		self.dx = dx
		self.dy = dy
		
		self.img = pygame.surface.Surface((self.w, self.h))
		self.img.fill((90,90,90))
		if baseImg:
			self.baseImg = pygame.image.load("graphics/icons/" + baseImg + ".png")
			self.img.blit(pygame.transform.scale(self.baseImg, (32,32)), (0,0))
		else:
			self.baseImg = None
		self.item = None
		
	def setOffset(self, dx, dy):
		self.dx = dx
		self.dy = dy
		
	def setbaseImg(self, imgName):
		self.baseImg = pygame.image.load("graphics/icons/" + imgName + ".png")
		self.img.blit(pygame.transform.scale(self.baseImg, (32,32)), (0,0))
		
	def setItem(self, item):
		self.item = item
		
	def removeItem(self):
		self.item = None
		
	def hasItem(self):
		if self.item:
			return True
		return False
		
	def is_hover(self):
		x, y = pygame.mouse.get_pos()
		return self.collidepoint(x-self.dx, y-self.dy)
		
	hover = property(is_hover)
		
	def blit(self, screen):
		self.img.fill((90,90,90))
		if self.baseImg:
			self.img.blit(pygame.transform.scale(self.baseImg, (32,32)), (0,0))
		if self.item:
			img = iconLoader.getImg(self.item.name)
			if img:
				self.img.blit(pygame.transform.scale(img, (32,32)), (0,0))
		screen.blit(self.img, self)
		
	def bind(self, func, params=[]):
		self.func = func
		self.params = params	
		
	def onClick(self):
		#print "button clicked"
		if self.func:
			#print "command sent"
			#print "function %s found, params are %s" % (self.func, self.params)
			if self.params:
				self.func(self.params)
			else:
				self.func()
		else:
			print "button %s doesn't have any function binded" % (self.name)

class PlayerSheet(pygame.Rect):
	def __init__(self, player, x=0, y=94):
		self.player = player
		w, h = 560,400
		pygame.Rect.__init__(self, x, y, w, h)
		self.img = pygame.surface.Surface((self.w, self.h))
		self.img.fill((120,120,120))
		self.bg = pygame.image.load("graphics/icons/sheet.png")
		
		self.slots = {}
		
		
		
		j = 0
		for i in range(8):
			slot = ItemSlotButton(210+i*34, 60, "bag_"+str(j), "generic", None, self.x, self.y)
			self.slots["bag_"+str(j)] = slot
			j += 1
			
		for i in range(9):
			slot = ItemSlotButton(176+i*34, 94, "bag_"+str(j), "generic", None, self.x, self.y)
			self.slots["bag_"+str(j)] = slot
			j += 1
		
		self.slots["bag_8"].setbaseImg("bag")
		
		self.slots["left_hand"] = ItemSlotButton(20,155, "left_hand", "left_hand", "left_hand", self.x, self.y)
		self.slots["right_hand"] = ItemSlotButton(155,155, "right_hand", "right_hand", "right_hand",self.x, self.y)
		
		self.slots["neck"] = ItemSlotButton(20,105, "neck", "neck", "neck", self.x, self.y)
		self.slots["head"] = ItemSlotButton(87,87, "head", "head", "head", self.x, self.y)
		
		self.slots["torso"] = ItemSlotButton(87,137, "torso", "torso", "torso", self.x, self.y)
		self.slots["legs"] = ItemSlotButton(87,187, "legs", "legs", "legs",self.x, self.y)
		
		self.slots["feet"] = ItemSlotButton(87,237, "feet", "feet", "feet",self.x, self.y)
		
		self.slots["weapon_0"] = ItemSlotButton(155,210, "weapon_0", "weapon", "equip",self.x, self.y)
		self.slots["weapon_1"] = ItemSlotButton(189,210, "weapon_1", "weapon", None, self.x, self.y)
		self.slots["weapon_2"] = ItemSlotButton(155,244, "weapon_2", "weapon", None, self.x, self.y)
		self.slots["weapon_3"] = ItemSlotButton(189,244, "weapon_3", "weapon", None, self.x, self.y)
		
		self.slots["purse_0"] = ItemSlotButton(20,210, "purse_0", "purse", "purse", self.x, self.y)
		self.slots["purse_1"] = ItemSlotButton(20,244, "purse_1", "purse", None, self.x, self.y)
		
		self.foodbar = HBar(100, 100, 300, 210, 150, 15, color = (255,150,20))
		self.waterbar = HBar(100,100, 300, 290, 150, 15, color= (0,20,250))
		
	def update(self):
		if self.player.leader:
			color = (250,180,0)
		else:
			color = (250,250,250)
				
		#self.img.blit(self.bg, (0,0))
		self.img.fill((120,120,120))
		self.img.blit(FONT.render(self.player.name.upper(), 0, color), (10,10))
		
		for slot in self.slots:
			self.slots[slot].item = self.player.inventory.getItem(slot)
			self.slots[slot].blit(self.img)
		
		self.foodbar.blit(self.img)
		self.waterbar.blit(self.img)
		
	def blit(self, screen):
		screen.blit(self.img, self)
		
class PlayerMedaillon(pygame.Rect):
	def __init__(self, player):
		self.player = player
		x = self.player.rank * 122
		y = 2
		w = 120
		h = 80
		if self.player.rank == 0:
			self.color = (250,0,0)
		elif self.player.rank == 1:
			self.color = (0,0,250)
		elif self.player.rank == 2:
			self.color = (0,250,0)
		elif self.player.rank == 3:
			self.color = (250,250,0)
			
		pygame.Rect.__init__(self, (x, y, w,h))
		
		self.img = pygame.surface.Surface((w,h))
		self.left_hand = ItemSlotButton(2,40,"left_hand", "left_hand", "left_hand", self.x, self.y)
		self.right_hand = ItemSlotButton(36,40,"right_hand", "right_hand", "right_hand", self.x, self.y)
		
		self.hp = VBar(self.player.getCarac("hp"), self.player.getCarac("hpmax"),
			76, 76, 10, 70, self.color)
			
		self.sp = VBar(self.player.getCarac("sp"), self.player.getCarac("spmax"),
			90, 76, 10, 70, self.color)
			
		self.mp = VBar(self.player.getCarac("mp"), self.player.getCarac("mpmax"),
			104, 76, 10, 70, self.color)
		
		self.state = "closed" # actually the state of the character sheet of the player
		self.portrait = portraitLoader.getImg(self.player.name)
		self.portrait = pygame.transform.scale(self.portrait, (self.portrait.get_width()*2, self.portrait.get_height()*2))
		
		self.update()
		
	def is_hover(self):
		x, y = pygame.mouse.get_pos()
		#return self.collidepoint((x-self.x, y-self.y))
		return self.collidepoint(x, y)
		
	hover = property(is_hover)
		
	def update(self):
		self.img.fill((120,120,120))
		
		if self.state == "closed":
			
			if self.player.leader:
				color = (250,180,0)
			else:
				color = (250,250,250)
				
			self.img.blit(FONT.render(self.player.name.upper(), 0, color), (2,2))
			self.left_hand.item = self.player.inventory.getItem("left_hand")
			self.left_hand.blit(self.img)
			self.right_hand.item = self.player.inventory.getItem("right_hand")
			self.right_hand.blit(self.img)
		else:
			self.img.blit(self.portrait, (5,7))
		
		self.hp.blit(self.img)
		self.sp.blit(self.img)
		self.mp.blit(self.img)
		
	def blit(self, screen):
		screen.blit(self.img, (self.player.rank*122+2, 2))
		
		
class GameGui(object):
	def __init__(self, game):
		self.game = game
		self.party = self.game.party
		self.updateParty()
		
	def updateParty(self):
		self.displaySheet = None # (when a sheet is open : PlayerSheet object)
		self.playerSheets = []
		for p in self.party.players:
			self.playerSheets.append(PlayerSheet(p))
		
		self.playerMedaillons = []
		for p in self.party.players:
			self.playerMedaillons.append(PlayerMedaillon(p))
	
	def openSheet(self, rank):	
		for medaillon in self.playerMedaillons:
			medaillon.state = "closed"
			
		self.playerMedaillons[rank].state = "open"
		self.displaySheet = self.playerSheets[rank]
		
	def closeSheet(self):
		for medaillon in self.playerMedaillons:
			medaillon.state = "closed"
		self.displaySheet = None
	
	def onClickRight(self):
		for medaillon in self.playerMedaillons:
			if medaillon.hover:
				if medaillon.state == "open":
					self.closeSheet()
				else:
					self.openSheet(medaillon.player.rank)
				return
		
		if not self.displaySheet and self.party.leader:
			self.openSheet(self.party.leader.rank)
		else:
			self.closeSheet()
		self.game.onRightClick()
		
	def onClickLeft(self):
		for medaillon in self.playerMedaillons:
			if medaillon.hover:
				rank = medaillon.player.rank
				if self.displaySheet:
					if self.displaySheet.player.rank == rank:
						self.onClickLeftMedaillon_sheet_open(rank)
						return
				self.onClickLeftMedaillon_sheet_closed(rank)
				return
		if self.displaySheet:
			self.onClickSheet()
			return
		
		self.game.onLeftClick()
		
	def onClickLeftMedaillon_sheet_closed(self, rank):
		medaillon = self.playerMedaillons[rank]
		if medaillon.left_hand.hover:
			print "handle left hand for %s" % (medaillon.player.name)
			self.onClickContainer(rank, "left_hand")
			
		elif medaillon.right_hand.hover:
			print "handle right hand for %s" % (medaillon.player.name)
			self.onClickContainer(rank, "right_hand")
			
		else:
			self.party.setLeader(rank)
	
	def onClickContainer(self, rank, slotName):
		item = self.party.players[rank].inventory.slots[slotName]
		if item:
			if self.game.handItem:
				self.party.players[rank].inventory.slots[slotName], self.game.handItem = self.game.handItem, self.party.players[rank].inventory.slots[slotName]
			else:
				self.game.handItem = item
				self.party.players[rank].inventory.slots[slotName] = None
		else:
			if self.game.handItem:
				self.party.players[rank].inventory.slots[slotName] = self.game.handItem
				self.game.handItem = None
			else:
				print "%s slot clicked, no item inside, no item in hand" % (slotName)
	
	def onClickLeftMedaillon_sheet_open(self, rank):
		medaillon = self.playerMedaillons[rank]
		self.party.setLeader(rank)
	
	def onClickSheet(self):
		rank = self.displaySheet.player.rank
		for slotName in self.displaySheet.slots:
			if self.displaySheet.slots[slotName].hover:
				
				#item = self.displaySheet.slots[slot].item
				item = self.party.players[rank].inventory.slots[slotName]
				
				if item:
					print "item %s found in slot %s" % (item.name, slotName)
					if self.game.handItem:
						self.party.players[rank].inventory.slots[slotName], self.game.handItem = self.game.handItem, self.party.players[rank].inventory.slots[slotName]
						
					else:
						self.game.handItem = item
						self.party.players[rank].inventory.slots[slotName] = None
						
				else:
					if self.game.handItem:
						print "putting %s in %s" % (self.game.handItem.name, slotName)
						self.party.players[rank].inventory.slots[slotName] = self.game.handItem
						self.game.handItem = None
					else:
						print "%s slot clicked, no item inside, no item in hand" % (slotName)
	
	def handleEvents(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 3:
					self.onClickRight()
				
				elif event.button == 1:
					self.onClickLeft()
					
			if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.game.running = False
	
	def blit(self, screen):
		if self.displaySheet:
			self.displaySheet.update()
			self.displaySheet.blit(screen)
		#print self.playerMedaillons	
		for medaillon in self.playerMedaillons:
			medaillon.update()
			medaillon.blit(screen)
	

	
	
