#!/usr/bin/env python3
import pydicom
import os
import os.path
import re
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

    # final protocol won't save out derivatives (e.g. moco, tenesorFA)
    # skip to save space and time
    if re.search('deriv|dwi.*_desc-',row["new_name"]):
        print(f'# skipping derivative {row["new_name"]}')
        continue

    old_folder = os.path.join(raw_root, row["folder"], "DICOM", row["seqno_oldseqname"])
    session = row["folder"]

    seq_file_list = glob(os.path.join(old_folder, "*IMA"))
    print(f"{session} {row['seqno_oldseqname']} => {row['new_name']} ({len(seq_file_list)} dicom)")
    for ex_dcm_file in seq_file_list:
        ex_dcm = pydicom.dcmread(ex_dcm_file)
        # (0018, 1030) Protocol Name                       LO: 'mtgre_noMT'
        # (0010, 0020) Patient ID                          LO: '20231103Luna_PilotSPA2
        # (0008, 1030) Study Description                   LO: 'MRRC^SPA_Luna'

        # setup what the new file should be called
        # use seq number, old folder (for session), and patient id
        # keeps dicom file name the same
        seq_num = int(ex_dcm[(0x0020,0x0011)].value)
        seq_dir = f"{seq_num:03d}_{row['new_name']}"
        patid = ex_dcm[(0x0010, 0x0020)].value
        session_dir = patid + '_ses-' + session
        out_dir = os.path.join("dcm-rehead", session_dir, seq_dir)
        new_file = os.path.join(out_dir, os.path.basename(ex_dcm_file))
        if os.path.exists(new_file):
            break  # have one have them all

        # all of above for this: rewrite header for reporin protocol name
        new_prot = pydicom.DataElement(
            value=row["new_name"], VR="LO", tag=(0x0018, 0x1030)
        )
        ex_dcm[(0x0018, 0x1030)] = new_prot

        # and save out
        os.makedirs(out_dir, exist_ok=True)
        ex_dcm.save_as(new_file)
        #print(f"# {out_dir}")
        #break  # only write one

# heudiconv -f reproin -o bids/ -d './{session}Luna{subject}_SPA2/new/*/*IMA' -s 20231103LunaPilot_SPA2

# heudiconv -f reproin -o bids/ --files dcm-rehead/2*/0*/*IMA
# # INFO: Study session for StudySessionInfo(locator='MRRC/SPA_Luna', session=None, subject='20231103lunapilotspa2')
# # INFO: PROCESSING STARTS: {'subject': '20231103lunapilotspa2', 'outdir': '/Volumes/Hera/Projects/SPA/scripts/reproin/bids/MRRC/SPA_Luna', 'session': None}

# bids/MRRC/SPA_Luna/20231103lunapilotspa2/sub-20231103lunapilotspa2/anat/sub-20231103lunapilotspa2_acq-noMT_MTR.nii.gz
