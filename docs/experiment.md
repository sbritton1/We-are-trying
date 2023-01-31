# Experimenteren

In dit document bespreken we hoe we hebben geëxperimenteerd en resultaten hebben verzameld. Ten eerste bespreken we dit voor de case met unieke kabels, dan met gedeelde kabels en dan met het verplaatsen van batterijen.

## Methode

METHODE BESPREKEN

> Voor het runnen van de code zijn meerdere verschillende laptops gebruikt met verschillende specificaties. Omdat dit grote gevolgen kan hebben voor de runtime van een programma. Om deze reden zetten we bij de resultaten neer welke PC het algoritme heeft gerund om bij een bepaalde tijd uit te komen, en wordt hier een lijst met de specificaties van de PCs neergezet: \
> PC 1 - CPU: i5-12400F, RAM: 32GB, 3400MHz DDR4 \
> PC 2 - CPU: i7-9750H, RAM: 16GB, 2667MHz DDR4 \
> PC 3 - CPU: i7-8750-H, RAM: 16GB, 2667MHz SODIMM \
> PC 4 - CPU: AMD Ryzen 7 4700U, RAM: 16 GB, 3200MHz SODIMM

## Theoretisch optimum

Het is voor deze case lastig te bepalen wanneer het absolute optimum is gevonden. Daarom is het interessant om te kijken naar een theoretisch optimum. Dit geeft een idee van hoe veel kosten je minimaal moet maken en dus hoe goed een oplossing is.

Voor het theoretisch optimum doen we de volgende aannames:
- Er zijn altijd 5 batterijen en 150 huizen.
- Elk huis heeft minstens 1 kabel nodig om de connectie tussen de batterij en het huis te verwezenlijken.

Deze aannames is ver van de daadwerkelijke situatie voor de unieke kabels case. Hierbij zouden namelijk alle huizen op een afstand van 1 van een batterij moeten zitten, wat zou betekenen dat er heel veel huizen op dezelfde plek zouden moeten zitten. 

Voor de gedeelde kabels case is dit echter wel mogelijk. Hierbij is het namelijk mogelijk dat alle huizen op een sliert liggen, met 1 afstand tussen elk huis en 1 afstand naar een batterij.

Het theoretische optimum kan volgens de volgende formule worden berekend.

$$theoretisch\ optimum = kosten_{per\ batterij} \cdot n_{batterijen} + kosten_{per\ kabel} \cdot n_{kabels}$$

$$theoretisch\ optimum = 5000 \cdot 5 + 9 \cdot 150 = 26350$$

## Unieke kabels

De case uitleg van de unieke kabels kan worden gevonden in de [README](../README.md). Voor deze case hebben we drie algoritmen gemaakt, de resultaten waarvan hieronder gevonden kunnen worden. De manier waarop deze algoritmen werken kan [hier](algorithms.md) gevonden worden.

### Resultaten

| **Algoritme**                 | **Beste resultaat** | **Runtime (H:MM:SS)** | **Aantal runs** | **PC**   |
|-------------------------------|---------------------|-----------------------|-----------------|----------|
| random                        | 70225               | 0:04:11               | 100000          | PC 2     |
| greedy                        | 56905               | 0:03:54               | 100000          | PC 2     |
| steepest descent hill climber | 56266               | 0:10:46               | 1000            | PC 2     |

### Conclusie

Voor deze case nemen geen van de algoritmen heel veel tijd in beslag. De steepest descent hill climber geeft de beste oplossing, met slechts een cost van 56266. Iedere run van dit algoritme kost ongeveer 1 seconde. De random en greedy algoritmen kosten beide ongeveer evenveel tijd per run, maar het greedy algoritme geeft een veel beter resultaat, dus als snel redelijk goede oplossing gevonden moet worden, is het greedy algoritme aan te raden.

## Gedeelde kabels

Ook hier moeten de kosten zo laag mogelijk gehouden worden. In deze casus mogen de huizen kabels delen, zonder dat de kosten verhogen, zodat de totale kosten verlagen. Het is daarbij ook belangrijk dat kabels op de goede plekken worden gelegd, zodat zoveel mogelijk huizen zoveel mogelijk kabels delen, om de kosten te drukken. Op deze case hebben we zeven algoritmes losgelaten. De manier waarop deze algoritmen werken kan [hier](algorithms.md) gevonden worden.

### Plant Propagation Algorithm

Voor de Plant Propagation Algorithm (PPA) zijn er veel parameters die de effectiviteit van het algoritme sterk bepalen. De parameters worden hieronder gegeven. Meer informatie over het algoritme en de parameters is [hier](algorithms.md#plant-propagation-algorithm) te vinden.

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
- Fitness functie is [hier](algorithms.md#plant-propagation-algorithm) te vinden

Door een gebrek aan tijd is het algoritme niet geheel geoptimaliseerd. Zoals eerder vermeld is het algoritme niet heel snel en dus lastig om veranderingen op te maken en hier snel de resultaten van te zien. Daarnaast was de informatievoorziening online ook beperkt en niet makkelijk te begrijpen. Zo is later gebleken dat de fitness functie nog door een tangens hyperbolicus gehaald had kunnen worden, wat de resultaten zou moeten verbeteren. 

### Resultaten

| **Algoritme**                 | **Beste resultaat** | **Runtime (H:MM:SS)** | **Aantal runs**   | **PC**            |
|-------------------------------|---------------------|-----------------------|-------------------|-------------------|
| Baseline                      | 34306               | 7:44:00               | 100000            | PC 2              |
| Greedy                        | 30562               | 0:04:01               | 100000            | PC 2              |
| Hill climber                  | 30724               | 2:04:16               | 40                | PC 4              |
| Steepest descent hill climber | 31534               | 7:47:45               | 1                 | PC 1              |
| Simulated annealing           | 30220               | 6:13:40               | 50                | PC 1              |
| Plant propagation             | 31534               | 1:40:32               | 1 (227 generaties)| PC 3              |
| Greedy + hill climber         | 29752               | 4:05:32               | 108               | PC 4              |

### Conclusie

Voor deze case zitten er duidelijke verschillen tussen de tijd en daarmee ook het aantal runs van de algoritmes.  Er valt niet duidelijk een beste algoritme te noemen. Als de hoogste prioriteit ligt op de minimale kosten, lijkt de combinatie van de hill climber met een greedy algoritme het beste resultaat te geven, omdat het ongeveer 400 kosten scheelt in vergelijking met de volgende laagste score van simulated annealing. Als er relatief snel een goede oplossing gevonden moet worden, is greedy het beste algoritme, sinds het in een aantal minuten tot een prima oplossing komt, in tegen stelling tot de uren die andere algoritmes moet runnen.

## Batterijen verplaatsen

Het vervolg op de casus is dat batterijen verplaatst kunnen worden in het grid, om een nog goedkopere oplossing te kunnen vinden. Bij het verplaatsen van de batterijen, kan een configuratie worden gevonden waarbij er minder kabels intotaal nodig zijn om alle huizen te verbinden, dan bij de locaties van de batterijen die in de bestanden van district 1, 2 en 3 worden meegegeven. Om te zoeken naar betere configuraties van de batterijen, hebben we twee algoritmes geschreven. De eerste is een clustering algoritme en de tweede is een hill climber voor de batterijen. Uitleg voor deze algoritmes worden [hier](algorithms.md) toegelicht.

### Resultaten

| **Algoritme**             | **Beste resultaat** | **Runtime (H:MM:SS)** | **Aantal runs**                | **PC** |
|---------------------------|---------------------|-----------------------|--------------------------------|--------|
| Clustering                | 29923               | 0:00:20               | 10                             | PC 3   |
| Hill climber              |                     |                       |                                |        |
| Clustering + hill climber | 29563               | 8:30:56               | 10 clusters + 50 hill climbers | PC 3   |

### Conclusie

