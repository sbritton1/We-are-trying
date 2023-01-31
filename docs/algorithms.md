# Algorithms

Hier bespreken we alle algoritmes.

## Baseline

[Hier](baseline.md) wordt meer informatie gegeven over de baseline met unieke kabels. Dit algoritme kan gerund worden door 'baseline' in te vullen bij `ALGORITHM`. De baseline voor gedeelde kabels werkt op een gelijke manier, maar dan worden de kabels op zo'n manier neergelegd, dat ze gedeeld worden met behulp van het [Lay shared cables algoritme](#Lay-shared-cables).

## Lay shared cables

Om alle huizen zo efficient mogelijk te verbinden met kabels, hebben we dit algoritme gemaakt. We hebben hiervoor per batterij gekeken. Een batterij heeft een paar belangrijke waardes hiervoor, zoals de kabels verbonden aan de batterij en de huizen waarmee de batterij is verbonden. Voor elk huis die verbonden moet worden aan de batterij wordt gekeken wat de afstand is tot de dichtstbijzijnde kabel reeds aan de batterij verbonden. Van alle huizen wordt dan het huis gekozen die het dichtste bij een kabel ligt en verbinden we het huis en de kabel met elkaar. Ook wordt deze kabel opgeslagen in de batterij class. Al deze stappen worden vervolgens herhaald tot alle huizen van de batterij zijn verbonden aan de batterij. Dit wordt herhaald voor alle batterijen.

## Greedy

Greedy verbindt constant het nog niet verbonden huis, die het dichtste bij een batterij staat met voldoende capaciteit om de verbinding aan te kunnen gaan. Omdat via deze methode niet altijd alle huizen verbonden zullen worden, wordt de functie resolve_error() aangeroepen, die huizen gaat wisselen tot alle huizen wel verbonden zijn. Vanwege de randomness in de resolve_error(), kan greedy dit meerdere keren proberen aan te roepen, en bewaart het alleen de goedkoopst gevonden oplossing.

Greedy_shared werkt op dezelfde manier, behalve dat deze op het einde de [gedeelde kabels](#Lay-shared-cables) neerlegt en hiervan de kosten berekent.

## Hill Climber

Dit algoritme maakt 1 willekeurige verandering op een random grid, en kijkt dan vervolgens of dit een betere oplossing is. De verandering wordt uitgevoerd door twee huizen met elkaar te swappen, waardoor ze aan een andere batterij verbonden zijn. Het kijkt een N aantal keer of er een verbetering is gevonden en als dit niet zo is wordt het algoritme gestopt. Als er wel een verbetering wordt gevonden, kijkt het algoritme opnieuw N keer met een willekeurige verandering of er een betere oplossing gevonden kan worden.

Dit algoritme kan ook worden gecombineerd met een greedy algoritme. Dan is het initiele grid niet een random grid, maar een oplossing uit het greedy algoritme, waardoor je in het algemeen begint met een betere oplossing die dan vervolgens wordt berekend met het algoritme.

## Steepest Descent Hill Climber

De steepest descent hill climber probeert elke combinatie van mogelijke swaps van twee huizen waarbij de capaciteit van beide batterijen niet overschreden wordt. Van elke swap berekent het de verbetering in kosten door de manhattan distance tussen de nieuwe verbindingen van twee huizen en de twee batterijen te berekenen en te vergelijken met de prijs van voor de swap. Als elke combinatie is geprobeerd, wordt de swap tussen twee huizen uitgevoerd die de kosten het meest verlaagt. Het algoritme stopt wanneer geen verbetering meer kan worden gevonden.

De steepest descent hill climber voor shared cables werkt op eenzelfde manier, behalve dat bij iedere mogelijke swap tussen twee huizen, de kabels van de twee batterijen betrokken compleet opnieuw neergelegd moeten worden. Vervolgens berekent het algoritme de kosten van de nieuwe gelegde kabels en vergelijkt dit met de originele kosten. Uiteindelijk worden dan de twee huizen geswapt, die ervoor zorgen dat de kosten tussen twee huizen zoveel mogelijk verlaagt worden. Dit blijft zich herhalen tot er geen verbetering meer kan worden gevonden.

## Simulated Annealing

Simulated annealing is een versie van een hill climber, waarin ook sommige verslechteringen kunnen worden doorgevoerd. Door middel van een "temperatuursfunctie" wordt bepaald hoe groot de kans is dat een verslechtering wordt geaccepteerd. De temperatuursfunctie begint hoog, wat ervoor zorgt dat er een grote kans is dat een verslechtering wordt geaccepteerd, en vervolgens daalt de temperatuur over tijd. Ook is de kans dat een grotere verslechtering wordt geaccepteerd kleiner dan die van een kleine verslechtering.

Iedere duizend stappen van de simulated annealing wordt de temperatuur iets omhoog gegooid, in de hoop dat het algoritme uit een locaal minimum kan springen naar een lager locaal minimum. Hoe hoger de stap, hoe lager deze bump is.

De temperatuursfunctie die gebruikt is om dit effect te krijgen is de volgende:
$$temperature = 500 * 0.997 ^ {iteration} + \frac{25}{(\sqrt{int(iteration / 1000)} + 1)} * 0.997 ^ {iteration \mod 1000}$$

Wanneer een grafiek wordt gemaakt van de temperatuursfunctie, ziet deze er dan als volgt uit.

<img src="images/Temperature_graph.png" width="50%" height="auto">


## Plant Propagation Algorithm

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

## Hill Climber Moveable Battery

De Hill climber moveable battery probeert de goedkoopste manier te vinden om shared cables neer te leggen, waarbij de 5 batterijen overal mogen liggen. Hierbij begint het algoritme met de 5 batterijen op een willekeurige positie neer te leggen. Vervolgens wordt de cost berekent van een greedy oplossing. Dan wordt één batterij in zowel de x als de y richting willekeurig tussen -10 en 10 stappen verplaatst. Hiervan wordt wederom de greedy oplossing berekent. Als deze oplossing goedkoper is dan het origineel, dan wordt de batterij op die positie neergelegd. Het schuiven van een willekeurige batterij wordt herhaalt tot er 100 iteraties lang geen verbetering is gevonden.

Het resultaat hiervan wordt in de [hill climber](#hill-climber) gestopt, om te kijken of er nog een paar kleine verbeteringen te vinden zijn.

## Clustering

Clustering is een algoritme voor de case met het bewegen van de batterijen (gradatie 3 in de [Case Uitleg](#case-uitleg)). Het idee is dat er voor elke batterij een cluster wordt gevonden en vervolgens wordt de batterij in het midden hiervan geplaatst. Vervolgens kan een algoritme van shared cables hiervan de optimale oplossing vinden. 

Voor het clusteren wordt er gebruik gemaakt van K-means clustering. Hierbij worden ten eerste de batterijen op willekeurige plekken op de grid geplaatst. Vervolgens worden alle huizen gekoppeld aan de dichtsbijzijnde batterij. Daarna wordt de batterij verplaatst naar het midden van al zijn gekoppelde huizen. Dit wordt een aantal keer herhaald en met een beetje mazzel worden er zo mooie clusters gevonden voor elke batterij. Hierna wordt het [greedy](#greedy) algoritme gebruikt om de daadwerkelijke connecties tussen de huizen en batterijen te maken.