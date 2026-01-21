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

    def get_file_metadata(file_path):
        try:
            # get file_path 
            file_stat = os.stat(file_path)

            filename = os.path.basename(file_path)
            file_size = file_stat.st_size  

            if stat.S_ISDIR(file_stat.st_mode):
                file_type = "Directory"
            elif stat.S_ISREG(file_stat.st_mode):
                file_type = "Regular File"
            elif stat.S_ISLNK(file_stat.st_mode):
                file_type = "Symbolic Link"
            else:
                file_type = "Other"

            # get owner & group
            try:
                owner = pwd.getpwuid(file_stat.st_uid).pw_name
                group = grp.getgrgid(file_stat.st_gid).gr_name
            except KeyError:
                owner = str(file_stat.st_uid)
                group = str(file_stat.st_gid)

            # permissions
            permissions = oct(file_stat.st_mode)[-3:]

            # timestamps
            creation_time = time.ctime(file_stat.st_ctime)
            modification_time = time.ctime(file_stat.st_mtime)


            print(f"--- Metadata: {filename} ---")
            print(f"Type:       {file_type}")
            print(f"Size:       {file_size} bytes")
            print(f"Owner/Grp:  {owner} / {group}")
            print(f"Perms:      {permissions}")
            print(f"Created:    {creation_time}")
            print(f"Modified:   {modification_time}")
            print("-" * 30)

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")

# self testing
if __name__ == "__main__":
    # create testing file
    test_file = "test_data.txt"
    with open(test_file, "w") as f:
        f.write("This is a test file for Student A.")
    
    get_file_metadata(test_file)
    
    # delete file after testing
    os.remove(test_file)