#!/usr/bin/env python

import subprocess
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from utils.gunzip import gunzip
from pathlib import Path

def find (args) : 
  seq_index = {}
  try : 
    seq_index = SeqIO.index (args.fin, "fasta")
  except ValueError : 
    gunzip (args.fin)
    seq_index = SeqIO.index (f"{Path (args.fin).name}_temp", "fasta")
  else : 
    seq_index = SeqIO.index (args.fin, "fasta")
  sr_list = []
  for k,v in seq_index.items () : 
    start = v.seq.find (args.pattern)
    if start == -1 : 
      continue
    else : 
      sr = SeqRecord (id = seq_index[k].id, description = f"start_position:{start+1}", seq = seq_index[k].seq)
      sr_list.append (sr)
      SeqIO.write (sr_list, args.fout, "fasta")
  subprocess.run (f"rm {Path (args.fin).name}_temp", shell = True, check = True)
