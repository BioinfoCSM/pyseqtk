#!/usr/bin/env python

import pandas as pd
import subprocess
from Bio import SeqIO
from Bio import SeqRecord
from utils.gunzip import gunzip
from pathlib import Path

class main : 

  #===initial method===
  def __init__ (self, args) : 
    self.args = args

  #===extract sequence by id list===
  def subseq_id_list (self) : 
    seq_index = {}
    try : 
      if self.args.fmt == "fasta" : 
        seq_index = SeqIO.index (self.args.fin, "fasta")
      else : 
         seq_index = SeqIO.index (self.args.fin, "fastq")
    except ValueError : 
      gunzip (self.args.fin) 
      if self.args.fmt == "fasta" : 
        seq_index = SeqIO.index (f"{Path (self.args.fin).name}_temp", "fasta")
      else : 
        seq_index = SeqIO.index (f"{Path (self.args.fin).name}_temp", "fastq")
    df = pd.read_csv (self.args.list, header = None)
    id_list = df.iloc [:, 0].tolist ()
    sr_list = [v for k,v in seq_index.items () if k in id_list]
    if self.args.fmt == "fasta" : 
      SeqIO.write (sr_list, self.args.fout, "fasta")
    else : 
      SeqIO.write (sr_list, self.args.fout, "fastq")
    if Path (f"{Path(self.args.fin).name}_temp").is_file () :
      subprocess.run (f"rm {Path(self.args.fin).name}_temp", shell = True, check = True)

  #===extract sequence by id bed===
  def subseq_id_bed (self) : 
    seq_index = {}
    try :
      if self.args.fmt == "fasta" :
        seq_index = SeqIO.index (self.args.fin, "fasta")
      else :
         seq_index = SeqIO.index (self.args.fin, "fastq")
    except ValueError :
      gunzip (self.args.fin)
      if self.args.fmt == "fasta" :
        seq_index = SeqIO.index (f"{Path (self.args.fin).name}_temp", "fasta")
      else :
        seq_index = SeqIO.index (f"{Path (self.args.fin).name}_temp", "fastq")    
    sr_list = []
    with open (self.args.bed) as fr : 
      for line in fr : 
        bed_list = line.strip ().split ("\t")
        idx, start, end = bed_list[0], bed_list[1], bed_list[2]
        sub_seq = seq_index [idx].seq[int(start)-1 : int (end)]
        sr = SeqRecord.SeqRecord (id = f"{idx}[{int(start)},{int(end)}]", description = seq_index[idx].description, seq = sub_seq)
        sr_list.append (sr) 
        if self.args.fmt == "fasta" : 
          SeqIO.write (sr_list, self.args.fout, "fasta")
        else : 
          SeqIO.write (sr_list, self.args.fout, "fastq")
    if Path (f"{Path(self.args.fin).name}_temp").is_file () :
      subprocess.run (f"rm {Path(self.args.fin).name}_temp", shell = True, check = True)


def excute (args) : 
  if args.list : 
    main (args = args).subseq_id_list ()
  elif args.bed : 
    main (args = args).subseq_id_bed ()
