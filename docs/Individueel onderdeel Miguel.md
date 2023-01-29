## Omschrijving

Voor het individuele onderdeel ga ik een simulated annealing algoritme maken, die optimaliseert op het probleem waarbij kabels gedeeld kunnen worden. simulated annealing is een versie van hill climber, waar in het begin het algoritme een verslechtering van de cost mag accepteren, in de hoop dat je hiermee eindigt in een lager locaal minimum. Naarmate de runtime afneemt zal het algoritme steeds minder een verslechtering accepteren.

## Nog te schrijven functies/classes

Voor dit onderdeel hoeven er geen nieuwe classes geschreven te worden. Qua functies heb ik er allereerst eentje nodig die huizen random aan batterijen verbindt, maar deze heb ik al geschreven voor de sd_hill_climber.py, dus deze kan rechtstreeks gekopiëerd worden. Vervolgens heb ik een functie nodig die daadwerkelijk het algoritme uitvoert. Hoe deze dit gaat doen is door constant een willekeurige swap te maken, en te kijken hoe deze de cost beinvloed. Vervolgens bereken je op basis van de "temperatuur" de kans dat deze verandering geaccepteerd wordt. Als je dit algoritme genoeg iteraties geeft, zullen er langzaam maar zeker geen verbeteringen meer zijn.

Ik wil ook een plot maken, die de cost van het grid plot ten opzichte van de iteratie waarop het programma zit. Als het goed is zie je dan in het begin een sterke daling van de cost, en uiteindelijk levelt deze uit.

## Experimenteel deel

Ik kan vervolgens ook testen of het algoritme een beter antwoord krijg als ik hem vraag om meerdere veranderingen te laten maken per stap, die geaccepteerd kunnen worden. Ook wil ik kijken hoe het resultaat verschilt wanneer ik de begintemperatuur, of de curve van de temperatuur aanpas.

## Aansluiting

Het programma sluit aan op het werk van de rest van het groep, doordat het één van de algoritmen is die een zo goed mogelijk antwoord probeert te zoeken voor onze casus. Het maakt natuurlijk gebruik van de reeds gecreëerde classes en de visualisatie, opdat je van het resultaat kan zien hoe goed de oplossing er intuitief uitziet. Natuurlijk kunnen de oplossingen van dit algoritme ook gebruikt worden om onze andere algoritmen mee te vergelijken, om te kijken hoe effectief ze onderling zijn

## Gedeeltes anders dan verwacht

Voor de temperatuur functie had ik origineel bedacht dat de temperatuur met een factor tot de macht van de iteratie zou verlagen. Bijvoorbeeld T = 500 * (0.997 ^ iteratie). Echter na de oefenpresentatie werd ons aangeraden om voor de temperatuur functie te zorgen dat de nieuwe oplossing nooit 10% slechter kan zijn dan de oplossing waar we mee begonnen. Ook werd opgemerkt dat met deze temperatuur functie, je na ongeveer 1800 iteraties gewoon een hill climber over hield. Om deze reden heb ik ervoor gezorgd dat bij iedere duizendste iteratie, de temperatuur wat omhoog wordt gebumpt, in de hoop dat de oplossing in een lager locaal minimum terecht komt.

## Links naar commits

https://github.com/sbritton1/We-are-trying/commit/a1b96d0e247985c5470a3f1e1973179a5170f33c:
Algoritme voor het grootste gedeelte werkend gemaakt

https://github.com/sbritton1/We-are-trying/commit/ab6b80b0edd19a0409b5522f557a6f2aef306c09:
Algoritme paar keer gerunt

https://github.com/sbritton1/We-are-trying/commit/d2d09914c55e3b72716ce3679069f15c4af1daa0:
Plot toegevoegd van cost over tijd

https://github.com/sbritton1/We-are-trying/commit/5836e67ddcc065f376d46fa4450e475fdbfa1b3f:
Plot verbeterd met titels etc

https://github.com/sbritton1/We-are-trying/commit/c97054257135b2b257e3736da773e1c089717d12:
Multiprocessing toegevoegd, om runtime veel te verlagen

https://github.com/sbritton1/We-are-trying/commit/1949effc774a0a76a7f4531091f5ac8c0be222c9:
Testen met temperatuurfunctie

https://github.com/sbritton1/We-are-trying/commit/ec824c08c726f0818d67d5cece31ed1eeec35413:
Aparte helperfuncties gemaakt van sommige functionaliteiten, die in meer algoritmes gebruikt worden

https://github.com/sbritton1/We-are-trying/commit/a190baec72cdac6a33b94cb3b77f22a6c1c78d00:
Vaker algoritme gerunt en temperatuursfunctie terug aangepast

https://github.com/sbritton1/We-are-trying/commit/3ccc9e6bdaab32483f0ecb2c7538bb4d54e32e62:
Comments en docstrings toegevoegd

https://github.com/sbritton1/We-are-trying/commit/9a92f954d90883ae6cb794ccd963529368be797a:
Comments en docstrings verbeterd

https://github.com/sbritton1/We-are-trying/commit/319bb890f56a30e5fb08db6d2719a433a7451c25: 
Meer helperfuncties gemaakt, zodat de .py bestanden van de algoritmes kleiner zijn en herhaling wordt voorkomen

https://github.com/sbritton1/We-are-trying/commit/4a24147a46c6765cdcd6aff1cf0a396fd20feed3: 
Met behulp van flake8 de stijl verbeterd

https://github.com/sbritton1/We-are-trying/commit/7ecce77922d533cde0ebc99d629926d8441431fc: 
Grote test gerund, dus aangepast hoevaak het algoritme een grid probeert te verbeteren

https://github.com/sbritton1/We-are-trying/commit/b7a6067d8c333d6b005064f63862cba8cfcbe852: 
Simulated annealing uitgetest met greedy oplossing als beginpunt in plaats van random beginpunt

https://github.com/sbritton1/We-are-trying/commit/0b4dada880b9235bf139c7f12fa448182b04d93a:
Betere temperatuursfunctie uitproberen

https://github.com/sbritton1/We-are-trying/commit/bad0ed0b36afeab5e57cc5ed69eafcedc7b5cce9:
Nieuwe temperatuursfunctie gebruikt die goed lijkt te werken, ook snelheid verbeterd door het algoritme minder onnodige dingen te laten doen

https://github.com/sbritton1/We-are-trying/commit/560871b42ea7422eaeefdf4f6306f926271d3502:
Grote test met random starting grid
