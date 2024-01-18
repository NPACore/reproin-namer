# Resources

# Pipeline
1. `00_dcm-rewrite-from-xlsx.py` rewrites `(0018, 1030) Protocol Name` using ReproIn conforming names in `7T-LunaSPA_ReproIn-SeqName.xlsx` (see sheet w/equations on [onedrive](https://pitt-my.sharepoint.com/:x:/g/personal/foran_pitt_edu/ERWaFHh1IRNCoIXmVds9QE8BzCRw-CqZGFjp4lqlOfOVmg?e=1fnslX))
1. `01_dcm-bids.sh` makes
```
bids/MRRC/SPA_Luna/20231103lunapilotspa2/sub-20231103lunapilotspa2/{anat,dwi,fmap,func}
```
with contents like
```
sub-20231103lunapilotspa2_acq-b0pfc_magnitude_dicom/
sub-20231103lunapilotspa2_acq-b0pfc_magnitude_heudiconv323_e1.nii.gz
sub-20231103lunapilotspa2_acq-b0pfc_magnitude_heudiconv323_e2.nii.gz
sub-20231103lunapilotspa2_acq-b0pfc_magnitude_heudiconv323_e3.nii.gz
sub-20231103lunapilotspa2_acq-b0pfc_magnitude_heudiconv323_e4.nii.gz
sub-20231103lunapilotspa2_acq-b0pfc_magnitude_heudiconv323_e5.nii.gz
```

See [`output-filelist.txt`](txt/output-filelist.txt) for full list.

# Outputs
[`Makefile`](Makefile) builds files in [`txt/`](txt/)

| file                | desc |
|-- |-- |
| [`input-orig.txt`](txt/input-orig.txt)      | original dicom headers per folder |
| [`input-repoin.txt`](txt/input-repoin.txt)  | edited dicom headers using `7T-LunaSPA_ReproIn-SeqName.xlsx` (`00_dcm-rewrite-from-xlsx.py`)|
| [`output-filelist.txt`](txt/output-filelist.txt) | heudiconv output: BIDS filelist |
| [`validate.txt`](txt/validate.txt)          | `bids-validator` output|

# Issues
* Does not pass bids validation. see [`validate.txt`](txt/validate.txt).
* how to encode session? only need in one sequence name?
* no `.json` files!? (see missing in [`output-filelist.txt`](txt/output-filelist.txt))
* have `_magnitude_heudiconv323_e1.nii.gz` but want `_echo-1_magnitude.nii.gz`
* path `SPA_Luna/20231103lunapilotspa2/sub-20231103lunapilotspa2` has redudant ID folder. Should be `SPA_Luna/sub-20231103lunapilotspa2`?
* `_dicom/` directoires are unwanted (but not a problem for Flywheel?) 

# Dicom Notes

* `00_dcm-rewrite-from-xlsx.py` edits `Protocol Name` and outputs to folders using `Series Number`. 
* `Study Description` sets output folder using `heudiconv --files`: `MRRC^SPA_Luna` becomes `bids/MRRC/SPA_Luna/`

| dicom header | example value |
|-- |--|
|`(0008, 1030) Study Description`| `LO: 'MRRC^SPA_Luna'`|
|`(0010, 0020) Patient ID`       | `LO: '20231103Luna_PilotSPA2` |
|`(0018, 1030) Protocol Name`    | `LO: 'mtgre_noMT'`|
|`(0020, 0011) Series Number`    | `IS: '48'`|
