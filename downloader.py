import os
import sys
import threading
import time
from argparse import ArgumentParser

import colorama

from config import Config as con
from helper import bcolors
from utils import download_course, download_track, get_completed_tracks, get_completed_courses, get_all_courses, get_all_tracks


def login_parser():
    parser = ArgumentParser()
    parser.add_argument("-t", "--token", required=True, type=str,
                        help="Specify your Datacamp authentication token.")
    parser.add_argument("-l", "--list", required=True, type=str,
                        help="List completed (T) for tracks, (C) for courses, (TA) for all track, (CA) for all courses")
    parser.add_argument("-p", "--path", required=False, default=os.getcwd(), type=str,
                        help="Path to download the contents, default is the current directory")
    parser.add_argument("-v", "--video", action='store_true',
                        help="Include it if you want to download the videos")
    parser.add_argument("-e", "--exercise", action='store_true',
                        help="Include it if you want to download the exercises")
    parser.add_argument("-d", "--dataset", action='store_true',
                        help="Include it if you want to download the datasets")
    parser.add_argument("-a", "--all", action='store_true',
                        help="Include it if you want to download all the track/course and data")
    return parser


def get_to_download():
    inp = input('Enter the id(s) you want to download separated by a space or '
                "you can enter 'a-b' to download courses from a to b: ")

    if '-' in inp:
        output = inp.split('-')
        output = [*range(int(output[0]), int(output[1]) + 1)]
    else:
        output = [int(x) for x in inp.split()]
    return output


def main():
    args = login_parser().parse_args()
    con.set_token(args.token)

    if not con.login:
        return

    print_dash()

    while True:
        if args.list == 'T':
            handle_tracks(args)
        elif args.list == 'C':
            handle_courses(args)
        elif args.list == 'TA':
            handle_all_tracks(args)
        elif args.list == 'CA':
            handle_all_courses(args)
        else:
            sys.stdout.write(
                f"{bcolors.FAIL} No valid list type provided! Only 'T' for tracks and 'C' for courses allowed! (args.list={args.list})  {bcolors.BKENDC}\n")
            break


def handle_courses(args):
    thread = start_thread(print_courses)
    if wait(thread):
        if len(get_completed_courses()) == 0:
            exit()

        required_courses = get_to_download()

        for course_id in required_courses:
            course = list(filter(lambda x: x.id == course_id,
                                 get_completed_courses()))[0]

            if(args.all):
                download_course(course.link, args.path,
                                args.all, args.all, args.all)
            else:
                download_course(course.link, args.path,
                                args.video, args.exercise, args.dataset)


def print_dash():
    print('=' * 100, end='\n')


def handle_tracks(args):
    thread = start_thread(print_tracks)
    if wait(thread):
        if len(get_completed_tracks()) == 0:
            exit()
        required_tracks = get_to_download()

        for track_id in required_tracks:
            track = list(filter(lambda x: x.id == track_id,
                                get_completed_tracks()))[0]
            if args.all:
                download_track(track.link, args.path,
                               args.all, args.all, args.all)
            else:
                download_track(track.link, args.path, args.video,
                               args.exercise, args.dataset)


def start_thread(func):
    thread = threading.Thread(target=func)
    thread.start()
    return thread


def wait(thread):
    i = 1
    if sys.version_info.major == 3 and sys.version_info.minor >= 9:
        living_thread = thread.is_alive
    else:
        living_thread = thread.isAlive

    while living_thread():
        print('Waiting %s%s' % ('.' * i, ' ' * (3 - i)), end='\r')
        i = i + 1 if i < 3 else 1
        time.sleep(0.4)
    print('', end='\r')
    return True


def print_courses():
    courses = get_completed_courses()
    if len(courses) == 0:
        sys.stdout.write(
            f'{bcolors.FAIL}No completed courses found!  {bcolors.BKENDC}\n')
    for course in courses:
        sys.stdout.write(
            f'{bcolors.BKGREEN} {course.id}. {course.name}  {bcolors.BKENDC}\n')


def print_tracks():
    tracks = get_completed_tracks()
    if len(tracks) == 0:
        sys.stdout.write(
            f'{bcolors.FAIL}No completed tracks found!  {bcolors.BKENDC}\n')

    for track in tracks:
        sys.stdout.write(
            f'{bcolors.BKBLUE} {track.id}. {track.name}  {bcolors.BKENDC}\n')


def print_all_courses():
    courses = get_all_courses()
    if len(courses) == 0:
        sys.stdout.write(
            f'{bcolors.FAIL}No completed courses found!  {bcolors.BKENDC}\n')
    for course in courses:
        sys.stdout.write(
            f'{bcolors.BKGREEN} {course.id}. {course.name}  {bcolors.BKENDC}\n')


def print_all_tracks():
    tracks = get_all_tracks()
    if len(tracks) == 0:
        sys.stdout.write(
            f'{bcolors.FAIL}No completed tracks found!  {bcolors.BKENDC}\n')

    for track in tracks:
        sys.stdout.write(
            f'{bcolors.BKBLUE} {track.id}. {track.name}  {bcolors.BKENDC}\n')


def handle_all_courses(args):
    thread = start_thread(print_all_courses)
    if wait(thread):
        if len(get_all_courses()) == 0:
            exit()

        required_courses = get_to_download()

        for course_id in required_courses:
            course = list(filter(lambda x: x.id == course_id,
                                 get_all_courses()))[0]

            if(args.all):
                download_course(course.link, args.path,
                                args.all, args.all, args.all)
            else:
                download_course(course.link, args.path,
                                args.video, args.exercise, args.dataset)


def handle_all_tracks(args):
    thread = start_thread(print_all_tracks)
    if wait(thread):
        if len(get_all_tracks()) == 0:
            exit()
        required_tracks = get_to_download()

        for track_id in required_tracks:
            track = list(filter(lambda x: x.id == track_id,
                                get_all_tracks()))[0]
            if args.all:
                download_track(track.link, args.path,
                               args.all, args.all, args.all)
            else:
                download_track(track.link, args.path, args.video,
                               args.exercise, args.dataset)


colorama.init()
if __name__ == "__main__":
    main()
