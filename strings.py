#!/usr/bin/env

import math

NUM_CHARACTERS = 256


# help functions
def sort_string(s):
    return "".join(sorted(s))


# answers
def q1_is_anagrams(s1, s2):
    return sort_string(s1) == sort_string(s2)


def q1_is_anagrams_better_solution(s1, s2):
    count1 = [0] * NUM_CHARACTERS
    count2 = [0] * NUM_CHARACTERS
    for c in s1:
        count1[ord(c)] += 1
    for c in s2:
        count2[ord(c)] += 1

    return count1 == count2


def q2_get_num_of_words(s):
    is_previous_alpha = False
    words_count = 0
    for c in s:
        if c.isalpha():
            if not is_previous_alpha:
                words_count += 1
            is_previous_alpha = True
        else:
            is_previous_alpha = False
    return words_count


def q3_string_to_int_without_using_int_func(str1):
    is_negative = str1[0] == '-'
    leftovers = str1[1:] if is_negative else str1
    result = 0

    for c in leftovers:
        if '0' <= c <= '9':
            result = result * 10 + ord(c) - ord('0')

    if is_negative:
        result *= -1
    return result


def q4_number_to_words():
    # skipped
    pass


def q5_roman_numeral_to_integer():
    # skipped
    pass


def q6_compress_string(str1):
    count = 1
    previous_char = str1[0]
    leftovers = str1[1:]
    result = ""
    for c in leftovers:
        if c is previous_char:
            count += 1
        else:
            result += previous_char + str(count)
            previous_char = c
            count = 1
    result += previous_char + str(count)
    return result


def q7_remove_dups(str1):
    was_char_observed = [0] * NUM_CHARACTERS
    result = ""
    for c in str1:
        if was_char_observed[ord(c)] is 0:
            result += c
        was_char_observed[ord(c)] += 1
    return result


def q8_replace_all_spaces(str1, to_replace='%20'):
    return to_replace.join(str1.split(' '))


if __name__ == '__main__':
    q1_is_anagrams("hello", "eollh")
    q1_is_anagrams_better_solution("hello", "eollh")
    q2_get_num_of_words("hello every body, 25414 how are you")
    q3_string_to_int_without_using_int_func("-987")
    q6_compress_string("aasssdd")
    q7_remove_dups("hellodh")
    print(q8_replace_all_spaces("hello how are you ?"))
