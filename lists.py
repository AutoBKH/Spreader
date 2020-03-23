#!/usr/bin/env


def q1_replace_with_next_biggest(a):
    n = len(a)
    local_max = a[n - 1]
    for i in range(n - 2, -1, -1):
        temp = a[i]
        a[i] = local_max
        local_max = max(local_max, temp)
    a[n - 1] = None


def q2_remove_instances(a, to_remove):
    fill_pos = 0
    n = len(a)
    for i in range(0, n):
        if a[i] is not to_remove:
            a[fill_pos] = a[i]
            fill_pos += 1
    del a[fill_pos:]


def q3_remove_dups_with_dic(a):
    d = {}
    n = len(a)
    for i in range(0, n):
        if i >= len(a):
            break
        if a[i] in d:
            del a[i]
        d[a[i]] = a[i]


def q3_remove_dups_with_sort(a):
    a.sort()
    i = 0
    while i < len(a) - 1:
        if a[i] is not a[i + 1]:
            i += 1
        else:
            del a[i]


def q4_remove_zeroes(a):
    fill_pos = 0
    num_zeroes = 0
    for i in range(0, len(a)):
        if a[i] is not 0:
            a[fill_pos] = a[i]
            fill_pos += 1
        else:
            num_zeroes += 1
    a = a[:fill_pos]
    return a


if __name__ == '__main__':
    q1_replace_with_next_biggest([0, 2, 8, 1, 3, 1, 5, 4])
    q2_remove_instances([0, 2, 8, 1, 3, 1, 5, 4], 1)
    q3_remove_dups_with_dic([0, 2, 8, 1, 3, 1, 5, 4])
    q3_remove_dups_with_sort([0, 2, 8, 1, 3, 1, 5, 4, 8, 8])
    q4_remove_zeroes([0, 2, 8, 1, 3, 1, 0, 0, 8, 8])
