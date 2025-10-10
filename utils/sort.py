#!/usr/bin/env python

import subprocess
from Bio import SeqIO
from pathlib import Path
from utils.gunzip import gunzip

def sort (args) : 
  try :
    seq_index = SeqIO.index (args.fin, "fasta")
  except ValueError : 
    gunzip (fin = args.fin)
    seq_index = SeqIO.index (f"{Path (args.fin).name}_temp", "fasta") 
    seq_sort = []
    if args.reverse : 
      seq_sort = sorted (list (seq_index.values ()), key = lambda x : len (x.seq), reverse = True)
    else : 
      seq_sort = sorted (list (seq_index.values ()), key = lambda x : len (x.seq), reverse = False)
    SeqIO.write (seq_sort, args.fout, "fasta")
    subprocess.run (f"rm {Path (args.fin).name}_temp", shell = True, check = True) 
  else : 
    seq_index = SeqIO.index (args.fin,  "fasta")
    seq_sort = []
    if args.reverse :
      seq_sort = sorted (list (seq_index.values ()), key = lambda x : len (x.seq), reverse = True)
    else : 
      seq_sort = sorted (list (seq_index.values ()), key = lambda x : len (x.seq), reverse = False)
    SeqIO.write (seq_sort, args.fout, "fasta")
  if Path (f"{Path(args.fin).name}_temp").is_file () :
    subprocess.run (f"rm {Path(args.fin).name}_temp", shell = True, check = True)
