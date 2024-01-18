#!/usr/bin/env bash

heudiconv `#-c none --command ls` -f reproin -o bids/ --files dcm-rehead/2*/0*/

# makes bids/MRRC/SPA_Luna/20231103lunapilotspa2/sub-20231103lunapilotspa2/{anat,dwi,fmap,func}

# # INFO: Study session for StudySessionInfo(locator='MRRC/SPA_Luna', session=None, subject='20231103lunapilotspa2')
# # INFO: PROCESSING STARTS: {'subject': '20231103lunapilotspa2', 'outdir': '/Volumes/Hera/Projects/SPA/scripts/reproin/bids/MRRC/SPA_Luna', 'session': None}

# heudiconv -f reproin -o bids/ -d 'dcm-rehead/{subject}SPA2/*/*IMA' -s 20231103Luna_Pilot


# bids/MRRC/SPA_Luna/20231103lunapilotspa2/sub-20231103lunapilotspa2/anat/sub-20231103lunapilotspa2_acq-noMT_MTR.nii.gz
