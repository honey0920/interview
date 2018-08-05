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



def delete_dup(list1):
    if(list1 is None or list1.next is None):
        return list1

    pre = None
    cur = list1
    while cur.next != None:
        if cur.val != cur.next.val:
            pre = cur
            cur = cur.next
        else :
            value = cur.val
            to_del = cur
            while to_del != None and to_del.val == value:
                nxt = to_del.next
                to_del = nxt
            if pre == None:
                list1 = nxt
            else :
                pre.next = nxt

            cur = nxt
    return list1

def is_loop(head):
    if head is None or head.next is None:
        return False
    slow = head.next
    fast = slow.next
    while fast != None:
        if  slow != fast :
            slow = slow.next
            fast = fast.next.next
        else:
            return True
    return False

def back_k(head, k):
    if head is None or k == 0:
        return head
    cur = head
    l = 0
    while cur != None:
        cur = cur.next
        l += 1
    if l < k:
        return None
    else:
        fast = head
        slow = head
        for i in range(k):
            fast = fast.next
        while fast != None:
            fast = fast.next
            slow = slow.next
        return slow

def merge_list(head1, head2):
    if head1 is None:
        return head2
    if head2 is None:
        return head1

    if head1.val > head2.val:
        head3 = ListNode(head2.val)
        head2 = head2. next
    else:
        head3 = ListNode(head1.val)
        head1 = head1.next

    cur = head3

    while head1 != None and head2 != None:
        if head1.val > head2.val:
            cur.next = ListNode(head2.val)
            head2 = head2.next
            cur = cur.next
        else :
            cur.next = ListNode(head1.val)
            head1 = head1.next
            cur = cur.next

    while head1 != None:
        cur.next = ListNode(head1.val)
        head1 = head1.next
        cur = cur.next

    while head2 !=None:
        cur.next = ListNode(head2.val)
        head2 = head2.next
        cur = cur.next
    return head3

a = init_list([1,3,5,7,8,9])
b = init_list([2,4 ,6, 7, 10])
# a.next.next = ListNode(3)

#r = delete_dup(a)
r = merge_list(a, b)
show(r)
