#!/usr/bin/env python

import time
from shutil import rmtree
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

from gen import run

class LiveReloadingEventHandler(RegexMatchingEventHandler):
    def __init__(self):
        RegexMatchingEventHandler.__init__(self,
            regexes=[r'\./content*', r'\./static*', r'gen.yml'],
            case_sensitive=False,
            ignore_directories=True
        )

    def on_any_event(self, event):
        print('rebuilding after change in {}...'.format(event.src_path))

        try:
            rmtree('www')
        except FileNotFoundError:
            print('skipping removal of www because it doesn\'t exist')

        print('building...')
        run()

if __name__ == "__main__":
    path = '.'
    event_handler = LiveReloadingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
