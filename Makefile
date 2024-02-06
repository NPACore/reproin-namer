.PHONY: all clean
.SUFFIXES:

all: txt/output-filelist.txt txt/validate.txt txt/input-diff.txt txt/input-diff2.txt

.venv/bin/activate:
	./setup_env.bash

txt/input-orig.txt: | txt/
	# dcmdirtab from lncdtools: https://github.com/lncd/lncdtools
	dcmdirtab -d '/Volumes/Hera/Raw/MRprojects/SPA/Pilot/2*/DICOM/*' > $@

dcm-rehead/:
	./00_dcm-rewrite-from-xlsx.py

txt/input-reproin.txt: dcm-rehead/ $(wildcard dcm-rehead/2*/0*/)
	dcmdirtab -d 'dcm-rehead/2*/0*/' > $@

txt/input-diff.txt: txt/input-orig.txt txt/input-reproin.txt
	bash -c "diff -W 30 -wby <(cut -f 2-3 txt/input-orig.txt|sort -n) <(cut -f 2-3 txt/input-reproin.txt|sort -n) || :" > $@

txt/input-diff2.txt: txt/input-orig.txt txt/input-reproin.txt
	Rscript seqdiff.R > $@

bids/:  txt/input-reproin.txt .venv/bin/activate
	./01_dcm-bids.sh

txt/output-filelist.txt: bids/
	find bids/ -iname '*nii.gz' -or -iname '*json' > $@

bids/MRRC/SPA_Luna/20231103lunapilotspa2/.bidsignore: bidsignore
	cp $< $@

txt/validate.txt: bids/ bids/MRRC/SPA_Luna/20231103lunapilotspa2/.bidsignore
	# NB. last directory shouldn't exist? see readme issues
	bids-validator --no-color bids/MRRC/SPA_Luna/20231103lunapilotspa2/ |tee $@

%/:
	mkdir -p $@

clean:
	rm -rf bids/ dcm-rehead/
