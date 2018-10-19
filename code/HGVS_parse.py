import pyhgvs as hgvs
import pyhgvs.utils as hgvs_utils
from pygr.seqdb import SequenceFileDB
import sys
import argparse



parser = argparse.ArgumentParser(description = 'Parse HGVS to VCF')
parser.add_argument('--infile', type=str, dest='infile', required=True, help='Input file [required]')
parser.add_argument('--outfile', type=str, dest='outfile', required=True, help='Output  [required]')
parser.add_argument('--ref', type=str, dest='ref', required=True, help='FASTA file with reference [required]')
parser.add_argument('--transcript',  type=str, dest='transcript', required=True, help='transcript file [required]')
args = parser.parse_args()


# Read genome sequence using pygr.
#genome = SequenceFileDB('/data/resources/fasta/grch38/GRCh38.primary_assembly.genome.fa')
genome = SequenceFileDB(args.ref)

# Read RefSeq transcripts into a python dict.
#with open('/home/mbosio/projects/rtt/code/chrx.txt') as infile:
with open(args.transcript) as infile:
    transcripts = hgvs.utils.read_transcripts(infile)

# Provide a callback for fetching a transcript by its name.
def get_transcript(name):
    return transcripts.get(name)

with open(args.infile) as rd,open(args.outfile,'w') as wr:
    wr.write('\t'.join(['#Chr','Start','End','Ref','Alt','Group']) + '\n')
    for line in rd:
        #print line.strip()

        try:
            a = hgvs.HGVSName(line.strip())
            a.chrom='X'
            outlist  = hgvs.get_vcf_allele(a,genome)
            outlist = [str(x) for x in outlist]
            outlist.append('Cases')
            wr.write('\t'.join(outlist)+'\n')
         
        except :
            wr.write('Error:%s %s \n'%(line.strip(),sys.exc_info()[0]))
            print line.strip()
            print sys.exc_info()[0]
            pass
        
