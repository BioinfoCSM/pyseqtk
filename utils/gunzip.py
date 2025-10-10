#!/usr/bin/env python

import random
import subprocess
from pathlib import Path

def gunzip (fin) :
  temp = Path (fin).name + "_temp"
  subprocess.run (f"gunzip -c {fin} > {temp}", shell = True, check = True)



  
  
