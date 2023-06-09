# Polish_Real_Town_Names
List of towns and villages from the government site with place names for OpenTTD.

1. Prepare data:
Tables with Cities and Villages (look Ludnosc folder)
2. Create pool names:
`python convert_CSV_to_NML`
3. Generate GRF file:
`nmlc.exe -c --grf polish_real_town_names.grf Polish_Real_Town_Names.nml --lang-dir=lang --custom-tags=custom_tags.txt`

Current:
```
nmlc info: 0 sprites, 0 cached, 0 orphaned, 0 duplicates, 0 newly encoded (python)
nmlc info: Town names: 127/128
```

Add number id town name:
`convert_options.ini` > `isTest=True`

##Screenshot from game

![Screenshot from game](https://github.com/Tomirad/Polish_Real_Town_Names/assets/12190843/021db00f-207b-438a-977e-1789cb22500f)


## Sources:
+ https://github.com/OpenTTD
+ https://www.openttd.org/
+ https://www.tt-forums.net/
+ https://www.tt-wiki.net/

+ https://dane.gov.pl/pl/dataset/188,wykaz-urzedowych-nazw-miejscowosci-i-ich-czesci
+ https://polskawliczbach.pl
