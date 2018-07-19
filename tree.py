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

def rebuild(pre, center):
    if not pre:
        return None
    cur = Node(pre[0])
    index = center.index(pre[0])
    cur.left = rebuild(pre[1:index+1], center[ :index])
    cur.right = rebuild(pre[index+1 :], center[index+1 : ])
    return cur


pos_travelsal(tree)
print("-*-*-*-----------------------------")
pos_travelsal_stack(tree)

