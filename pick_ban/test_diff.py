import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel

df = pd.read_csv('winrate.csv')




plt.figure(figsize=(10, 6))
sns.kdeplot(df['winrate'], label='var1', fill=True, alpha=0.5)
sns.kdeplot(df['adj'], label='var2', fill=True, alpha=0.5)

plt.title("Distribution of Paired Variables")
plt.xlabel("Value")
plt.ylabel("Density")
plt.legend()
plt.show()


diffs = df['winrate'] - df['adj']
sns.kdeplot(diffs)
plt.title("Distribution of Paired Differences")
plt.show()


t_stat, p_value = ttest_rel(df['winrate'], df['adj'])

print(f"t-statistic: {t_stat:.3f}, p-value: {p_value:.3f}")
