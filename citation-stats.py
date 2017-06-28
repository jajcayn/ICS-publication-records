#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import scipy.stats as sts
import pandas as pd
import plot_functions as pf # custom plotting
import matplotlib.pyplot as plt

df = pd.read_pickle("UI-data-w-WoS-LAMR-citations.bin")

print len(df)
print df.columns

# citations
yearly_cit = df.groupby(['RokVydání'])['PočetCitací'].sum()
total_cit = df['PočetCitací'].sum()
mean_cit, sd_cit, max_cit = df['PočetCitací'].mean(), df['PočetCitací'].std(), df['PočetCitací'].max()
print yearly_cit
# total citations, mean and SD, max cit
print total_cit, mean_cit, sd_cit, max_cit

pf.plot_year_time_series(yearly_cit.index, yearly_cit.values, ylabel = None, legend = ['citations'],
        fname = "figs/yearly_citations.eps")

ifactor, cit = np.array(df['ImpFaktor']), np.array(df['PočetCitací'])
nans = np.logical_or(np.isnan(cit), np.isnan(ifactor))
plt.figure(figsize = (7,7))
plt.scatter(cit, ifactor, marker = 'x', s = 20, color = '#00734a')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
slope, intercept, _, _, _ = sts.linregress(cit[~nans], ifactor[~nans])
plt.plot(np.linspace(cit[~nans].min(), cit[~nans].max(), 200), slope*np.linspace(cit[~nans].min(), cit[~nans].max(), 200) + intercept, 
    linewidth = 1.4, color = "#00734a")
# plt.gca().set_xscale('log')
# plt.gca().set_yscale('log')
plt.xticks(size = 22)
plt.yticks(size = 22)
plt.ylabel("IF", size = 27)
plt.xlabel("CITATIONS", size = 27)
print sts.pearsonr(cit[~nans], ifactor[~nans])
plt.savefig("figs/IF-vs-citations.eps", bbox_inches = 'tight')
