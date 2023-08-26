import os
import pickle
import json
import glob
import re


def order_files_by_num(files:list[str])->list[str]:
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    return files

def wipe_dir(dir_path):
    files = glob.glob(f"{dir_path}*")
    for f in files:
        os.remove(f)

def get_all_files(dir_path):
    return glob.glob(f"{dir_path}*")

def get_all_dirs(directory_path):
    return [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]


def create_dir_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)
        
        
def does_file_exist(filename):
    return os.path.isfile(filename)
        

def get_filename(path:str)->str:
    return os.path.basename(path)


def convert_script(path, is_return=False):
    script = read_file(path)
    if is_return:
        script += "\nreturn zResult"
    return script
        

supported_files = ["json", "pickle", "html"]

def write_file(path:str, content):
    ext = os.path.splitext(path)[-1].lower()[1:]
    if ext=="html":
        write_html(path, content)
    if ext=="txt":
        write_txt(path, content)
    elif ext=="json":
        write_json(path, content)
    elif ext=="pickle":
        write_pickle(path, content)
    else:
        print(f"Cannot write {ext} filetype.")

def read_file(path:str):
    ext = os.path.splitext(path)[-1].lower()[1:]
    if ext=="html":
        return read_html(path)
    if ext=="txt":
        return read_txt(path)
    if ext=="js":
        return read_js(path)
    elif ext=="json":
        return read_json(path)
    elif ext=="pickle":
        return read_pickle(path)
    else:
        print(f"Cannot read {ext} filetype.")

def write_html(path, content):
    with open(path, 'w', encoding="utf-8") as file:
        file.write(content)

def read_html(path):
    with open(path, 'r', encoding="utf-8") as file:
        return file.read()

def write_json(path, content):
    with open(path, 'w') as file:
        json.dump(content, file)

def read_json(path):
    with open(path, 'r') as file:
        return json.load(file)

def write_pickle(path, content):
    with open(path, 'wb') as file:
        pickle.dump(content, file)

def read_pickle(path):
    with open(path, 'rb') as file:
        return pickle.load(file)
    
def write_txt(path, content):
    with open(path, 'w', encoding="utf-8") as f:
        f.write(content)

def read_txt(path):
    with open(path, 'r', encoding="utf-8") as file:
        return file.read()
    
def read_js(path):
    with open(path, 'r', encoding="utf-8") as file:
        return file.read().rstrip()