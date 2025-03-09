import pandas as pd
import statsmodels.api as sm
import xgboost as xgb
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score,roc_curve,auc

df = pd.read_csv('data1.csv')

df = df[df['Lane'] == 'MIDDLE']

df['dmg/taken'] = df['Damage_done']/df['Damage_taken']
df['dmg/min']= df['Damage_done']/df['Match_length']
df['dmg/gold_min'] = df['Damage_done']/(df['Gold_earned']/df['Match_length'])
df['cs/min'] =  (df['Minions_slain'] + df['Monsters_killed'])/df['Match_length']
# df['gold_diff7'] = df[['gold7me', 'gold7opp']].apply(lambda x: max(x['gold7me'] - x['gold7opp'], 0), axis=1)
# df['gold_diff15'] = df[['gold15me', 'gold15opp']].apply(lambda x: max(x['gold15me'] - x['gold15opp'], 0), axis=1)
# df['xp_diff7'] = df[['xp7me', 'xp7opp']].apply(lambda x: max(x['xp7me'] - x['xp7opp'], 0), axis=1)
# df['xp_diff15'] = df[['xp7me', 'xp15opp']].apply(lambda x: max(x['xp15me'] - x['xp15opp'], 0), axis=1)



df['gold_diff7'] = df['gold7me'] - df['gold7opp']
df['gold_diff15'] = df['gold15me'] - df['gold15opp']
df['xp_diff7'] = df['xp7me'] - df['xp7opp']
df['xp_diff15'] = df['xp15me'] - df['xp15opp']



df = df.dropna()



y = df['Win']  
X = df[['dmg/taken', 'dmg/min', 'dmg/gold_min', 'cs/min','gold_diff7','gold_diff15' ,'xp_diff7','xp_diff15']]

average = X.mean()
median = X.median()
standard_dev = X.std()
ranges = X.max() - X.min()


statistics_table = pd.DataFrame({
    'Average': average,
    'Median': median,
    'Standard deviation': standard_dev,
    'Range': ranges
})

# Display the table
print(statistics_table)


plt.figure(figsize=(12, 10))

# Loop through each column in X and plot its distribution
for i, column in enumerate(X.columns, 1):
    plt.subplot(2, 4, i)  # 2 rows, 4 columns
    sns.histplot(X[column], kde=True, bins=20, color='blue', stat='density', linewidth=0,  kde_kws={'bw_adjust': 0.5})
    plt.title(f'Distribution of {column}')
    plt.tight_layout()

# Show the plots
plt.show()

# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)

# model = LogisticRegression()

# # Perform stepwise feature selection
# sfs = SFS(model, 
#           k_features='best',  # 'best' will select the optimal number of features
#           forward=True,       # Forward selection
#           floating=False,     # If set to True, it will allow features to be added and removed
#           scoring='accuracy', # The metric used to evaluate the model (can also use 'roc_auc' etc.)
#           cv=5)               # Cross-validation to assess performance

# # Fit the model
# sfs = sfs.fit(X_scaled, y)

# # Get the selected features
# selected_features = list(sfs.k_feature_names_)
# print(f"Selected features: {selected_features}")

# # Fit the logistic regression model with selected features
# X_selected = [X_scaled, sfs.k_feature_idx_]
# final_model = model.fit(X_selected, y)

# # Get model coefficients
# print("Model coefficients:")
# print(final_model.coef_)






# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# dtrain = xgb.DMatrix(X_train, label=y_train)
# dtest = xgb.DMatrix(X_test, label=y_test)

# # Set up parameters for XGBoost (binary classification)
# params = {
#     'objective': 'binary:logistic',  # Binary classification (win/loss)
#     'eval_metric': 'logloss',  # Log loss for evaluating model
#     'max_depth': 6,  # Maximum depth of trees
#     'learning_rate': 0.1,  # Step size at each iteration
#     'n_estimators': 100,  # Number of boosting rounds
# }

# # Train the model
# model = xgb.train(params, dtrain, num_boost_round=100)

# y_pred_prob = model.predict(dtest)

# # Convert probabilities to binary predictions (0.5 threshold)
# y_pred = (y_pred_prob > 0.5).astype(int)

# # Evaluate accuracy
# accuracy = accuracy_score(y_test, y_pred)
# print(f'Accuracy: {accuracy:.4f}')

# # Evaluate AUC (Area Under the Curve)
# aucer = roc_auc_score(y_test, y_pred_prob)
# print(f'AUC Score: {aucer:.4f}')

# xgb.plot_importance(model, importance_type='total_gain', title='Feature Importance', xlabel='F-Score', ylabel='Features')
# plt.show()

#X = sm.add_constant(X)
#model = logit_model = sm.Logit(y, X).fit()
# model = logit_model = sm.OLS(y, X).fit()
# print(model.summary())



# # Set up the subplots
# fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# # Plot distributions
# sns.histplot(df['dmg/taken'], kde=True, ax=axes[0, 0])
# axes[0, 0].set_title('Distribution of dmg/taken')

# sns.histplot(df['dmg/min'], kde=True, ax=axes[0, 1])
# axes[0, 1].set_title('Distribution of dmg/min')

# sns.histplot(df['dmg/gold_min'], kde=True, ax=axes[1, 0])
# axes[1, 0].set_title('Distribution of dmg/gold_min')

# sns.histplot(df['cs/min'], kde=True, ax=axes[1, 1])
# axes[1, 1].set_title('Distribution of cs/min')

# plt.tight_layout()
# plt.show()