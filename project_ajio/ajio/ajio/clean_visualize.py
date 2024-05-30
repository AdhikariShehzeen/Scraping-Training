import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'C:\Users\Admin\Documents\Scraping Training\project_ajio\ajio\response.csv')
print(df)
df['discountPercent'] = df['discountPercent'].apply(lambda x: float(x.strip('%')))
df['new_price'] = df['new_price'].astype(float)
df['old_price'] = df['old_price'].astype(float)
df['rating'] = df['rating'].astype(float)
df['rating_count'] = df['rating_count'].astype(int)


# Summary statistics
print(df.describe())

plt.figure(figsize=(10, 6))
sns.histplot(df['discountPercent'], bins=20, kde=True, color='green')
plt.title('Distribution of Discounts')
plt.xlabel('Discount (%)')
plt.ylabel('Frequency')
plt.show()

