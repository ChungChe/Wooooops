#!/usr/bin/env python
import sys
from file_utility import file_holder

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} search_string".format(sys.argv[0]))
        sys.exit()
    h = file_holder()
    if sys.argv[1] == "-p":
        #h.show_possible_match(sys.argv[2], True)
        h.show(sys.argv[2], True)
    else:
        #h.show_possible_match(sys.argv[1])
        h.show(sys.argv[1])

