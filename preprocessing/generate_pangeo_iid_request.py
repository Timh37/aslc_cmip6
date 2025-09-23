#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 16:00:35 2025

@author: timhermans
"""

from pangeo_forge_esgf.parsing import parse_instance_ids
import intake

def zstore_to_iid(zstore: str):
    # this is a bit whacky to account for the different way of storing old/new stores
    iid =  '.'.join(zstore.replace('gs://','').replace('.zarr','').replace('.','/').split('/')[-11:-1])
    if not iid.startswith('CMIP6'):
        iid =  '.'.join(zstore.replace('gs://','').replace('.zarr','').replace('.','/').split('/')[-10:])
    return iid

def search_iids(col_url:str):
    col = intake.open_esm_datastore(col_url)
    iids_all= [zstore_to_iid(z) for z in col.df['zstore'].tolist()]
    return [iid for iid in iids_all if iid in iids_requested]


#SSPs
parse_iids = [
    "CMIP6.ScenarioMIP.*.*.[ssp126,ssp245,ssp370,ssp585].*.Amon.psl.*.*",
]
# Comma separated values in square brackets will be expanded and the above is equivalent to:
# parse_iids = [
#     "CMIP6.PMIP.*.*.lgm.*.*.[uo, vo].*.*", # this is equivalent to passing
#     "CMIP6.PMIP.*.*.lgm.*.*.vo.*.*",
# ]
iids_1 = []
for piid in parse_iids:
    iids_1.extend(parse_instance_ids(piid))
'''

#piC & hist
parse_iids = [
    "CMIP6.CMIP.*.*.[piControl,historical].*.Amon.psl.*.*",
]
# Comma separated values in square brackets will be expanded and the above is equivalent to:
# parse_iids = [
#     "CMIP6.PMIP.*.*.lgm.*.*.[uo, vo].*.*", # this is equivalent to passing
#     "CMIP6.PMIP.*.*.lgm.*.*.vo.*.*",
# ]
iids_2 = []
for piid in parse_iids:
    iids_2.extend(parse_instance_ids(piid))
iids_1.extend(iids_2)

'''
#check against what's already available
iids_requested = iids_1

url_dict = {
    'qc':"https://storage.googleapis.com/cmip6/cmip6-pgf-ingestion-test/catalog/catalog.json",
    'non-qc':"https://storage.googleapis.com/cmip6/cmip6-pgf-ingestion-test/catalog/catalog_noqc.json",
    'retracted':"https://storage.googleapis.com/cmip6/cmip6-pgf-ingestion-test/catalog/catalog_retracted.json"
}

iids_found = []
for catalog,url in url_dict.items():
    iids = search_iids(url)
    iids_found.extend(iids)
    print(f"Found in {catalog=}: {iids=}\n")

missing_iids = list(set(iids_requested) - set(iids_found))
print(f"\n\nStill missing {len(missing_iids)} of {len(iids_requested)}: \n{missing_iids=}")

