---
# You can also start simply with 'default'
theme: seriph
# random image from a curated Unsplash collection by Anthony
# like them? see https://unsplash.com/collections/94734566/slidev
background: https://up.pumping.lol/1625
# some information about your slides (markdown enabled)
title: Welcome to Slidev
info: |
  ## Slidev Starter Template
  Presentation slides for developers.

  Learn more at [Sli.dev](https://sli.dev)
# apply unocss classes to the current slide
class: text-center
colorSchema: light
# https://sli.dev/features/drawing
drawings:
  persist: false
# slide transition: https://sli.dev/guide/animations.html#slide-transitions
transition: slide-left
# enable MDC Syntax: https://sli.dev/features/mdc
mdc: true

# open graph
# seoMeta:
#  ogImage: https://cover.sli.dev
---

# CO2-utslipp i Norge

Av Jo

<!--
The last comment block of each slide will be treated as slide notes. It will be visible and editable in Presenter Mode along with the slide. [Read more in the docs](https://sli.dev/guide/syntax.html#notes)
-->

---
transition: fade-out
---

<img src="https://ektedata.uib.no/wp-content/uploads/sites/5/2016/11/atmosf%C3%A6risk_co2.png">

<!--
You can have `style` tag in markdown to override the style for the current page.
Learn more: https://sli.dev/features/slide-scope-style
-->

<style>
h1 {
  background-color: #2B90B6;
  background-image: linear-gradient(215deg, #4EC5D4 10%, #146b8c 20%);
  background-size: 100%;
  -webkit-background-clip: text;
  -moz-background-clip: text;
  -webkit-text-fill-color: transparent;
  -moz-text-fill-color: transparent;
}
</style>

<!--
Here is another comment.
-->

---
transition: slide-up

---

# Oppgave A

<div>
<br>

Gå først inn på nettsiden [www.globalcarbonatlas.org/en/CO2-emissions](http://www.globalcarbonatlas.org/en/CO2-emissions) og velg unit «MtCO2».



<p v-click>
Hvor stort var Norges totale CO2 utslipp i 2017?
</p>

</div>

---
transition: slide-down
layout: default
---

# Koden

```py {all|1-3|7-8|9|all}{maxHeight:'410px'} twoslash
import csv
import numpy as np
import matplotlib.pyplot as plt

data = {}
countries = []
  
with open("export_emissions_global.csv", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    total_lines = len(f.readlines())

    f.seek(0)

    for index, line in enumerate(reader):
        if index == 0 or (total_lines - index < 4):
            continue

        year = None

        for item_index, item in enumerate(line):
            if (index == 1):
                if (item_index == 0): continue
                countries.append(item)
                data[item] = {}
            else:
                if (item_index == 0):
                    year = item
                else:
                    data[countries[item_index - 1]][year] = item
```

<arrow v-click="[3, 4]" x1="650" y1="350" x2="465" y2="294" color="#000" width="2" arrowSize="1" />

<style>
.footnotes-sep {
  @apply mt-5 opacity-10;
}
.footnotes {
  @apply text-sm opacity-75;
}
.footnote-backref {
  display: none;
}
</style>

<!--
Notes can also sync with clicks

[click] This will be highlighted after the first click

[click] Highlighted with `count = ref(0)`

[click:3] Last click (skip two clicks)
-->

---
transition: fade

---

# Oppgave A

<div>
<br>

Gå først inn på nettsiden [www.globalcarbonatlas.org/en/CO2-emissions](http://www.globalcarbonatlas.org/en/CO2-emissions) og velg unit «MtCO2».

<p>
Hvor stort var Norges totale CO2 utslipp i 2017?
</p>

<div v-click>

```py
>>> data["Norway"]["2017"]
'44.165'
```
</div>

<p v-click>
Hvilke 3 land har de største CO2-utslippene i verden og hvilken rangering har Norge i total CO2 utslipp?
</p>

<div v-click>

```python {*}
countries_2017_emissions = []

for country in countries:
    if (data[country]["2017"] == ""):
        continue

    countries_2017_emissions.append((country, float(data[country]["2017"])))

countries_2017_emissions.sort(key=lambda x: x[1], reverse=True)
```
</div>

</div>

---
transition: slide-up

---

# Oppgave A

<div>
<br>

<p>
Hvilke 3 land har de største CO2-utslippene i verden og hvilken rangering har Norge i total CO2 utslipp?
</p>

<div>

```python {*}
>>> countries_2017_emissions
[
    ('China', 10006.343),
    ('United States of America', 5212.1623),
    ('India', 2426.6069),
    ('Russian Federation', 1666.1212),
    ('Japan', 1187.4845),
    ...
    ('Montserrat', 0.029312),
    ('Wallis and Futuna Islands', 0.025648),
    ('Saint Helena', 0.010992),
    ('Tuvalu', 0.010992),
    ('Niue', 0.007328)
]
```
</div>

</div>


---
transition: fade

---

# Oppgave B

<div>
<br>

På samme websiden som i oppgave **a)** velg å unit «tCO2/person». Dette viser hvor stort CO2-utslipp de forskjellige landene har per person.


<p v-click>
Hvilke land har nå de høyeste utslippene? Forklar hvorfor dene rangereringen er så annerledes enn i oppgave a).
</p>

<div v-click>
```py
[
    ('Qatar', 36.91753127),
    ('Curaçao', 28.96620881),
    ('Trinidad and Tobago', 27.26762419),
    ('Kuwait', 25.20063497),
    ('United Arab Emirates', 23.47885424),
    ...
    ('Malawi', 0.068770679),
    ('Burundi', 0.045982316),
    ('Central African Republic', 0.0432642),
    ('Somalia', 0.042890912),
    ('Democratic Republic of the Congo', 0.034610663)
]
```
</div>


</div>

<!--
Vi ser i rangeringen per capita er veldig forskjellig fra de tidligere, top 5 landene i denne rangeringen er land med små befolkninger på toppen. Den tidligere rangeringen hadde store industri land som Kina, USA og India som har store befolkninger og store industrier som resulterer i et så stort utslipp. Den store befolkningen er grunnen til at de ikke kommer opp på den andre rangeringen fordi utslippet er delt på befolkningen. Den små befolkningen er ikke det eneste men de er også høy karbon utslipp land, f.eks. Qatar, Kuwait og UAE er olje land. Hvis vi ser på landene på bunden av denne rangeringen så ser vi bare Afrikanske land og dette kan lett bli forklart med lite infrastruktur og dermed lite technology og industri som utslipper karbon og en høy populasjon.
-->


---
transition: slide-up

---

# Oppgave B

<div>
<br>

<p>
Forklar også hvordan Norge sin rangering har endret seg. Hvordan er Norge sine CO2 utslipp sammenlignet med det globale gjennomsnittet?
</p>

```py
for index, item in enumerate(countries_2017_emissions):
    if (item[0] == "Norway"):
        print("Norway index: ", index)
        break

mean = np.mean([x[1] for x in per_capita_2017_emissions])
print("Mean: ", mean)
```
```py
L1: Norway: 8.368716972
L2: Mean: 4.879282147882629
```

</div>

<!--
Vi ser Norge sin rangering gå fra `#63` til `#39` dette viser at når vi ikke bare tar utslippet av Norge til hensyn men også befolkningen til så gjør Norge den drastisk verre. Dette er kan forklares med den små befolkningen, høy personlig strømbruk og industri (olje, etc).


Vi endrer litt på koden fra og bare bytter den fra å logge indeksen/rangering av Norge til å logge verdien ved å søke opp indeksen i den sorterte listen vår og hente den verdien ved å hente det andre elementet (format: `navn,verdi`). Vi ser at for hver person i Norge er det utslipp på `8.37` tonn CO2 i forhold til det globale gjennomsnittet som var `4.88`tonn C02 per person.
-->


---
transition: fade

---

# Oppgave C

<div>
<br>

Figur 2 viser CO2-utslipp i Norge fra alle innenlandskilder fra 1990 til 2017. Les av grafen for å finne de totale utslippene i år 1990 og i år 2017.

<img width="60%" src="https://ektedata.uib.no/wp-content/uploads/sites/5/2016/11/co2_norway-offshore-768x455.png">
</div>

---
transition: fade

---

# Oppgave C

<div>
<br>

Figur 2 viser CO2-utslipp i Norge fra alle innenlandskilder fra 1990 til 2017. Les av grafen for å finne de totale utslippene i år 1990 og i år 2017.

```python
norway_emissions = 0

for year in range(1990, 2018):
    norway_emissions -= float(data["Norway"][str(year)])

print("Norway 1990-2017 emissions:", norway_emissions)
```
```py
L1: Norway 1990-2017 emissions: 1177.815
```

Totalt utslipp av `252.64` millioner tonn $CO_2$ mellom `1990` og `2017`.
</div>


---
transition: slide-up

---

# Oppgave C

<div>
<br>

Hvor stor er i økningen og hva tilsvarer dette i prosentvis økning?

```python
delta = norway_emissions[2017] - norway_emissions[1990]
delta_percentage = delta / norway_emissions[1990] * 100

print("delta  : ", delta)
print("delta %: ", delta_percentage)
```
```py
L1: delta  : 9.161999999999999
L2: delta %: 26.174899294346194
```

Vi har en økning av `9.16` millioner tonn $CO_2$ mellom `1990` og `2017`, dette er en økning av `26.17` prosent fra `1990`.

</div>



---
transition: slide-left

---

# Oppgave D

<div>
<br>

Last nå ned datasettet med årlig CO2 utslipp i Norge fra 1960-2017: [co2_norway](https://ektedata.uib.no/wp-content/uploads/sites/5/2016/11/co2_norway.txt)

Kopier tallverdiene inn i regnearket i Geogebra og lag en liste med punkter.

La x-aksen være år (tid) og y-aksen CO2-nivået.

</div>

---
layout: image
image: https://up.pumping.lol/950a
transition: slide-up

backgroundSize: contain
---

<div class="bg-black bg-opacity-50 px-5 py-0.5 rounded-sm backdrop-blur-sm absolute bottom-20 right-0 text-right">

Forklar utviklingen av av CO2 med ord. Hva ser du?<br>
Kan du se noen spesielle endringer eller mønstre?<br>
Er det noen tidsperioder som skiller seg ut?

</div>

<!--
Vi ser kraftig økning fra 1960-1975 hvor utslippene nesten trippler, veksten bremser og vi ser at det blir ganske flat mellom 1975-1990, fra 1990-2005 så vokser det igjen fra rundt 35Mt til 45mt hvor den deretter bremser igjen og faktisk begynner nedgang som vi flytter til fornybar strøm og elektriske biler, etc.
-->

---
transition: slide-left
---

# Oppgave E

<br>

Vi ønsker nå å finne en enkel modell som beskriver datapunktene våre.

Bruk regresjonsverktøyet i Geogebra til finne både en lineær funksjon og en andregradsfunksjon som passer bra til CO2-verdiene.

Hva er utrykkene til funksjonene og hvilken synes du er mest realistisk?

---
transition: slide-left
---

```py {all}{maxHeight:'460px'}
from matplotlib import pyplot as plt
import numpy as np

data = np.loadtxt("co2_norway.txt", delimiter=",")

x = data[:, 0]
y = data[:, 1]

linear_fit = np.polyfit(x, y, 1)
polynomial_fit = np.polyfit(x, y, 2)

def polynomial_function(x):
    return polynomial_fit[0] * x**2 + polynomial_fit[1] * x + polynomial_fit[2]

def linear_function(x):
    return linear_fit[0] * x + linear_fit[1]

def plot_data():    
    plt.scatter(x, y, c="black", s=10)

    plt.xlabel("Time (Year)")
    plt.ylabel("MtCO2")
    plt.legend()

    plt.show()

plt.plot(x, linear_function(x), color="red", label="Linear Fit")
plot_data()

plt.plot(x, polynomial_function(x), color="red", label="Polynom Fit")
plot_data()
```

---
transition: slide-up
---

|Lineær|Andregradsfunksjon|
|----|----|
|<img width="100%" src="https://up.pumping.lol/a73f">|<img width="100%" src="https://up.pumping.lol/6f9d">|
|$f(x) = 0.5634x - 1085.9435$|$f(x) = -0.01x^2 + 37.31x - 37608.90$|

<!--
*husk: bruker 2dp på for lettere lesing av numre*

Andregrads funksjonen er mye mer realistisk, den viser at trenden bremser og snur seg rundt og det er mye mer realistisk til dataen i forhold til en den lineær modellen som kun går oppover.

Vi kan prøve det samme i python og sjekke om vi får det samme:
-->

---
transition: slide-left
---

# Oppgave F
<br>
Hvordan tror du funksjonsutrykkene i oppgave E passer utenfor vårt definisjonsområde, altså før 1960 og etter 2017?
<br>
<br>

```py
x_extended = np.arange(1940, 2100)

y_linear_extended = linear_function(x_extended, linear_fit)
y_polynomial_extended = polynomial_function(x_extended, polynomial_fit)

plt.plot(x_fit, y_linear_fit, color="red", linestyle="-", label="Linear Fit")
plt.plot(x_fit, y_polynomial_fit, color="blue", linestyle="--", label="Polynomial Fit")
```
 
---
transition: slide-up
layout: image
image: https://up.pumping.lol/bd50
backgroundSize: contain
---

<!--
Den lineære modellen er helt av på trenden på starten og slutten av dataen imens andregrads funksjonen følger den mye nærmere og ser ut som den hadde vært nøyaktig (accurate?) til mengder utenfor det vi ga til GeoGebra.
-->

---
transition: fade
---

# Oppgave G
<br>

Vi kan bruke derivasjon til å lære noe om en graf og hvordan den endrer seg.

Deriver andregradsfunksjonen i forrige oppgave først for hand og kontroler deretter svaret ved å bruke derivasjonsverktøyet i Geogebra.

<br>

$$ {0|1|2|3}
\begin{aligned}
f(x) = -0.01x^2 + 37.31x - 37608.90\\
f(x) = 2*-0.01x + 37.31\\
f(x) = -0.02x + 37.31\\
\end{aligned}
$$

---
transition: fade
---

# Oppgave G
<br>

Vi kan bruke derivasjon til å lære noe om en graf og hvordan den endrer seg.

Deriver andregradsfunksjonen i forrige oppgave først for hand og kontroler deretter svaret ved å bruke derivasjonsverktøyet i Geogebra.

<br>

```py
derivative = np.polyder(polynomial_fit)
print(derivative)
```
```py
L1: [-1.84839590e-02  3.73094674e+01]
```

<br>

**raw** $[-0.018483959, 37.3094674]$

**2dp** 
$[-0.02, 37.31]$

---
transition: slide-up
---

# Oppgave G

<br>

Når begynner $CO_2$ utslippene å avtale i følge funksjonen din?

<br>

```py
extremum = np.roots(derivative)
print(extremum)
```
```py
L1: [2018.47814663]
```

Andregradsfunksjonen sier at $CO_2$ utslippene begynte å minske rundt midten av  `2018`.

---
transition: slide-up
---

# Oppgave H

<br>

Bruk derivasjon til å regne ut stigningen til grafen i årene 1970, 1990 og 2010. Hva er den fysiske forklaringen og enheten til stigningstallet? Beksriv hva stigningstallet forteller oss med egne ord.

<br>

```py
gradient_1970 = np.polyval(derivative, 1970)
gradient_1990 = np.polyval(derivative, 1990)
gradient_2010 = np.polyval(derivative, 2010)

print("Gradient in 1970: ", gradient_1970)
print("Gradient in 1990: ", gradient_1990)
print("Gradient in 2010: ", gradient_2010)
```
```py
L1: Gradient in 1970:  0.8960680770424929
L2: Gradient in 1990:  0.5263888960439544
L3: Gradient in 2010:  0.15670971504540887
```
<br>

<div v-click class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-black bg-opacity-50 text-white p-3 backdrop-blur-sm rounded-md text-xs">

> Hva er den fysiske forklaringen og enheten til stigningstallet?

<br>

> Beksriv hva stigningstallet forteller oss med egne ord.
</div>

<!--
Stigningstallet representerer endringshastigheten i CO2 utslipp i et tidspunkt. Dette forteller oss hvor raskt utslippet øker eller minker. Det er målt i millioner tonn CO2 per år. Så hvis stignigstallet er positivt så  øker utslippene, mens et negativt stigningstall betyr at utslippene avtar.

Vi ser et stigningstall på `0.9` i `1970` dette forteller oss at det var massiv vekst fra året før, når vi kommer til `1990` så ser vi at veksten bremser og `2010` viser at vi nærmer oss en reversering.
-->


---
transition: slide-up
---

# Oppgave I

<br>

Hvis du skulle beskrive utviklingen av CO2-utslipp i Norge mellom 1960 og 1970 ved en lineær linje. Hva ville funksjonsuttrykket til denne rette linjen være? Og hva med perioden 2010-2017? Hva forteller disse funksjonsutrykkene deg?

<br>


**1960-1970:**
$$
f(x) = 1.3021x - 2540.6089
$$

**2010-2017:**
$$
f(x) = 0.0828x - 121.7406
$$

<!--
Linjeære funksjoner er f(x) = ax + b hvor a er stignigstallet, vi ser at mellom `1960-1970` så er stignigstallet `1.3021` imens mellom `2010-2017` er det `0.0828`, dette er mer en 15 ganger mindre en `1960-1970`. Dette forteller oss at vi har bremset industrilisering for å utvikle og adoptere fornybar teknologi og energi.
-->



---
transition: slide-up
---

# Oppgave J

Vil vi bruke en enkel modell slik vi fant i oppgave E til å si noe om hvordan utslipp av CO2 kan se ut i fremtiden. Tror du en slik tilnærming er realistisk? Hvorfor eller hvorfor ikke?

|Lineær|Andregradsfunksjon|
|----|----|
|<img width="100%" src="https://up.pumping.lol/a73f">|<img width="100%" src="https://up.pumping.lol/6f9d">|
|$f(x) = 0.5634x - 1085.9435$|$f(x) = -0.01x^2 + 37.31x - 37608.90$|


<!--
Jeg tror at en andregrads funksjon er ganske realistisk fordi som et land industrialiserer og raskt blir mer teknologisk ved bruk av brennstoff fordi det er: raskt og billig. Som land blir mer teknologiske så begynner de å adoptere andre kilder av energi, f.eks. sol, kjerne og hydro i Norge. Dette betyr at for en periode av tid så må et land bruke brennstoff for å holde følge med energi kravene. Den lineære modellen er urealistisk fordi å forsette med å adoptere og bruke brennstoff er urealistisk fordi det er bare en midlertidig/mellomliggende kilde av energi for en sivilisasjon.
-->

---
transition: slide-up
---

# Oppgave K

<br>

Hvis vi antar at utviklingen av utslipp følger mønsteret som er beskrevet av andregradpolynomet du fant i oppgave E, når vil Norge sine utslipp av CO2 bli lik null? Tror du svaret ditt er realistisk?

```py
roots = np.roots(polynomial_fit)
print("Roots of the polynomial function: ", roots)
```
```py
L1: Roots of the polynomial function:  [2088.46989883 1948.48639442]
```

---
transition: slide-up
---

# Oppgave I

<br>

Figur 3 viser hvordan hvordan utslippene i Norge er fordelt på ulike sektorer i samfunnet. Kan du tenke på tiltak som kan gjøres i Norge for å begrense og minske CO2 utslippene? Hvor må Norge gjøre størst grep om vi skal klare å snu trenden i CO2-utslipp?