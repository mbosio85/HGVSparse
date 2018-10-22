
# HGVSparse
Simple utility to parse HGVS to VCF (and optionally annotate them with local installation of `[Ensembl-vep](https://github.com/Ensembl/ensembl-vep)`) 

### Usage example
For a quick example run the provided example.sh. 
This tool requires to have a fasta reference file (chrX provided) and an annotated transcript file
The example focuses on MECP2 gene, here the GTF transcript file example, required to infer the mutation type:

    0 NC_000023.11 X - 1 156040895 1 156040895 10 67092175,67096251,67103237,67111576,67113613,67115351,67125751,67127165,67131141,67134929, 6  
7093604,67096321,67103382,67111644,67113756,67115464,67125909,67127257,67131227,67134971, 0 C1orf141 none none -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,

The example also requires to specify region names to keep for parsing. In this case, we chose to process HGVS entries from `NC_000023.11:g.,NM_004992.3:c.`  **[-r line in example.sh ]**


    ## example.sh ##
    # 1st: unzip the fasta file
    gzip -d example/chrX.fa.gz
    # 2nd: make the output directory
    mkdir -p example/results
    # 3rd: run the conversion tool
    sh HGVS_to_VEP.sh \
      -i example/variants_in.txt \
      -o example/results \
      -p test \
      -g example/chrX.fa \
      -t example/chrx.txt \
      -r NC_000023.11:g.,NM_004992.3:c.
    
#### Run with VEP local annotaion
This requires a local installation of Ensembl-vep with the appropriate cache and fasta references.
It also requires to have dbNSFP and  dbscSNV plugins installed.
To add the VEP annotation, add a `-v` flag to the execution line of `HGVS_to_VEP.sh` call

