.PHONY: all clean
.SUFFIXES:

.ONESHELL:
all: txt/validate.txt txt/input-diff.txt

.ONESHELL:
examples/dicom/6/: examples/
	cd examples
	wget https://github.com/user-attachments/files/15515915/gre_phantom_dcm_nii.zip
	unzip gre_phantom_dcm_nii.zip
	cd dicom/
	mkdir {5,6}
	mv TESTBR.MR.DEV-SCHIRDA_041119_BRAINO.0005.* 5
	mv TESTBR.MR.DEV-SCHIRDA_041119_BRAINO.0006.* 6

.venv/bin/activate:
	./setup_env.bash

dcm-rehead/: examples/dicom/6/ | .venv/bin/activate
	source .venv/bin/activate && \
	dicom-rewrite-pname -o $@/5 -n fmap_acq-dwi examples/dicom/5/*
	dicom-rewrite-pname -o $@/6 -n fmap_acq-dwi examples/dicom/6/*

bids/:  dcm-rehead/
	./01_dcm-bids.sh $</*/

txt/validate.txt:	bids/ 
	# NB. last directory shouldn't exist? see readme issues
	bids-validator --verbose --no-color bids/dev/schirda/041119_BRAINO/testbr/ |tee $@

#### diffing checking name changes
txt/input-orig.txt: | txt/
	# dcmdirtab from lncdtools: https://github.com/lncd/lncdtools
	dcmdirtab -d 'examples/dicom/*' > $@

txt/input-reproin.txt: dcm-rehead/ $(wildcard dcm-rehead/*)
	dcmdirtab -d 'dcm-rehead/*' > $@

txt/input-diff.txt: txt/input-orig.txt txt/input-reproin.txt
	bash -c "diff -W 30 -wby <(cut -f 2-3 txt/input-orig.txt|sort -n) <(cut -f 2-3 txt/input-reproin.txt|sort -n) || :" > $@

txt/input-diff2.txt: txt/input-orig.txt txt/input-reproin.txt
	Rscript seqdiff.R > $@

txt/output-filelist.txt: bids/
	find bids/ -iname '*nii.gz' -or -iname '*json' > $@

%/:
	mkdir -p $@

clean:
	rm -rf bids/ dcm-rehead/ txt/input-*.txt
