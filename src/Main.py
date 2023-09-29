import sys

import Log

from Game import Game

if __name__ == '__main__':
	Log.getLogger().setLevel(Log.DEBUG)
	Log.msg(Log.DEBUG, 'Creating new Game()...')
	game = Game()
	Log.msg(Log.DEBUG, 'Entering game main()...')
	result = game.main()
	Log.msg(Log.DEBUG, f"main() returned with value {result}.")
	sys.exit(result)

