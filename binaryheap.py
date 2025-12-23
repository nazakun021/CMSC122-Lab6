from typing import List, Any, Optional


class BinaryHeap:
    """Array-backed binary heap.

    Parameters
    - min_heap: if True (default) the heap is a min-heap (root is smallest).
                if False the heap is a max-heap (root is largest).
    """

    def __init__(self, min_heap: bool = True) -> None:
        self.data: List[Any] = []                               # underlying list storing heap elements
        self.min_heap = min_heap                                # True for min-heap, False for max-heap

    # ---------- helpers ----------
    def _compare(self, a: Any, b: Any) -> bool:
        """Return True if a should be above b in the heap ordering."""
        return a < b if self.min_heap else a > b                # use < for min-heap, > for max-heap

    def _parent(self, idx: int) -> int:
        return (idx - 1) // 2                                   # parent index formula for array-backed binary tree

    def _left(self, idx: int) -> int:
        return 2 * idx + 1                                      # left child index

    def _right(self, idx: int) -> int:
        return 2 * idx + 2                                      # right child index

    def _sift_up(self, idx: int) -> None:
        # Move the element at idx up until heap property restored
        while idx > 0:                                                          # while not at the root
            p = self._parent(idx)                                               # compute parent index
            if self._compare(self.data[idx], self.data[p]):                     # if current should be above parent
                self.data[idx], self.data[p] = self.data[p], self.data[idx]     # swap with parent
                idx = p                                                         # continue sifting up from parent's index
            else:
                break                                                           # heap property satisfied, stop

    def _sift_down(self, idx: int) -> None:
        # Move the element at idx down until heap property restored
        n = len(self.data)                                                      # current heap size
        while True:
            l = self._left(idx)                                                 # left child index
            r = self._right(idx)                                                # right child index
            candidate = idx                                                     # assume current is the candidate to keep
            if l < n and self._compare(self.data[l], self.data[candidate]):
                candidate = l                                                   # left child is a better candidate
            if r < n and self._compare(self.data[r], self.data[candidate]):
                candidate = r                                                   # right child beats current candidate
            if candidate == idx:
                break                                                           # no child is better, heap property restored
            self.data[idx], self.data[candidate] = self.data[candidate], self.data[idx]  # swap down
            idx = candidate                                                     # continue sifting down from new position
  
    def insert(self, value: Any) -> None:
        """Insert `value` into the heap."""
        self.data.append(value)                                                 # append to maintain complete tree shape
        self._sift_up(len(self.data) - 1)                                       # restore heap property by sifting up

    def peek(self) -> Optional[Any]:
        """Return the root value without removing it (None if empty)."""
        return self.data[0] if self.data else None                              # root at index 0 or None if empty

    def extract_root(self) -> Optional[Any]:
        """Remove and return the heap root (min or max). Returns None if empty."""
        if not self.data:
            return None                                                         # empty heap
        root = self.data[0]                                                     # save root to return
        last = self.data.pop()                                                  # remove last element
        if self.data:
            # Move last element to root and sift down
            self.data[0] = last                                                 # place last element at root
            self._sift_down(0)                                                  # restore heap property by sifting down
        return root                                                             # return the original root

    def __len__(self) -> int:
        return len(self.data)                                                   # number of elements in heap

    def __bool__(self) -> bool:
        return bool(self.data)                                                  # truthy when heap is non-empty

    def __repr__(self) -> str:
        t = "min" if self.min_heap else "max"                                   # textual heap type
        return f"BinaryHeap({t}, data={self.data!r})"                           # debug representation


def _demo():
    print("BinaryHeap demo")                                                    # header
    h = BinaryHeap(min_heap=True)                                               # create a min-heap instance
    for v in [5, 3, 8, 1, 6, 2]:                                                # sample values to insert
        print(f"insert {v}")                                                    # show operation
        h.insert(v)                                                             # insert value
        print(" heap:", h.data)                                                 # show underlying array after insert

    print("\nMin-heap order:")                                                  # extraction header
    while h:                                                                    # while heap has elements (uses __bool__)
        print(h.extract_root(), end=" ")                                        # extract and print root repeatedly
    print("\n")  

    # max-heap demo
    h2 = BinaryHeap(min_heap=False)                                             # create a max-heap instance
    for v in [5, 3, 8, 1, 6, 2]:                                                # sample values to insert
        h2.insert(v)                                                            # insert into max-heap
    
    print(f"Peek root: {h2.peek()}")                                           # check root without removing
    single_extract = h2.extract_root()                                          # extract the current root
    print(f"Extracted single root: {single_extract}")                          # show what was removed
    print(f"Heap after extraction: {h2.data}")                                 # show re-balanced array
    
    print("Max-heap order:")                                                    # header for max-heap extraction
    while h2:                                                                   # while max-heap has elements (uses __bool__)
        print(h2.extract_root(), end=" ")                                      # print roots (largest first)
    print()                                                                     # final newline

if __name__ == "__main__":
    _demo()                                                                 
   