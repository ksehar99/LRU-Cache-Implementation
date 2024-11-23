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



lru_cache = LRUCache(5)

# Adding 5 elements initially
lru_cache.put(1, 10)
lru_cache.put(2, 20)
lru_cache.put(3, 30)
lru_cache.put(4, 40)
lru_cache.put(5, 50)

# Access some elements to change their usage order
lru_cache.get(3)  # Cache: {1, 2, 4, 5, 3}
lru_cache.get(1)  # Cache: {2, 4, 5, 3, 1}

# Add more elements to trigger evictions
lru_cache.put(6, 60)  # Evicts key 2; Cache: {4, 5, 3, 1, 6}
lru_cache.put(7, 70)  # Evicts key 4; Cache: {5, 3, 1, 6, 7}
lru_cache.put(8, 80)  # Evicts key 5; Cache: {3, 1, 6, 7, 8}

# Access elements to prevent their eviction
lru_cache.get(6)  # Cache: {3, 1, 7, 8, 6}
lru_cache.get(1)  # Cache: {3, 7, 8, 6, 1}

# Add more elements to continue evictions
lru_cache.put(9, 90)   # Evicts key 3; Cache: {7, 8, 6, 1, 9}
lru_cache.put(10, 100) # Evicts key 7; Cache: {8, 6, 1, 9, 10}

# Access some elements and add more
lru_cache.get(8)  # Cache: {6, 1, 9, 10, 8}
lru_cache.put(11, 110) # Evicts key 6; Cache: {1, 9, 10, 8, 11}
lru_cache.put(12, 120) # Evicts key 1; Cache: {9, 10, 8, 11, 12}

# Add and access more to simulate real-world usage
for i in range(13, 21):
    lru_cache.put(i, i * 10)  # Adding keys 13 to 20 with values 130 to 200
    lru_cache.get(i - 1)  # Access the previously added key to prevent eviction

# Final misses and hits
lru_cache.get(19)  # Cache: Hit
lru_cache.get(2)   # Cache: Miss (evicted earlier)
lru_cache.get(15)  # Cache: Hit
lru_cache.get(5)   # Cache: Miss (evicted earlier)

# Calculate and print the miss rate
print("Cache Miss Rate:", round(lru_cache.get_miss_rate(),3))

# Retrieve statistics and display them
stats = lru_cache.data()
display_data(stats)