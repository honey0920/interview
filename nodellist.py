class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def init_list(list):
    if len(list) == 0:
        return None
    head = ListNode(list[0])
    node = head
    for val in list[1:]:
        node.next = ListNode(val)
        node = node.next
    return head


def show(head):
    node = head
    while node != None:
        print(node.val)
        node = node.next


def reverse(head):
    if head is None or head.next is None:
        return head
    pre = head
    cur = head.next
    head.next = None
    while pre is not None and cur is not None:
        next = cur.next
        cur.next = pre
        pre = cur
        cur = next
    return pre


def reverse_r(head):
    if head is None or head.next is None:
        return head
    else:
        new_head = reverse_r(head.next)
        head.next.next = head
        head.next = None
    return new_head


def swapPairs(head):
    if head is None or head.next is None:
        return head

    else:
        cur_1 = head
        cur_2 = head.next
        node = head.next
        while cur_2 is not None and cur_2.next is not None:
            next_1 = cur_2.next
            next_2 = next_1.next
            cur_1.next = next_1
            cur_2.next = cur_1
            cur_1 = next_1
            cur_2 = next_2
        return node


def swapPairs_r(head):
    if head is None or head.next is None:
        return head
    else:
        next = head.next
        head.next = swapPairs_r(next.next)
        next.next = head
        return next


def common_node(list1, list2):
    head1 = list1
    head2 = list2
    len1, len2 = 0
    while(list1.next):
        list1 = list1.next
        len1 += 1
    while(list2.next):
        list2 = list2.next
        len2 += 1

    if list1.next == list2.next:
        if(len1 < len2):
            for _ in range(len1 - len2):
                head2 = head2.next
                return head2
        else:
            for _ in range(len2 - len1):
                head1 = head1.next
                return head1
    return None




a = init_list([1, 2, 3, 4])
# a.next.next = ListNode(3)

r = swapPairs(a)
show(r)
