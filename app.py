import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 1. Page Configuration
st.set_page_config(page_title="Fraud Pattern Explorer", layout="wide")
st.title("Transaction Fraud Pattern Explorer")
st.write("Analyze fintech transaction data for potential fraud risks.")

# 2. Load Data (Use caching so it doesn't reload every time you click)
@st.cache_data
@st.cache_data
def load_data():
    DATA_DIR = Path("data")
    df = pd.read_csv(DATA_DIR / "transactions.csv")
    
    # Add these lines inside the function:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Hour'] = df['Timestamp'].dt.hour
    
    return df

df = load_data()

# 3. Sidebar for User Inputs (Interactive filtering)
st.sidebar.header("Filter Options")
amount_threshold = st.sidebar.slider("Amount Threshold", 0, 100000, 50000)
show_night_txns = st.sidebar.checkbox("Show Night Transactions Only")

# 4. Apply your logic (from your notebook)
filtered_df = df[df['Amount'] > amount_threshold]
# Convert Timestamp to datetime and extract the hour
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Hour'] = df['Timestamp'].dt.hour

# Now apply the filter
filtered_df = df[df['Amount'] > amount_threshold]
if show_night_txns:
    filtered_df = filtered_df[filtered_df['Hour'].isin([0,1,2,3,4,5])]
if show_night_txns:
    # Apply your hour logic here
    filtered_df = filtered_df[filtered_df['Hour'].isin([0,1,2,3,4,5])]

# 5. Display Data
st.subheader("Filtered Transactions")
st.dataframe(filtered_df.head(100))

# 6. Display Visualizations
st.subheader("Fraud Patterns")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['Amount'], ax=ax)
    st.pyplot(fig) # Streamlit handles matplotlib figures natively

with col2:
    # 1. Close old figures to prevent the "static/frozen" bug in Streamlit
    plt.close('all') 
    
    # 2. Create the new figure
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    
    # 3. Plot using the FILTERED data (so it fluctuates with the slider)
    # We use a boxplot here to show the difference in Amount between Fraud (1) and Not Fraud (0)
    sns.boxplot(
        data=filtered_df, 
        x='Is_Fraud', 
        y='Amount', 
        ax=ax2,
        palette={'0': '#4c72b0', '1': '#c44e52'} # Blue for normal, Red for fraud
    )
    
    # 4. Format the graph
    ax2.set_title('Amount Distribution by Fraud Status')
    ax2.set_xlabel('Is Fraud? (0 = No, 1 = Yes)')
    ax2.set_ylabel('Transaction Amount')
    
    # 5. Render it
    st.pyplot(fig2)

# 7. Export functionality
st.download_button(
    label="Download Suspicious Transactions CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='suspicious_transactions.csv',
    mime='text/csv',
)