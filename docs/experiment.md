# Experimenteren

In dit document bespreken we hoe we hebben geëxperimenteerd en resultaten hebben verzameld. Ten eerste bespreken we dit voor de case met unieke kabels, dan met gedeelde kabels en dan met het verplaatsen van batterijen.

## Methode

METHODE BESPREKEN

> HIER INFO OVER PCs
> 

## Theoretisch optimum

Het is voor deze case lastig te bepalen wanneer het absolute optimum is gevonden. Daarom is het interessant om te kijken naar een theoretisch optimum. Dit geeft een idee van hoe veel kosten je minimaal moet maken en dus hoe goed een oplossing is.

Voor het theoretisch optimum doen we de volgende aannames:
- Er zijn altijd 5 batterijen en 150 huizen.
- Elk huis heeft minstens 1 kabel nodig om de connectie tussen de batterij en het huis te verwezenlijken.

Deze aannames is ver van de daadwerkelijke situatie voor de unieke kabels case. Hierbij zouden namelijk alle huizen op een afstand van 1 van een batterij moeten zitten, wat zou betekenen dat er heel veel huizen op dezelfde plek zouden moeten zitten. 

Voor de gedeelde kabels case is dit echter wel mogelijk. Hierbij is het namelijk mogelijk dat alle huizen op een sliert liggen, met 1 afstand tussen elk huis en 1 afstand naar een batterij.

Het theoretische optimum kan volgens de volgende formule worden berekend.

$$theoretisch\; optimum = kosten_{per\; batterij} \cdot n_{batterijen} + kosten_{per\; kabel} \cdot n_{kabels}$$

$$theoretisch\; optimum = 5000 \cdot 5 + 9 \cdot 150 = 26350$$

## Unieke kabels

intro

### Resultaten

| **Algoritme**                 | **Beste resultaat** | **Runtime** | **Aantal runs** | **PC**   | **Parameters** |
|-------------------------------|---------------------|-------------|-----------------|----------|----------------|
| random                        | 70225               | 0:04:11     | 100000          | i7-9750H | /              |
| greedy                        | 56905               | 0:03:54     | 100000          | i7-9750H | /              |
| steepest descent hill climber | 56266               | 0:10:46     | 1000            | i7-9750H | /              |

## Gedeelde kabels

intro

### Plant Propagation Algorithm

Voor de Plant Propagation Algorithm (PPA) zijn er veel parameters die de effectiviteit van het algoritme sterk bepalen. De parameters worden hieronder gegeven. Meer informatie over het algoritme en de parameters is [hier](../README.md#plant-propagation-algorithm) te vinden.

PPA parameters:
- $n_{roots}$
- $n_{runners_{min}}$ 
- $n_{runners_{max}}$ 
- $n_{changes_{min}}$ 
- $n_{changes_{max}}$
- $n_{generations}$
- Maximum generations with no improvement
- Fitness functie

De uiteindelijke parameters zijn achterhaald door trial en error. Hierbij is het gebleken dat de minimale aantal changes erg laag moet zijn, om zo met kleine aanpassingen op een optimum te komen. Daarnaast moet het maximale aantal changes niet te laag zijn, om zo nog uit een lokaal optimum te kunnen 'springen'. Dit bleek een lastig optimalisatieprobleem, ook door de redelijk lange runtijd van het algoritme. 

De runtijd moest aan de andere kant namelijk niet uit de hand lopen, wat voornamelijk bepaald werd door het aantal runners. Hierbij is voornamelijk met het maximale aantal runners geëxperimenteerd, omdat de minimale aantal runners eigenlijk 1 of 2 is geweest. 

De uiteindelijke parameters zijn hieronder gegeven:
- $n_{roots}$ = 8
- $n_{runners_{min}}$ = 2 
- $n_{runners_{max}}$ = 6
- $n_{changes_{min}}$ = 1
- $n_{changes_{max}}$ = 8
- $n_{generations}$ = 300
- Maximum generations with no improvement = 20
- Fitness functie is [hier](../README.md#plant-propagation-algorithm) te vinden

Door een gebrek aan tijd is het algoritme niet geheel geoptimaliseerd. Zoals eerder vermeld is het algoritme niet heel snel en dus lastig om veranderingen op te maken en hier snel de resultaten van te zien. Daarnaast was de informatievoorziening online ook beperkt en niet makkelijk te begrijpen. Zo is later gebleken dat de fitness functie nog door een tangens hyperbolicus gehaald had kunnen worden, wat de resultaten zou moeten verbeteren. 

### Resultaten

| **Algoritme**                 | **Beste resultaat** | **Runtime (H:MM:SS)** | **Aantal runs** | **PC**            |
|-------------------------------|---------------------|-----------------------|-----------------|-------------------|
| Baseline                      | 34306               | 7:44:00               | 100000          | i7-9750H          |
| Greedy                        | 30562               | 0:04:01               | 100000          | i7-9750H          |
| Hill climber                  | 30724               | 2:04:16               | 40              | AMD Ryzen 7 4700U |
| Steepest descent hill climber | 31534               | 7:47:45               | 1               | i5-12400F         |
| Simulated annealing           | 30220               | 6:13:40               | 50              | i5-12400F         |
| Plant propagation             | 31534               | 1:40:32               | 1 (227 generaties)| Sander laptop     |
| Greedy + hill climber         | 29752               | 1:32:00               | 24              | AMD Ryzen 7 4700U |
| Greedy + hill climber 2.0     | 29905               | 4:05:32               | 108             | AMD Ryzen 7 4700U |

### Conclusie

## Batterijen verplaatsen

intro

### Resultaten

| **Algoritme** | **Beste resultaat** | **Tijd per core** | **Parameters** |
|---------------|---------------------|-------------------|----------------|
|               |                     |                   |                |
|               |                     |                   |                |
|               |                     |                   |                |

clustering met hill climber battery:
- best cost 29563
- time taken 1:03:52
- 50 keer hill climber

