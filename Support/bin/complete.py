#!/usr/bin/python
# encoding: utf-8

import re
import os
import TextMate
from rlcompleter import Completer


def get_completions(current_word):
    list = []
    if current_word != None:
        completer = Completer()
        new_word = completer.complete(current_word, 0)
        i = 0
        while new_word:
            list.append(new_word)
            i += 1
            new_word = completer.complete(current_word, i)

    # TODO: Sort list, but by what criteria? __underscores__ last?
    # Possible to sort by properties, methods, classes, packages?
    return list


def main():
    current_word = TextMate.current_word(r"[\w_\.]*", 'left')
    completions = get_completions(current_word)
    num_completions = len(completions)
    if num_completions:
        if num_completions > 1:
            completion = TextMate.menu(completions)
        else:
            completion = completions[0]

        if completion is not None:
            new_text = re.sub(r'^' + current_word,'', completion)
            TextMate.exit_insert_snippet(new_text)
    else:
        TextMate.exit_show_tool_tip("No completions")


if __name__ == "__main__":
    main()


