import streamlit as st
import pandas as pd
import seaborn as s
import matplotlib.pyplot as plt
import plotly.express as px
from pytrends.request import TrendReq

# Page settings
st.set_page_config(layout="centered", page_title="Google Search Analysis")

# Heading
st.markdown("<h1 style='text-align: center; color: navy;'>Google Search Analysis</h1>", unsafe_allow_html=True)

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# --- Single Keyword Analysis ---
st.subheader("🔍 Deep Analysis of a Single Keyword")
keyword = st.text_input("Enter a keyword for analysis")

if st.button("Analyze Keyword"):
    if keyword.strip() == "":
        st.warning("Please enter a keyword.")
    else:
        pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')

        # Country-wise analysis
        region = pytrends.interest_by_region()
        if not region.empty:
            region = region.sort_values(by=keyword, ascending=False).head(20)

            st.markdown("#### 🌍 Country-wise Interest")
            fig1, ax = plt.subplots(figsize=(10,6))
            s.barplot(x=region[keyword], y=region.index, palette='coolwarm', ax=ax)
            ax.set_title(f"Top Countries Searching for '{keyword}'")
            ax.set_xlabel("Search Interest")
            ax.set_ylabel("Country")
            st.pyplot(fig1)

            # Choropleth Map
            st.markdown("#### 🗺️ Map View of Search Interest")
            region = region.reset_index()
            fig2 = px.choropleth(region,
                                 locations='geoName',
                                 locationmode='country names',
                                 color=keyword,
                                 color_continuous_scale='reds',
                                 title=f"Search Interest Map for '{keyword}'")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.error("No data found for the given keyword.")

# --- Multiple Keyword Comparison ---
st.markdown("---")
st.subheader("📊 Multiple Keyword Analysis (Trend Over Time)")

col1, col2, col3, col4 = st.columns(4)
k1 = col1.text_input("Keyword 1")
k2 = col2.text_input("Keyword 2")
k3 = col3.text_input("Keyword 3")
k4 = col4.text_input("Keyword 4")

if st.button("Analyze Multiple Keywords"):
    keyword_list = [k1, k2, k3, k4]
    clean_keywords = [k for k in keyword_list if k.strip() != ""]

    if len(clean_keywords) < 2:
        st.warning("Please enter at least 2 keywords for comparison.")
    else:
        pytrends.build_payload(clean_keywords, cat=0, timeframe='today 12-m', geo='', gprop='')
        compare = pytrends.interest_over_time()

        if not compare.empty:
            st.markdown("#### 📈 Trend Over Time for Multiple Keywords")
            fig3, ax = plt.subplots(figsize=(12,6))
            for k in clean_keywords:
                ax.plot(compare.index, compare[k], label=k)
            ax.set_title("Google Trends Comparison")
            ax.set_xlabel("Date")
            ax.set_ylabel("Search Interest")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig3)
        else:
            st.error("Trend data not available for the selected keywords.")
