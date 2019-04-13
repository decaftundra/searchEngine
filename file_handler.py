#TODO: write file OPENER and file writer
#TODO: write vocab stemmer to have file
#TODO: compare stemmed vocab to stemmed query and retrieve all docs from stemmed query
import json

def open_json_file(path):
    
    the_file = open_file(path)
    loaded_file = json.load(the_file)

    the_file.close()

    return loaded_file

def write_json_file(data_to_write, path):
    the_file = write_file(path)

    json.dump(data_to_write, the_file)

    the_file.close()

def open_file(path):

    the_file = open(path, 'r')

    return the_file

def write_file(path):
    the_file = open(path , 'w')

    return the_file



