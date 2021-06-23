from os import write

from math import floor
from data_json import add_json
from data_json import delete_json
import json

class stat:
    def __init__(self, str = 10, dex = 10, con = 10, wis = 10, intel = 10 , cha = 10):
        self.str = str
        self.dex = dex
        self.con = con
        self.wis = wis
        self.intel = intel
        self.cha = cha
    
    def getModifier(self, name):
        modifier = floor((self.__getattribute__(name) - 10) / 2)
        return modifier

class character(stat):
    def __init__(self, str = 10, dex = 10, con = 10, wis = 10, intel = 10, cha = 10, name = '', creator = ''):
        super().__init__(str=str, dex=dex, con=con, wis=wis, intel=intel, cha=cha)
        self.char_name = name
        self.creator = creator
        self.json = {
            'character_name': self.char_name,
            'creator': self.creator,
            'str': self.str,
            'dex': self.dex,
            'con': self.con,
            'wis': self.wis,
            'intel': self.intel,
            'cha': self.cha
        }
        self.data_file = 'character.json'
        add_json(self.json, self.data_file, self.char_name)

    def update_json(self):
        self.json = {
            'character_name': self.char_name,
            'creator': self.creator,
            'str': self.str,
            'dex': self.dex,
            'con': self.con,
            'wis': self.wis,
            'intel': self.intel,
            'cha': self.cha
        }
    
    def delete(self):
        delete_json(self.data_file, key = 'character_name', value = self.char_name)
        del self
    
    def setStat(self, stat: str, value: 10):
        self.__setattr__(stat, value)
        self.update_json()
        add_json(new_data = self.json, filename = self.data_file, char_name = self.char_name)

def loadCharater(char_name) -> character:
    with open('character.json', 'r+') as file:
        file_data = json.load(file)
        for i in range(len(file_data)):
            if file_data[i]['character_name'].lower() == char_name.lower():
                return character(str = file_data[i]['str'], dex = file_data[i]['dex'], con = file_data[i]['con'],
                wis = file_data[i]['wis'], intel = file_data[i]['intel'], cha = file_data[i]['cha'],
                name = file_data[i]['character_name'], creator = file_data[i]['creator'])
    return None

def checkCharacter(char_name) -> bool:
    with open('character.json', 'r') as file:
        file_data = json.load(file)
        for i in range(len(file_data)):
            if file_data[i]['character_name'].lower() == char_name.lower():
                return True
    return False

if __name__ == "__main__":
    human = character(name = 'Theor', creator = 'Thao')
    elf = character(name = 'Teirist', creator = 'ThuAn')
    dwarf = loadCharater('theor')
    print(dwarf.json)

