#!/usr/bin/env python3
import pydicom
import os
import os.path
from glob import glob
import pandas as pd

seq_conv = pd.read_excel("./7T-LunaSPA_ReproIn-SeqName.xlsx").rename(
    columns={"new reproIn seq name": "new_name"}
)
raw_root = "/Volumes/Hera/Raw/MRprojects/SPA/Pilot/"
for i, row in seq_conv.iterrows():
    if (
        pd.isna(row["new_name"])
        or pd.isna(row["seqno_oldseqname"])
        or pd.isna(row["folder"])
    ):
        continue

    print(f"{row['folder']}/{row['seqno_oldseqname']} => {row['new_name']}")
    old_folder = os.path.join(raw_root, row["folder"], "DICOM", row["seqno_oldseqname"])
    for ex_dcm_file in glob(os.path.join(old_folder, "*IMA")):
        ex_dcm = pydicom.dcmread(ex_dcm_file)
        # (0018, 1030) Protocol Name                       LO: 'mtgre_noMT'
        # (0010, 0020) Patient ID                          LO: '20231103Luna_PilotSPA2
        # (0008, 1030) Study Description                   LO: 'MRRC^SPA_Luna'
        #
        # (0020, 0012) Acquisition Number                  IS: '1'

        new_prot = pydicom.DataElement(
            value=row["new_name"], VR="LO", tag=(0x0018, 0x1030)
        )
        out_dir = f"{int(ex_dcm[(0x0020,0x0012)].value):03d}_{row['new_name']}"
        out_dir = os.path.join("dcm-rehead", ex_dcm[(0x0010, 0x0020)].value, out_dir)
        new_file = os.path.join(out_dir, os.path.basename(ex_dcm_file))
        if os.path.exists(new_file):
            break  # have one have them all

        ex_dcm[(0x0018, 0x1030)] = new_prot
        os.makedirs(out_dir, exist_ok=True)
        ex_dcm.save_as(new_file)
        #break  # only write one

# heudiconv -f reproin -o bids/ -d './{session}Luna{subject}_SPA2/new/*/*IMA' -s 20231103LunaPilot_SPA2

# heudiconv -f reproin -o bids/ --files dcm-rehead/2*/0*/*IMA
# # INFO: Study session for StudySessionInfo(locator='MRRC/SPA_Luna', session=None, subject='20231103lunapilotspa2')
# # INFO: PROCESSING STARTS: {'subject': '20231103lunapilotspa2', 'outdir': '/Volumes/Hera/Projects/SPA/scripts/reproin/bids/MRRC/SPA_Luna', 'session': None}

# bids/MRRC/SPA_Luna/20231103lunapilotspa2/sub-20231103lunapilotspa2/anat/sub-20231103lunapilotspa2_acq-noMT_MTR.nii.gz
