import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import ttest_ind
from scipy.stats import f_oneway



df = pd.read_csv('neme_data.csv')

df = df[df['Lane'] == 'MIDDLE']

cols_to_convert = ['gold7me', 'gold15me', 'gold7opp', 'gold15opp', 'xp7me','xp15me','xp7opp','xp15opp']   # replace with your column names
df[cols_to_convert] = df[cols_to_convert].astype(float)


df['dmg/taken'] = df['Damage_done']/df['Damage_taken']
df['dmg/min']= df['Damage_done']/df['Match_length']
df['dmg/gold_min'] = df['Damage_done']/(df['Gold_earned']/df['Match_length'])
df['cs/min'] =  (df['Minions_slain'] + df['Monsters_killed'])/df['Match_length']

df['gold_diff7'] = df['gold7me'] - df['gold7opp']
df['gold_diff15'] = df['gold15me'] - df['gold15opp']
df['xp_diff7'] = df['xp7me'] - df['xp7opp']
df['xp_diff15'] = df['xp15me'] - df['xp15opp']

df['lead7'] = df['gold_diff7'] > 0 
df['lead15'] = df['gold_diff15'] > 0 

#Test of two means seperated by a categorical variable
def t_test_func(col):
    group_1 = df[df[col] == True]['Win']
    group_2 = df[df[col] == False]['Win']
    
    print(f"True mean: {group_1.mean():.4f}, False mean : {group_2.mean():.4f}")

    t_stat, p_val = ttest_ind(group_1, group_2, equal_var=False)
    print(f"T-statistic: {t_stat:.4f}, p-value: {p_val:.4f}")



# y = df['Win']  
# X = df[['dmg/taken', 'dmg/min', 'dmg/gold_min', 'cs/min','gold_diff7','gold_diff15' ,'xp_diff7','xp_diff15']]

# average = X.mean()
# median = X.median()
# standard_dev = X.std()
# ranges = X.max() - X.min()


# statistics_table = pd.DataFrame({
#     'Average': average,
#     'Median': median,
#     'Standard deviation': standard_dev,
#     'Range': ranges
# })

# # Display the table
# print(statistics_table)


# plt.figure(figsize=(12, 10))

# # Loop through each column in X and plot its distribution
# for i, column in enumerate(X.columns, 1):
#     plt.subplot(2, 4, i)  # 2 rows, 4 columns
#     sns.kdeplot(X[column])
#     plt.title(f'Distribution of {column}')
#     plt.tight_layout()

# # Show the plots
# plt.show()

X = df['Deaths'] 
X = sm.add_constant(X)              
y = df['Win']                         

model = sm.Logit(y, X).fit()
print(model.summary())


# group1 = df[df['Win'] == True]['gold_diff7']
# group2 = df[df['Win'] == False]['gold_diff7']

# t_stat, p_val = ttest_ind(group1, group2, equal_var=False)
# print(group1.mean(), group2.mean())
# print(f"T-statistic: {t_stat:.4f}, p-value: {p_val:.4f}")


# sns.kdeplot(group1, label='Win', fill=True, bw_adjust=0.2)
# sns.kdeplot(group2, label='Loss', fill=True, bw_adjust=0.2)

# plt.legend()
# plt.show()




