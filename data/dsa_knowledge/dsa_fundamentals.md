# Data Structures and Algorithms - Knowledge Base

## Arrays

### Definition

An array is a collection of elements stored at contiguous memory locations. Elements can be accessed randomly using indices.

### Time Complexities

- Access: O(1)
- Search: O(n) for unsorted, O(log n) for sorted (binary search)
- Insertion: O(n) at arbitrary position, O(1) at end (amortized for dynamic arrays)
- Deletion: O(n) at arbitrary position, O(1) at end

### Dynamic Arrays

Dynamic arrays (like Python's list, Java's ArrayList) automatically resize when capacity is exceeded. Typically doubles in size, giving amortized O(1) insertion at the end.

---

## Linked Lists

### Definition

A linked list is a linear data structure where elements are stored in nodes, and each node points to the next node in the sequence.

### Types

1. **Singly Linked List**: Each node has data and a pointer to the next node
2. **Doubly Linked List**: Each node has data and pointers to both next and previous nodes
3. **Circular Linked List**: Last node points back to the first node

### Time Complexities

- Access: O(n)
- Search: O(n)
- Insertion at head: O(1)
- Insertion at tail: O(n) for singly, O(1) for doubly with tail pointer
- Deletion: O(1) if node is given, O(n) to find and delete

### Comparison with Arrays

| Aspect             | Array      | Linked List    |
| ------------------ | ---------- | -------------- |
| Memory             | Contiguous | Non-contiguous |
| Random Access      | O(1)       | O(n)           |
| Insertion at start | O(n)       | O(1)           |
| Cache Performance  | Better     | Worse          |

---

## Stacks

### Definition

A stack is a LIFO (Last In, First Out) data structure. The last element added is the first one removed.

### Operations

- **push(x)**: Add element to top - O(1)
- **pop()**: Remove element from top - O(1)
- **peek()/top()**: View top element - O(1)
- **isEmpty()**: Check if stack is empty - O(1)

### Applications

- Function call stack (recursion)
- Expression evaluation and parsing
- Undo operations
- Backtracking algorithms
- Balanced parentheses checking

---

## Queues

### Definition

A queue is a FIFO (First In, First Out) data structure. The first element added is the first one removed.

### Types

1. **Simple Queue**: Basic FIFO
2. **Circular Queue**: Efficient array implementation
3. **Priority Queue**: Elements have priorities
4. **Deque**: Double-ended queue

### Operations

- **enqueue(x)**: Add element to rear - O(1)
- **dequeue()**: Remove element from front - O(1)
- **front()**: View front element - O(1)
- **isEmpty()**: Check if queue is empty - O(1)

---

## Trees

### Binary Tree

A tree where each node has at most two children (left and right).

### Binary Search Tree (BST)

A binary tree where:

- All nodes in left subtree have values less than the root
- All nodes in right subtree have values greater than the root
- Both left and right subtrees are also BSTs

### Time Complexities (BST)

- Search: O(h) where h is height
- Insertion: O(h)
- Deletion: O(h)
- Best case (balanced): O(log n)
- Worst case (skewed): O(n)

### Balanced Trees

To prevent O(n) operations:

- **AVL Tree**: Self-balancing, maintains height difference ≤ 1
- **Red-Black Tree**: Self-balancing using color properties
- **B-Tree**: Used in databases, multiple keys per node

### Tree Traversals

1. **Inorder (Left, Root, Right)**: Gives sorted order for BST
2. **Preorder (Root, Left, Right)**: Used for tree copying
3. **Postorder (Left, Right, Root)**: Used for deletion
4. **Level Order**: Uses queue, BFS approach

---

## Graphs

### Definition

A graph G = (V, E) consists of vertices (V) and edges (E) connecting them.

### Types

- **Directed vs Undirected**
- **Weighted vs Unweighted**
- **Cyclic vs Acyclic**
- **Connected vs Disconnected**

### Representations

1. **Adjacency Matrix**: O(V²) space, O(1) edge lookup
2. **Adjacency List**: O(V+E) space, more efficient for sparse graphs

### Graph Traversals

#### BFS (Breadth-First Search)

- Uses a queue
- Explores all neighbors at current depth before moving deeper
- Time: O(V+E)
- Space: O(V)
- Applications: Shortest path in unweighted graphs, level-order traversal

#### DFS (Depth-First Search)

- Uses a stack (or recursion)
- Explores as far as possible along each branch
- Time: O(V+E)
- Space: O(V)
- Applications: Cycle detection, topological sort, finding connected components

---

## Sorting Algorithms

### Comparison-based Sorts

| Algorithm      | Best       | Average    | Worst      | Space    | Stable |
| -------------- | ---------- | ---------- | ---------- | -------- | ------ |
| Bubble Sort    | O(n)       | O(n²)      | O(n²)      | O(1)     | Yes    |
| Selection Sort | O(n²)      | O(n²)      | O(n²)      | O(1)     | No     |
| Insertion Sort | O(n)       | O(n²)      | O(n²)      | O(1)     | Yes    |
| Merge Sort     | O(n log n) | O(n log n) | O(n log n) | O(n)     | Yes    |
| Quick Sort     | O(n log n) | O(n log n) | O(n²)      | O(log n) | No     |
| Heap Sort      | O(n log n) | O(n log n) | O(n log n) | O(1)     | No     |

### Key Concepts

- **Stable Sort**: Maintains relative order of equal elements
- **In-place Sort**: Uses O(1) extra space
- **Lower bound**: Comparison-based sorting is Ω(n log n)

---

## Searching Algorithms

### Linear Search

- Time: O(n)
- Works on any array (sorted or unsorted)

### Binary Search

- Time: O(log n)
- Requires sorted array
- Divides search space in half each iteration

```
function binarySearch(arr, target):
    left = 0, right = n-1
    while left <= right:
        mid = (left + right) / 2
        if arr[mid] == target: return mid
        else if arr[mid] < target: left = mid + 1
        else: right = mid - 1
    return -1
```

---

## Dynamic Programming

### Definition

Dynamic Programming (DP) solves complex problems by breaking them into overlapping subproblems and storing results to avoid redundant computation.

### Key Properties

1. **Optimal Substructure**: Optimal solution can be constructed from optimal solutions of subproblems
2. **Overlapping Subproblems**: Same subproblems are solved multiple times

### Approaches

1. **Top-Down (Memoization)**: Recursive with caching
2. **Bottom-Up (Tabulation)**: Iterative, builds solution from base cases

### Classic DP Problems

- Fibonacci sequence
- Longest Common Subsequence (LCS)
- Longest Increasing Subsequence (LIS)
- 0/1 Knapsack
- Coin Change
- Matrix Chain Multiplication
- Edit Distance

---

## Time Complexity Analysis

### Big O Notation

Describes upper bound of algorithm's growth rate.

### Common Complexities (fastest to slowest)

1. O(1) - Constant
2. O(log n) - Logarithmic
3. O(n) - Linear
4. O(n log n) - Linearithmic
5. O(n²) - Quadratic
6. O(n³) - Cubic
7. O(2ⁿ) - Exponential
8. O(n!) - Factorial

### Space Complexity

Amount of extra memory an algorithm uses relative to input size.

---

## Hash Tables

### Definition

Data structure that maps keys to values using a hash function.

### Operations

- Insert: O(1) average, O(n) worst
- Search: O(1) average, O(n) worst
- Delete: O(1) average, O(n) worst

### Collision Resolution

1. **Chaining**: Each bucket contains a linked list
2. **Open Addressing**: Probe for next available slot
   - Linear probing
   - Quadratic probing
   - Double hashing

### Load Factor

α = n/m (number of elements / number of buckets)
When α exceeds threshold (typically 0.75), rehashing is needed.

---

## Heaps

### Definition

A heap is a complete binary tree that satisfies the heap property.

### Types

- **Max Heap**: Parent ≥ children
- **Min Heap**: Parent ≤ children

### Operations

- Insert: O(log n) - Add at end, bubble up
- Extract Max/Min: O(log n) - Remove root, bubble down
- Peek: O(1)
- Heapify: O(n)

### Applications

- Priority Queues
- Heap Sort
- Dijkstra's algorithm
- Finding k largest/smallest elements
