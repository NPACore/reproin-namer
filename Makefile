SHELL := /bin/bash
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
	mkdir 5 6
	mv TESTBR.MR.DEV-SCHIRDA_041119_BRAINO.0005.* 5
	mv TESTBR.MR.DEV-SCHIRDA_041119_BRAINO.0006.* 6

.venv/bin/activate:
	./setup_env.bash

# want to rename each dicom's acquistion name stored in the header
# will match reproin format (BIDS-like)
# ISSUE: one scanner sequence produces two folders. one should be fmap-mag the other fmap-phase
#        but can only set one name (at the scanner). so leave off the '-mag' or '-phase'
.ONESHELL:
dcm-rehead/: examples/dicom/6/ | .venv/bin/activate
	# rename 's/[-_]//g' examples/dicom/[56]/*
	# NB!! why kill the - and _ separaters in the original files?
	#      probably don't want to touch these
	#      we are only testing what happens if we change the dicom acq. seq. name
	#      we can't control the actual output file names
	#
	. .venv/bin/activate
	dicom-rewrite-pname -o dcm-rehead/5 -n fmap_acq-dwi examples/dicom/5/*
	dicom-rewrite-pname -o dcm-rehead/6 -n fmap_acq-dwi examples/dicom/6/*

txt/input-reproin.txt: dcm-rehead/ $(wildcard dcm-rehead/*)
	dcmdirtab -d 'dcm-rehead/*' > $@
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
