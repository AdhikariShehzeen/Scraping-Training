import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_excel(r'C:\Users\Admin\Documents\Scraping Training\project_Yatra\flights.xlsx')
print(df.describe())
df['total_fare'] = df['total_fare'].apply(lambda x: float(x.strip('Rs')))
flight_counts = df['flight_name'].value_counts()
plt.figure(figsize=(10, 8))
plt.pie(flight_counts, labels=flight_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Total Number of Flights of each Flight Company')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

# plt.figure(figsize=(10, 5))
# plt.scatter(df['flight_name'], df['total_fare'], color='skyblue')

# plt.xlabel('Flight Name')
# plt.ylabel('Total Fare')
# plt.title('Total Fare of Each Flight')
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.show()