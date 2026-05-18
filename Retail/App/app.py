import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if "page" not in st.session_state:
    st.session_state.page = "📊 Dashboard"

# Data
rfm = pd.read_csv("data/final_rfm_with_clusters.csv")
#cleaned_df = pd.read_csv("C:/Users/somes/OneDrive/Desktop/Retail/Data/cleaned_retail.csv")

# COLORS  ==========================================================================
COLORS = {
    "primary": "#546B41",
    "secondary": "#99AD7A",
    "accent": "#DCCCAC",
    "dark": "#3E4E30",
    "background": "#FFF8EC"
}

custom_palette = ["#546B41", "#99AD7A", "#DCCCAC", "#3E4E30"]

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS ==========================================================================
st.markdown("""
<style>

/* Background */
.main {
    background-color: #FFF8EC;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #546B41, #3E4E30);
}

/* Center sidebar */
section[data-testid="stSidebar"] > div {
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #FFF8EC;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h3 {
    color: #DCCCAC !important;
    font-weight: 700;
}

/* Divider */
section[data-testid="stSidebar"] hr {
    background: rgba(255,255,255,0.3);
    height: 1px;
    border: none;
    width: 80%;
}

/*Shadow*/
section[data-testid="stSidebar"] .stButton button {
    width: 85% !important;
    margin: 10px auto !important;
    padding: 10px !important;

    background: rgba(255, 255, 255, 0.10) !important;
    color: #FFF8EC !important;

    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;

    backdrop-filter: blur(6px);

    /*CENTERED INNER SHADOW ONLY */
    box-shadow: inset 0px 0px 10px rgba(0,0,0,0.45) !important;

    font-weight: 600 !important;
}


/* KPI Cards */
[data-testid="metric-container"] {
    background-color: white;
    border-left: 4px solid #99AD7A;
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
}

/* KPI hover */
[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
}

/* Headings */
h1, h2, h3 {
    color: #546B41;
    font-weight: 700;
}

/* Spacing */
.element-container {
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR NAV

col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("📊 Dashboard"):
        st.session_state.page = "📊 Dashboard"

with col2:
    if st.button("📂 Explorer"):
        st.session_state.page = "📂 Data Explorer"

page = st.session_state.page
st.sidebar.markdown("---")

# Controls
st.sidebar.markdown("⚙️ Controls")
show_top = st.sidebar.checkbox("Show Top Customers", value=True)
show_charts = st.sidebar.checkbox("Show Charts", value=True)

st.sidebar.markdown("---")

# Filters
st.sidebar.title("🔍 Filters")

selected_cluster = st.sidebar.multiselect(
    "Select Cluster",
    options=rfm['Cluster'].unique(),
    default=rfm['Cluster'].unique()
)

selected_segment = st.sidebar.multiselect(
    "Select Segment",
    options=rfm['Segment'].unique(),
    default=rfm['Segment'].unique()
)

filtered_data = rfm[
    (rfm['Cluster'].isin(selected_cluster)) &
    (rfm['Segment'].isin(selected_segment))
]

#DASHBOARD ==========================================================================
if page == "📊 Dashboard":

    st.markdown(
        "<h2 style='text-align: center;'>📊 Customer Segmentation Dashboard</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # KPI
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Customers", f"{len(filtered_data):,}")
    col2.metric("Revenue", f"${filtered_data['monetary'].sum():,.0f}")
    col3.metric("Avg Order", f"${filtered_data['monetary'].mean():,.2f}")
    col4.metric("Avg Frequency", f"{filtered_data['frequency'].mean():.2f}")

    st.markdown("---")

    # ROW 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Customer Distribution")

        fig, ax = plt.subplots(figsize=(4.5,2.8))
        filtered_data['Cluster'].value_counts().plot(
            kind='bar',
            color=COLORS["primary"],
            width=0.5,
            ax=ax
        )
        ax.tick_params(labelsize=8)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Recency vs Monetary")

        fig, ax = plt.subplots(figsize=(4.5,2.8))
        sns.scatterplot(
            data=filtered_data,
            x='recency',
            y='monetary',
            hue='Cluster',
            palette=custom_palette,
            s=15,
            ax=ax
        )
        ax.tick_params(labelsize=8)
        plt.tight_layout()
        st.pyplot(fig)

    # ROW 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Segment")

        segment_rev = filtered_data.groupby('Segment')['monetary'].sum()

        fig, ax = plt.subplots(figsize=(4.5,2.8))
        segment_rev.plot(
            kind='bar',
            color=COLORS["secondary"],
            width=0.5,
            ax=ax
        )
        ax.tick_params(labelsize=8)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Customers by Segment")

        segment_count = filtered_data['Segment'].value_counts()

        fig, ax = plt.subplots(figsize=(4.5,2.8))
        segment_count.plot(
            kind='bar',
            color=COLORS["accent"],
            width=0.5,
            ax=ax
        )
        ax.tick_params(labelsize=8)
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")

    # Insights + Recommendations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Business Insights")
        st.markdown("""
        -  High-value customers contribute major revenue  
        -  High recency customers are at risk  
        -  Frequent buyers are loyal  
        """)

    with col2:
        st.subheader("🚀 Recommendations")
        st.markdown("""
        -  Target high-value users  
        -  Re-engage churn risk users  
        -  Reward loyal customers  
        """)


#DATA EXPLORER ==========================================================================
elif page == "📂 Data Explorer":

    st.markdown(
        "<h2 style='text-align: center;'>📂 Customer Data Explorer</h2>",
        unsafe_allow_html=True
    )

    st.subheader("🔍 Customer Lookup")

    customer_id = st.text_input("Enter Customer ID")

    if customer_id:
        result = filtered_data[
            filtered_data['CustomerID'].astype(str) == customer_id
        ]
        st.write(result)

    st.subheader("Segment Insights")

    segment_data = filtered_data.groupby('Segment').agg({
        'recency': 'mean',
        'frequency': 'mean',
        'monetary': 'mean'
    })

    st.dataframe(segment_data)

    st.markdown("---")

    if show_top:
        st.subheader("🏆 Top Customers")
        top_customers = filtered_data.sort_values(by='monetary', ascending=False).head(10)
        st.dataframe(top_customers[['CustomerID','monetary','frequency','recency']])

# Run Using--> python -m streamlit run app/streamlit.py
