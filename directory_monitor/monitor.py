# import libraries
import os
import time
import stat
import pwd
import grp

class DirectoryMonitor:
    def __init__(self, path_to_watch):
        self.path_to_watch = path_to_watch
        self.files_state = {}
        self.running = True
        print(f"[Init] Scanning directory: {self.path_to_watch}")
        self.update_state()

    def get_metadata(self, file_path):
        try:
            stats = os.stat(file_path)
            filename = os.path.basename(file_path)
            try:
                owner = pwd.getpwuid(stats.st_uid).pw_name
                group = grp.getgrgid(stats.st_gid).gr_name
            except KeyError:
                owner = str(stats.st_uid)
                group = str(stats.st_gid)

            return {
                "filename": filename,
                "size": stats.st_size,
                "permissions": oct(stats.st_mode)[-3:],
                "owner": owner,
                "mtime": stats.st_mtime,
                "mtime_str": time.ctime(stats.st_mtime)
            }
        except FileNotFoundError:
            return None
