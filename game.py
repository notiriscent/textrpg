import random
from rich.console import Console
from rpc import getrpc, gettime
import os

enemies = ["Smorc", "Goblin", "Rat", "Zompig"]

os.system('cls')

con = Console()

def main():
	c = con.input("[yellow bold]Select an action:[/]\n\n1 - New Run\n\n2 - Exit\n\n3 - Skill Info\n\n\n[green]>>[/] ")
	if(c == "1"):
		newrun()
	elif(c == "2"):
		getrpc().close()
		quit()
	elif(c == "3"):
		info()
	else:
		main()

def info():
	os.system('cls')
	con.print("[red bold]HP[/]: Amount of health points entity has.\n[yellow bold]DMG[/]: Damage entity does\n[cyan bold]ACC[/]: Chance that your player will hit the attack.\n[green bold]MOV[/]: Multiplier of chance that entity will dodge the attack. OR, chance of escaping the battle.\n\n")
	main()

def printinfo(plrdat):
	con.print("[yellow bold]Your stats[/]:\n\n[red bold]HP[/]: " + str(plrdat["hp"]) + "\n[yellow bold]DMG[/]: " + str(plrdat["dmg"]) + "\n[cyan bold]ACC[/]: " + str(plrdat["acc"]) + "\n[green bold]MOV[/]: " + str(plrdat["mov"]) + "\n")

def newrun():
	os.system('cls')
	plrdat = {"hp":0,"dmg":0,"acc":0,"mov":0,"type":""}
	c = con.input("[yellow bold]Select hero type[/]:\n\n[yellow bold]Archer[/] - very accurate yet easy to kill warrior, good against rats and goblins.\n[cyan bold]Thief[/] - weak but really sneaky guy, everyone hates him... WAIT WHERE DID MY GOLDEN WATCH GO?!?\n[red bold]Berserk[/] - strong but really inaccurate warrior, muscles.\n\n[green]>>[/] ")
	if(c == "1" or c.lower() == "archer"):
		# Archer stats: hp = 5-7, dmg = 3-5, acc = 7-10, mov = 3-6
		plrdat["hp"] = random.randint(5,7)
		plrdat["dmg"] = random.randint(2,4)
		plrdat["acc"] = random.randint(7,10)
		plrdat["mov"] = random.randint(3,6)
		plrdat["type"] = "Archer"
		os.system('cls')
		printinfo(plrdat)
		run(plrdat)
	elif(c == "2" or c.lower() == "thief"):
		# Thief stats: hp = 6-9, dmg = 2-5, acc = 7-9, mov = 6-9
		plrdat["hp"] = random.randint(6,9)
		plrdat["dmg"] = random.randint(1,3)
		plrdat["acc"] = random.randint(7,9)
		plrdat["mov"] = random.randint(6,9)
		plrdat["type"] = "Thief"
		os.system('cls')
		printinfo(plrdat)
		run(plrdat)
	elif(c == "3" or c.lower() == "berserk"):
		# Berserk stats: hp = 9-13, dmg = 6-7, acc = 4-6, mov = 4-6
		plrdat["hp"] = random.randint(7,10)
		plrdat["dmg"] = random.randint(4,5)
		plrdat["acc"] = random.randint(4,6)
		plrdat["mov"] = random.randint(4,6)
		plrdat["type"] = "Berserk"
		os.system('cls')
		printinfo(plrdat)
		run(plrdat)
	else:
		newrun()

class Enemy:
	def __init__(self, dat):
		self.stat = dat
	def getstatpretty(self):
		return "[red bold]HP[/]: " + str(self.stat["hp"]) + "\n[yellow bold]DMG[/]: " + str(self.stat["dmg"]) + "\n[green bold]MOV[/]: " + str(self.stat["mov"])
	def getstat(self):
		return self.stat
	def attack(self, plr):
		att = self.stat["dmg"]
		hp = plr["hp"]
		plr["hp"] -= att
		con.print("[red]" + self.stat["type"] + "[/] Attacked you and did " + str(att) + " damage!")
		return plr["hp"]

def run(dat):
	os.system('cls')
	enem = random.choice(enemies)
	getrpc().update(details="Playing as " + dat["type"], state="Fighting with " + enem, large_image="icon", large_text="Text RPG 0.0.1", start=gettime())
	if(enem == "Rat"):
		enemstat = {"hp":random.randint(1,3),"dmg":random.randint(0,1),"mov":random.randint(1,5),"type":enem}
	elif(enem == "Smorc"):
		enemstat = {"hp":random.randint(2,6),"dmg":random.randint(1,4),"mov":random.randint(2,4),"type":enem}
	elif(enem == "Goblin"):
		enemstat = {"hp":random.randint(2,4),"dmg":random.randint(1,2),"mov":random.randint(4,5),"type":enem}
	elif(enem == "Zompig"):
		enemstat = {"hp":random.randint(4,6),"dmg":random.randint(3,4),"mov":random.randint(3,5),"type":enem}
	enemy = Enemy(enemstat)
	fight(dat, enemy)

def pause(plr):
	con.input("\n\n[yellow bold]Select an action[/]:\n[cyan bold]any[/] - Go next\n[green]>>[/] ")
	run(plr)


def pausemain():
	con.input("\n\n[yellow bold]Select an action[/]:\n[cyan bold]any[/] - Go next\n[green]>>[/] ")
	os.system('cls')
	main()

def fight(plr, enem):
	#con.print("[red bold]HP[/]: " + str(plr["hp"]) + "  [yellow bold]DMG[/]: " + str(plr["dmg"]) + "  [cyan bold]ACC[/]: " + str(plr["acc"]) + "  [green bold]MOV[/]: " + str(plr["mov"]))
	con.print("\n\nYou are fighting [red]" + enem.getstat()["type"] + "[/] !\n\n")
	con.print("[yellow bold]Its stats[/]:\n" + enem.getstatpretty())
	c = con.input("\n\n[yellow bold]Select an action[/]:\n1 - Attack\n2 - Check Your Stats\n3 - Run\n4 - Main Menu\n[green]>>[/] ")
	if(c == "1"):
		att = plr["dmg"]
		enemstat = enem.getstat()
		chance = random.randint(0,3)
		if(plr["acc"] - chance < enemstat["mov"]):
			con.print("\n[red][-][/]You missed your attack!")
		else:
			enem.getstat()["hp"] -= att
			con.print("\n[green][+][/]You Attacked and did " + str(att) + " damage!" +"\n\n")
			if(enem.getstat()["hp"] <= 0):
				con.print("\n[yellow][!][/]You killed [red]" + enem.getstat()["type"] + "[/]! Skipping to the next enemy...")
				pause(plr)
		
		plrhpn = enem.attack(plr)
		if(plrhpn <= 0):
			con.print("\n\n[red][!][/]You have no health left... Good luck next time!\n\n")
			getrpc().update(details="In Main Menu", state="Died last run...", large_image="icon", large_text="Text RPG 0.0.1", start=gettime())
			pausemain()
		else: 
			fight(plr, enem)
	elif(c == "2"):
		con.print("\n******\n[yellow bold]Your stats[/]:\n\n[red bold]HP[/]: " + str(plr["hp"]) + "\n[yellow bold]DMG[/]: " + str(plr["dmg"]) + "\n[cyan bold]ACC[/]: " + str(plr["acc"]) + "\n[green bold]MOV[/]: " + str(plr["mov"]) + "\n******")
		fight(plr, enem)
	elif(c == "3"):
		chance = random.randint(1,9)
		skill = plr["mov"]
		if(skill<chance):
			con.print("\n[red][!][/]You tried to escape, but failed... You tripped and got killed.\n\n\n\n\n\n")
			getrpc().update(details="In Main Menu", state="Died last run...", large_image="icon", large_text="Text RPG 0.0.1", start=gettime())
			pausemain()
		elif(skill>chance):
			con.print("\n[green][+][/]You tried to escape, and did it! Skipping to the next enemy...")
			pause(plr)
		else:
			con.print("\n[red][-][/]Something went terribly wrong. . .\n\n\n")
			pausemain()
	elif(c == "4"):
		cc = con.input("\n[red][-] Are you sure? [/]\n[green]>> [/][yellow](y/N) [/]")
		if(cc.lower() == "y"):
			pausemain()
		elif(cc.lower() == "n"):
			fight(plr, enem)
		else:
			fight(plr, enem)
	else:
		fight(plr, enem)

if __name__ == '__main__':
	main()