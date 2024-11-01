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
                raise ValueError("Key must be an integer.")
            self.capacity = capacity
            self.cache = {}  # Dictionary to hold key-node pairs
            self.head = Node(0, 0)
            self.tail = Node(0, 0)
            self.head.next = self.tail
            self.tail.prev = self.head
            self.miss_count = 0
            self.access_count = 0   # total number of cache accesses (hits/misses)

        except ValueError as e:
            print(f"Error: {e}")

    def get(self, key):    # return the value of the corresponding key
        self.access_count += 1
        try:
            if not isinstance(key, int):
                raise ValueError("Key must be an integer.")

            if key in self.cache:
                node = self.cache[key]   # value of the key is of type Node
                self.remove_node(node)
                self.add_node(node)
                return node.value
            else:
                self.miss_count += 1
                return -1

        except ValueError as e:
            print(f"Error: {e}")
            return -1

    def put(self, key, value):
        try:
            if not (isinstance(key, int) or isinstance(value, int)):
                raise ValueError("Key and value both must be integers.")

            if key in self.cache:
                self.remove_node(self.cache[key])
            elif len(self.cache) >= self.capacity:
                lru = self.head.next    # lru is a node type variable
                self.remove_node(lru)
                del self.cache[lru.key]

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


lru_cache = LRUCache(2)
lru_cache.put(1, 1)
lru_cache.put(2, 2)
print(lru_cache.get(1))  # return 1
lru_cache.put(3, 3)  # LRU key was 2 so, evicts key 2
print(lru_cache.get(2))  # returns -1
print(lru_cache.get_miss_rate())
