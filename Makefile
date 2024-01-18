.PHONY: all clean
.SUFFIXES: txt/output-filelist.txt

all: txt/output-filelist.txt txt/validate.txt txt/input-diff.txt

txt/input-orig.txt: | txt/
	# dcmdirtab from lncdtools: https://github.com/lncd/lncdtools
	dcmdirtab -d '/Volumes/Hera/Raw/MRprojects/SPA/Pilot/2*/DICOM/*' > $@

dcm-rehead/:
	./00_dcm-rewrite-from-xlsx.py

txt/input-repoin.txt: dcm-rehead/ $(wildcard dcm-rehead/2*/0*/) 
	dcmdirtab -d 'dcm-rehead/2*/0*/' > $@

txt/input-diff.txt: txt/input-orig.txt txt/input-repoin.txt
	bash -c "diff -y <(cut -f 2-4 txt/input-orig.txt|sort) <(cut -f 2-4 txt/input-repoin.txt|sort) || :" > $@

bids/: txt/input-repoin.txt
	./01_dcm-bids.sh

txt/output-filelist.txt: bids/
	find bids/ -iname '*nii.gz' -or -iname '*json' > $@

txt/validate.txt: bids/
	# NB. last directory shouldn't exist? see readme issues
	bids-validator --no-color bids/MRRC/SPA_Luna/20231103lunapilotspa2/ |tee $@

%/:
	mkdir -p $@

clean:
	rm -rf bids/ dcm-rehead/
