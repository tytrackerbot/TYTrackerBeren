from TYItem import TYItem
import os
import jsonpickle

data_path = os.path.dirname(os.path.abspath(
    __file__)) + os.path.sep + os.path.join('..', 'data')

if not os.path.isdir(data_path):
    print('NO SUCH DIRECTORY FOUND!')
else:
    with open(os.path.join(data_path, 'tracked_items.json'), 'r') as file:
        content = file.read()
        items = jsonpickle.decode(content)

    for item in items:
        item.update()

    with open(os.path.join(data_path, 'tracked_items.json'), 'w') as file:
        frozen = jsonpickle.encode(items)
        file.write(frozen)
        file.truncate()
