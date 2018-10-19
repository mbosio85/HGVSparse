
set -e
  ## Try to set some flags
  #  -i : input file
  #  -o : output folder
  #  -p : output prefix
  #  -c : code folder with the script. Default './'
  #  -v : execute VEP locally or not 
  #  -g : fasta reference file
  #  -t : transcript file :see example/chrx.txt


alias python='/home/mbosio/anaconda2/bin/python'
CODE='/home/mbosio/projects/rtt/code/'
CODE='./code/'
VEP='FALSE'
dbNSFP='/data/resources/vep/dbNSFP.gz'
dbscSNV='/data/resources/vep/dbscSNV1.1_GRCh38.txt.gz'

  while getopts 'i:o:p:c:g:t:v' flag; do
    case "${flag}" in
      i) INFILE="${OPTARG}" ;;
      o) OUTFOLDER="${OPTARG}" ;;
      p) PREFIX="${OPTARG}" ;;
      c) CODE="${OPTARG}" ;;
      g) REF="${OPTARG}" ;;
      t) TRANSCRIPT="${OPTARG}" ;;
      v) VEP="TRUE" ;; 
      *) "Unexpected option ${flag}" ;;
    esac
  done

echo "############################################"
echo "#Step 1 : parse the data from excel to HGVS like "
echo "############################################"

  python $CODE/parse_vars.py $INFILE > $OUTFOLDER/$PREFIX"_HGVS_parsed.txt"
  echo "Done"
  echo " " 


echo "############################################"
echo "#Step 2 : extract only the parsed column for VCF parsing"
echo "############################################"

  awk -F '\t' '{print $4}' < $OUTFOLDER/$PREFIX"_HGVS_parsed.txt" > $OUTFOLDER/$PREFIX"_HGVS_input.txt"

  echo "Done"
  echo " "

echo "############################################"
echo "#Step3  : parse to VCF"
echo "############################################"

 python $CODE/HGVS_parse.py \
	--infile $OUTFOLDER/$PREFIX"_HGVS_input.txt" \
	--outfile $OUTFOLDER/$PREFIX".vcf" \
        --ref $REF \
        --transcript $TRANSCRIPT  &> $OUTFOLDER/$PREFIX"_step3.log"


 grep    Error $OUTFOLDER/$PREFIX".vcf"    > $OUTFOLDER/$PREFIX".error.vcf" 
 grep -v Error $OUTFOLDER/$PREFIX".vcf"    > $OUTFOLDER/$PREFIX".ok.vcf"


echo "Done"
echo " "
echo ">>>>>>>>>  VCF to annotate :  $OUTFOLDER/$PREFIX".ok.vcf" <<<<<<<<"
echo " "


if (( $VEP = 'TRUE' )) ; then

	echo "############################################"
        echo "#Step 4 : Annotate with VEP" 
	echo "############################################"
        ~/software/ensembl-vep/vep  --cache \
         -i $OUTFOLDER/$PREFIX".ok.vcf"  \
         -o $OUTFOLDER/$PREFIX"_annotated.txt"  \
          --everything \
         --format vcf \
         --flag_pick \
         --force_overwrite \
         --plugin dbNSFP,$dbNSFP \
         --plugin dbscSNV,$dbscSNV
       
       echo "############################################"
       echo "#Step 5 extract protein position for the variants"
       echo "############################################"

       python $CODE/parse_vep_for_protein_place.py $OUTFOLDER/$PREFIX"_annotated.txt" > $OUTFOLDER/$PREFIX"_R_full_input.tsv"
        # grep -e 'Uploaded_variation' -e 'PICK' $OUTFOLDER/$PREFIX"_R_full_input.tsv" > $OUTFOLDER/$PREFIX"_R_picked_input.tsv"
    
       head -n1 $OUTFOLDER/$PREFIX"_R_full_input.tsv" > $OUTFOLDER/$PREFIX"_R_picked_input.tsv"
       
       awk '$20 == "1" { print $0 }'  $OUTFOLDER/$PREFIX"_R_full_input.tsv" >> $OUTFOLDER/$PREFIX"_R_picked_input.tsv"

else
   echo "############################################"
   echo 'Step4-5 not executed. Add -v flag to run it'
   echo "It requires to specify dbNSFP and dbscSNV plugins"
   echo "############################################"

 fi
