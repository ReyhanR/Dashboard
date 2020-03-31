import pandas as pd 
import seaborn as sns

tips = sns.load_dataset('tips')
tips.to_csv(r'D:\User\Reyhan\Purwadhika\Latihan\DASHBOARD\tips.csv', index=False)

# print(len(tips))