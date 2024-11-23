import time

class LRUCache:
    def __init__(self, capacity, ttl):
        self.capacity = capacity
        self.ttl = ttl  # Set Time-to-Live for cache entries
        self.cache = {}
        self.access_order = []  # Keeps track of the access order for eviction
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.timestamps = {}  # Store timestamps for TTL tracking

    def put(self, key, value):
        current_time = time.time()
        # Remove expired keys before inserting new ones
        self._remove_expired_keys(current_time)

        # Handle cache eviction if the cache is full
        if key in self.cache:
            self.access_order.remove(key)  # Move the key to the end if it already exists
        elif len(self.cache) >= self.capacity:
            oldest = self.access_order.pop(0)  # Evict the least recently used (oldest) item
            del self.cache[oldest]
            del self.timestamps[oldest]
            self.evictions += 1

        self.cache[key] = value
        self.timestamps[key] = current_time
        self.access_order.append(key)  # Add key to the access order list

    def get(self, key):
        current_time = time.time()
        # Remove expired keys before accessing
        self._remove_expired_keys(current_time)

        if key in self.cache:
            self.access_order.remove(key)  # Move accessed key to the end
            self.access_order.append(key)
            self.hits += 1
            return self.cache[key]
        else:
            self.misses += 1
            return None

    def clear(self):
        self.cache.clear()
        self.access_order.clear()
        self.timestamps.clear()

    def get_statistics(self):
        # Return cache statistics (hits, misses, and evictions)
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
        }

    def get_cache_details(self):
        current_time = time.time()
        self._remove_expired_keys(current_time)
        return [{"Key": k, "Value": v} for k, v in self.cache.items()]

    def _remove_expired_keys(self, current_time):
        # Remove expired keys based on TTL
        expired_keys = [key for key, timestamp in self.timestamps.items()
                        if current_time - timestamp >= self.ttl]
        for key in expired_keys:
            self.cache.pop(key, None)  # Remove expired key from cache
            self.timestamps.pop(key, None)  # Remove expired key from timestamps
            self.access_order.remove(key)  # Remove expired key from access order
