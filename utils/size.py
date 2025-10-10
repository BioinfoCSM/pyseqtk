#!/usr/bin/env python

import subprocess
from Bio import SeqIO
from utils.gunzip import gunzip
from pathlib import Path

def size (args) : 
  seq_index = {}
  try : 
    if args.fmt == "fasta" : 
      seq_index = SeqIO.index (args.fin, "fasta")
    else : 
      seq_index = SeqIO.index (args.fin, "fastq")
  except ValueError : 
    gunzip (args.fin)
    if args.fmt == "fasta" : 
      seq_index = SeqIO.index (f"{Path(args.fin).name}_temp", "fasta")
    else : 
      seq_index = SeqIO.index (f"{Path(args.fin).name}_temp", "fastq")
  else : 
    if args.fmt == "fasta" : 
      seq_index = SeqIO.index (args.fin, "fasta")
    else :
      seq_index = SeqIO.index (args.fin, "fastq")
  seq_num = len (seq_index)
  base_num = 0
  for v in seq_index.values () : 
    base_num += len (v.seq) 
  mystr = f"""number of sequences : {seq_num}
number of bases : {base_num}"""
  print (mystr)
  subprocess.run (f"rm {Path(args.fin).name}_temp", shell = True, check = True)
