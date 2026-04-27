import sqlite3
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

conn = sqlite3.connect("data/retail.db")

query = """
SELECT 
    CustomerID,
    MAX(InvoiceDate) AS last_purchase,
    COUNT(DISTINCT Invoice) AS frequency,
    SUM(Quantity * Price) AS monetary
FROM retail
GROUP BY CustomerID
"""

rfm = pd.read_sql(query, conn)

print(rfm.head())

rfm['last_purchase'] = pd.to_datetime(rfm['last_purchase'])

snapshot_date = rfm['last_purchase'].max()

rfm['recency'] = (snapshot_date - rfm['last_purchase']).dt.days

rfm.to_csv("data/rfm_sql.csv", index=False)

print("✅ RFM table created")


#RFM Scoring
rfm['r_score'] = pd.qcut(rfm['recency'], q=4, labels=False, duplicates='drop') + 1
rfm['f_score'] = pd.qcut(rfm['frequency'], q=4, labels=False, duplicates='drop') + 1
rfm['m_score'] = pd.qcut(rfm['monetary'], q=4, labels=False, duplicates='drop') + 1

#Creating RFM Score
rfm['RFM_SCORE'] = (
    rfm['r_score'].astype(str) +
    rfm['f_score'].astype(str) +
    rfm['m_score'].astype(str)
)

#segmentation
def segment_customer(row):
    if row['RFM_SCORE'] == '444':
        return 'High Value'
    elif row['r_score'] == 4:
        return 'Recent Customers'
    elif row['f_score'] == 4:
        return 'Loyal Customers'
    elif row['m_score'] == 4:
        return 'Big Spenders'
    else:
        return 'Others'
    
rfm['Segment'] = rfm.apply(segment_customer, axis=1)

print(rfm['Segment'].value_counts())

#K-Means Clustering

X = rfm[['recency', 'frequency', 'monetary']]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42)
rfm['Cluster'] = kmeans.fit_predict(X_scaled)

print(rfm['Cluster'].value_counts())

print(
    rfm.groupby('Cluster').agg({
        'recency': 'mean',
        'frequency': 'mean',
        'monetary': 'mean'
    })
)
rfm.to_csv("data/final_rfm_with_clusters.csv", index=False)

print("✅ RFM with clusters saved")

rfm.to_csv("data/final_rfm_with_clusters.csv", index=False)
print(rfm.columns)

# segmentation
rfm['Segment'] = rfm.apply(segment_customer, axis=1)

# clustering
rfm['Cluster'] = kmeans.fit_predict(X_scaled)

# DEBUG
print(rfm.columns)

rfm.to_csv("data/final_rfm_with_clusters.csv", index=False)
