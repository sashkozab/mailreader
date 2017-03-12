# -*- coding: utf-8 -*-
#! /usr/bin/env python3

import re
from bs4 import BeautifulSoup, FeatureNotFound


def find_valid_ip(string):
    """
    Find possible ip adress through the regular expression.
    :param string: string where we search for ip adress.
    TO-DO: inmprove regular expression to exclude matching that are not ip adresses.
    """
    ip_pattern = re.compile("(((0|1?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}(0|1?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))")
    return ip_pattern.findall(string)


def text_from_html(html):
    """
    Get all text from the given html code.
    This function is require beautifulsoup4 and lxml modules.
    :param html: html code, that is a string or an open filehandle.
    """
    try:
        soup = BeautifulSoup(html, "lxml")
    except FeatureNotFound as e:
        soup = BeautifulSoup(html, "html.parser")
        print("\n***********\nUserWarning:", e, "\nOtherwise we will use built-in html.parser that is good for most base parsing tasks.\n")

    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text
