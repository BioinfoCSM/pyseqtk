#!/usr/bin/env python

import random
import subprocess
from Bio import SeqIO
from pathlib import Path
 
def shuffle (args) : 
  try : 
    seq_index = SeqIO.index (args.fin, "fasta")
  except ValueError : 
    gunzip (args.fin)
    seq_index = SeqIO.index (f"{Path (args.fin).name}_temp", "fasta")
    sr_list = list (seq_index.values ())
    random.shuffle (sr_list)
    SeqIO.write (sr_list, args.fout, "fasta")
    subprocess.run (f"rm {Path (args.fin).name}_temp", shell = True, check = True) 
  else : 
    seq_index = SeqIO.index (args.fin, "fasta")
    sr_list = list (seq_index.values ())
    random.shuffle (sr_list)
    SeqIO.write (sr_list, args.fout, "fasta")
  if Path (f"{Path(args.fin).name}_temp").is_file () :
    subprocess.run (f"rm {Path(args.fin).name}_temp", shell = True, check = True)
