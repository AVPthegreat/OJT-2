# Common DSA Interview Questions

## Arrays

### Q: What's the difference between an array and a linked list?

**Expected Answer:**
Arrays store elements in contiguous memory locations allowing O(1) random access but O(n) insertion/deletion. Linked lists store elements in nodes with pointers, allowing O(1) insertion/deletion at known positions but O(n) access. Arrays have better cache locality. Choose arrays for frequent access, linked lists for frequent insertions/deletions.

### Q: How does dynamic array resizing work?

**Expected Answer:**
When capacity is exceeded, a new array (typically 2x size) is allocated, elements are copied, and old array is deallocated. While individual resize is O(n), amortized cost of n insertions is O(n), giving O(1) amortized per insertion.

---

## Linked Lists

### Q: How do you detect a cycle in a linked list?

**Expected Answer:**
Floyd's Cycle Detection (Tortoise and Hare): Use two pointers, slow moves 1 step, fast moves 2 steps. If they meet, cycle exists. Time: O(n), Space: O(1). Alternative: HashSet to store visited nodes - O(n) time and space.

### Q: How do you reverse a linked list?

**Expected Answer:**
Iterative: Use three pointers (prev, curr, next). For each node, save next, point curr to prev, move prev and curr forward. Time: O(n), Space: O(1).
Recursive: Reverse rest of list, then adjust pointers. Time: O(n), Space: O(n) for call stack.

---

## Trees

### Q: What makes a tree a Binary Search Tree?

**Expected Answer:**
For every node: all values in left subtree are smaller, all values in right subtree are larger. Both subtrees must also be valid BSTs. This property enables O(log n) search in balanced trees by eliminating half the search space at each step.

### Q: What happens when a BST becomes unbalanced? How do you prevent it?

**Expected Answer:**
Unbalanced BST degrades to O(n) operations (becomes like a linked list). Prevention: Use self-balancing trees like AVL (maintains height difference ≤ 1 using rotations) or Red-Black trees (uses color properties to maintain balance). These guarantee O(log n) operations.

### Q: Explain the three tree traversals.

**Expected Answer:**

- Inorder (Left, Root, Right): Visits nodes in sorted order for BST. Used for getting elements in order.
- Preorder (Root, Left, Right): Visits root first. Used for copying trees or prefix expression evaluation.
- Postorder (Left, Right, Root): Visits root last. Used for deleting trees or postfix expression evaluation.

---

## Graphs

### Q: When would you use BFS vs DFS?

**Expected Answer:**
BFS: Use for shortest path in unweighted graphs, finding nodes at specific distance, level-order traversal. Uses queue, O(V+E) time.
DFS: Use for detecting cycles, topological sort, finding connected components, solving mazes. Uses stack/recursion, O(V+E) time.
Memory: BFS uses more memory (stores entire level) while DFS uses stack depth.

### Q: How do you detect a cycle in a graph?

**Expected Answer:**
Undirected: DFS - if you visit an already visited node that's not the parent, cycle exists.
Directed: DFS with three colors - white (unvisited), gray (in current path), black (processed). Finding gray node means back edge = cycle.
Alternative: Kahn's algorithm for topological sort - if not all nodes processed, cycle exists.

---

## Dynamic Programming

### Q: What is dynamic programming?

**Expected Answer:**
DP is an optimization technique that solves problems by breaking them into overlapping subproblems and storing results to avoid redundant computation. Requirements: optimal substructure (optimal solution built from optimal subproblems) and overlapping subproblems. Approaches: top-down with memoization or bottom-up with tabulation.

### Q: Solve the 0/1 Knapsack problem.

**Expected Answer:**
Given items with weights and values, maximize value within weight capacity.
State: dp[i][w] = max value using first i items with capacity w.
Recurrence: dp[i][w] = max(dp[i-1][w], dp[i-1]w-weight[i]] + value[i])
Time: O(n*W), Space: O(n*W) or O(W) with optimization.

---

## Sorting

### Q: Compare Merge Sort and Quick Sort.

**Expected Answer:**
Merge Sort: Always O(n log n), stable, but O(n) extra space. Good for linked lists.
Quick Sort: O(n log n) average, O(n²) worst (mitigated by random pivot). O(log n) space. In-place, not stable. Generally faster due to cache efficiency.
Choose Merge Sort when stability needed or working with linked lists. Choose Quick Sort for arrays when average case is acceptable.

### Q: Why is the lower bound for comparison-based sorting O(n log n)?

**Expected Answer:**
Any comparison-based sort can be modeled as a decision tree. With n elements, there are n! possible orderings. The tree needs n! leaves, so height is at least log(n!) = Ω(n log n). Therefore, at least O(n log n) comparisons are needed in the worst case.

---

## Complexity Analysis

### Q: What's the difference between O(n) and θ(n)?

**Expected Answer:**
Big O is an upper bound - the algorithm runs in at most this time. Theta (θ) is a tight bound - the algorithm runs in exactly this time asymptotically. Big Omega (Ω) is a lower bound. For example, array access is θ(1), while linear search is O(n) in general but θ(n) for worst/average case.

### Q: What is amortized analysis?

**Expected Answer:**
Amortized analysis averages the cost of operations over a sequence, giving a more accurate picture than worst-case. Example: dynamic array insertion is O(n) worst case (during resize) but O(1) amortized because resizes happen infrequently. Methods: aggregate analysis, accounting method, potential method.

---

## Hash Tables

### Q: How do hash tables handle collisions?

**Expected Answer:**
Two main approaches:

1. Chaining: Each bucket stores a linked list of colliding elements. Simple but uses extra space.
2. Open Addressing: Find next available slot using probing (linear, quadratic, or double hashing). Better cache performance but more complex deletion.
   Load factor (n/m) affects performance - when too high, rehash to larger table.

### Q: Why is hash table lookup O(1) average but O(n) worst case?

**Expected Answer:**
Average O(1) because good hash function distributes keys uniformly across buckets. Worst case O(n) when all keys hash to same bucket (unlikely with good hash function). Maintaining low load factor and using quality hash functions minimizes collision probability.
