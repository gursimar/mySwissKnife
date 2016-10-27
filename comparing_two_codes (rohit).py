import re
import base64
import operator
import os
import sys
import time
import nltk
import csv
from nltk.util import ngrams

scanner = re.Scanner([
    (r"[a-z_A-Z][a-z_A-Z0-9]*", lambda scanner, token: ("IDENTIFIER", token)),
    (r"[0-9]+", lambda scanner, token: ("INTEGER_CONSTANT", token)),
    (r"[.]", lambda scanner, token: ("DOT", token)),
    (r"[@]", lambda scanner, token: ("@", token)),
    (r"[,]+", lambda scanner, token: ("PUNCTUATION", token)),
    (r"[{]", lambda scanner, token: ("CURLY_BRACE_START", token)),
    (r"[}]", lambda scanner, token: ("CURLY_BRACE_END", token)),
    (r"[[]", lambda scanner, token: ("SQUARE_START", token)),
    (r"[]]", lambda scanner, token: ("SQUARE_END", token)),
    (r"[;]", lambda scanner, token: ("SEMICOLON", token)),
    (r"[:]", lambda scanner, token: ("COLON", token)),
    (r"[?]", lambda scanner, token: ("CONDITIONAL_COLON", token)),
    (r"[(]", lambda scanner, token: ("PARANTHESIS_START", token)),
    (r"[)]", lambda scanner, token: ("PARANTHESIS_END", token)),
    (r"[=]{2}", lambda scanner, token: ("EQUAL_TO", token)),
    (r"[>][=]", lambda scanner, token: ("GREATER_EQUAL_TO", token)),
    (r"[>]", lambda scanner, token: ("GREATER", token)),
    (r"[=]{1}", lambda scanner, token: ("ASSIGNMENT", token)),
    (r"[<]{1}[=]{1}", lambda scanner, token: ("LESS_THAN_EQUAL_TO", token)),
    (r"[<]{1}", lambda scanner, token: ("LESS_THAN", token)),
    (r"[+]{2}", lambda scanner, token: ("INCREMENT", token)),
    (r"[-]{2}", lambda scanner, token: ("DECREMENT", token)),
    (r"[+]{1}[=]{1}", lambda scanner, token: ("ADDITION_COMPOUND", token)),
    (r"[+]{1}", lambda scanner, token: ("ADDITION", token)),
    (r"[-]{1}[=]{1}", lambda scanner, token: ("SUBTRACTION_COMPOUND", token)),
    (r"[-]{1}", lambda scanner, token: ("SUBTRACTION", token)),
    (r"[*]{1}[=]{1}", lambda scanner, token: ("MULTIPLICATION_COMP0UND", token)),
    (r"[*]{1}", lambda scanner, token: ("MULTIPLICATION", token)),
    (r"[\^]{1}[=]{1}", lambda scanner, token: ("EXPONENT_COMP0UND", token)),
    (r"[\^]{1}", lambda scanner, token: ("EXPONENT", token)),
    (r"[/]{1}[=]{1}", lambda scanner, token: ("DIVISION_COMP0UND", token)),
    (r"[/]{1}", lambda scanner, token: ("DIVISION", token)),
    (r"[%]{1}[=]{1}", lambda scanner, token: ("MOD_COMP0UND", token)),
    (r"[%]{1}", lambda scanner, token: ("MOD", token)),
    (r"[|]{2}", lambda scanner, token: ("LOGICAL_OR", token)),
    (r"[&]{2}", lambda scanner, token: ("LOGICAL_AND", token)),
    (r"[|]{1}", lambda scanner, token: ("OR", token)),
    (r"[&]{1}", lambda scanner, token: ("AND", token)),
    (r"[!]", lambda scanner, token: ("NOT", token)),
    (r"'(''|[^'])*'", lambda scanner, token: ("CHAR_CONSTANT", token)),
    (r'"(""|[^"])*"', lambda scanner, token: ("CHAR_CONSTANT", token)),
    (r"\s+", None),
    (r"[^\x00-\x7F]+", None),
    (r".", lambda scanner, token: ("RANDOM", token)),
])


def remove_comments(data):
    p = re.compile('(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)')
    comments = p.search(data)
    while comments is not None:
        data = data[:comments.span()[0]] + data[comments.span()[1]:]
        comments = p.search(data)
    return data


def line_number_to_remove(data, start_line):
    data_source = "\n".join(data[start_line:])
    it = 0
    line_number = 0
    while it < len(data_source) and data_source[it] != '{':
        if data_source[it] == '\n':
            line_number += 1
        it += 1
    if it == len(data_source):
        return -1
    it += 1
    open_brace = 1
    close_brace = 0
    while it < len(data_source) and open_brace > close_brace:
        if data_source[it] == '}':
            close_brace += 1
        elif data_source[it] == '{':
            open_brace += 1
        if data_source[it] == '\n':
            line_number += 1
        it += 1

    return start_line + line_number + 1


def remove_extra_part(source):
    return source[0:source.find("public")]


with open(r"codes.csv", "rb") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        source_initial = row[0]
        source_final = row[1]
        source_initial = remove_comments(source_initial)
        source_initial = re.sub('[^\x00-\x7F]+', '', source_initial)
        source_initial_lines = source_initial.split('\n')
        start_line = 0
        found_main = 0
        for line in source_initial_lines:
            p = re.findall('main\s*\(\s*String', line)
            if len(p) > 0:
                found_main = 1
                break
            start_line += 1
        if found_main == 1:
            try:
                x = line_number_to_remove(source_initial_lines, start_line)
            except:
                x = -5
            print x
            if x != -1 and x != -5:
                source_initial_lines[start_line] = remove_extra_part(source_initial_lines[start_line])
                source_initial = '\n'.join(source_initial_lines[0:start_line + 1]) + "\n" + '\n'.join(
                    source_initial_lines[x:])
        source_final = remove_comments(source_final)
        source_final = re.sub('[^\x00-\x7F]+', '', source_final)
        source_final_lines = source_final.split('\n')
        start_line = 0
        found_main = 0
        for line in source_final_lines:
            p = re.findall('main\s*\(\s*String', line)
            if len(p) > 0:
                found_main = 1
                break
            start_line += 1
        if found_main == 1:
            try:
                x = line_number_to_remove(source_final_lines, start_line)
            except:
                x = -5
            print x
            if x != -1 and x != -5:
                source_final_lines[start_line] = remove_extra_part(source_final_lines[start_line])
                source_final = '\n'.join(source_final_lines[0:start_line + 1]) + "\n" + '\n'.join(
                    source_final_lines[x:])

        tokens_initial, remainder_initial = scanner.scan(source_initial)
        tokens_final, remainder_final = scanner.scan(source_final)
        tk_1 = []
        tk_2 = []
        for tk in tokens_initial:
            pre = ''
            if (tk[0] == ';' and pre == ';') or (tk[0] == ';' and pre == '}'):
                continue
            else:
                pre = tk[0]
                tk_1.append(tk[0])

        for tk in tokens_final:
            pre = ''
            if (tk[0] == ';' and pre == ';') or (tk[0] == ';' and pre == '}'):
                continue
            else:
                pre = tk[0]
                tk_2.append(tk[0])

        diff = len(tk_1) - len(tk_2)

        data = base64.b64encode(source_initial) + "," + base64.b64encode(source_final) + "," + str(diff) + "\n"
        f = open(r"result.csv", "a")
        f.write(data)
        f.close()