## example.sh ##
# 1st: unzip the fasta file
  gzip -d example/chrX.fa.gz
# 2nd: make the output directory
   mkdir -p example/results
# 3rd: run the conversion tool
 sh HGVS_to_VEP.sh \
	-i example/variants_in.txt  \
	-o example/results  \
	-p test \
	-g example/chrX.fa  \
	-t example/chrx.txt \
        -r NC_000023.11:g.,NM_004992.3:c.
	
