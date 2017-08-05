'''remove quotation mark'''
#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json

def str2int(strnum):
    if strnum:
        return int(strnum)
    else:
        return strnum

def main():
    '''main function'''
    with open("volunteer_list.json", 'r', encoding='utf8') as raw_file:
        raw_list = json.load(raw_file)
    new_list = list()
    for line in raw_list:
        line[0] = int(line[0])
        line[1] = str2int(line[1])
        line[5] = str2int(line[5])
        line[8] = str2int(line[8])
        line[9] = float(line[9])
        new_list.append(line)
    with open("volunteer_list.json", 'w', encoding='utf8') as new_file:
        json.dump(new_list, new_file, ensure_ascii=False)
        print("Done.")

if __name__ == '__main__':
    main()
