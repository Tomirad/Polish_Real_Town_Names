
import re

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


# TOWNS

townNames = {}
for id in range(0, 17):
    i = 0
    fileId = '{:0>2}'.format(id)
    poolNames = []
    with open('Ludnosc\\PolishCities'+fileId+'.csv', encoding='utf-8') as rows:
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
    'capitals': {},
    'cities': {},
    'villages': {}
}

poolTowns = {
    'capitols': [],
    'cities': [],
    'town': [],
    'villages1': [],
    'villages2': [],
    'villages3': [],
    'villages4': []
}
i = 0
steps = [16320, 8160, 4080, 2040]
for name, town in townNames.items():
    if town.status == -1:
        poolTowns['capitols'].append(town.name)
    elif town.status == 0:
        if town.pop >= 50_000:
            poolTowns['cities'].append(town.name)
        else:
            poolTowns['town'].append(town.name)
    else:
        if i < steps[0]:
            poolTowns['villages1'].append(town.name)
        elif i < steps[0] + steps[1]:
            poolTowns['villages2'].append(town.name)
        elif i < steps[0] + steps[1] + steps[2]:
            poolTowns['villages3'].append(town.name)
        elif i < steps[0] + steps[1] + steps[2] + steps[3]:
            poolTowns['villages4'].append(town.name)
        i += 1

countTownNames = 0
for typeTown in poolTowns.keys():
    print(typeTown, len(poolTowns[typeTown]))
    countTownNames += len(poolTowns[typeTown])
print('count town names in NML', countTownNames)

# CREATE .NML

townNamesDict = {
    'CITIES': [poolTowns['capitols'], 100, 100, len(poolTowns['capitols'])] + [poolTowns['cities'], 10, 1, len(poolTowns['cities'])] + [poolTowns['town'], 10, 1, len(poolTowns['town'])],
    'VILLAGES1': [poolTowns['villages1'], 10, 1, len(poolTowns['villages1'])],
    'VILLAGES2': [poolTowns['villages2'], 10, 1, len(poolTowns['villages2'])],
    'VILLAGES3': [poolTowns['villages3'], 10, 1, len(poolTowns['villages3'])],
    'VILLAGES4': [poolTowns['villages4'], 10, 1, len(poolTowns['villages4'])],
}

townNamesPool = [] 
townNamesFunc = [] 
for key, item in townNamesDict.items():
    townNamesPool.append(createTownFunc(key, createTextElement(item[0], item[1]), item[3]))
    townNamesFunc.append(createTownNames(key, item[2]))

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

