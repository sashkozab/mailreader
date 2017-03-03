# -*- coding: utf-8 -*-
#! /usr/bin/env python3
import imaplib
import email
from email.parser import BytesParser
from email import policy
from email.header import decode_header
import pprint

def connect_to_mail(imap_server, account, passwd):
    M = imaplib.IMAP4_SSL(imap_server)
    M.login(account, passwd)
    return M


def fetch_all(connected_mail):
    result, data = connected_mail.uid('search', None, "ALL") # search and return uids instead
    email_uid_list = data[0].split()
    for email_uid in email_uid_list:
        _, email_data = connected_mail.uid('fetch', email_uid, '(RFC822)')
        # print(connected_mail.fetch(email_uid, "(BODY[HEADER.FIELDS (FROM)])"))
        # print(email_data[0][1])
        print("\nEmail UID: ", email_uid)
        yield email_data[0][1]


class EmailComponents:
    """
    Class for fetching all particular components from every email message.
    """
    def __init__(self, mailObject):
        self.mailObject = mailObject

        self.UID = None
        # self.from_adress = None
        # self.from_name = None
        # self.to_adress = []
        # self.to_name = []
        self.date = None
        self.time = None
        # self.subject = None
        self.body_text = ""
        self.body_html = ""
        self.links_object = None
        self.filenames = []
        self.attachments = {}

        self.msg = None

    def init_msg_from_bytes(self):
        """
        Just initialize message from mailObject using message_from_bytes method 
        of email mudule. Otherwise by default self.msg == None
        """
        # self.msg = email.message_from_bytes(self.mailObject)
        self.msg = BytesParser(policy=policy.default).parsebytes(self.mailObject)

    def name_adress(self, to="To"):
        """
        List of tuples that containe recipient's ('To') or sender's ('From') pair of (Name, Adress) each.
        :param to: field name of mail object. Default is 'To'
        """
        to_value = self.msg.get_all(to, [])
        names_adresses = self.get_decoded_adresses(to_value)
        name, adress = [], []
        if names_adresses:
            for name_adress in names_adresses:
                name.append(name_adress[0])
                adress.append(name_adress[1])
        return (name, adress)

    def get_header(self, subject="Subject"):
        """
        Return list containing parts of decoded particular email header. 
        :param subject: field name of mail object. Default is 'Subject'
        """
        header_value = self.msg.get_all(subject, [])
        decoded_value = [self.get_decoded_value(header_chunk) for header_chunk in header_value]
        return decoded_value


    def get_decoded_value(self, field_value):
        """
        Get and return decoded non ASCII single value from message field.
        """
        if field_value:
            decoded_value = decode_header(field_value)
            value_final = ""
            for chunk in decoded_value:
                value_final += chunk[0].decode(chunk[1]) if chunk[1] else chunk[0] + " "
            return value_final
        else:
            return field_value

    def get_decoded_adresses(self, field_value):
        """
        Get and return decoded non ASCII range adresses from message field value.
        """
        if field_value:
            adresses = email.utils.getaddresses(field_value)
            decoded_adresses = []
            for adress in adresses:
                decoded_name, decoded_adress = decode_header(adress[0]),decode_header(adress[1])
                name_final, adress_final = "","" 
                for dec_n in decoded_name:
                    name_final += dec_n[0].decode(dec_n[1]) if dec_n[1] else dec_n[0] + " "
                for dec_a in decoded_adress:
                    adress_final += dec_a[0].decode(dec_a[1]) if dec_a[1] else dec_a[0] + " "
                decoded_adresses.append((name_final, adress_final))
            return decoded_adresses
        else:
            return field_value

    def datetime(self, date="Date"):
        """
        Return email date. Example: 'Thu, 5 Jan 2017 21:52:41 +0200'.
        :param date: field name of mail object. Default is 'Date'
        """
        date_value = self.msg.get_all(date, [])
        return email.utils.parsedate(date_value[0])

    def set_body_message(self):
        """
        Get body message(html or text parts or both). Doesn't return anything, but define
        class variables self.body_html and self.body_text if exists.
        """
        if self.msg.is_multipart():
            for m in self.msg.walk():
                # print("Is attached in grab: ", m.is_attachment())
                # [print("!!!! Attached : ", a) for a in self.msg.iter_attachments() if m.is_attachment()]
                self.grab_text_or_html(m)
        else:
            self.grab_text_or_html(self.msg)

    def grab_text_or_html(self, message):
        """
        Looking for particular message maintype and grab each  with assigning to respective class variable.
        Also append attached filename to self.filenames list if detect.
        """
        if message.get_filename():
            self.filenames.append(message.get_filename())
            self.attachments.update({message.get_filename() : message.get_payload()})
        elif message.get_content_type() == "text/plain":
            self.body_text += message.get_payload(None, True).decode('utf-8') + "\n"
        elif message.get_content_type() == "text/html":
            self.body_html += message.get_payload(None, True).decode('utf-8')

