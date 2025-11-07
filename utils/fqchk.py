#!/usr/bin/env python

import re
import math
from Bio import SeqIO
import subprocess
from pathlib import Path
from utils.gunzip import gunzip

#======
def get_seq_index (args) : 
  seq_index = {}
  try : 
    seq_index = SeqIO.index (args.fin, "fastq")
  except ValueError : 
    gunzip (args.fin)
    seq_index = SeqIO.index (f"{Path (args.fin).name}_temp", "fastq")
  else : 
    seq_index = SeqIO.index (args.fin, "fastq")
  return seq_index

#======
def length_summary (args) : 
  seq_index = get_seq_index (args = args)
  with open (args.fout, "wt") as fw : 
    sr_list = [v for v in seq_index.values ()]
    min_len = len (sorted (sr_list, key = lambda x : len (x.seq))[0].seq)
    max_len = len (sorted (sr_list, key = lambda x : len (x.seq))[-1].seq)
    total_len = sum ([len (v.seq) for v in seq_index.values ()])
    total_count = len (seq_index)
    avg_len = "{:.2f}".format (total_len/total_count)
    mystr = f"min_len: {min_len}; max_len: {max_len}; avg_len: {avg_len};" + "\n"
    header = "\t".join (["POS", "#bases", "%A", "%C", "%G", "%T", "%N", "avgQ", "errQ", "%low", "%high"]) + "\n"
    fw.write (mystr)
    fw.write (header)
    return max_len

#======
def all_stat (args) : 
  seq_index = get_seq_index (args = args)
  with open (args.fout, "wt") as fw : 
    total_len = sum ([len (v.seq) for v in seq_index.values ()])
    total_base = "".join ([str (v.seq) for v in seq_index.values ()])
    a_content = "{:.1f}".format (len (re.findall ("A", total_base))/len (total_base)*100)
    c_content = "{:.1f}".format (len (re.findall ("C", total_base))/len (total_base)*100)
    g_content = "{:.1f}".format (len (re.findall ("G", total_base))/len (total_base)*100)
    t_content = "{:.1f}".format (len (re.findall ("T", total_base))/len (total_base)*100)
    n_content = "{:.1f}".format (len (re.findall ("N", total_base))/len (total_base)*100)
    avgQ = "{:.1f}".format (sum ([sum (v.letter_annotations["phred_quality"]) for v in seq_index.values ()])/total_len)
    q_list = [v.letter_annotations["phred_quality"] for v in seq_index.values ()]
    q_list_new = []
    for subq_list in q_list : 
      q_list_new.extend ([10**(-q/10) for q in subq_list])
    errQ = "{:.1f}".format (-10*math.log10 (sum (q_list_new)/len (q_list_new)))
    q_list_low = []
    for subq_list in q_list : 
      q_list_low.extend ([q for q in subq_list if q < args.quality ])
    low_content = "{:.1f}".format ((len (q_list_low)/total_len)*100)
    high_content = 100 - float (low_content)
    mystr = "\t".join (["ALL", str (total_len), str (a_content), str (c_content), str (g_content), str (t_content), str (n_content), str (avgQ), str (errQ), str (low_content), str (high_content)]) + "\n"
    fw.write (mystr)

#======
def pos_stat (args) : 
  with open (args.fout, "at") as fw :
    seq_index = get_seq_index (args = args)
    max_len = length_summary (args = args)
    for pos in range (1, max_len+1) : 
      pos_len = len ([v for v in seq_index.values () if len (v.seq) >= pos])
      pos_base = "".join ([v.seq[pos-1] for v in seq_index.values () if len (v.seq) >= pos])
      a_content = "{:.1f}".format ((len (re.findall ("A", pos_base))/pos_len)*100)
      c_content = "{:.1f}".format ((len (re.findall ("C", pos_base))/pos_len)*100)
      g_content = "{:.1f}".format ((len (re.findall ("G", pos_base))/pos_len)*100)
      t_content = "{:.1f}".format ((len (re.findall ("T", pos_base))/pos_len)*100)
      n_content = "{:.1f}".format ((len (re.findall ("N", pos_base))/pos_len)*100)
      avgQ = "{:.1f}".format (sum ([v.letter_annotations["phred_quality"][pos-1] for v in seq_index.values () if len (v.seq) >= pos])/pos_len)
      q_list = [v.letter_annotations["phred_quality"][pos-1] for v in seq_index.values () if len (v.seq) >= pos]
      errQ = "{:.1f}".format (-10*math.log10 (sum ([10**(-q/10) for q in q_list])/pos_len))
      low_content = "{:.1f}".format ((len ([q for q in q_list if q < args.quality])/pos_len)*100)
      high_content = 100 - float (low_content)
      mystr = "\t".join ([str (pos), str (pos_len), str (a_content), str (c_content), str (g_content), str (t_content), str (n_content), str (avgQ), str (errQ), str (low_content), str (high_content)]) + "\n"
      fw.write (mystr)

#======
def execute (args) : 
  length_summary (args = args)
  all_stat (args = args) 
  pos_stat (args = args)
  subprocess.run (f"rm {Path(args.fin).name}_temp", shell = True, check = True)


 

