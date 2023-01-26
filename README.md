# Smart Grid

Welkom bij ons project voor het vak 'Algoritmen en Heuristieken' voor de minor programmeren aan de Universiteit van Amsterdam. Hier proberen we een onmogelijke case op te lossen. Wij hebben voor de case Smart Grid gekozen.

## Aan de slag

### Vereisten 

Dit project is volledig geprogrammeerd in Python. De vereiste modules kunnen geïnstalleerd worden m.b.v. het volgende command.

```bash
python3 -m pip install -r requirements.txt
```

> NOTE:
> Dit command kan per persoon verschillen afhankelijk van de installatie van python.

### Hoe te gebruiken

Het programma kan worden gerund door de main.py file te runnen. Hiervoor moeten wel nog enkele command-line arguments worden toegevoegd voordat het programma kan werken. Zo moet het eerste argument het district zijn en het tweede argument welk algoritme. Een algemeen voorbeeld is hieronder gegeven:

```bash
python3 main.py [DISTRICT] [ALGORITHM]
```

Voor `district` kan je 0 t/m 4 invullen en voor `algorithm` kan je kiezen uit een van de volgende algoritmes:
- baseline
- greedy
- sd_hill_climber
- baseline_shared
- hill_climber_shared
- sd_hill_climber_shared
- simulated_annealing

Na het runnen zou een matplotlib venster moeten openen met de verbonden Smart Grid, zoals het voorbeeld hieronder.

![](results/BestOf10%20district1%20simulated%20annealing.png)

Resultaten van runs worden opgeslagen in een json bestand in de results folder. Om deze te visualiseren kan het volgende commando gebruikt worden:

```bash
python3 visualize_json.py [FILEPATH]
```

### Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- /code: bevat alle code van dit project
    - /code/algorithms: bevat de code voor algoritmes
    - /code/classes: bevat de benodigde classes voor deze case
    - /code/visualisation: bevat de code voor de visualisatie
    - /code/export: bevat de code voor het exporteren naar een JSON bestand
    - /code/helper_functions: bevat functies die in meerdere algoritmes worden gebruikt
- /data: bevat de verschillende databestanden die nodig zijn om de grid in te laden
- /docs: bevat de verslagen voor dit project
- /results: bevat de resultaten van eerdere runs 

## Auteurs

- Xander Broos
- Miguel Siewe
- Sander Britton

## Credits

[Home Page](https://icons8.com/icon/103183/home-page) icon by [Icons8](https://icons8.com)

[Normal battery](https://icons8.com/icon/Vw6xKWsHOBPo/battery) icon by [Icons8](https://icons8.com)

[PowerStar battery](https://icons8.com/icon/Sy5Roz5qTmgs/battery) icon by [Icons8](https://icons8.com)

[Imerse-II battery](https://icons8.com/icon/nhowbLkfABQB/battery) icon by [Icons8](https://icons8.com)

[Imerse-III battery](https://icons8.com/icon/09kDf3bDCwgu/battery) icon by [Icons8](https://icons8.com)
