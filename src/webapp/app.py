import streamlit as st
from datetime import datetime
import os

from webapp.constants import UPDATE_FREQ_SEC
from webapp.crypto_api import get_crypto_data
from webapp.utils import format_number_with_suffix

st.set_page_config(page_title="Crypto Price", layout="centered")

# Get build info from environment
build_date = os.getenv('BUILD_DATE', 'Unknown')
git_sha = os.getenv('GIT_SHA', 'Unknown')

# Display in your app
st.sidebar.text(f"Built: {build_date}")
st.sidebar.text(f"Version: {git_sha[:7]}")

@st.fragment(run_every=UPDATE_FREQ_SEC)
def display_crypto_price():
    try:
        data = get_crypto_data()

        price = data.get("price", 0)
        change_24h = data.get("percent_change_24h", 0)
        symbol = data.get("symbol", "")

        st.metric(
            label=symbol,
            value=format_number_with_suffix(price),
            delta=f"{change_24h:.2f}%",
            border=True,
        )

        # Add raw JSON data table
        st.subheader("📊 Raw API Data")
        
        # Create a nice table from the JSON
        if data:
            # Convert to a more readable format
            json_data = []
            for key, value in data.items():
                json_data.append({
                    "Field": key,
                    "Value": str(value)
                })
            
            st.dataframe(json_data, hide_index=True)

    except Exception as e:
        st.error(f"Failed to load data: {e}")


if __name__ == "__main__":
    display_crypto_price()
