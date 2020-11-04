import json
import os
if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    print(dirname)
    filename = os.path.join(dirname, 'poll_data_test.json')
    print(filename)
    with open(filename) as file:
        data = json.load(file)
        print(data)
        print(len(data))
        print(data[-1]["id"])
    new_data = data[1]
    new_data["id"] = 3
    data.append(new_data)
    print(data)
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)
