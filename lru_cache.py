import time

class LRUCache:
    def __init__(self, capacity: int, ttl: int):
        self.capacity = capacity
        self.ttl = ttl
        self.cache = {}  # Store key-value pairs
        self.order = []  # Track the order of keys for eviction (Most recent at end)
        self.timestamps = {}  # Store timestamps for each cache entry
        self.hits = 0  # Cache hits
        self.misses = 0  # Cache misses
        self.total_accesses = 0  # Total cache accesses
        self.evictions = 0  # Cache evictions

    def put(self, key, value):
        """Add an item to the cache."""
        self.total_accesses += 1  # Increment total accesses every time a cache operation happens
        print(f"Attempting to put key: {key} => {value}")

        if key in self.cache:
            # Cache hit
            self.hits += 1  # Increment the hit counter
            self.cache[key] = value  # Update the value
            self.order.remove(key)  # Move the key to the most recent position in the order list
            self.order.append(key)
            self.timestamps[key] = time.time()  # Update the timestamp for the key
            print(f"Cache hit: Updated key {key} with value {value}. Hits: {self.hits}")
            return "Cache Hit: Updated value."

        # Cache miss
        self.misses += 1  # Increment the miss counter
        if len(self.cache) >= self.capacity:
            self._evict_if_needed()  # Evict if necessary

        # Add the new key-value pair to the cache
        self.cache[key] = value
        self.order.append(key)  # Add the new key to the order list
        self.timestamps[key] = time.time()  # Store the timestamp for the key
        print(f"Cache miss: Added key {key} with value {value}. Misses: {self.misses}")

        return "Cache Miss: New entry added."


    def get(self, key):
        """Retrieve an item from the cache."""
        current_time = time.time()
        # Remove expired keys before accessing
        self._remove_expired_keys(current_time)

        self.total_accesses += 1  # Every time a key is accessed, it's counted as an access
        
        if key in self.cache:
            # Move the accessed key to the most recent position in the order list
            self.order.remove(key)
            self.order.append(key)
            self.hits += 1
            return self.cache[key]
        else:
            self.misses += 1  # Increment miss only if the key is not found
            return None

    def clear(self):
        """Clear the cache and reset statistics."""
        self.cache.clear()
        self.order.clear()
        self.timestamps.clear()
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.total_accesses = 0

    def get_statistics(self):
        """Return cache statistics (hits, misses, and evictions)."""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
        }

    def get_cache_details(self):
        """Return the current cache state."""
        current_time = time.time()
        self._remove_expired_keys(current_time)
        return [{"Key": k, "Value": v} for k, v in self.cache.items()]

    def get_miss_rate(self):
        """Calculate and return the miss rate."""
        if self.total_accesses == 0:  # Prevent division by zero
            return 0.0
        return (self.misses / self.total_accesses) * 100

    def _remove_expired_keys(self, current_time):
        """Remove expired keys based on TTL."""
        expired_keys = [key for key, timestamp in self.timestamps.items()
                        if current_time - timestamp >= self.ttl]
        for key in expired_keys:
            self.cache.pop(key, None)  # Remove expired key from cache
            self.timestamps.pop(key, None)  # Remove expired key from timestamps
            self.order.remove(key)  # Remove expired key from order list
            self.evictions += 1  # Increment evictions

    def _evict_if_needed(self):
        """Evict the least recently used (LRU) item."""
        lru_key = self.order.pop(0)  # Remove the first (least recently used) key
        del self.cache[lru_key]  # Delete the LRU key-value pair
        del self.timestamps[lru_key]  # Remove the timestamp for the LRU item
        self.evictions += 1  # Increment eviction count
