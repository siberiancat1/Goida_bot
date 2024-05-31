import pickle
from pprint import pprint
def write_data_to_file(data):
        file_path = 'data.pickle'
        with open(file_path, 'wb') as file:
                pickle.dump(data, file)
        return True;

def read_data_from_file():
        try:
                file_path = 'data.pickle'
                with open(file_path, 'rb') as file:
                        data = pickle.load(file)
                return data
        except:
                dict ={}
                return dict;

def read_one(key, default):
        try:
                a = read_data_from_file();
                return a.get(key);
        except:
                return default;
def write_one(key, value):
        data_loaded = read_data_from_file()
        data_loaded[key] = value;
        write_data_to_file(data_loaded);
        return True;
def read(gKey, key, default): #юзать только это блять
        try:
                a = read_one(str(gKey) + "/" + str(key), default);
                if a == None:
                        return default;
                else:
                        return a;
        except:
                default;
def write(gKey, key, value): #юзать только это блять
        write_one(str(gKey)+ "/" + str(key), value);
        return True;

print("save_load work")
