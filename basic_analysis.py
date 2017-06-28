#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import glob
import os
import numpy as np
import scipy.stats as sts
import matplotlib.pyplot as plt
import enchant # english dict
from wordcloud import WordCloud # word cloud
import plot_functions as pf # custom plotting

import matplotlib as mpl
mpl.rcParams['font.size'] = 15
mpl.rcParams['font.family'] = 'serif'


colors = ["#00be00", "#00c9ff", "#dc8200", "#fc65ff", "#993a03", "#00734a", "#9e46a8", "#32587c"]


def get_data():
    cwdir = os.path.dirname(os.path.realpath(__file__))
    files = glob.glob(cwdir + "/data/*.txt")
    # read as pandas dataframe
    frames = []
    for f in files:
        frames.append(pd.read_csv(f))

    df = pd.concat(frames)
    # drop duplicates by ID
    df = df.drop_duplicates(subset = ['Sysno'], keep = 'last')
    # get unique index
    df = df.set_index(np.arange(df.shape[0]))

    # parse authors as list
    for idx, row in df.iterrows():
        df.set_value(idx, 'AutořiAV', str(df.at[idx, 'AutořiAV']).split(" - "))

    return df


def pie_values_not_percents(vals):
    def autopct(pct):
        total = np.sum(vals)
        val = int(round(pct*total/100.0))
        return str(val)
    return autopct


if __name__ == "__main__":

    df = get_data()
    print df.columns
    # print df


    # pub no.
    # pd Series with index as year, value as cnt of publications
    cnt_years = df['RokVydání'].value_counts().sort_index()
    aut_per_years = df.groupby(['RokVydání'])['AutořiAV'].sum().values
    aut_per_years = [len(list(set(i))) for i in aut_per_years]
    pf.plot_year_time_series(cnt_years.index, [cnt_years.values, aut_per_years], ylabel = None, legend = ['pub count', 'unique authors'],
        fname = "yearly_pub_count.eps")
    print sts.pearsonr(aut_per_years, cnt_years.values)



    # language
    overall_cnt_lang = df['Jazyk'].value_counts()
    print overall_cnt_lang
    yearly_lang = df.groupby(['Jazyk', 'RokVydání']).size()
    # print yearly_lang['eng']

    # type
    overall_cnt_type = df['ZpZveřejnění'].value_counts()
    print overall_cnt_type
    plt.figure(figsize = (5,5))
    plt.pie(overall_cnt_type.values, explode = (0, 0, 0.05, 0.1, 0.2, 0.4, 0.65), labels = overall_cnt_type.index, 
        autopct = pie_values_not_percents(overall_cnt_type.values), colors = colors[:len(overall_cnt_type)])
    plt.gca().axis('equal')
    plt.savefig("type-pie-chart.eps", bbox_inches = 'tight')
    yearly_type = df.groupby([ 'RokVydání', 'ZpZveřejnění']).size()
    cumsum = yearly_type.cumsum(0)


    # impact factor
    mean_if = df['ImpFaktor'].mean()
    median_if = df['ImpFaktor'].median()
    max_if = df['ImpFaktor'].max()
    pf.histogram(df['ImpFaktor'].dropna(), bins = 50, fname = "IF-hist.eps")
    print mean_if, max_if, median_if
    print df.loc[df['ImpFaktor'] == max_if]['BiblCit']
    yearly_mean = df.groupby(['RokVydání'])['ImpFaktor'].mean()
    print yearly_mean
    

    # field
    cnt_fieldRIV = df['KódOborRIV'].value_counts()[:7]
    others = df['KódOborRIV'].value_counts()[7:].sum()
    print cnt_fieldRIV
    print others
    plt.figure(figsize = (5,5))
    explode = [(x**2)/30. for x in np.linspace(0, 2, len(cnt_fieldRIV)+1)]
    plt.pie(list(cnt_fieldRIV.values) + [others], explode = explode, labels = list(cnt_fieldRIV.index) + ['others'], 
        autopct = pie_values_not_percents(cnt_fieldRIV.values), colors = colors[:len(cnt_fieldRIV)+1])
    plt.gca().axis('equal')
    plt.savefig("RIV-field-pie-chart.eps", bbox_inches = 'tight')
    # plt.show()

    # keywords - WORDCLOUD
    d = enchant.Dict("en_US")
    keywords = []
    for k in df['KlíčSlova']:
        k = str(k)
        if k != 'nan':
            words = k.split(' - ')
            for w in words:
                if d.check(w):
                    keywords.append(w)

    # TODO font to match poster font
    wordcloud = WordCloud(background_color = None, max_font_size = 90, margin = 15, normalize_plurals = True, 
        relative_scaling = 1., colormap = plt.get_cmap('cool'), mode = 'RGBA', width = 1500, height = 750, 
        font_step = 5, font_path = '/Users/nikola/Library/Fonts/Courier New.ttf').generate(' '.join(keywords))
    wordcloud.to_file("figs/keywords-cloud.png")

