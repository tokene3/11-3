import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("C:/Users/theoa/Downloads/GPU_DATA/gpu_specs_v6.csv")

# Convert possible numeric columns safely
numeric_cols = ["memSize", "gpuClock", "memClock", "unifiedShader", "tmu", "rop", "releaseYear"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")  # convert to numeric, replace invalid with NaN

# Replace missing values in memSize with a default (e.g., 1)
df["memSize"] = df["memSize"].fillna(1)

st.title("💻 GPU Specification Explorer")
st.markdown("Explore GPU specifications interactively by manufacturer or feature.")

# Sidebar filters
manufacturer = st.sidebar.multiselect(
    "Select Manufacturer(s):",
    options=df["manufacturer"].dropna().unique(),
    default=df["manufacturer"].dropna().unique()
)

x_axis = st.sidebar.selectbox("X-axis", options=df.columns, index=list(df.columns).index("gpuClock"))
y_axis = st.sidebar.selectbox("Y-axis", options=df.columns, index=list(df.columns).index("memClock"))

filtered_df = df[df["manufacturer"].isin(manufacturer)]

# Drop rows where the selected axes are not numeric
filtered_df = filtered_df.dropna(subset=[x_axis, y_axis])

# Interactive scatter plot
fig = px.scatter(
    filtered_df,
    x=x_axis,
    y=y_axis,
    color="manufacturer",
    size="memSize",  # we fixed missing values above
    hover_name="productName",
    title=f"{y_axis} vs {x_axis} by Manufacturer",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# Show table below
st.subheader("📊 Raw Data")
st.dataframe(filtered_df)
