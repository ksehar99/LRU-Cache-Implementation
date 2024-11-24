import streamlit as st
import time
from lru_cache import LRUCache

# Set up the page configuration
st.set_page_config(page_title="LRU Cache Dashboard", page_icon="🧑‍💻")

# Initialize cache state if it doesn't exist
if "cache" not in st.session_state:
    st.session_state.cache = None  # Cache will be initialized after user input for size and TTL

# Sidebar Navigation
st.sidebar.title("Navigation")
buttons = ["🏠 HOME", "➕ ADD CACHE", "🔍 GET CACHE", "🗑️ CLEAR CACHE", "📊 CACHE STATISTICS"]

# Manage selected button state
if "selected_button" not in st.session_state:
    st.session_state.selected_button = "🏠 HOME"

# Button to switch between sections in the sidebar
for button in buttons:
    if st.sidebar.button(button):
        st.session_state.selected_button = button

# Define custom CSS for consistent design
st.markdown("""
    <style>
        .stButton > button {
            background-color: #1E6E64;
            color: white;
            width: 100%;
            margin-top: 5px;
            font-size: 16px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stButton > button:hover {
            background-color: #22998a;
        }
        .project-title {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            color: #14B8A6;
            margin-bottom: 20px;
        }
        body { background-color: #2c2f33; color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# Main Content Based on the selected button
if st.session_state.selected_button == "🏠 HOME":
    st.title("Welcome to LRU Cache Dashboard")
    st.markdown("<div class='project-title'>Manage Your Least Recently Used Cache</div>", unsafe_allow_html=True)
    st.info("Enter cache configuration details below:")

    # Input fields for cache size and TTL
    cache_size = st.number_input("Cache Size (default: 5):", min_value=1, value=5, step=1)
    ttl = st.number_input("Time-to-Live (TTL) in seconds for entries:", min_value=1, value=60, step=1)

    # Initialize cache with user-defined size and TTL
    if st.button("Initialize Cache"):
        st.session_state.cache = LRUCache(cache_size, ttl)
        st.success(f"Cache initialized with size {cache_size} and TTL {ttl} seconds.")

elif st.session_state.selected_button == "➕ ADD CACHE":
    # Ensure cache is initialized before adding entries
    if st.session_state.cache is None:
        st.error("Please initialize the cache first from the HOME screen.")
    else:
        st.title("Add Cache Entry")
        key = st.number_input("Enter Key:", min_value=0, step=1)
        value = st.text_input("Enter Value:")

        if st.button("Add Entry"):
            st.session_state.cache.put(key, value)
            st.success(f"Entry Added: {key} -> {value}")

elif st.session_state.selected_button == "🔍 GET CACHE":
    # Ensure cache is initialized before retrieving entries
    if st.session_state.cache is None:
        st.error("Please initialize the cache first from the HOME screen.")
    else:
        st.title("Get Cache Entry")
        key = st.number_input("Enter Key to Retrieve:", min_value=0, step=1)

        if st.button("Retrieve Entry"):
            value = st.session_state.cache.get(key)
            if value is not None:
                st.success(f"Cache Hit: {key} -> {value}")
            else:
                st.warning(f"Cache Miss: No entry found for key {key}")

elif st.session_state.selected_button == "🗑️ CLEAR CACHE":
    # Ensure cache is initialized before clearing
    if st.session_state.cache is None:
        st.error("Please initialize the cache first from the HOME screen.")
    else:
        st.title("Clear Cache")
        if st.button("Clear All Entries"):
            st.session_state.cache.clear()
            st.success("Cache cleared successfully!")

elif st.session_state.selected_button == "📊 CACHE STATISTICS":
    # Ensure cache is initialized before displaying statistics
    if st.session_state.cache is None:
        st.error("Please initialize the cache first from the HOME screen.")
    else:
        st.title("Cache Statistics")

        # Fetch statistics from the cache
        stats = st.session_state.cache.get_statistics()

        # Display metrics using Streamlit's columns for layout
        cols = st.columns(4)
        cols[0].metric("Cache Hits", stats["hits"])
        cols[1].metric("Cache Misses", stats["misses"])
        cols[2].metric("Evictions", stats["evictions"])

        # Calculate and display Miss Rate
        total_requests = stats["hits"] + stats["misses"]
        miss_rate = (stats["misses"] / total_requests * 100) if total_requests > 0 else 0.0
        cols[3].metric("Miss Rate", f"{miss_rate:.2f}%")

        # Display detailed cache information
        st.subheader("Detailed Cache Information")
        cache_details = st.session_state.cache.get_cache_details()

        # Check and display active cache entries
        if cache_details:
            st.table(cache_details)
        else:
            st.info("No active cache entries")

        # Add button to show graphical representation
        if st.button("Show Graph"):
            import matplotlib.pyplot as plt

            # Prepare data for the graph
            stats["Miss Rate (%)"] = miss_rate
            labels = list(stats.keys())
            values = list(stats.values())

            # Create the graph
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(
                labels,
                values,
                color=['darkcyan', 'lightseagreen', 'mediumturquoise', 'paleturquoise']
            )
            ax.set_xlabel("Metrics", fontsize=14)
            ax.set_ylabel("Values", fontsize=14)
            ax.set_title("LRU Cache Statistics", fontsize=16)
            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels,fontsize=12)

            # Add data labels on top of the bars
            for bar in bars:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f"{bar.get_height():.2f}",
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.3')
                )

            # Display the graph in Streamlit
            st.pyplot(fig)
