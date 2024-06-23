#!/usr/bin/env python3
"""
"""
import pandas as pd
import reproin_namer

def rename_with_xlsx(xlsx_file, raw_root):
    """with spreadsheet file containing
      'new reproIn seq name', 'folder','seqno_oldseqname', and 'new_name'
    """
    seq_conv = pd.read_excel(xslx_file).rename(
        columns={"new reproIn seq name": "new_name"}
    )
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


        dcm_list = os.path.join(old_folder, "*IMA")
        out_dir = name_from_dicom(dcm_list[0])
        print(f"{session} {row['seqno_oldseqname']} => {row['new_name']} ({len(seq_file_list)} dicom)")
        change_protocol_name(row["new_name"], dcm_list, out_dir)

if __name__ == "__main__":
    xlsx_file = "./7T-LunaSPA_ReproIn-SeqName.xlsx"
    raw_root = "/Volumes/Hera/Raw/MRprojects/SPA/Pilot/"
    rename_with_xlsx(xlsx_file, raw_root)

# heudiconv -f reproin -o bids/ -d './{session}Luna{subject}_SPA2/new/*/*IMA' -s 20231103LunaPilot_SPA2

# heudiconv -f reproin -o bids/ --files dcm-rehead/2*/0*/*IMA
# # INFO: Study session for StudySessionInfo(locator='MRRC/SPA_Luna', session=None, subject='20231103lunapilotspa2')
# # INFO: PROCESSING STARTS: {'subject': '20231103lunapilotspa2', 'outdir': '/Volumes/Hera/Projects/SPA/scripts/reproin/bids/MRRC/SPA_Luna', 'session': None}

# bids/MRRC/SPA_Luna/20231103lunapilotspa2/sub-20231103lunapilotspa2/anat/sub-20231103lunapilotspa2_acq-noMT_MTR.nii.gz
