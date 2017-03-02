# -*- coding: utf-8 -*-
#! /usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mailreader.mailparser import *
import email_credentials as EC

if __name__ == "__main__":
    mail = connect_to_mail(EC.host, EC.adress, EC.passward)
    pprint.pprint(mail.list())
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox", readonly=True) # connect to inbox.

    for r in fetch_all(mail):
        messageObj = EmailComponents(r)
        messageObj.init_msg_from_bytes()
        messageFull = messageObj.msg
        decoded_to_name_adress = messageObj.name_adress()
        decoded_from_name_adress = messageObj.name_adress("From")
        decoded_subject = messageObj.get_subject()
        email_date = messageObj.datetime()
        messageObj.set_body_message()
        html_part = messageObj.body_html
        text_part = messageObj.body_text
        print("\n=======================")
        print("Content type: ", messageFull["Content-Type"])
        print("Full message:",messageFull, "\n++++++++++++++++++++")
        print("CLASS: ",messageFull.__class__)
        try:
            print("Get body: =====================>\n", messageFull.get_body(preferencelist=('related', 'html', 'plain')), "\n---------------------")
        except AttributeError as e:
            print(e)
        print("maintype: ", messageObj.msg.get_content_type())
        print("Date: ", email_date)
        print("Names To: ", decoded_to_name_adress[0])
        print("Adresses To: ", decoded_to_name_adress[1])
        print("Names from: ", decoded_from_name_adress[0])
        print("Adresses from: ", decoded_from_name_adress[1])
        print("Subject: ", decoded_subject)
        print("Body Text part: \n",text_part)
        print("Body HTML part: \n",html_part)
        print("Attached files: ", messageObj.filenames)
        # print("Get payload[0]: ", "\n====================\n",messageFull.get_payload()[0], "\n===========================")
        # print("Get payload[1]: ", "\n====================\n",messageFull.get_payload()[1], "\n===========================")
        [print("Attached FILENAME: ", k, "\nFile Content: \n", messageObj.attachments[k]) for k in messageObj.attachments.keys()]


    # msg = email.message_from_bytes(r)
    # maintype = msg.get_content_maintype()
    # print("\n===========================")
    # print(maintype)
    # try:
    #   print("Pure MESSAGE To: ",msg.get_all('To', []))
    #   print("Pure MESSAGE From: ",msg.get_all('from', []))
    #   print("Pure MESSAGE Subject: ",msg.get_all('subject', []))
    #   print("Pure MESSAGE Date: ",msg.get_all('date', []))
    #   print(decode_header(msg['From']),decode_header(msg['Subject']))
    #   print(decode_header(msg.get_all('To', [])[0]),decode_header(msg['Date']))
    #   print(email.utils.getaddresses(msg.get_all('To', [])))
    #   print(email.utils.getaddresses(msg.get_all('Message-ID', [])))
    #   print(email.utils.parsedate(msg.get_all('date', [])[0]))
    #   print("Subject", decode_header(msg.get_all('subject', [])[0]))
    #   print("Decode:",decode_header(email.utils.getaddresses(msg.get_all('To', []))[1][0])[0][0].decode('utf-8'))

    #   print(decode_header(msg['From'])[0][0].decode('utf-8'))
    #   print(decode_header(msg['From'])[1][0].decode('utf-8'))
    #   print(decode_header(msg['Subject'])[0][0].decode('utf-8'))
    #   # print("MESSAGE FROM: ",email.utils.parseaddr(decode_header(msg['From'])[0].decode('utf-8')))
    #   # print("MESSAGE FROM: ",email.utils.parseaddr(decode_header(msg['From'])[1].decode('utf-8')))
    # except (AttributeError,IndexError) as er:
    #   print("EXCEPTION way: ", er,repr(decode_header(msg['From'])))
    # print("MESSAGE FROM: ",email.utils.parseaddr(msg['From'])[0])
    # print(msg.keys())
    # for m in msg.walk():
    #   print(m.get_content_type())
    #   if m.get_content_type() == "text/plain":
    #       payload = m.get_payload(None, True).decode('utf-8')
    #       # print("This is text plain part:",payload)
    #   elif m.get_content_type() == "text/html":
    #       payload = m.get_payload(None, True).decode('utf-8')
    #       # print("This is text HTML part:",payload)