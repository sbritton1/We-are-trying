# Experimenteren

In dit document bespreken we hoe we hebben geëxperimenteerd en resultaten hebben verzameld. Ten eerste bespreken we dit voor de case met unieke kabels, dan met gedeelde kabels en dan met het verplaatsen van batterijen.

## Methode

METHODE BESPREKEN

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

227 generaties gerund met beste cost 31534. 
n_roots = 8
    min_runners = 2
    max_runners = 6
    min_changes = 1
    max_changes = 8
    n_generations = 300
    max_times_no_improvement = 20

### Resultaten

| **Algoritme**                 | **Beste resultaat** | **Runtime (H:MM:SS)** | **Aantal runs** | **PC**        |
|-------------------------------|---------------------|-----------------------|-----------------|---------------|
| Baseline                      | 34306               | 7:44:00               | 100000          | i7-9750H      |
| Greedy                        | 30562               | 0:04:01               | 100000          | i7-9750H      |
| Hill climber                  | 30724               | 2:04:16               | 40              | Xander laptop |
| Steepest descent hill climber | 31534               | 7:47:45               | 1               | i5-12400F     |
| Simulated annealing           | 30220               | 6:13:40               | 50              | i5-12400F     |
| Plant propagation             | 31534               | 1:40:32               | 1               | Sander laptop |
| Greedy + hill climber         | 29752               | 1:32:00               | 24              | Xander laptop |
| Greedy + hill climber 2.0     | 29905               | 1:01:23???            | 108             | Xander laptop |

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