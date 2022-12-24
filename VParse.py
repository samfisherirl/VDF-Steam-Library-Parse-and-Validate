import subprocess
import codecs
import os
import sys
import shutil
import json
import os.path
import library_paths as LP

appinfo = r'C:\Program Files (x86)\Steam\appcache\appinfo.vdf'
 


def verify_vdf_location(directory):
    global appinfo
    try:
        shutil.copy2(appinfo, (os.path.join(directory, 'appinfo.vdf')))
        return True

    except:
        print(
            'file not found in \'C:\Program Files (x86)\Steam\appcache\appinfo.vdf\'\nTry placing it in the same directory as this application.\nIf you already have, ignore this error.')
    try:
        if os.path.exists(os.path.join(directory, 'appinfo.vdf')):
            print('\n\nFound it!')
            appinfo = os.path.join(directory, 'appinfo.vdf')
            return True
    except:
        return False


def call_vdfp(directory):
    # Joining the directory and the VDFP.exe file.
    VDFexe = os.path.join(directory, 'VDFP.exe')
    out = os.path.join(directory, 'output.json')

    result = subprocess.run([VDFexe, appinfo, '-p'], capture_output=True)  # , "--pretty", ">output.json"
    # It's converting the output of the command to a string.
    val = str(result.stdout.strip(), encoding='utf-8')

    vals = json.loads(val)
    list = vals['datasets']
    return list


def parse_json(list):
    global gameLib
    gameLib = []
    game = {}
    # data format
    # list of games
    # games have attributes (dict)
    # this separates games, dupes and vals
    dot = '.'
    x = 0
    iterator = ['name', 'path', 'exe', 'longpath']

    for i in list:
        x = x + 1
        try:
            exe = i['data']['appinfo']['config']['launch']
        except:
            continue
        try:
            wd = i['data']['appinfo']['config']['installdir']
            wd.replace('/', '\\')
            name = i['data']['appinfo']['common']['name']
            name.replace('/', '\\')
        except:
            continue
        z = 0
        for i, z in enumerate(exe.items()):
            try:
                executable = exe[str(i)]['executable']
                executable = executable.replace('/', '\\')
            except:
                continue
            if ".exe" in executable:
                p = 'C:\\program files\\Steam\common\\'
                holder = [
                    wd,
                    name,
                    executable,
                    'xxxxxx'
                ]

                for t, y in zip(iterator, holder):
                    try:
                        # game.update({f"{i}": f"{y}" })
                        game.update({f'{t}': f'{y}'})
                        # writer(iterator, holder, x)
                    except:
                        break

                gameLib.append(game)
                # writer(iterator, holder, x)
                game = {}
            # exes = exe['0']['executable']
            # holder = [wd, name, i['executable']]
            else:
                continue
            dot = dot + '.'
    return gameLib



class Library:
    def __init__(self, exe, path, name, longpath):
        self.exe = str(exe)
        self.path = str(path)
        self.name = str(name)
        self.longpath = str(longpath)
 

def class_constructor(gameLib):
    # create library objects,
    # using a list to keep track
    lib = []
    x = 0
    for i in gameLib:
        lib.append(Library(i['exe'], i['path'], i['name'], 'xxxxx'))
    x = x + 1
    return lib





def callLibrary(lib, directory):
    pathers = LP.main(directory)
    print(str(pathers))
    print(lib[3].path + lib[3].exe)
    return pathers


def pathValidator(paths, lib):
    global matched
    matched = []
    for i in lib:
        for path in paths:
            struct = i.path  # + "\\" + i.exe
            post = i.path + "\\" + i.exe
            x = path + struct.replace('\\\\', '\\')
            if os.path.exists(x):
                i.longpath = x + "\\" + i.exe
                matched.append(i.longpath)
    print('finished')
    print(str(matched))
    return [lib, matched]
    # exampled output times 1k 
    #  path: 'C:\\program files\\Steam\\# It's a string.
    # common\\\\Half-Life\\hlds.exe'
    #   exe:  'hlds.exe'
    #   name: 'Half-Life Dedicated Server'
    #


# f'{VDFexe} {appinfo} --pretty >output.json'
 

def writer(lib, directory):
    log = os.path.join(directory, 'output.txt')
    csv = os.path.join(directory, 'output.csv')
    try:
        os.path.remove(log)
        os.path.remove(csv)
    except:
        print("")
    with open(log, 'w', encoding='utf-8') as f:
        with open(csv, 'w', encoding='utf-8') as g:
            f.write('here are your matched paths, next update includes name. ')
            x = 0
            for i in matched:
                f.write(i)
                f.write('\n')
                g.write(i)
                g.write('\n')
                # for key, val in i.items():
                #     g.write(("\n   " + key + ': ' + val + '\n'))
                #     g.write('\n')
                #     f.write((key + "\n" + val + "\n"))
                #     f.write('\n')

 
