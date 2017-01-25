#! /usr/bin/env python
# -*- coding: utf-8 -*-
# DB query CLI 
import upjav_hunter as up
import sys
if __name__ == "__main__":
    #f = "post_date, title, actress, cover_link, preview_link, rapid_link"
    #c = "available is 0 and is_censored is 1 and rapid_link is not null"
    if len(sys.argv) < 3:
        print("Usage: {} 'condition' output_file".format(sys.argv[0]))
        sys.exit()
    if sys.argv[1] == "-h":
        print("""
            -h help
            -l list all fields
            """)
        sys.exit()
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
    try:
        u = up.upjav_hunter("tmp4.db")
        u.query(sys.argv[1], sys.argv[2])
    except Exception as e:
        print("Error: {}".format(e))
