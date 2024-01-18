
# Pipeline
1. `00_dcm-rewrite-from-xlsx.py` rewrites `(0018, 1030) Protocol Name` using ReproIn conforming names in `7T-LunaSPA_ReproIn-SeqName.xlsx`
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

# Outputs
[`Makefile`](Makefile) builds files in [`txt/`](txt/)

| file                | desc |
|-- |-- |
| [`input-orig.txt`](txt/input-orig.txt)      | original dicom headers per folder |
| [`input-repoin.txt`](txt/input-repoin.txt)  | edited dicom headers using `7T-LunaSPA_ReproIn-SeqName.xlsx` (`00_dcm-rewrite-from-xlsx.py`)|
| [`output-filelist.txt`](txt/output-filelist.txt) | heudiconv output: BIDS filelist |

# Issues

* no `.json` files!?
* have `_magnitude_heudiconv323_e1.nii.gz` but want `_echo-1_magnitude.nii.gz`
* path `SPA_Luna/20231103lunapilotspa2/sub-20231103lunapilotspa2` has redudant ID folder. Should be `SPA_Luna/sub-20231103lunapilotspa2`?
* `_dicom/` directoires are unwanted (but not a problem for Flywheel?) 
