# Environment
python>=3.7
***
# Description
A python implementation of seqtk-lightweigth tools for processing biological sequences in FASTA/Q format.
# Deployment
## clone
```
git clone https://github.com/BioinfoCSM/pyseqtk.git
```
## set environment
```
chmod 755 pyseqtk
echo 'export PATH="path/pyseqtk:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
## install package
```
pip install biopython
pip install pandas
```
# Usage
```
pyseqtk -h
```
```
usage: pyseqtk [-h] {sample,sort,shuffle,subseq,find,size,comp,fqchk,mergepe} ...

A toolkit for processing FASTA/Q files

options:
  -h, --help            show this help message and exit

subcommands:
  python pyseqtk <subcommand> <arguments>

  {sample,sort,shuffle,subseq,find,size,comp,fqchk,mergepe}
    sample              subsample sequences
    sort                sort by sequence length
    shuffle             shuffle the sequence
    subseq              extract subsequences from FASTA/Q
    find                find sequences by sequence
    size                report the number of sequences and bases
    comp                get the nucleotide composition of FASTA/Q
    fqchk               fastq QC (base/quality summary)
    mergepe             interleave two PE FASTA/Q files
```
***
# Info
* Author:BioinfoCSM(Siming Cheng)
* Email:simoncheng158@gmail.com
