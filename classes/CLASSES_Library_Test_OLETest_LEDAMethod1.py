# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

import os
os.chdir("c:/Program Files/Python/Tools/idle")
try:
    import PyShell
    PyShell.main()
except SystemExit:
    raise
except:
    import traceback
    traceback.print_exc()
    raw_input("Hit return to exit...")



