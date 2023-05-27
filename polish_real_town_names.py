def addToFile(file, list):
    var = open(file, "w")
    for name in list:
        var.write(name + "\n")
    var.close()

modPoolNames = []
with open('plnames0.txt', encoding='utf-8') as names:
    for name in names:
        modPoolNames.append(name.rstrip("\n"))

poolNames = []
for i in range(2,5):
#for i in [5]:
    filePoolNames = open('plnames'+str(i)+'.txt', encoding='utf-8')
    for name in filePoolNames:
        poolNames.append(name.rstrip("\n"))
    filePoolNames.close()

names.close()

addToPool1 = set(modPoolNames).difference(poolNames)
addToPool2 = set(poolNames).difference(modPoolNames)

addToFile('stats1.txt', addToPool1)
addToFile('stats2.txt', addToPool2)

print("\nNazw w modzie: ", len(modPoolNames))
print("Nazw w bazie: ", len(poolNames))
print("Różnica: ", len(poolNames) - len(modPoolNames))
print("Brakujących nazw: ", len(addToPool1), len(addToPool2))

