# Coded by Christopher Sabater Cordero, Washington DC

import sys
from data import main
from data.main import main

if __name__ == '__main__':
  if len(sys.argv) >= 3:
    print 'Error: Too many arguments passed to Pong.py'
  elif len(sys.argv) == 2 and sys.argv[1] != '--debug':
    print 'Error: Unknown argument ', sys.argv[1]
  elif len(sys.argv) == 2 and sys.argv[1] == '--debug':
    main('DEBUG')
  elif len(sys.argv) == 1:
    main('NORMAL')