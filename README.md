# Smart Grid

Welkom bij ons project voor het vak 'Algoritmen en Heuristieken' voor de minor programmeren aan de Universiteit van Amsterdam. Hier proberen we een onmogelijke case op te lossen. Wij hebben voor de case 'Smart Grid' gekozen.

## Case Uitleg

In de case 'Smart Grid' wordt een grid gegeven met huizen die allemaal energie kunnen leveren. Op de grid staan ook batterijen die deze energie moeten opslaan. Deze batterijen hebben wel een maximum capaciteit die niet overschreden mag worden. Om de energie van een huis naar een batterij te brengen moeten kabels worden gelegd. Deze kabels kosten geld en dus is het belangrijk om dit zo efficient mogelijk te doen. Aan ons de taak om de kosten zo laag mogelijk te houden. 

Hierbij moeten we ons aan bepaalde vereisten houden:
- Batterijen mogen niet aan elkaar verbonden zijn. Ook niet via een huis.
- Een huis mag niet aan meerdere batterijen verbonden zijn.
- Er mogen meerdere kabels over dezelfde gridsegmenten lopen.

Dit probleem heeft verschillende gradaties in moeilijkheid:
1. Alle huizen moeten een unieke kabel naar een batterij hebben.
2. Huizen mogen kabels delen.
3. Batterijen mogen verplaatst worden.
4. Je mag zelf batterijen kiezen uit een selectie en deze overal plaatsen waar je wil.

Bij elke gradatie is het doel om de kosten zo laag mogelijk te houden. De kosten kunnen berekend worden door voor elke kabel 9 te rekenen en voor elke 'normale' batterij (de batterijen van gradatie 1 t/m 3) 5000 te rekenen.

Bij de laatste gradatie kan uit de volgende batterijtypes worden gekozen met elk hun eigen prijs en capaciteit.

| **Batterijtype** | **Capaciteit** | **Prijs** |
|------------------|----------------|-----------|
| PowerStar        | 450            | 900       |
| Imerse-II        | 900            | 1350      |
| Imerse-III       | 1800           | 1800      |

Om ons algoritme te testen, zijn er drie dummy-woonwijken opgesteld. Deze zijn gegeven in csv-bestanden. Deze wijken zien er als volgt uit:

![Voorbeeld wijk](docs/images/Wijk1.png)

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

Voor `DISTRICT` kan je 1 t/m 3 invullen en voor `ALGORITHM` kan je kiezen uit een van de volgende algoritmes([hier](#algoritmes) meer info):
- baseline
- greedy
- sd_hill_climber
- baseline_shared
- greedy_shared
- hill_climber_shared
- sd_hill_climber_shared
- simulated_annealing
- plant_propagation
- hill_climber_battery
- clustering

Standaard wordt het resultaat opgeslagen in een JSON bestand te vinden op `/results/output.json`. Daarnaast wordt het ook gevisualiseerd in een matplotlib venster. Deze output methodes kunnen worden uitgeschakeld door de desbetreffende regel te commenten in regels 51 t/m 55 in main.py.

De visualisatie zou er ongeveer zo uit moeten komen te zien:

![](docs/images/example_grid.png)

Om de eerdere resultaten die opgeslagen zijn een JSON bestand te visualiseren kan het volgende commando gebruikt worden:

```bash
python3 visualize_json.py [FILEPATH]
```

### Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- /code: bevat alle code van dit project
    - /code/algorithms: bevat de code voor algoritmes
      - /code/algorithms/own_cables: bevat alle algoritmes voor het unieke kabel probleem
      - /code/algorithms/shared_cables: bevat alle algoritmes voor het gedeelde kabel probleem
      - /code/algorithms/battery_move: bevat alle algoritmes voor het gedeelde kabel en batterij bewegen probleem
    - /code/classes: bevat de benodigde classes voor deze case
    - /code/visualisation: bevat de code voor de visualisatie
    - /code/export: bevat de code voor het exporteren naar een JSON bestand
    - /code/helper_functions: bevat functies die in meerdere algoritmes worden gebruikt
- /data: bevat de verschillende databestanden die nodig zijn om de grid in te laden
- /docs: bevat de verslagen voor dit project
- /results: bevat de resultaten van eerdere runs geordend

## Algoritmes

Hier bespreken we de algoritmes die we hebben.

### Baseline

[Hier](docs/baseline.md) wordt meer informatie gegeven over de baseline met unieke kabels. Dit algoritme kan gerund worden door 'baseline' in te vullen bij `ALGORITHM`.

> WAT INVULLEN VOOR BASELINE SHARED

### Greedy

Greedy verbindt constant het nog niet verbonden huis, die het dichtste bij een batterij staat met voldoende capaciteit om de verbinding aan te kunnen gaan. Omdat via deze methode niet altijd alle huizen verbonden zullen worden, wordt de functie resolve_error() aangeroepen, die huizen gaat wisselen tot alle huizen wel verbonden zijn. Vanwege de randomness in de resolve_error(), kan greedy dit meerdere keren proberen aan te roepen, en bewaart het alleen de goedkoopst gevonden oplossing.

Greedy_shared werkt op dezelfde manier, behalve dat deze op het einde de gedeelde kabels neerlegt en hiervan de kosten berekent.

### Hill Climber

> WAT INVULLEN VOOR HILL CLIMBER

Dit algoritme maakt 1 willekeurige verandering op een random grid, en kijkt dan vervolgens of dit een betere oplossing is. De verandering wordt uitgevoerd door twee huizen met elkaar te swappen, waardoor ze aan een andere batterij verbonden zijn. Het kijkt een N aantal keer of er een verbetering is gevonden en als dit niet zo is wordt het algoritme gestopt. Als er wel een verbetering wordt gevonden, kijkt het algoritme opnieuw N keer met een willekeurige verandering of er een betere oplossing gevonden kan worden.

Dit algoritme kan ook worden gecombineerd met een greedy algoritme. Dan is het initiele grid niet een random grid, maar een oplossing uit het greedy algoritme, waardoor je in het algemeen begint met een betere oplossing die dan vervolgens wordt berekend met het algoritme.

### Steepest Descent Hill Climber

De steepest descent hill climber probeert elke combinatie van mogelijke swaps van twee huizen waarbij de capaciteit van beide batterijen niet overschreden wordt. Van elke swap berekent het de verbetering in kosten door de manhattan distance tussen de nieuwe verbindingen van twee huizen en de twee batterijen te berekenen en te vergelijken met de prijs van voor de swap. Als elke combinatie is geprobeerd, wordt de swap tussen twee huizen uitgevoerd die de kosten het meest verlaagt. Het algoritme stopt wanneer geen verbetering meer kan worden gevonden.

De steepest descent hill climber voor shared cables werkt op eenzelfde manier, behalve dat bij iedere mogelijke swap tussen twee huizen, de kabels van de twee batterijen betrokken compleet opnieuw neergelegd moeten worden. Vervolgens berekent het algoritme de kosten van de nieuwe gelegde kabels en vergelijkt dit met de originele kosten. Uiteindelijk worden dan de twee huizen geswapt, die ervoor zorgen dat de kosten tussen twee huizen zoveel mogelijk verlaagt worden. Dit blijft zich herhalen tot er geen verbetering meer kan worden gevonden.

### Simulated Annealing

Simulated annealing is een versie van een hill climber, waarin ook sommige verslechteringen kunnen worden doorgevoerd. Door middel van een "temperatuursfunctie" wordt bepaald hoe groot de kans is dat een verslechtering wordt geaccepteerd. De temperatuursfunctie begint hoog, wat ervoor zorgt dat er een grote kans is dat een verslechtering wordt geaccepteerd, en vervolgens daalt de temperatuur over tijd. Ook is de kans dat een grotere verslechtering wordt geaccepteerd kleiner dan die van een kleine verslechtering.

Iedere duizend stappen van de simulated annealing wordt de temperatuur iets omhoog gegooid, in de hoop dat het algoritme uit een locaal minimum kan springen naar een lager locaal minimum. Hoe hoger de stap, hoe lager deze bump is.

De temperatuursfunctie die gebruikt is om dit effect te krijgen is de volgende:
$$temperature = 500 * 0.997 ^ {iteration} + \frac{25}{(\sqrt{int(iteration / 1000)} + 1)} * 0.997 ^ {iteration \bmod 1000}$$

### Plant Propagation Algorithm

Plant Propagation Algorithm (PPA) is een population-based algorithm gebaseerd op de propagatie van een aardbeienplant ([bron](https://www.researchgate.net/publication/252321319_Nature-Inspired_Optimisation_Approaches_and_the_New_Plant_Propagation_Algorithm)). Dit algoritme heeft de volgende parameters:

- $n_{roots}$
- $n_{runners_{min}}$ 
- $n_{runners_{max}}$ 
- $n_{changes_{min}}$ 
- $n_{changes_{max}}$
- $n_{generations}$
- Maximum generations with no improvement
- Fitness functie

Voor onze case hebben we het zo geïmplementeerd dat we beginnen met $n_{roots}$ willekeurige oplossingen van de grid. Deze oplossingen zijn onze eerste generatie. Deze krijgen elk een fitness score tussen de 0 en 1 op basis van hun kosten vergeleken met de rest van de populatie. Hiervoor wordt de volgende formule gebruikt:

$$fitness(cost) = \frac{cost_{max} - cost}{cost_{max} - cost_{min}}$$

Hierbij zijn $cost_{max}$ en $cost_{min}$ de maximale en minimale cost van de huidige generatie. Op basis van deze fitness worden het aantal runners en het aantal aanpassingen berekend. Het aantal runners bepaald hoe veel kinderen een parent krijgt en het aantal aanpassingen bepaalt hoe veel deze kinderen verschillen van de parent. Een aanpassing is een wisseling van connecties bij twee willekeurige huizen, waarbij deze aanpassing nog steeds een valide oplossing geeft. De volgende formules worden gebruikt voor het bepalen van het aantal runners en het aantal aanpassingen:

$$n_{runners}(fitness) = \lceil fitness \cdot (n_{runners_{max}} - n_{runners_{min}}) \rceil + n_{runners_{min}}$$

$$n_{changes}(fitness) = \lceil (1 - fitness) \cdot (n_{changes_{max}} - n_{changes_{min}}) \rceil + n_{changes_{min}}$$

Van deze nieuwe generatie (inclusief de parents) worden de beste $n_{roots}$ bewaard. Hier kan vervolgens een nieuwe generatie mee worden gemaakt. Dit wordt herhaald tot er een bepaald aantal keer geen verbetering wordt gevonden (max times no improvement) of tot een maximaal aantal generaties $n_{generaties}$. 

### Hill Climber Moveable Battery

De Hill climber moveable battery probeert de goedkoopste manier te vinden om shared cables neer te leggen, waarbij de 5 batterijen overal mogen liggen. Hierbij begint het algoritme met de 5 batterijen op een willekeurige positie neer te leggen. Vervolgens wordt de cost berekent van een greedy oplossing. Dan wordt één batterij in zowel de x als de y richting willekeurig tussen -10 en 10 stappen verplaatst. Hiervan wordt wederom de greedy oplossing berekent. Als deze oplossing goedkoper is dan het origineel, dan wordt de batterij op die positie neergelegd. Het schuiven van 1 batterij wordt herhaalt tot er 100 iteraties lang geen verbetering is gevonden.

Het resultaat hiervan wordt in de hill climber shared gestopt, om te kijken of er nog een paar kleine verbeteringen te vinden zijn.

### Clustering

Clustering is een algoritme voor de case met het bewegen van de batterijen (gradatie 3 in de [Case Uitleg](#case-uitleg)). Het idee is dat er voor elke batterij een cluster wordt gevonden en vervolgens wordt de batterij in het midden hiervan geplaatst. Vervolgens kan een algoritme van shared cables hiervan de optimale oplossing vinden. 

Voor het clusteren wordt er gebruik gemaakt van K-means clustering. Hierbij worden ten eerste de batterijen op willekeurige plekken op de grid geplaatst. Vervolgens worden alle huizen gekoppeld aan de dichtsbijzijnde batterij. Daarna wordt de batterij verplaatst naar het midden van al zijn gekoppelde huizen. Dit wordt een aantal keer herhaald en met een beetje mazzel worden er zo mooie clusters gevonden voor elke batterij. Hierna wordt het [greedy](#greedy) algoritme gebruikt om de daadwerkelijke connecties tussen de huizen en batterijen te maken.


## Experimenteren

Documentatie van onze experimenten en resultaten met de verschillende algoritmes is [hier](docs/experiment.md) te vinden.

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
