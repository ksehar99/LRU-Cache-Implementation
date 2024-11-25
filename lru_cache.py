import time

class LRUCache:
    def __init__(self, capacity: int, ttl: int):
        self.capacity = capacity
        self.ttl = ttl
        self.cache = {}  # Storing the key-value pairs
        self.order = []  # Tracking the order of keys for eviction (Most recent at end)
        self.timestamps = {}  # Storing timestamps for each cache entry
        self.hits = 0  
        self.misses = 0  
        self.total_accesses = 0  
        self.evictions = 0 

    def put(self, key, value):
        """Add an item to the cache with validation."""
        self.total_accesses += 1

    
        if not (1 <= self.capacity <= 50):
            return "Error: Cache capacity must be between 1 and 50."
        if not (0 <= key <= 100):
            return "Error: Key must be between 0 and 100."
        if not (0 <= value <= 100):
            return "Error: Value must be between 0 and 100."

        if key in self.cache:
            self.hits += 1
            self.cache[key] = value
            self.order.remove(key)
            self.order.append(key)
            self.timestamps[key] = time.time()
            return "Cache Hit: Updated value."

        self.misses += 1
        if len(self.cache) >= self.capacity:
            self._evict_if_needed()

        self.cache[key] = value
        self.order.append(key)
        self.timestamps[key] = time.time()
        return "Cache Miss: New entry added."


    def get(self, key):
        """Retrieve an item from the cache."""
        current_time = time.time()
        # Remove expired keys before accessing
        self._remove_expired_keys(current_time)

        self.total_accesses += 1  

        if key in self.cache:
            
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
        if self.total_accesses == 0:  
            return 0.0
        return (self.misses / self.total_accesses) * 100

    def _remove_expired_keys(self, current_time):
        """Remove expired keys based on TTL."""
        expired_keys = [key for key, timestamp in self.timestamps.items()
                        if current_time - timestamp >= self.ttl]
        for key in expired_keys:
            self.cache.pop(key, None)  # Remove expired key from cache
            self.timestamps.pop(key, None)  
            self.order.remove(key)  # Remove expired key from order list
            self.evictions += 1  

    def _evict_if_needed(self):
        """Evict the least recently used (LRU) item."""
        lru_key = self.order.pop(0) 
        del self.cache[lru_key]  # Delete the LRU key-value pair
        del self.timestamps[lru_key]  
        self.evictions += 1  # Increment eviction count

