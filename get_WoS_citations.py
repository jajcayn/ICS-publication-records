#!/usr/bin/python
# -*- coding: utf-8 -*-

## USING PARTS OF CODE FROM https://github.com/rpritchett/wos-amr

import sys
from basic_analysis import get_data
import numpy as np
import xml.etree.ElementTree as ET

## client taken from https://github.com/rpritchett/wos-amr
## if this script is to be used, one need to insert USERNAME and PASSWORD for WoS LAMR API into client.py
import client


# xml template for API calls
id_request_template = u"""<?xml version="1.0" encoding="UTF-8" ?>
<request xmlns="http://www.isinet.com/xrpc42" src="app.id=API Demo">
  <fn name="LinksAMR.retrieve">
    <list>
      <!-- authentication -->
      <map>
        <val name="username">{user}</val>
        <val name="password">{password}</val>
      </map>
      <!-- what to to return -->
       <map>
         <list name="WOS">
           <val>doi</val>
           <val>ut</val>
           <val>timesCited</val>
         </list>
       </map>
       <!-- LOOKUP DATA -->
       {items}
    </list>
  </fn>
</request>
"""


def prep_request(items, local_id="id"):
    """
    Process the incoming items into an AMR request.

    <map name="cite_1">
        <val name="{id_type}">{value}</val>
    </map>
    """
    map_items = ET.Element("map")
    for idx, pub in enumerate(items):
        if pub is None:
            continue
        local_id_value = pub.get(local_id) or pub.get(local_id.upper())
        if local_id_value is None:
            local_id_value = str(idx)
        this_item = ET.Element("map", name=local_id_value)
        for k, v in pub.items():
            if v is None:
                continue
            de = ET.Element("val", name = k.lower())
            de.text = v.strip()
            this_item.append(de)
        map_items.append(this_item)

    request_items = ET.tostring(map_items)
    xml = id_request_template.format(user = client.USER, password = client.PASSWORD, items = request_items)
    return xml


df = get_data()


lookup_dois = []
found_dois = []

# put all publications with DOI or WoS number to list
for idx, row in df.iterrows():
    doi = df['DOI'][idx]
    ut = df['UT WOS'][idx]
    d = {}
    if doi != 'nan':
        d['doi'] = str(doi)
    if ut != 'nan':
        d['ut'] = str(ut)
    lookup_dois.append(d)
print("Calling WoS Links AMR...")
print("...getting info for %d papers with DOI defined..." % len(lookup_dois))
lookup_groups = client.grouper(lookup_dois, client.BATCH_SIZE)

# call WoS API
for idx, batch in enumerate(lookup_groups):
    xml = prep_request(batch)
    print("...processing batch %d..." % idx)
    # Post the batch
    rsp = client.get(xml)
    found_dois.append(rsp)
print("Done!")
print("Found %d groups..." % len(found_dois))

# concat results into one big dictionary
final_dict = {}
cnt = 0
for grp in found_dois:
    for k, item in grp.items():
        ut_lamr = item.get('ut')
        doi_lamr = item.get('doi')
        times_cited = item.get('timesCited')
        if (doi_lamr is not None) and (times_cited is not None):
            final_dict[cnt] = {'doi' : doi_lamr, 'UT' : ut_lamr, 'TC' : times_cited}
            cnt += 1

# update citation counts for every publication we got result
for k, item in final_dict.items():
    ut = item.get('UT')
    doi = item.get('doi')
    citations = int(item.get('TC'))
    try:
        ndx = df[df['UT WOS'] == 'wos:%s' % ut].index[0]
    except IndexError:
        try:
            ndx = df[df['DOI'] == doi].index[0] ## yields the same result
        except IndexError:
            continue
    try:
        old_ct = int(df['PočetCitací'][ndx])
    except ValueError:
        old_ct = np.nan
    # print old_ct, citations
    cit_max = int(np.nanmax([old_ct, citations]))
    df.set_value(ndx, 'PočetCitací', cit_max)

df.to_pickle('UI-data-w-WoS-LAMR-citations.bin')
        








