import pydicom
import os
import os.path
import re
from glob import glob
import pandas as pd

# (0018, 1030) Protocol Name      LO: 'mtgre_noMT'
# (0010, 0020) Patient ID         LO: '20231103Luna_PilotSPA2
# (0008, 1030) Study Description  LO: 'MRRC^SPA_Luna'


def name_from_dicom(ex_dcm_file: str, basedir="dcm-rehead") -> os.PathLike:
    "use seq number and pat info to set output dir"
    ex_dcm = pydicom.dcmread(ex_dcm_file)
    seq_num = int(ex_dcm[(0x0020, 0x0011)].value)
    seq_dir = f"{seq_num:03d}_{row['new_name']}"
    patid = ex_dcm[(0x0010, 0x0020)].value
    session_dir = patid + "_ses-" + session
    out_dir = os.path.join(basedir, session_dir, seq_dir)
    return out_dir


def change_protocol_name(new_name: str, seq_file_list: list, out_dir: os.PathLike):
    """
    run through list of dicom files and update
    """
    for ex_dcm_file in seq_file_list:
        ex_dcm = pydicom.dcmread(ex_dcm_file)
        # setup what the new file should be called
        # use seq number, old folder (for session), and patient id
        # keeps dicom file name the same
        new_file = os.path.join(out_dir, os.path.basename(ex_dcm_file))
        if os.path.exists(new_file):
            break  # have one have them all

        # all of above for this: rewrite header for reporin protocol name
        new_prot = pydicom.DataElement(value=new_name, VR="LO", tag=(0x0018, 0x1030))
        ex_dcm[(0x0018, 0x1030)] = new_prot

        # and save out
        os.makedirs(out_dir, exist_ok=True)
        ex_dcm.save_as(new_file)
        # print(f"# {out_dir}")
        # break  # only write one


def dicom_rewrite_pname():
    """
    cli tool to rename protocol tag. called as dicom-rewrite-pname
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Change dicom header protocol name to test heudiconv ReproIn heuristic"
    )
    parser.add_argument(
        "-n",
        "--new_name",
        required=True,
        help="New protocol name to insert into (0018,1030) tag",
    )
    parser.add_argument(
        "-o",
        "--output_folder",
        required=True,
        help="Directory to save new dicoms with modified protocol name",
    )
    parser.add_argument("filename", nargs="+")
    args = parser.parse_args()
    change_protocol_name(args.new_name, args.filename, args.output_folder)


if __name__ == "__main__":
    dicom_rewrite_pname()
