# Coded by Christopher Sabater Cordero, Washington DC

import sys
from data import main
from data.main import main
from data import constants as c

if __name__ == '__main__':
  if len(sys.argv) >= 3:
    print 'Error: Too many arguments passed to Pong.py'
  elif len(sys.argv) == 2 and (sys.argv[1] != '--debug' and sys.argv[1] != '--easy'):
    print 'Error: Unknown argument ', sys.argv[1]
  elif len(sys.argv) == 2 and sys.argv[1] == '--debug':
    main('DEBUG')
  elif len(sys.argv) == 2 and sys.argv[1] == '--easy':
    main('EASY')
  elif len(sys.argv) == 1:
    main('NORMAL')