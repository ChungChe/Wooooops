#! /usr/bin/env python
# -*- coding: utf-8 -*-
# DB query CLI 
import upjav_hunter as up
import sys
if __name__ == "__main__":
    #f = "post_date, title, actress, cover_link, preview_link, rapid_link"
    #c = "available is 0 and is_censored is 1 and rapid_link is not null"
    
    if len(sys.argv) > 1 and sys.argv[1] == "-h":
        print("""
        OPTION_FLAG                 PARAM               DESCRIPTION
        ===================================================================
            -h                                          help
            -l                                          list all fields
            -s                  search_string
            -sn                 search_string           list unavailable only
            -c                  'SQL condition...'
            """)
        sys.exit()
    if len(sys.argv) != 4:
        print("Usage: {} OPTION_FLAG PARAM output_file, use -h for more information.".format(sys.argv[0]))
        sys.exit()
    condition = "" 
    if sys.argv[1] == "-s" or sys.argv[1] == "-sn": 
        if sys.argv[2] == None:
            print("""
                -s search_string
            """)
            sys.exit()
        else:
            ss = '"%{}%"'.format(sys.argv[2])
            if sys.argv[1] == "-sn":
                condition = 'available is 0 AND (pid LIKE {} OR title LIKE {} OR actress LIKE {} OR rapid_link LIKE {})'.format(ss, ss, ss, ss)
            else:
                condition = 'pid LIKE {} OR title LIKE {} OR actress LIKE {} OR rapid_link LIKE {}'.format(ss, ss, ss, ss)
            print(condition)
    elif sys.argv[1] == "-l":
        print("""   current fields:
            1. url_id
            2. post_date
            3. title
            4. actress
            5. cover_link
            6. preview_link
            7. pid
            8. release_date
            9. is_censored
           10. rapid_link
           11. available
        """)
        sys.exit()
    elif sys.argv[1] == "-c":
        condition = sys.argv[2]
    try:
        u = up.upjav_hunter("tmp4.db")
        u.query(condition, sys.argv[3])
    except Exception as e:
        print("Error: {}".format(e))
