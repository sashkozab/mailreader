# -*- coding: utf-8 -*-
#! /usr/bin/env python3

"""
test_mailparser.py

Usage: python test_mailparser.py [OPTION]...[ARGUMENT]...
Note: you should use python 3 for this script. So, maybe you should call python3 ....

Options:
  -h, --help                     Show this usage options.
  -f, --file=FILEPATH            Select message file path wich you want to parse.
  -d, --dir-with-files=DIRPATH   Select the Directory with specific message files that you want to parse. It parses files recursively inside that folder.
                                 By default file extension is '.eml'. If you want select another - use '-e or --extension' option.
  -e, --extension=.eml           Choose extension of files that you want to parse(example '.eml').It works with -d/--dir-with-files parameter.
  -a, --accounts                 It defines to parse from specific email mailbox of particular account that you set in settings.

Examples:
  python3 test_mailparser.py -h     Show help message.
  python3 test_mailparser.py -f ~/mailreader/Lab/original_msg.eml   Parse particular file that you selected.
  ./test_mailparser.py --file ~/mailreader/Lab/original_msg.eml     Same as previous.
  python3 test_mailparser.py -d ~/mailreader/Lab -e .eml             Parse recursively all files with extension '.eml' inside selected folder '~/mailreader/Lab'
  python3 test_mailparser.py --dir-with-files ~/mailreader/Lab --extension .eml  The same as previous.
  python3 test_mailparser.py -a      Parse messages from specific email mailbox of particular account that you set in settings.

!Note: you must use Python 3 for this scripts.

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/sashkozab/mailreader

"""


import sys
import os
import getopt
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mailreader.mailparser import *
import mailreader.utils as utils
import email_credentials as EC


def test_data_set(data_and_uid):
    messageObj = EmailComponents(data_and_uid)
    try:
        messageObj.init_msg_from_bytes()
    except AttributeError:
        messageObj.init_msg_from_file()
    messageFull = messageObj.msg
    decoded_to_name_adress = messageObj.name_adress()
    decoded_from_name_adress = messageObj.name_adress("From")
    decoded_subject = messageObj.get_header()
    email_date = messageObj.datetime()
    messageObj.set_body_message()
    all_ip_in_received = [match_ip[0] for match_ip in utils.find_valid_ip(" ".join(messageObj.get_header("Received")))]
    html_part = messageObj.body_html
    text_part = messageObj.body_text
    print("\n==========BEGINNING=============")
    print("UID: ", messageObj.UID)
    print("Content type: ", messageFull["Content-Type"])
    print("Full message:\n++++++++++++++++++++++++++++\n",messageFull, "\n++++++++++++++++++++")
    print("CLASS: ",messageFull.__class__)
    # try:
    #     print("Get body: =====================>\n", messageFull.get_body(preferencelist=('related', 'html', 'plain')), "\n---------------------")
    # except AttributeError as e:
    #     print(e)
    print("maintype: ", messageObj.msg.get_content_type())
    print("Date: ", email_date)
    print("Names To: ", decoded_to_name_adress[0])
    print("Adresses To: ", decoded_to_name_adress[1])
    print("Names from: ", decoded_from_name_adress[0])
    print("Adresses from: ", decoded_from_name_adress[1])
    print("All Received headers", messageObj.get_header("Received"))
    print("All Received IP: ", all_ip_in_received)
    print("X-Originating-IP (if exists): ", utils.find_valid_ip(" ".join(messageObj.get_header("X-Originating-IP"))))
    print("Subject: ", " ".join(decoded_subject))
    print("Body Text part: \n",text_part)
    print("Body HTML part: \n",html_part)
    print("Attached files: ", messageObj.filenames)
    # print("Get payload[0]: ", "\n====================\n",messageFull.get_payload()[0], "\n===========================")
    # print("Get payload[1]: ", "\n====================\n",messageFull.get_payload()[1], "\n===========================")
    [print("Attached FILENAME: ", k, "\nFile Content: \n", messageObj.attachments[k]) for k in messageObj.attachments.keys()]
    print("============END================")


def main():
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hf:d:e:a", ["help", "file=", "dir-with-files=", "extension=", "accounts"])
    except getopt.GetoptError:
        print(__doc__)
        return

    f, d, e, a = False, False, False, False
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(__doc__)
            return
        elif opt in ("-f", "--file"):
            f = arg
        elif opt in ("-d", "--dir-with-files"):
            d = arg
        elif opt in ("-e", "--extension"):
            e = arg
        elif opt in ("-a", "accounts"):
            a = True

    if f:
        with open(f) as file_object:
            test_data_set((file_object, None))
    elif d:
        if not e: e = ".eml"
        for root, dirs, files in os.walk(d):
            for filename in files:
                if e == filename[-len(e):]:
                    filepath = os.path.join(root, filename)
                    with open(filepath) as file_object:
                        test_data_set((file_object, None))
    if a:
        mail = connect_to_mail(EC.host, EC.adress, EC.passward)
        pprint.pprint(mail.list())
        # Out: list of "folders" aka labels in gmail.
        mail.select("inbox", readonly=True) # connect to inbox.
        for data_and_uid in fetch_all(mail): test_data_set(data_and_uid)

if __name__ == "__main__":
    main()
    