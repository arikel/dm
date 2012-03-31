#!/usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------
# Item
#-------------------------------------------------------------------


class Item(object):
	def __init__(self, name):
		self.name = name
		self.weight = 0.1
		
		# TODO : medium, big? it's to check if it will pass through a fence or not, but maybe this will have to change and take character's dexterity into account, will see later.
		self.size = "small"
		
		self.container = False
		self.edible = False
		self.weapon = False
		self.shield = False
		self.ammo = False
		self.ammoWeapon = [] # slinger, bow, crossbow...

	def getWeight(self):
		# to redefine for containers
		return self.weight
		

#-------------------------------------------------------------------
# PlayerInventory
#-------------------------------------------------------------------
class PlayerInventory(object):
	def __init__(self):
		self.slots = {}
		for i in range(17):
			name = "bag_" + str(i)
			self.slots[name] = None
		for name in ["left_hand", "right_hand", "neck", "head", "torso", "legs", "feet", "purse_0", "purse_1", "weapon_0", "weapon_1", "weapon_2", "weapon_3"]:
			self.slots[name] = None
		
	def getItem(self, slotName):
		if slotName in self.slots:
			return self.slots[slotName]
		return None
		
	def setItem(self, slotName, item):
		self.slots[slotName] = item
		
	def removeItem(self, slot):
		self.slots[slot] = None
		
	
#-------------------------------------------------------------------
# Player
#-------------------------------------------------------------------
class Player(object):
	def __init__(self, name, rank=0):
		self.name = name
		self.rank = rank # rank in the players list of the party
		self.position = rank # position in the party
		self.leader = False
		self.carac = {}
		
		self.xp = {"warrior":0, "ninja":0, "priest":0, "wizard":0}
		
		self.setCarac("hp", 30)
		self.setCarac("hpmax", 30)
		self.setCarac("sp", 30)
		self.setCarac("spmax", 30)
		self.setCarac("mp", 30)
		self.setCarac("mpmax", 30)
		
		self.setCarac("strength", 1)
		self.setCarac("dexterity", 1)
		self.setCarac("wisdom", 1)
		self.setCarac("vitality", 1)
		self.setCarac("antimagic", 1)
		self.setCarac("antifire", 1)
		
		self.setCarac("food", 100)
		self.setCarac("foodmax", 100)
		self.setCarac("water", 100)
		self.setCarac("watermax", 100)
		
		self.inventory = PlayerInventory()
		
	def getCarac(self, carac):
		if carac in self.carac:
			return self.carac[carac]
		return 0
		
	def setCarac(self, carac, n):
		self.carac[carac] = n
		
	def addCarac(self, carac, n):
		if carac in self.carac:
			self.carac[carac] += n
		else:
			self.setCarac(carac, n)

#-------------------------------------------------------------------
# PlayerParty
#-------------------------------------------------------------------
class PlayerParty(object):
	def __init__(self):
		self.players = []
		self.leader = None
		
	def addPlayer(self, player):
		if len(self.players)==4:
			print "no more than 4 players allowed"
			return
		self.players.append(player)
		if len(self.players)==1:
			self.leader = self.players[0]
			self.players[0].leader = True
			
	def setLeader(self, rank):
		for p in self.players:
			if p.rank != rank:
				print "%s is not a leader" % (p.name)
				p.leader = False
			else:
				p.leader = True
				self.leader = p
				print "%s is now the leader" % (p.name)
	
	
	
