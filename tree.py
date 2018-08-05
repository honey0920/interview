class Node(object):
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

tree = Node(1, Node(3, Node(7, Node(0)), Node(6)), Node(2, Node(5), Node(4)))
def mid_travelsal(root):
    if root is None:
        return

    if root.left is not None:
        mid_travelsal(root.left)
    print(root.data)
    if root.right is not None:
        mid_travelsal(root.right)

def mid_travelsal_stack(root):
    stack = []
    p = root
    while p is not None or len(stack) > 0 :
        while p :
            stack.append(p)
            p = p.left

        top = stack[-1]
        print(top.data)
        stack.pop(-1)

        p = top.right

def pre_travelsal(root):
    if not root :
        return
    print(root.data)
    if root.left is not None:
        pre_travelsal(root.left)
    if root.right is not Node:
        pre_travelsal(root.right)

def pre_travelsal_stack(root):
    stack = []
    p = root
    while p is not None or len(stack) > 0:
        while p :
            print(p.data)
            stack.append(p)
            p = p.left

        top = stack[-1]
        stack.pop(-1)
        p = top.right

def pos_travelsal(root):
    if not root :
        return

    if root.left is not None:
        pos_travelsal(root.left)
    if root.right is not Node:
        pos_travelsal(root.right)
    print(root.data)


def pos_travelsal_stack(root):
    stack = []
    p = root
    pre = None
    while p is not None or len(stack) > 0:
        while p :
            stack.append(p)
            p = p.left

        top = stack[-1]
        if top.right is None or top.right == pre:
            print(top.data)
            stack.pop(-1)
            pre = top

        else :
            p = top.right

def max_depth(root):
    if not root:
        return 0
    return max(max_depth(root.left), max_depth(root.right)) + 1

def print_tree(root):
    if root is None:
        return
    queue = []
    queue.append(root)
    while queue != []:
        node = queue[0]
        queue.pop(0)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
        print(node.data)

def print_line(root):
    if root is None:
        return
    queue = []
    lines = []
    queue.append(root)
    lines.append(0)
    cur_line = 0
    while queue != [] :
        node = queue[0]
        line = lines[0]
        queue.pop(0)
        lines.pop(0)
        if node.left:
            queue.append(node.left)
            lines.append(line+1)
        if node.right:
            queue.append(node.right)
            lines.append(line+1)
        if(cur_line != line):
            print("")
            cur_line = line
        print str(node.data) + " "



def rebuild(pre, center):
    if not pre:
        return None
    cur = Node(pre[0])
    index = center.index(pre[0])
    cur.left = rebuild(pre[1:index+1], center[ :index])
    cur.right = rebuild(pre[index+1 :], center[index+1 : ])
    return cur

def next_node(cur):
    if cur is None:
        return cur

    if cur.right != None:
        right = cur.right
        while right.left != None :
            right = right.left
        return right
    elif cur.parent != None :
        parent = cur.parent
        node = cur
        while parent != None and node == parent.right:
            node = parent
            parent = parent.parent
        return parent
    return None

def find_path_core(root, target,  cur, paths, cur_path):
    cur += root.data
    cur_path.append(root.data)
    if cur == target and root.left == None and root.right == None:
        paths.append(tuple(cur_path))

    if root.left != None:
        find_path_core(root.left, target, cur, paths, cur_path)
    if root.right != None:
        find_path_core(root.right, target, cur, paths, cur_path)
    cur_path.pop(-1)



def find_path(root, target):
    if root is None:
        return None
    else:
        paths = []
        find_path_core(root, target, 0, paths, [])
        return paths


def verify_seq(seq):
    if seq == []:
        return False

    root = seq[-1]
    i = 0
    while seq[i] <= root and  i < len(seq)-1:
        i += 1

    for j in range(i, len(seq)):
        if seq[j] < root:
            return False
    left = True
    if i>0 :
        left = verify_seq(seq[:i])
    right = True
    if i < len(seq)-1:
        right = verify_seq(seq[i:-1])
    return left and right

#print(find_path(tree, 8))
#pos_travelsal(tree)
#print("-*-*-*-----------------------------")
#pos_travelsal_stack(tree)
print(verify_seq([5,7,6,9,11,10,8]))

