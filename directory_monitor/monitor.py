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
                "owner": owner/group,
                "mtime": stats.st_mtime,
                "mtime_str": time.ctime(stats.st_mtime)
            }
        except FileNotFoundError:
            return None

    def update_state(self):
        current_state = {}
        if os.path.exists(self.path_to_watch):
            for filename in os.listdir(self.path_to_watch):
                filepath = os.path.join(self.path_to_watch, filename)
                if os.path.isfile(filepath):
                    metadata = self.get_metadata(filepath)
                    if metadata:
                        current_state[filename] = metadata
        self.files_state = current_state

    def check_changes(self):
        current_files = set(os.listdir(self.path_to_watch))
        monitored_files = set(self.files_state.keys())
        logs = []

        # check created
        added_files = current_files - monitored_files
        for filename in added_files:
            filepath = os.path.join(self.path_to_watch, filename)
            if os.path.isfile(filepath):
                meta = self.get_metadata(filepath)
                if meta:
                    logs.append(f"[CREATED] {filename} | Size: {meta['size']}B | Time: {meta['mtime_str']}")
                    self.files_state[filename] = meta
