
import re

# Script CONVERT_CSV_TO_NML.PY
# - Converts CSV placename databases
# - Prepares the NML file to generate the newGRF file
#
# Author: Tomirad, 28.05.2023, version: 1.5

def addToFile(file, list):
    var = open(file, "w")
    for name in list:
        var.write(name + "\n")
    var.close()

class TownNames:
    def __init__(self, name, pop, status):
        self.name = name
        self.pop = int(pop)
        self.status = int(status)
 
    def addPop(self, pop):
        self.pop += int(pop)

    def __repr__(self):
        return '{' + self.name + ', ' + str(self.pop) + ', ' + str(self.status) + '}'


def createTextElement(pool, prop):
    townNameTextTemplate = "\t\ttext(\"NAME\", PROP),"
    townPool = []
    for town in pool:
        text = townNameTextTemplate
        var = {'NAME': town, 'PROP': prop}
        for key in var.keys():
            text = text.replace(key, str(var[key]))
        townPool.append(text)
    return "\n".join(townPool)

def createTownFunc(func, text, count):
    townNameFuncTemplate = "//elements: NUMBER\ntown_names(FUNC) {\n\t{\nTEXT\n\t}\n}"
    townFunc = townNameFuncTemplate
    var = {'NUMBER': count, 'FUNC': func, 'TEXT': text}
    for key in var.keys():
        townFunc = townFunc.replace(key, str(var[key]))
    return townFunc

def createTownNames(func, text):
    townNameStyleTemplate = "\t\ttown_names(FUNC, PROP),"
    townFunc = townNameStyleTemplate
    var = {'FUNC': func, 'PROP': text}
    for key in var.keys():
        townFunc = townFunc.replace(key, str(var[key]))
    return townFunc

# GET OPTIONS
optionsType = {
    'isTest': 'bool',
    'insertionTestContent': 'strlist',
    'town_names_CITIES': 'int',
    'town_names_VILLAGES1': 'int',
    'town_names_VILLAGES2': 'int',
    'town_names_VILLAGES3': 'int',
    'town_names_VILLAGES4': 'int',
    'town_names_VILLAGES5': 'int',
    'text_names_CAPITOLS': 'int',
    'text_names_CITIES': 'int',
    'text_names_TOWNS': 'int',
    'text_names_VILLAGES': 'int',
    'populationForCities': 'int',
    'stepList': 'list',
    'sourceToDatabase': 'string',
    'countDatabases': 'int'
}
options = {
    'isTest': False,
    'insertionTestContent': 'suffix',
    'town_names_CITIES': 100,
    'town_names_VILLAGES1': 1,
    'town_names_VILLAGES2': 1,
    'town_names_VILLAGES3': 1,
    'town_names_VILLAGES4': 1,
    'town_names_VILLAGES5': 1,
    'text_names_CAPITOLS': 100,
    'text_names_CITIES': 50,
    'text_names_TOWNS': 2,
    'text_names_VILLAGES': 1,
    'populationForCities': 50_000,
    'stepList': [46, 16320, 8160, 4080, 1020, 1020],
    'sourceToDatabase': "Ludnosc\\PolishCities",
    'countDatabases': 16
}
optionsFile = open('convert_options.ini')
for row in optionsFile:
    param = row.rstrip("\n").split('=')
    if len(param[0]) > 0 and param[0] in optionsType.keys():
        match optionsType[param[0]]:
            case 'bool':
                options[param[0]] = str(param[1]) in ('True')
            case 'int':
                options[param[0]] = int(param[1])
            case 'list':
                options[param[0]] = list(param[1])
            case 'strlist':
                if str(param[1]) in ('suffix', 'prefix'):
                    options[param[0]] = str(param[1])
            case _:
                options[param[0]] = str(param[1])

optionsFile.close()
# TOWNS

townNames = {}
for id in range(0, options['countDatabases']+1):
    i = 0
    fileId = '{:0>2}'.format(id)
    poolNames = []
    with open(options['sourceToDatabase']+''+fileId+'.csv', encoding='utf-8') as rows:
        for row in rows:
            if i > 0:
                row = row.rstrip("\n").split(';')
                name = row[1]
                pop = row[4]
                status = id
                if fileId == '00':
                    name = row[0]
                    pop = row[3]
                    status = row[5]
                name = re.sub('"[A-Z]"', '', name)

                if name not in townNames.keys():
                    townNames[name] = TownNames(name, pop, status)
                    poolNames.append(name)
                elif id == 0:
                    townNames[name].addPop(pop)
                else:
                    townNames[name].addPop(pop)
            i += 1
countTownNames = len(townNames)
print('count town names in LIST', countTownNames)

poolTowns = {
    'capitols': [],
    'cities': [],
    'towns': [],
    'villages': [],
    'villages1': [],
    'villages2': [],
    'villages3': [],
    'villages4': [],
    'villages5': [],
    'lost_names': []
}

def townName(name, symbol, nameId, isTest = False, insertion='suffix'):
    left = right = ''
    if isTest == True:
        formatedNameId = '{:0>5}'.format(nameId)
        textInsertion = '['+symbol+']['+formatedNameId+']'
        if insertion == 'prefix':
            left = textInsertion + ' '
        else:
            right = ' ' + textInsertion
    return left + name + right

poolVillages = []
townId = 1
for name, town in townNames.items():
    if town.status == -1:
        poolTowns['capitols'].append(townName(town.name, 'S', townId, options['isTest'], options['insertionTestContent']))
        townId += 1
    elif town.status == 0:
        if town.pop >= options['populationForCities']:
            poolTowns['cities'].append(townName(town.name, 'C', townId, options['isTest'], options['insertionTestContent']))
        else:
            poolTowns['towns'].append(townName(town.name, 'T', townId, options['isTest'], options['insertionTestContent']))
        townId += 1
    else:
        poolVillages.append({'name': town.name, 'pop': town.pop})

poolVillages.sort(key = lambda s: (-s['pop'], s['name']))

i = 0
for town in poolVillages:
    if i < sum(options['stepList'][:1]):
        poolTowns['villages'].append(townName(town['name'], 'V', townId, options['isTest'], options['insertionTestContent']))
    elif i < sum(options['stepList'][:2]):
        poolTowns['villages1'].append(townName(town['name'], 'V1', townId, options['isTest'], options['insertionTestContent']))
    elif i < sum(options['stepList'][:3]):
        poolTowns['villages2'].append(townName(town['name'], 'V2', townId, options['isTest'], options['insertionTestContent']))
    elif i < sum(options['stepList'][:4]):
        poolTowns['villages3'].append(townName(town['name'], 'V3', townId, options['isTest'], options['insertionTestContent']))
    elif i < sum(options['stepList'][:5]):
        poolTowns['villages4'].append(townName(town['name'], 'V4', townId, options['isTest'], options['insertionTestContent']))
    elif i < sum(options['stepList'][:6]):
        poolTowns['villages5'].append(townName(town['name'], 'V5', townId, options['isTest'], options['insertionTestContent']))
    else:
        poolTowns['lost_names'].append(townName(town['name'], 'LT', townId, options['isTest'], options['insertionTestContent']))
        
    townId += 1
    i += 1

for key in poolTowns:
    poolTowns[key].sort()


for typeTown in poolTowns.keys():
    countTownNames += len(poolTowns[typeTown])

# CREATE .NML

townNamesDict = {
    'CITIES': {
        'capitols': [poolTowns['capitols'], options['text_names_CAPITOLS'], options['town_names_CITIES'], len(poolTowns['capitols'])],
        'cities': [poolTowns['cities'], options['text_names_CITIES'], options['town_names_CITIES'], len(poolTowns['cities'])],
        'towns': [poolTowns['towns'], options['text_names_TOWNS'], options['town_names_CITIES'], len(poolTowns['towns'])],
        'villages': [poolTowns['villages'], options['text_names_VILLAGES'], options['town_names_CITIES'], len(poolTowns['villages'])]
    },
    'VILLAGES1': [poolTowns['villages1'], options['text_names_VILLAGES'], options['town_names_VILLAGES1'], len(poolTowns['villages1'])],
    'VILLAGES2': [poolTowns['villages2'], options['text_names_VILLAGES'], options['town_names_VILLAGES2'], len(poolTowns['villages2'])],
    'VILLAGES3': [poolTowns['villages3'], options['text_names_VILLAGES'], options['town_names_VILLAGES3'], len(poolTowns['villages3'])],
    'VILLAGES4': [poolTowns['villages4'], options['text_names_VILLAGES'], options['town_names_VILLAGES4'], len(poolTowns['villages4'])],
    'VILLAGES5': [poolTowns['villages5'], options['text_names_VILLAGES'], options['town_names_VILLAGES5'], len(poolTowns['villages5'])],
}

townNamesPool = [] 
townNamesFunc = [] 
textElements = []
countTownNames = 0
for key, item in townNamesDict.items():
    if type(item) is dict:
        countElements = 0
        for itemKey, data in item.items():
            print(key, itemKey, data[3])
            textElements.append(createTextElement(data[0], data[1]))
            countElements += data[3]
            countTownNames += data[3]
        townNamesPool.append(createTownFunc(key, "\n".join(textElements), countElements))
        townNamesFunc.append(createTownNames(key, 100))
    else:
        print(key, item[3])
        countTownNames += item[3]
        townNamesPool.append(createTownFunc(key, createTextElement(item[0], item[1]), item[3]))
        townNamesFunc.append(createTownNames(key, item[2]))

print('count town names in NML', countTownNames)

townNameFileTemplate = open("Polish_Real_Town_Names.tnml", encoding='utf-8')
strPyDict = {
    'STR_PY_TOWNS_NAMES_COUNT': countTownNames,
    'STR_PY_TOWNS_NAMES_POOL': "\n\n".join(townNamesPool),
    'STR_PY_TOWNS_NAMES_FUNC': "\n".join(townNamesFunc),
}

townNameFile = open("Polish_Real_Town_Names.nml", "w", encoding='utf-8')
for row in townNameFileTemplate:
    for key in strPyDict.keys():
        row = row.replace(key, str(strPyDict[key]))
    townNameFile.write(row)
townNameFile.close()

townNameFileTemplate.close()

if len(poolTowns['lost_names']) > 0:
    lostTownNameFile = open("lost_names.txt", 'w', encoding='utf-8')
    lostTownNameFile.write("# Count: "+ str(len(poolTowns['lost_names'])))
    for row in poolTowns['lost_names']:
        lostTownNameFile.write("\n" + row)
    lostTownNameFile.close()

