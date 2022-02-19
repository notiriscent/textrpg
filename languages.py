import json
from rich.console import Console
from game import stop_game

def load_lang(type):
	try:
		with open(lang + ".json") as f:
			return json.load(f)
	except:
		con.print("[red bold]\n\n\nGame locales are corrupted, please send this message to github issues page of the game!\n\n\n[/]")
		stop_game()