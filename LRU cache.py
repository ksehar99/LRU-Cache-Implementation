import time

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        try:
            if not isinstance(capacity, int):
                raise ValueError("Capacity must be an integer.")
            self.capacity = capacity
            self.cache = {}  # Dictionary to hold key-node pairs
            self.head = Node(0, 0)
            self.tail = Node(0, 0)
            self.head.next = self.tail
            self.tail.prev = self.head
            self.miss_count = 0
            self.access_count = 0
            self.hits_count = 0
            self.evictions = 0
            self.access_times = []
            self.eviction_times = []
        except ValueError as e:
            print(f"Error: {e}")

    def get(self, key):
        self.access_count += 1
        start_time = time.time()
        try:
            if not isinstance(key, int):
                raise ValueError("Key must be an integer.")

            if key in self.cache:
                self.hits_count += 1
                node = self.cache[key]
                self.remove_node(node)
                self.add_node(node)
                self.access_times.append(time.time() - start_time)
                return node.value
            else:
                self.miss_count += 1
                self.access_times.append(time.time() - start_time)
                return -1
        except ValueError as e:
            print(f"Error: {e}")
            return -1

    def put(self, key, value):
        try:
            if not (isinstance(key, int) and isinstance(value, int)):
                raise ValueError("Key and value must be integers.")
            start_time = time.time()
            if key in self.cache:
                self.remove_node(self.cache[key])
            elif len(self.cache) >= self.capacity:
                lru = self.head.next
                self.remove_node(lru)
                del self.cache[lru.key]
                self.evictions += 1
                self.eviction_times.append(time.time() - start_time)

            new_node = Node(key, value)
            self.add_node(new_node)
            self.cache[key] = new_node
        except ValueError as e:
            print(f"Error: {e}")
            return -1

    def remove_node(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def add_node(self, node):
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node

    def get_miss_rate(self) -> float:
        if self.access_count == 0:
            return 0.0
        return self.miss_count / self.access_count

    def data(self):
        total_requests = self.hits_count + self.miss_count
        hit_rate = self.hits_count / total_requests if total_requests > 0 else 0
        miss_rate = 1 - hit_rate
        avg_access_time = sum(self.access_times) / len(self.access_times) if self.access_times else 0
        avg_eviction_time = sum(self.eviction_times) / len(self.eviction_times) if self.eviction_times else 0

        return {
            "Hit rate": hit_rate,
            "Miss rate": miss_rate,
            "Eviction count": self.evictions,
            "Average access time (s)": avg_access_time,
            "Average eviction time (s)": avg_eviction_time
        }

# Testing the LRUCache and displaying stats
lru_cache = LRUCache(2)
lru_cache.put(1, 1)
lru_cache.put(2, 2)
print(lru_cache.get(1))  # should return 1
lru_cache.put(3, 3)  # evicts key 2
print(lru_cache.get(2))  # should return -1
print("Miss rate:", lru_cache.get_miss_rate())
print("Statistics:", lru_cache.data())
