import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

rfm = pd.read_csv("data/final_rfm_with_clusters.csv")

#Customer Districution Graph
rfm['Cluster'].value_counts().plot(kind='bar')
plt.title("Customer Distribution by Cluster")
plt.xlabel("Cluster")
plt.ylabel("Number of Customers")
plt.show()

#Scatter Plot Recency vs Monetary
sns.scatterplot(
    data=rfm,
    x='recency',
    y='monetary',
    hue='Cluster'
)

plt.title("Customer Segments (Recency vs Monetary)")
plt.show()

#Frequency vs Monetary
sns.scatterplot(
    data=rfm,
    x='frequency',
    y='monetary',
    hue='Cluster'
)

plt.title("Frequency vs Monetary by Cluster")
plt.show()

#Cluster Analysis
print(
    rfm.groupby('Cluster').agg({
        'recency': 'mean',
        'frequency': 'mean',
        'monetary': 'mean'
    })
)
