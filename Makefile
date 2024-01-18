.PHONY: all
.SUFFIXES: txt/output-filelist.txt

all: txt/output-filelist.txt

txt/input-orig.txt: | txt/
	dcmdirtab -d '/Volumes/Hera/Raw/MRprojects/SPA/Pilot/2*/DICOM/*' > $@

dcm-rehead/:
	./00_dcm-rewrite-from-xlsx.py

txt/input-repoin.txt: dcm-rehead/ $(wildcard dcm-rehead/2*/0*/) 
	dcmdirtab -d 'dcm-rehead/2*/0*/' > $@

bids/: txt/input-repoin.txt
	./01_dcm-bids.sh

txt/output-filelist.txt: bids | txt/
	find bids/ -iname '*nii.gz' -or -iname '*json' > $@

%/:
	mkdir -p $@
