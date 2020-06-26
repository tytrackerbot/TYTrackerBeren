from TYItem import TYItem
import os
import jsonpickle
import eel
import json
import subprocess
import posixpath
import ntpath

# Directory Paths
file_path = os.path.dirname(os.path.abspath(__file__))
data_path = file_path + os.path.sep + os.path.join('..', 'data')
web_path = file_path + os.path.sep + os.path.join('..', 'web')
server_path = file_path + os.path.sep + os.path.join('..', 'server')

# Bash Script Paths
upload_path = os.path.join(server_path, 'upload.sh')
unix_upload_path = upload_path.replace(ntpath.sep, posixpath.sep)
download_path = os.path.join(server_path, 'download.sh')
unix_download_path = download_path.replace(ntpath.sep, posixpath.sep)

# Initialize eel
eel.init(web_path)


@eel.expose
def getItemsJSON():
    global data_path
    with open(os.path.join(data_path, 'tracked_items.json'), 'r') as file:
        content = file.read()
        items = jsonpickle.decode(content)
    return [dict(item) for item in items]


@eel.expose
def addItem(url, threshold):
    items = getItemsObject()
    if getItemFromURL(items, url):
        return True
    else:
        try:
            new_item = TYItem(url, threshold)
        except:
            return False
        else:
            items.append(new_item)
            saveItemsToJSON(items)
            return True


@eel.expose
def removeItem(url):
    items = getItemsObject()
    removed_item = getItemFromURL(items, url)
    if removed_item:
        items.remove(removed_item)
        saveItemsToJSON(items)
        return True
    else:
        return False


@eel.expose
def editThreshold(url, new_threshold):
    items = getItemsObject()
    editted_item = getItemFromURL(items, url)
    if editted_item:
        editted_item.setThreshold(float(new_threshold))
        editted_item.setInformed(state=False)
        saveItemsToJSON(items)
        return True
    else:
        return False


@eel.expose
def uploadItems():
    global unix_upload_path
    if os.name == 'nt':
        subprocess.call(['bash', unix_upload_path], shell=True)
    else:
        subprocess.call(['bash', unix_upload_path])


@eel.expose
def downloadItems():
    global unix_download_path
    if os.name == 'nt':
        subprocess.call(['bash', unix_download_path], shell=True)
    else:
        subprocess.call(['bash', unix_download_path])


def getItemsObject():
    global data_path
    with open(os.path.join(data_path, 'tracked_items.json'), 'r') as file:
        content = file.read()
        items = jsonpickle.decode(content)
    return items


def saveItemsToJSON(items):
    with open(os.path.join(data_path, 'tracked_items.json'), 'w') as file:
        frozen = jsonpickle.encode(items)
        file.write(frozen)
        file.truncate()


def getItemFromURL(items, url):
    for item in items:
        if item.url == url:
            return item
    return None


downloadItems()
try:
    eel.start('index.html', size=(1200, 700), position=(200, 50), port=8080)
except (SystemExit, MemoryError, KeyboardInterrupt):
    # We can do something here if needed
    # But if we don't catch these safely, the script will crash
    pass
uploadItems()
