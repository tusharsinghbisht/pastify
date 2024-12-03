import os
import time
from app import Pastify
import threading
from utils import message

BASE = "./pastify"

class Watcher:
    def __init__(self, app: Pastify, file):
        self.app = app
        self.watching = True
        self.file = file

    def get_all_files(self, dir):
        files = []
        dir_list = [os.path.join(dir, x) for x in os.listdir(dir)]

        for p in dir_list:
            if os.path.isdir(p):
                files.extend(self.get_all_files(p))
            else:
                files.append(p)

        return files
            
    
    def watch(self, dir=".", interval=1):
        last_mtime = { f: os.path.getmtime(f) for f in self.get_all_files(dir) }
        while self.watching:
            for file in last_mtime.keys():
                curr_time = os.path.getmtime(file)

                if curr_time != last_mtime.get(file, None):
                    last_mtime[file] = curr_time
                    print(f"\nChanges detected in file {file}... restarting...")
                    self.restart()

            time.sleep(interval)

    
    def listen(self, callback):
        try:
            self.server = threading.Thread(target=self.app.listen, args=(callback,))
            self.watcher = threading.Thread(target=self.watch, args=(BASE,))

            message.green("Starting app in watch mode... Listening to changes...")

            self.watcher.start()
            
            self.server.start()

            self.server.join()
            message.red("\n• Server Socket Stopped")

            self.watcher.join()
            message.red("• Watcher stopped")

            message.green("\n✔ Restarting...\n")

            
            os.execv("/usr/bin/python3", ["python"]+[self.file])
        except KeyboardInterrupt:
            message.red("\nServer stopped by user...")
            self.watching = False
            exit()


    def restart(self):
        self.watching = False
        self.app.shutdown()