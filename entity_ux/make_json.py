#!/usr/bin/env python3
import bidsschematools.schema as schema
from markdown import markdown
import json
import re

def write_json(fname, data):
    "quickly write json out from python object"
    with open(fname, 'w') as json_fh:
        json.dump(data, json_fh, default=lambda o: f'nonserial:{type(o)}')

# load and save full bids schema
bids = schema.load_schema()
ver = re.sub('-', '', bids['bids_version'])
bids_dict = bids.to_dict()
write_json(f'bids-all_ver-{ver}.json', bids_dict)


"""
build a table indexed by datatype. with list of suffix properties (display_name, description, entities)
>>> table.keys()
dict_keys(['anat', 'dwi', 'fmap', 'func', 'perf', 'pet'])
>>> table['anat'][0].keys()
dict_keys(['entities', 'value', 'display_name', 'description', 'unit'])

>>> bids_dict['rules']['files']['raw']['anat']['mp2rage']
{'suffixes': ['MP2RAGE'], 'extensions': ['.nii.gz', '.nii', '.json'], 'datatypes': ['anat'], 'entities': {'subject': 'required', 'session': 'optional', 'task': 'optional', 'acquisition': 'optional', 'ceagent': 'optional', 'reconstruction': 'optional', 'run': 'optional', 'echo': 'optional', 'flip': 'optional', 'inversion': 'required', 'part': 'optional', 'chunk': 'optional'}}

"""

# make html from descriptions
for obj in ['entities', 'suffixes']:
    for k in bids_dict['objects'][obj].keys():
        bids_dict['objects'][obj][k]['description'] = markdown(bids_dict['objects'][obj][k]['description'])

table = dict()
for keydesc, rules in bids_dict['rules']['files']['raw'].items():
    for rule in rules.values():

        # only care about nifti files (MR data)
        if '.nii' not in rule['extensions']:
            continue

        # get full entity information. repeats a lot of info but easy to query
        entities = {k: {**bids_dict['objects']['entities'][k], 'required': v}
                    for  k,v in rule['entities'].items()}
        # repeat entities and pull full object (desc, unit, display_name) for each suffix
        suffix_full = [{'entities': entities,
                        **bids_dict['objects']['suffixes'][i]} for i in rule['suffixes']]

        # NB. currently all datatypes of interest are only in one datatype?
        # shouldn't epi be repeated for fmap and func? sbref for func and dwi?
        for datatype in rule['datatypes']:
            if datatype in table.keys():
                table[datatype] += suffix_full
            else:
                table[datatype] = suffix_full

write_json(f'bids-table_ver-{ver}.json', table)
