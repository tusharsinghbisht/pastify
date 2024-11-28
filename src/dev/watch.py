import os
import time
from app import Pastify
import threading
from utils import message

BASE = "./src"

class Watcher:
    def __init__(self, app: Pastify):
        self.app = app
        self.watching = True

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

                if curr_time != last_mtime[file]:
                    last_mtime[file] = curr_time
                    message.blue(f"Changes detected in file {file}... restarting...")
                    self.restart()

            time.sleep(interval)

    
    def listen(self, callback):

        self.server = threading.Thread(target=self.app.listen, args=(callback,))
        self.watcher = threading.Thread(target=self.watch, args=(BASE,))

        message.green("Starting app in watch mode... Listening to changes...")

        self.watcher.start()
        
        self.server.start()

        self.watcher.join()
        print("watcher stopped")

        self.server.join()
        print("server stop")

    def restart(self):
        self.watching = False
        time.sleep(5)
        print("tmkoc")
        self.app.shutdown()