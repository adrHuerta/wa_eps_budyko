import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.25, rc={"lines.linewidth": 2})

budyko = pickle.load(open("./data/processed/budyko.pkl","rb"))

# table
budyko["clim"]["Q/P"] = budyko["clim"]["Q"]/budyko["clim"]["PP"]
budyko["clim"]["P/PET"] = budyko["clim"]["PP"]/budyko["clim"]["PET"]
budyko["clim"]["PET/P"] = budyko["clim"]["PET"]/budyko["clim"]["PP"]

df_min = budyko["clim"].groupby("Vertiente").min()[['Q', 'PP', "PET"]]
df_min.index.name = "Mínimo"

df_mean = budyko["clim"].groupby("Vertiente").mean()[['Q', 'PP', "PET"]]
df_mean.index.name = "Promedio"

df_max = budyko["clim"].groupby("Vertiente").max()[['Q', 'PP', "PET"]]
df_max.index.name = "Máximo"

ldf = [df_min, df_mean, df_max]

pd.concat(ldf,keys= ['Mínimo', 'Promedio', 'Máximo'],axis=0).reset_index(level=1).round(2).to_csv("./data/output/figs/table_char.csv")

# Budyko clim

fig, ax = plt.subplots(dpi=150)
sns.scatterplot(x="Ai", y="Ei", data=budyko["clim"], hue="Vertiente", s = 50)
ax.set_ylim(-.4, 1.15)
ax.set_xlim(0, 5)
ax.set_ylabel("AE/P")
ax.set_xlabel("PE/P")
ax.plot([1, 250], [1, 1], 'k-', lw=2)
ax.plot([0, 1], [0, 1], 'k-', lw=2)
texts = [ax.text(budyko["clim"]["Ai"].values[i], budyko["clim"]["Ei"].values[i], budyko["clim"]["Outlet"].values[i], size = 7, fontweight='bold', alpha = .6) for i in range(len(budyko["clim"]["Outlet"]))]
adjust_text(texts, arrowprops={"arrowstyle":'-', "color":'red', "alpha":.65, "lw":.1}, expand_text=(2, 2), only_move={'objects': 'xy', 'points': 'xy', 'text': 'y'}, ax = ax)

plt.savefig('./data/output/figs/04_Budyko_clim.png',
            bbox_inches='tight',pad_inches = 0, dpi = 150)
plt.close()

#
fig, ax = plt.subplots(dpi=150)
sns.scatterplot(x="P/PET", y="Q/P", data=budyko["clim"], hue="Vertiente", s = 50)
ax.set_xlim(0, 2.5)
ax.set_ylim(-0.01, 1.25)
ax.plot([0, 2.5], [1, 1], 'k-', lw=2)
ax.plot([0, 1], [0, 0], 'k-', lw=2)
QQ_c = np.arange(0, 150, .01)
PP_c = np.arange(1, 151, .01)
PET_c = PP_c - QQ_c
ax.plot(PP_c/PET_c, QQ_c/PP_c, 'k-', lw=2)

fig, ax = plt.subplots(dpi=150)
sns.scatterplot(x="PET/P", y="Q/P", data=budyko["clim"], hue="Vertiente", s = 50)
ax.set_xlim(0, 5)
ax.set_ylim(0, 1.25)
ax.plot([0, 5], [1, 1], 'k-', lw=2)
ax.plot([0, 1], [1, 0], 'k-', lw=2)
#.plot([1, 5], [0, 0], 'k-', lw=2)


# Budyko by year 1

fig, axs = plt.subplots(3, 2, sharey=True, sharex=True, figsize=(8, 20), dpi=100)

for ((i, ax), year) in zip(enumerate(fig.axes), list(budyko.keys())[1:7]):
    data = budyko[year]
    sns.scatterplot(ax=ax,x="Ai", y="Ei", data=data, hue="Vertiente", s=60, legend=None)
    ax.set_ylim(-.4, 1.15)
    ax.set_xlim(0, 5)
    ax.set_title(year)
    ax.set_ylabel("AE/P")
    ax.set_xlabel("PE/P")
    ax.plot([1, 250], [1, 1], 'k-', lw=1)
    ax.plot([0, 1], [0, 1], 'k-', lw=1)

plt.savefig('./data/output/figs/04_Budyko_year1.png',
            bbox_inches='tight',pad_inches = .1, dpi = 100)
plt.close()


fig, axs = plt.subplots(3, 2, sharey=True, sharex=True, figsize=(8, 20), dpi=100)

for ((i, ax), year) in zip(enumerate(fig.axes), list(budyko.keys())[7:13]):
    data = budyko[year]
    sns.scatterplot(ax=ax,x="Ai", y="Ei", data=data, hue="Vertiente", s=60, legend=None)
    ax.set_ylim(-.4, 1.15)
    ax.set_xlim(0, 5)
    ax.set_title(year)
    ax.set_ylabel("AE/P")
    ax.set_xlabel("PE/P")
    ax.plot([1, 250], [1, 1], 'k-', lw=1)
    ax.plot([0, 1], [0, 1], 'k-', lw=1)

plt.savefig('./data/output/figs/04_Budyko_year2.png',
            bbox_inches='tight',pad_inches = .1, dpi = 100)
plt.close()


fig, axs = plt.subplots(3, 2, sharey=True, sharex=True, figsize=(8, 20), dpi=100)

for ((i, ax), year) in zip(enumerate(fig.axes), list(budyko.keys())[13:]):
    data = budyko[year]
    sns.scatterplot(ax=ax,x="Ai", y="Ei", data=data, hue="Vertiente", s=60, legend=None)
    ax.set_ylim(-.4, 1.15)
    ax.set_xlim(0, 5)
    ax.set_title(year)
    ax.set_ylabel("AE/P")
    ax.set_xlabel("PE/P")
    ax.plot([1, 250], [1, 1], 'k-', lw=1)
    ax.plot([0, 1], [0, 1], 'k-', lw=1)

axs.flat[-1].set_visible(False) # to remove last plot

plt.savefig('./data/output/figs/04_Budyko_year3.png',
            bbox_inches='tight',pad_inches = .1, dpi = 100)
plt.close()