#!/usr/bin/python
# -*- coding: utf-8 -*-

from basic_analysis import get_data
import numpy as np

## from https://github.com/ckreibich/scholar.py ##
from scholar import scholar as sch

df = get_data()

for idx, row in df.iterrows():
    print idx
    # get basic data
    authors = df['AutořiVšichni'][idx] 
    title = str(df['OrigNázev'][idx].strip())
    year = df['RokVydání'][idx]
    cits = df['PočetCitací'][idx]
    # query Google Scholar
    querier = sch.ScholarQuerier()
    query = sch.SearchScholarQuery()
    query.set_author(authors.decode('utf-8'))
    query.set_timeframe(year, year)
    query.set_words(title.decode('utf-8'))
    query.set_scope(True) # searching title only
    querier.send_query(query)
    # get articles
    articles = querier.articles
    for art in articles:
        title_sch = str(art.attrs['title'][0].encode('utf-8').strip())
        if not repr(title_sch.lower()) == repr(title.lower()):
            print("**WARNING: titles not matching!")
        # get number of citations
        cits_sch = art.attrs['num_citations'][0]
        # take maximum between scholar and our db
        cit_max = int(np.nanmax([cits, cits_sch]))
        # set cit count
        df.set_value(idx, 'PočetCitací', cit_max)


df.to_pickle("UI-data-w-scholar-citations.bin")

yearly_cit = df.groupby(['RokVydání'])['PočetCitací'].sum()
total_cit = df['PočetCitací'].sum()
mean_cit, sd_cit = df['PočetCitací'].mean(), df['PočetCitací'].std()
# print yearly_cit

