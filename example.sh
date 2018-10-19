gzip -d example/chrX.fa.gz
mkdir -p example/results
sh HGVS_to_VEP.sh \
	-i example/variants_in.txt  \
	-o example/results  \
	-p test \
	-g example/chrX.fa  \
	-t example/chrx.txt 
