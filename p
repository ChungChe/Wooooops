#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from javlib_handler import *

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: {} search_string".format(sys.argv[0]))
        sys.exit()
    s = sys.argv[1]
    h = javlib_handler()
    m = h.search(s)

    for ele in m:
        print(ele.title)
        links = h.get_rapid_links(ele.rapid_links) 
        for l in links:
            print(l)
        print('')
    print("Total {} matches".format(len(m)))
