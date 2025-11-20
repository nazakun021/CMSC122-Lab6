from collections import deque

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  

class AVLTree:
    def __init__(self):
        self.root = None

    #helper funct

    # get h of tree
    def get_height(self, n):
        if n is None:
            return 0
        return n.height

    # get balance fctr of node N
    def get_balance(self, n):
        if n is None:
            return 0
        return self.get_height(n.left) - self.get_height(n.right)

    # Right Rotate Utility (LL Case)
    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # Rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1

        return x

    # Left Rotate Utility (RR Case)
    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # Rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1

        return y

    # Find the node with minimum value (for deletion)
    def min_value_node(self, node):
        current = node
        # Loop down to find the leftmost leaf
        while current.left is not None:
            current = current.left
        return current

    # insert logic
    
    def _insert_node(self, node, key):
        # 1. Perform the normal BST insertion
        if node is None:
            return Node(key)

        if key < node.key:
            node.left = self._insert_node(node.left, key)
        elif key > node.key:
            node.right = self._insert_node(node.right, key)
        else:
            return node

        # 2. update height of this ancestor node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # 3. gwt the balance factor of this ancestor node
        balance = self.get_balance(node)

        # 4. If this node becomes unbalanced, handle 4 cases

        # LL Case
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # RR Case
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # LR Case
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # RL Case
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    #dlete logic

    def _delete_node(self, root, key):
        # 1. Standard BST delete
        if root is None:
            return root

        if key < root.key:
            root.left = self._delete_node(root.left, key)
        elif key > root.key:
            root.right = self._delete_node(root.right, key)
        else:
            # Node with only one child or no child
            if root.left is None or root.right is None:
                temp = root.left if root.left else root.right

                # No child case
                if temp is None:
                    temp = root
                    root = None
                else:
                    # One child case
                    root = temp
                
            else:
                # Node with two children: Get the inorder successor
                temp = self.min_value_node(root.right)

                # Copy the inorder successor's data to this node
                root.key = temp.key

                # Delete the inorder successor
                root.right = self._delete_node(root.right, temp.key)

        if root is None:
            return root

        # 2. updt height of the current node
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3. get the balance factor
        balance = self.get_balance(root)

        # 4. balance the tree if needed

        # LL Case
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # LR Case
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # RR Case
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # RL Case
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    #public methods

    def insert(self, key):
        self.root = self._insert_node(self.root, key)
        print(f"Inserted: {key}")

    def remove(self, key):
        self.root = self._delete_node(self.root, key)
        print(f"Deleted: {key}")

    #Traversal Helpers (DFS)
    
    def _pre_order_helper(self, root):
        if root is not None:
            print(root.key, end=" ")
            self._pre_order_helper(root.left)
            self._pre_order_helper(root.right)

    def _in_order_helper(self, root):
        if root is not None:
            self._in_order_helper(root.left)
            print(root.key, end=" ")
            self._in_order_helper(root.right)

    def _post_order_helper(self, root):
        if root is not None:
            self._post_order_helper(root.left)
            self._post_order_helper(root.right)
            print(root.key, end=" ")

    #Public Traversal Methods

    def print_pre_order(self):
        print("Preorder (DFS):", end=" ")
        self._pre_order_helper(self.root)
        print()

    def print_in_order(self):
        print("Inorder (DFS):", end=" ")
        self._in_order_helper(self.root)
        print()

    def print_post_order(self):
        print("Postorder (DFS):", end=" ")
        self._post_order_helper(self.root)
        print()

    def print_bfs(self):
        print("Level Order (BFS):", end=" ")
        if self.root is None:
            print()
            return

        q = deque([self.root])

        while q:
            current = q.popleft() # Equivalent to q.front() + q.pop()
            print(current.key, end=" ")

            if current.left is not None:
                q.append(current.left)
            if current.right is not None:
                q.append(current.right)
        print()

# mf to test implemntation
if __name__ == "__main__":
    tree = AVLTree()

    print("--- Building the AVL Tree ---")
    # Inserting nodes to test auto-balancing
    tree.insert(10)
    tree.insert(20)
    tree.insert(30) # shud cause rotation
    tree.insert(40)
    tree.insert(50)
    tree.insert(25)

    print("\n--- Visualizing Traversals ---")
    tree.print_pre_order()
    tree.print_in_order()
    tree.print_post_order()
    tree.print_bfs()

    print("\n--- Testing Deletion ---")
    # Deleting a node that might cause rotation
    tree.remove(40)
    tree.print_bfs()

    tree.remove(20) # Deleting node with children
    tree.print_in_order() # Should still be sorted
    tree.print_bfs()