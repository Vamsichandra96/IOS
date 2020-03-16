"""import time
import fcntl
import os
import signal

FNAME = "/home/sirapu/Downloads/tiny_web_server/version_7/www"

def handler(signum, frame):
    print ("File %s modified", (FNAME))

signal.signal(signal.SIGIO, handler)
fd = os.open(FNAME,  os.O_RDONLY)
fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
fcntl.fcntl(fd, fcntl.F_NOTIFY,
            fcntl.DN_MODIFY | fcntl.DN_CREATE | fcntl.DN_MULTISHOT)

while True:
    time.sleep(10000)

"""
"""
import inotifywait

while inotifywait -q -e modify  "/home/sirapu/Downloads/tiny_web_server/version_7/www" ; do
    echo "filename is changed"
    # do whatever else you need to do
done"""

"""
import pyinotify
# import watchdog


event_notifier = pyinotify.ThreadedNotifier(watch_manager, EventProcessor())

watch_this = os.path.abspath("notification_dir")
watch_manager.add_watch(watch_this, pyinotify.ALL_EVENTS)
event_notifier.start()"""

import inotify.adapters
def main():
    i = inotify.adapters.Inotify()
    i.add_watch(FNAME)
    # fileName = FNAME + "/" + uri.split("/")[-1]
    # with open(fileName,'w'):
    #     pass

    for event in i.event_gen(yield_nones = False):
        (_,type_names,path,filename) = event
        print(filename)
        # break
        # print("PATH = [{}] FILENAME = [{}] EVENT_TYPES = {}".format(path,filename,type_names))

FNAME = "/home/sirapu/Downloads/tiny_web_server/version_7/www"

if __name__ == "__main__":
    main()
