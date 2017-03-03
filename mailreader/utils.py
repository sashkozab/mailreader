# -*- coding: utf-8 -*-
#! /usr/bin/env python3

import re

def find_valid_ip(string):
	ip_pattern = re.compile("(((0|1?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}(0|1?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))")
	return ip_pattern.findall(string)

