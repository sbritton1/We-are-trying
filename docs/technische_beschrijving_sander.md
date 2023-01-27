# Technische Beschrijving Sander Britton

In dit document ga ik een plan uitwerken voor mijn individuele onderdeel van de Smart Grid case. Eerst ga ik een omschrijving geven mijn onderdeel. Vervolgens ga ik uitschrijven wat ik hiervoor nog moet doen. Als laatste bespreek ik hoe dit onderdeel in het geheel van het project past.

## Omschrijving

Als individueel onderdeel wil ik een Plant Propagation Algorithm maken. Dit algoritme zou gebruik moeten kunnen maken van verschillende hill-climber algoritmes om zo dus voor own-cables en shared-cables te werken. Hierin zou ik dus ook eventueel kunnen testen met verschillende types hill-climbers.

Als extra onderdeel wil ik het ook mogelijk maken om de JSON files te visualiseren in een grid, wat nu alleen mogelijk is na het runnen van een algoritme.

## Wat te doen

Hier bespreek ik wat ik per onderdeel moet doen.

### Plant Propagation Algorithm
In principe hoef ik alleen het Plant Propagation Algorithm te schrijven, omdat we al een steepest descent hill climber hebben die ik kan gebruiken. Deze hill climber zal ik waarschijnlijk wel nog een class van moeten maken.

Voor de Plant Propagation Algorithm ga ik een apart bestand aanmaken met hierin een soort 'main' functie die gebruikt kan worden om de algorithm te laten runnen. Deze grote functie zal ik onderdelen in meerdere kleine functies om het overzicht te behouden. 

### JSON Visualisatie
Voor de visualisatie van JSON bestanden zal ik een bestand aanmaken om de JSON files in te lezen en deze om te zetten naar een correct Grid object. Hiermee kan ik namelijk de bestaande visualisatie weer hergebruiken.

## Aansluiting project

De plant Propagation Algorithm zal gebruikt kunnen worden om een oplossing te vinden voor het probleem. Hier mee kunnen de anderen hun eigen algoritme vergelijken met die van mij en dus bepalen of hun algoritme waarschijnlijk beter kan of niet. 

De JSON visualisatie kan gebruikt worden om de resultaten van lange runs op te slaan in JSON formaat en deze vervolgens later te visualiseren. Dit maakt het makkelijker om tweaks te maken aan de visualisatie, zonder het programma opnieuw lang te laten runnen. 

## Uitvoering

In dit hoofdstuk zal ik gaan terugblikken op hoe de uitvoering van de eerder genoemde plannen is gegaan. Hierbij zal ik vooral ingaan op wat...

### Plant Propagation Algorithm
Voor de Plant Propagation Algorithm (PPA) is er het een en ander anders uitgepakt dan verwacht. Dit is vooral te danken aan het feit dat ik het algoritme niet duidelijk had begrepen. Zo dacht ik dat na het creëren van een nieuwe generatie er een 'x' aantal hill climber stappen zou worden gezet. Dit bleek echter niet het plan. Zo worden er nu alleen verbeteringen aangebracht door het creëren van nieuwe generaties. 

Iets anders wat ik verkeerd had geïnterpreteerd is het feit dat de parents niet zouden worden meegenomen in een nieuwe generatie, waardoor verslechtering mogelijk werd. Na de feedback op onze oefenpresentatie bleek dit anders te zijn en dus heb ik dit snel aangepast.

#### Evaluatie
Het maken van de PPA ging eigenlijk redelijk soepel. Het probleem zat hem vooral in het achterhalen wat de precieze bedoeling van het algoritme was. Als enige bron had ik het college van Bas Terwijn en het daarin genoemde paper. Dit paper was lastig te volgen. Toch geloof ik dat ik uiteindelijk een goede interpretatie van het algoritme heb gekregen. 

Het lastige aan dit algoritme is het bepalen van alle parameters, die de effectiviteit van het algoritme sterk bepalen. Zo kan je kiezen welke fitness-functie je gebruikt, om te bepalen hoe veel runners een root krijgt en de distance daarvan, maar ook het aantal overlevende roots, minimale en maximale aantal runners, minimale en maximale distance van deze runners en het aantal generaties. Hierin is dan ook nog veel ruimte voor optimalisatie, maar de gelimiteerde tijd heb ik mij hier niet volledig in kunnen storten.

Daarnaast geeft het algoritme ook geen geweldige resultaten. Dit komt denk ik voornamelijk door de manier waarop de distance van een runner wordt geïmplementeerd. De distance bepaalt namelijk hoe veel aanpassingen van connecties er worden gemaakt, waarbij een aanpassing inhoudt dat twee huizen van batterij wisselen, mits deze aanpassing nog een valide oplossing oplevert. Dit maakt het lastig voor het algoritme om precies de 'goede' aanpassingen te kunnen maken. De resultaten van het algoritme zijn dan ook niet beter dan ons greedy algoritme, die gebruik maakt van heuristieken.

#### Commits
Hier zal ik een overzicht geven van de commits die betrekking hebben op de PPA.

- [Main commit](https://github.com/sbritton1/We-are-trying/commit/63a20729fdb01661cd65c255c8d8b689a99617d9): Hierin heb ik eigenlijk bijna het hele algoritme geschreven.
- Kleine aanpassingen/toevoegingen:
  - [Functie opgesplitst](https://github.com/sbritton1/We-are-trying/commit/90f249c36c54a3002a7d81b4c155987ac20a465e): Het verkrijgen van de start roots heb ik hier in een aparte functie gezet.
  - [Flake8](https://github.com/sbritton1/We-are-trying/commit/d070019a702ae32675d6f84ebd7810986f77cb6a): Na het runnen van flake8 op plant_propagation.py heb ik de errors bijna allemaal weggekregen.
  - [Small changes](https://github.com/sbritton1/We-are-trying/commit/284bb4a4a888f31144402a0cb54ca2f533ceac3a): Hier heb ik wat missende type hints toegevoegd, aan flake8 gewerkt en er voor gezorgd dat het algoritme alleen print als de variable `print_stuff` True is.
  - [Aantal start roots apart tunable](https://github.com/sbritton1/We-are-trying/commit/b3e61d87c40d36be9bdd9f2e941202ec14454e1b): Ik heb er voor gezorgd dat het aantal start roots van een generatie niet meer afhankelijk was van het maximale aantal runners.
  - [Plot van results](https://github.com/sbritton1/We-are-trying/commit/9c1fb089da5ad42767c1e9b20daa3768f9eb584d): Toegevoegd dat als `plot_stuff` True is, dat er een plot wordt gemaakt met de beste root van elke generatie.
  - [Houden van parents bij een nieuwe generatie](https://github.com/sbritton1/We-are-trying/commit/618b1fcdc99b5ba879666b54b13fd12c70dd8703): Hierna werden de parents van een generatie ook meegenomen in het bepalen van de beste roots voor de volgende generatie.

## JSON Visualisatie
Voor de JSON visualisatie is er niet heel veel anders uitgepakt dan verwacht. Het enige wat echt anders is uitgepakt is het feit dat ik twee bestanden heb aangemaakt. Een soort 'main' file in de root folder van de repository en een file in de /code/visualization die de daadwerkelijke functies heeft.

Ook heb ik nog het een en ander moeten aanpassen en/of toevoegen bij de grid, house en battery classes om alles werkend te krijgen. Zo had ik nog een aantal methods nodig om bepaalde eigenschappen gelijk toe te kennen aan de objecten, in plaats van ze deze zelf uit te laten vogelen. Daarnaast moest ik in de grid class een extra variabele toe te voegen om aan te geven dat je de grid niet uit een csv bestand wilde laden.

### Evaluatie
Zoals hiervoor vermeld is er niet veel anders uitgepakt dan verwacht en werkt het programma dan ook naar behoren. Het is mogelijk om de eerder geprogrammeerde visualisatie te hergebruiken met JSON bestanden, wat qua modulariteit erg handig is. Zo heb ik nu met het advanced gedeelte ook redelijk makkelijk kunnen toevoegen dat er ook andere batterijen kunnen worden gevisualiseerd. 

Het later kunnen visualiseren van JSON bestanden is vaak nog erg handig gebleken, omdat we niet elke keer naast het JSON bestand ook nog de visualisatie moesten opslaan als we een run hadden gedaan. Nu kunnen we ook makkelijk de visualisatie aanpassen en alsnog de grids opnieuw genereren.

### Commits
Hier zal ik een overzicht geven van de commits die betrekking hebben op de JSON visualisatie.

- [Main commit](https://github.com/sbritton1/We-are-trying/commit/e6597a886105e782ee3806d7502bf23f7c81e396): Hier heb ik vrijwel het hele programma geschreven.
- Kleine aanpassingen/toevoegingen:
  - [Documentatie + opschonen](https://github.com/sbritton1/We-are-trying/commit/c3ac3298281f5ecad5223db3d632ed408b902901): Docstrings aan de functies en methods toegevoegd en code opgeschoond.
