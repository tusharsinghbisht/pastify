import os
import time
from pastify.app import Pastify
import threading
from pastify.utils import message

class Watcher:
    '''
    Watcher class that can run the pastify server in `watch mode`

    ## Watch Mode
    Check's for all files in current directory and performs hot reloads based on changes, basically detects changes and restart the server upon those changes

    ### Parameters: 
        - `app (Pastify)`: pastify app on which watch mode is to be implemented
        -  `file`: file object (__file__) of the file in which our `app` is initialized
    '''
    def __init__(self, app: Pastify, file):
        self.app = app
        self.watching = True
        self.file = file

    def get_all_files(self, dir):
        '''Get all files recursively from a directory'''
        files = []
        dir_list = [os.path.join(dir, x) for x in os.listdir(dir)]

        for p in dir_list:
            if os.path.isdir(p):
                files.extend(self.get_all_files(p))
            else:
                files.append(p)

        return files
            
    
    def watch(self, dir, interval=1):
        '''Watches all the files in the present working directory for changes'''
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
        '''
        Listens to server in `watch mode`, keeping checks on file changes and running server concurrently
        '''
        try:
            self.server = threading.Thread(target=self.app.listen, args=(callback,))
            self.watcher = threading.Thread(target=self.watch, args=(os.getcwd(),))

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
        '''Restart the entire program'''
        self.watching = False
        self.app.shutdown()