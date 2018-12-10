import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()

df = pd.read_csv('Data/cleaned_unnormalized_data.csv')

ax = sns.regplot('racePctWhite', 'ViolentCrimesPerPop', data = df, scatter_kws={"color": sns.xkcd_rgb["kiwi green"]}, line_kws={"color": sns.xkcd_rgb["dark grass green"]})
ax = sns.regplot('racepctblack', 'ViolentCrimesPerPop', data = df, scatter_kws={"color": sns.xkcd_rgb["blue"]}, line_kws={"color": sns.xkcd_rgb["royal blue"]})
ax = sns.regplot('racePctHisp', 'ViolentCrimesPerPop', data = df, scatter_kws={"color": sns.xkcd_rgb["manilla"]}, line_kws={"color": sns.xkcd_rgb["sun yellow"]})
ax = sns.regplot('racePctAsian', 'ViolentCrimesPerPop', data = df, scatter_kws={"color": sns.xkcd_rgb["pale red"]}, line_kws={"color": sns.xkcd_rgb["crimson"]})
plt.savefig('Visuals/crimesPlot.png', dpi = 300)


ax = sns.regplot('racePctWhite', 'medIncome', data = df, scatter_kws={"color": sns.xkcd_rgb["kiwi green"]}, line_kws={"color": sns.xkcd_rgb["dark grass green"]})
ax = sns.regplot('racePctHisp', 'medIncome', data = df, scatter_kws={"color": sns.xkcd_rgb["manilla"]}, line_kws={"color": sns.xkcd_rgb["sun yellow"]})
ax = sns.regplot('racepctblack', 'medIncome', data = df, scatter_kws={"color": sns.xkcd_rgb["blue"]}, line_kws={"color": sns.xkcd_rgb["royal blue"]})
ax = sns.regplot('racePctAsian', 'medIncome', data = df, scatter_kws={"color": sns.xkcd_rgb["pale red"]}, line_kws={"color": sns.xkcd_rgb["crimson"]})
plt.savefig('Visuals/incomePlot.png', dpi = 300)