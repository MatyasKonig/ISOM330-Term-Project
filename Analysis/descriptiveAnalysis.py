import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()

df = pd.read_csv('Data/cleaned_unnormalized_data.csv')


def graph(xVar, yVar, title, xLabel, yLabel, imgName):
	tempData = df.groupby('state')[xVar, yVar].mean()
	ax = sns.regplot(xVar, yVar, data = tempData)
	ax.set(title = title, xlabel = xLabel, ylabel = yLabel)
	plt.savefig(imgName + '.png', dpi = 300)
	plt.show()
	print(tempData.corr())
    
graph('ViolentCrimesPerPop', 'racepctblack', 'Violent Crimes per Pct of African American Population',
	'Violent Crimes Per Population', 'Percentage of Pop African American', 'crimeVSblackpctpop')

ax = sns.regplot('ViolentCrimesPerPop', 'racepctblack', data = df, line_kws={"color": "darkblue"})
ax = sns.regplot('ViolentCrimesPerPop', 'racePctAsian', data = df, line_kws={"color": sns.xkcd_rgb["pale red"]})
ax = sns.regplot('ViolentCrimesPerPop', 'racePctWhite', data = df, line_kws={"color": "darkgreen"})
ax = sns.regplot('ViolentCrimesPerPop', 'racePctHisp', data = df, line_kws={"color": "black"})
plt.savefig('Visuals/plot.png', dpi = 300)
