from typing import List, Any, Optional


class BinaryHeap:
    """Array-backed binary heap.

    Parameters
    - min_heap: if True (default) the heap is a min-heap (root is smallest).
                if False the heap is a max-heap (root is largest).
    """

    def __init__(self, min_heap: bool = True) -> None:
        self.data: List[Any] = []
        self.min_heap = min_heap

    # ---------- helpers ----------
    def _compare(self, a: Any, b: Any) -> bool:
        """Return True if a should be above b in the heap ordering."""
        return a < b if self.min_heap else a > b

    def _parent(self, idx: int) -> int:
        return (idx - 1) // 2

    def _left(self, idx: int) -> int:
        return 2 * idx + 1

    def _right(self, idx: int) -> int:
        return 2 * idx + 2

    def _sift_up(self, idx: int) -> None:
        # Move the element at idx up until heap property restored
        while idx > 0:
            p = self._parent(idx)
            if self._compare(self.data[idx], self.data[p]):
                self.data[idx], self.data[p] = self.data[p], self.data[idx]
                idx = p
            else:
                break

    def _sift_down(self, idx: int) -> None:
        # Move the element at idx down until heap property restored
        n = len(self.data)
        while True:
            l = self._left(idx)
            r = self._right(idx)
            candidate = idx
            if l < n and self._compare(self.data[l], self.data[candidate]):
                candidate = l
            if r < n and self._compare(self.data[r], self.data[candidate]):
                candidate = r
            if candidate == idx:
                break
            self.data[idx], self.data[candidate] = self.data[candidate], self.data[idx]
            idx = candidate

    # ---------- public API ----------
    def insert(self, value: Any) -> None:
        """Insert `value` into the heap."""
        self.data.append(value)
        self._sift_up(len(self.data) - 1)

    def peek(self) -> Optional[Any]:
        """Return the root value without removing it (None if empty)."""
        return self.data[0] if self.data else None

    def extract_root(self) -> Optional[Any]:
        """Remove and return the heap root (min or max). Returns None if empty."""
        if not self.data:
            return None
        root = self.data[0]
        last = self.data.pop()
        if self.data:
            # Move last element to root and sift down
            self.data[0] = last
            self._sift_down(0)
        return root

    def __len__(self) -> int:
        return len(self.data)

    def __bool__(self) -> bool:
        return bool(self.data)

    def __repr__(self) -> str:
        t = "min" if self.min_heap else "max"
        return f"BinaryHeap({t}, data={self.data!r})"


def _demo():
    print("BinaryHeap demo")
    h = BinaryHeap(min_heap=True)
    for v in [5, 3, 8, 1, 6, 2]:
        print(f"insert {v}")
        h.insert(v)
        print(" heap:", h.data)

    print("\nExtracting all roots (min-heap):")
    while h:
        print(h.extract_root(), end=" ")
    print("\n")

    # max-heap demo
    h2 = BinaryHeap(min_heap=False)
    for v in [5, 3, 8, 1, 6, 2]:
        h2.insert(v)
    print("Max-heap order:")
    while h2:
        print(h2.extract_root(), end=" ")
    print()


if __name__ == "__main__":
    _demo()
