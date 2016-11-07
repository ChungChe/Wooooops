#!/usr/bin/env python3
import os
import urllib.request

def get_content(link):
    content = ""
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    try:
        req = urllib.request.Request(link, headers=hdr)
        with urllib.request.urlopen(req) as response:
            content = u''.join(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print("URLError Exception for {}, {}".format(link, e.reason))
        return
    except urllib.error.HTTPError as e:
        print("HTTPError Exception for {}, {}".format(link), e.reason)
        return
    except Exception:
        print("Exception for {}".format(link))
        return
    return content
