#!/usr/bin/env python

from Bio import SeqIO
from utils.gunzip import gunzip
from pathlib import Path

def mergepe (args) : 
  seq_index1 = seq_index2 = {} 
  try : 
    seq_index1 = SeqIO.index (args.fq1, "fastq") 
    seq_index2 = SeqIO.index (args.fq2, "fastq")
  except ValueError : 
    gunzip (args.fq1) 
    seq_index1 = SeqIO.index (f"{Path(args.fq1).name}_temp", "fastq")
    gunzip (args.fq2)
    seq_index2 = SeqIO.index (f"{Path(args.fq2).name}_temp", "fastq")
  else : 
    seq_index1 = SeqIO.index (args.fq1, "fastq")
    seq_index2 = SeqIO.index (args.fq2, "fastq")
  sr_list1 = [v for v in seq_index1.values ()]
  sr_list2 = [v for v in seq_index2.values ()]
  sr_list_new = []
  for i in list (range (0, len(seq_index1))) : 
    sr_list_new.append (sr_list1[i]) 
    sr_list_new.append (sr_list2[i])
  SeqIO.write (sr_list_new, args.fout, "fastq")

