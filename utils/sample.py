#!/usr/bin/env python

import math
import random
import subprocess
from Bio import SeqIO

class main () : 

#===initial method===
  def __init__ (self, args) : 
    self.args = args

#===subsequence of fasta===
  def sample_fa (self) : 
    try : 
      seq_index = SeqIO.index (self.args.fin, "fasta")
    except ValueError : 
      temp_fa = str (random.randint (1, 1_000_000)) + "_temp.fa"
      subprocess.run (f"gunzip -c {self.args.fin} > {temp_fa}", shell = True, check = True)
      seq_index = SeqIO.index (temp_fa, "fasta")
      random.seed (self.args.seed)
      sample_id = ""
      if self.args.num :
        sample_id = random.sample (list (seq_index.keys ()), self.args.num)
      else : 
        sample_id = random.sample (list (seq_index.keys ()), math.ceil (len (seq_index)*self.args.frac))
      seq_index_new = {k : v for k,v in seq_index.items () if k in sample_id}
      SeqIO.write (seq_index_new.values (), self.args.fout, "fasta")
      subprocess.run (f"rm {temp_fa}", shell = True, check = True)
    else : 
      seq_index = SeqIO.index (self.args.fin, "fasta")
      random.seed (self.args.seed)
      sample_id = ""
      if self.args.num :
        sample_id = random.sample (list (seq_index.keys ()), self.args.num)
      else :
        sample_id = random.sample (list (seq_index.keys ()), math.ceil 
(len (seq_index)*self.args.frac))
      seq_index_new = {k : v for k,v in seq_index.items () if k in sample_id}
      SeqIO.write (seq_index_new.values (), self.args.fout, "fasta")

#===subsequence of fastq===
  def sample_fq (self) : 
    try :
      seq_index = SeqIO.index (self.args.fin, "fastq")
    except ValueError : 
      temp_fq = str (random.randint (1, 1_000_000)) + "_temp.fq"
      subprocess.run (f"gunzip -c {self.args.fin} > {temp_fq}", shell = True, check = True)
      seq_index = SeqIO.index (f"{temp_fq}", "fastq")
      random.seed (self.args.seed)
      sample_id = ""
      if self.args.num :
        sample_id = random.sample (list (seq_index.keys ()), self.args.num)
      else :
        sample_id = random.sample (list (seq_index.keys ()), math.ceil 
(len (seq_index)*self.args.frac))
      seq_index_new = {k : v for k,v in seq_index.items () if k in sample_id}
      SeqIO.write (seq_index_new.values (), self.args.fout, "fastq") 
      subprocess.run (f"rm {temp_fq}", shell = True, check = True)
    else : 
      seq_index = SeqIO.index (self.args.fin, "fastq")
      random.seed (self.args.seed)
      sample_id = ""
      if self.args.num :
        sample_id = random.sample (list (seq_index.keys ()), self.args.num)
      else :
        sample_id = random.sample (list (seq_index.keys ()), math.ceil 
(len (seq_index)*self.args.frac))
      seq_index_new = {k : v for k,v in seq_index.items () if k in sample_id}
      SeqIO.write (seq_index_new.values (), self.args.fout, "fastq")


def execute (args) : 
  if args.fmt == "fasta" : 
    main (args = args).sample_fa ()
  else : 
    main (args = args).sample_fq ()

