from lru_cache import LRUCache  # Ensure main.py contains the LRUCache class as defined previously
import matplotlib.pyplot as plt


def display_data(stats):
    labels = list(stats.keys())
    values = list(stats.values())

    plt.figure(figsize=(12, 8))

    plt.bar(labels, values, color=['blue', 'orange', 'green', 'red', 'purple'])
    plt.xlabel('Metrics')
    plt.ylabel('Values')
    plt.title("LRU Cache Statistics")

    # Display values on each bar
    for index, value in enumerate(values):
        plt.text(index, value, f"{value:.2f}", ha='center', va='bottom')

    plt.show()


# Initialize the LRU Cache
lru_cache = LRUCache(capacity=5, ttl=30)  # Example: TTL of 30 seconds

# Perform cache operations to simulate usage
lru_cache.put(1, 10)
lru_cache.put(2, 20)
lru_cache.put(3, 30)
lru_cache.get(1)
lru_cache.put(4, 40)
lru_cache.put(5, 50)
lru_cache.get(6)  # Miss
lru_cache.put(6, 60)  # Evicts the least recently used (2)
lru_cache.get(2)  # Miss (2 has been evicted)

# Retrieve statistics and miss rate
statistics = lru_cache.get_statistics()
statistics["miss_rate (%)"] = lru_cache.get_miss_rate()

# Display statistics using matplotlib
display_data(statistics)