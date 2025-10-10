#!/usr/bin/env python

import subprocess
from pathlib import Path
from Bio import SeqIO
from utils.gunzip import gunzip


def comp (args) : 
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
  with open (args.fout, "wt") as fw : 
    header = "\t".join (["id", "length", "number_of_A", "number_of_C", "number_of_G", "number_of_T", "number_of_U", "number_of_others", "number_of_CpG"]) + "\n"
    fw.write (header)
    for sr in seq_index.values () : 
      idx = sr.id
      seq_len = len (sr.seq)
      a_num = sr.seq.upper ().count ("A")
      c_num = sr.seq.upper ().count ("C")
      g_num = sr.seq.upper ().count ("G")
      t_num = sr.seq.upper ().count ("T")
      u_num = sr.seq.upper ().count ("U")
      others_num = seq_len - (a_num + c_num + g_num + t_num + u_num) 
      cg_num = sr.seq.upper ().count ("CG")
      mystr = "\t".join ([idx, str (seq_len), str (a_num), str (c_num), str (g_num), str (t_num), str (u_num), str (others_num), str (cg_num)]) + "\n"
      fw.write (mystr)
  if Path (f"{Path(args.fin).name}_temp").is_file () : 
    subprocess.run (f"rm {Path(args.fin).name}_temp", shell = True, check = True)
