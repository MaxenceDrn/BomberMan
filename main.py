#!/usr/bin/python3

import sys
from Application import Application, Window

app = Application(sys.argv)
win = Window()
sys.exit(app.exec_())