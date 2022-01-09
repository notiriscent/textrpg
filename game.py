import random
from rpc import getrpc, gettime

enemies = ["Smorc", "Goblin", "Rat", "Zompig"]


def main():
	c = input("Select an action:\n\n1 - New Run\n\n2 - Exit\n\n3 - Skill Info\n\n\n>> ")
	if(c == "1"):
		newrun()
	elif(c == "2"):
		# getrpc().close()
		quit()
	elif(c == "3"):
		info()
	else:
		main()

def info():
	print("HP: Amount of health points entity has.\nDMG: Damage entity does\nACC: Chance that your player will hit the attack.\nMOV: Multiplier of chance that entity will dodge the attack.\n\n")
	main()

def newrun():
	plrdat = {"hp":0,"dmg":0,"acc":0,"mov":0,"type":""}
	c = input("Select hero type:\n\nArcher - very accurate yet easy to kill warrior, good against rats and goblins\nThief - weak but really sneaky guy, everyone hates him... WAIT WHERE DID MY GOLDEN WATCH GO?!?\nBerserk - strong but really inaccurate warrior, muscles.\n\n>>")
	if(c == "1" or c.lower() == "archer"):
		# Archer stats: hp = 3-6, dmg = 3-5, acc = 6-10, mov = 3-6
		plrdat["hp"] = random.randint(3,6)
		plrdat["dmg"] = random.randint(3,5)
		plrdat["acc"] = random.randint(6,10)
		plrdat["mov"] = random.randint(3,6)
		plrdat["type"] = "Archer"
		print("Your stats:\n\nHP: " + str(plrdat["hp"]) + "\nDMG: " + str(plrdat["dmg"]) + "\nACC: " + str(plrdat["acc"]) + "\nMOV: " + str(plrdat["mov"]))
		run(plrdat)
	elif(c == "2" or c.lower() == "thief"):
		# Thief stats: hp = 6-9, dmg = 2-5, acc = 7-9, mov = 6-9
		plrdat["hp"] = random.randint(6,9)
		plrdat["dmg"] = random.randint(2,5)
		plrdat["acc"] = random.randint(7,9)
		plrdat["mov"] = random.randint(6,9)
		plrdat["type"] = "Thief"
		print("Your stats:\n\nHP: " + str(plrdat["hp"]) + "\nDMG: " + str(plrdat["dmg"]) + "\nACC: " + str(plrdat["acc"]) + "\nMOV: " + str(plrdat["mov"]))
		run(plrdat)
	elif(c == "3" or c.lower() == "berserk"):
		# Berserk stats: hp = 9-13, dmg = 6-7, acc = 2-6, mov = 4-6
		plrdat["hp"] = random.randint(7,10)
		plrdat["dmg"] = random.randint(6,7)
		plrdat["acc"] = random.randint(2,6)
		plrdat["mov"] = random.randint(4,6)
		plrdat["type"] = "Berserk"
		print("Your stats:\n\nHP: " + str(plrdat["hp"]) + "\nDMG: " + str(plrdat["dmg"]) + "\nACC: " + str(plrdat["acc"]) + "\nMOV: " + str(plrdat["mov"]))
		run(plrdat)
	else:
		newrun()

class Enemy:
	def __init__(self, dat):
		self.stat = dat
	def getstatpretty(self):
		return "HP: " + str(self.stat["hp"]) + "\nDMG: " + str(self.stat["dmg"]) + "\nMOV: " + str(self.stat["mov"])
	def getstat(self):
		return self.stat
	def attack(self, plr):
		att = self.stat["dmg"]
		hp = plr["hp"]
		plr["hp"] -= att
		print(self.stat["type"] + " Attacked you and did " + str(att) + " damage!")

def run(dat):
	enem = random.choice(enemies)
	getrpc().update(details="Playing as " + dat["type"], state="Fighting with " + enem, large_image="icon", large_text="Text RPG 0.0.1", start=gettime())
	if(enem == "Rat"):
		enemstat = {"hp":random.randint(1,3),"dmg":random.randint(0,1),"mov":random.randint(1,5),"type":enem}
	elif(enem == "Smorc"):
		enemstat = {"hp":random.randint(2,6),"dmg":random.randint(1,4),"mov":random.randint(2,4),"type":enem}
	elif(enem == "Goblin"):
		enemstat = {"hp":random.randint(2,4),"dmg":random.randint(1,2),"mov":random.randint(4,7),"type":enem}
	elif(enem == "Zompig"):
		enemstat = {"hp":random.randint(4,7),"dmg":random.randint(3,5),"mov":random.randint(5,7),"type":enem}
	enemy = Enemy(enemstat)
	fight(dat, enemy)

def fight(plr, enem):
	print("\n\nYou are fighting " + enem.getstat()["type"] + " !\n\n")
	print("Its stats:\n" + enem.getstatpretty())
	c = input("\n\nSelect an action:\n1 - Attack\n2 - Check Your Stats\n3 - Run\n>> ")
	if(c == "1"):
		att = plr["dmg"]
		enemstat = enem.getstat()
		chance = random.randint(0,10)
		if(plr["acc"] - chance < enemstat["mov"]):
			print("\nYou missed your attack!")
			fight(plr,enem)
		else:
			enem.getstat()["hp"] -= att
		print("\nYou Attacked and did " + str(att) + " damage!" +"\n\nIts stats:\n" + enem.getstatpretty())
		if(enem.getstat()["hp"] <= 0):
			print("\nYou killed " + enem.getstat()["type"] + "! Skipping to the next enemy...")
			run(plr)
		else:
			enem.attack(plr)
			if(plr["hp"] <= 0):
				print("\n\nYou have no health left... Good luck next time!\n\n")
				main()
			else: 
				fight(plr, enem)
	elif(c == "2"):
		print("\n******\nYour stats:\n\nHP: " + str(plr["hp"]) + "\nDMG: " + str(plr["dmg"]) + "\nACC: " + str(plr["acc"]) + "\nMOV: " + str(plr["mov"]) + "\n******")
		fight(plr, enem)
	elif(c == "3"):
		chance = random.randint(1,9)
		skill = plr["mov"]
		if(skill<chance):
			print("\nYou tried to escape, but failed... You tripped and got killed.\n\n\n\n\n\n")
			getrpc().update(details="In Main Menu", state="Died last run...", large_image="icon", large_text="Text RPG 0.0.1", start=gettime())
			main()
		elif(skill>chance):
			print("\nYou tried to escape, and did it! Skipping to the next enemy...")
			run(plr)
		else:
			print("\nSomething went terribly wrong. . .\n\n\n")
			main()
	else:
		fight(plr, enem)

if __name__ == '__main__':
	main()