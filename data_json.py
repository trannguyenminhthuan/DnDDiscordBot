import json

# function to add new data to JSON
def add_json(new_data, filename='data.json', char_name = ''):
    with open(filename, 'r') as file:
        file_data = json.load(file)
        for i in range(len(file_data)):
            if file_data[i]['character_name'].lower() == char_name.lower():
                file_data.pop(i)
                break
    with open(filename,'w') as file:
        # Join new_dat3a with file_data
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
        

def delete_json(filename = 'data.json', key = 'key', value = 'value'):
    with open(filename, 'r') as file:
        file_data = json.load(file)
        for i in range(len(file_data)):
            if file_data[i][key].lower() == value.lower():
                file_data.pop(i)
                break
    with open(filename, 'w') as file:
        json.dump(file_data, file, indent = 4)
        
if __name__ == "__main__":
    delete_json(filename = 'character.json', key = 'character_name', value = 'Teirist')
