import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()

df = pd.read_csv('Data/cleaned_unnormalized_data.csv')

ax = sns.regplot('racePctWhite', 'ViolentCrimesPerPop', label = 'White', data = df, scatter_kws={"color": sns.xkcd_rgb["kiwi green"]}, line_kws={"color": sns.xkcd_rgb["dark grass green"]})
ax.set(xlabel= 'Percentage of White Population', ylabel= 'Violent Crimes')
plt.savefig('Visuals/crimesPlot5.png', dpi = 300)
ax = sns.regplot('racepctblack', 'ViolentCrimesPerPop', label = 'African American', data = df, scatter_kws={"color": sns.xkcd_rgb["blue"]}, line_kws={"color": sns.xkcd_rgb["royal blue"]})
ax.set(xlabel= 'Percentage of African American Population', ylabel= 'Violent Crimes')
plt.savefig('Visuals/crimesPlot5.png', dpi = 300)
ax = sns.regplot('racePctHisp', 'ViolentCrimesPerPop', label = 'Hispanic', data = df, scatter_kws={"color": sns.xkcd_rgb["manilla"]}, line_kws={"color": sns.xkcd_rgb["sun yellow"]})
ax.set(xlabel= 'Percentage of Hispanic Population', ylabel= 'Violent Crimes')
plt.savefig('Visuals/crimesPlot5.png', dpi = 300)
ax = sns.regplot('racePctAsian', 'ViolentCrimesPerPop', label = 'Asian', data = df, scatter_kws={"color": sns.xkcd_rgb["pale red"]}, line_kws={"color": sns.xkcd_rgb["crimson"]})
ax.set(xlabel= 'Percentage of Population', ylabel= 'Violent Crimes')
ax.legend(loc=9, bbox_to_anchor=(0.5, -0.15), ncol = 4)
plt.savefig('Visuals/crimesPlot5.png', dpi = 300, bbox_inches="tight")


ax = sns.regplot('racePctWhite', 'perCapInc', label = 'White', data = df, scatter_kws={"color": sns.xkcd_rgb["kiwi green"]}, line_kws={"color": sns.xkcd_rgb["dark grass green"]})
ax.set(xlabel= 'Percentage of White Population', ylabel= 'Per Capita Income')
plt.savefig('Visuals/incomePlot5.png', dpi = 300, bbox_inches="tight")
ax = sns.regplot('racepctblack', 'perCapInc', label = 'African American', data = df, scatter_kws={"color": sns.xkcd_rgb["blue"]}, line_kws={"color": sns.xkcd_rgb["royal blue"]})
ax.set(xlabel= 'Percentage of African American Population', ylabel= 'Per Capita Income')
plt.savefig('Visuals/incomePlot5.png', dpi = 300, bbox_inches="tight")
ax = sns.regplot('racePctHisp', 'perCapInc', label = 'Hispanic', data = df, scatter_kws={"color": sns.xkcd_rgb["manilla"]}, line_kws={"color": sns.xkcd_rgb["sun yellow"]})
ax.set(xlabel= 'Percentage of Hispanic Population', ylabel= 'Per Capita Income')
plt.savefig('Visuals/incomePlot5.png', dpi = 300, bbox_inches="tight")
ax = sns.regplot('racePctAsian', 'perCapInc', label = 'Asian', data = df, scatter_kws={"color": sns.xkcd_rgb["pale red"]}, line_kws={"color": sns.xkcd_rgb["crimson"]})
ax.set(xlabel= 'Percentage of Population', ylabel= 'Per Capita Income')
ax.legend(loc=9, bbox_to_anchor=(0.5, -0.15), ncol = 4)
plt.savefig('Visuals/incomePlot5.png', dpi = 300, bbox_inches="tight")
