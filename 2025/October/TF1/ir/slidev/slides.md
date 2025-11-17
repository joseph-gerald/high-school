---
# try also 'default' to start simple
theme: seriph
# random image from a curated Unsplash collection by Anthony
# like them? see https://unsplash.com/collections/94734566/slidev
background: https://images.unsplash.com/photo-1617634840550-76e978d59093?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1170
title: Welcome to Slidev
info: |
  ## Slidev Starter Template
  Presentation slides for developers.

  Learn more at [Sli.dev](https://sli.dev)
# apply UnoCSS classes to the current slide
class: text-center
# https://sli.dev/features/drawing
drawings:
  persist: false
# slide transition: https://sli.dev/guide/animations.html#slide-transitions
transition: slide-left
# enable MDC Syntax: https://sli.dev/features/mdc
mdc: true
---

# Infrarøde Avstandssensor

Av Joseph og Philip

<!--
The last comment block of each slide will be treated as slide notes. It will be visible and editable in Presenter Mode along with the slide. [Read more in the docs](https://sli.dev/guide/syntax.html#notes)
-->

---
transition: fade-out
---

# Hva er en infrarød avstandssensor og hvordan funker den

(IR avstandssensoren oftest brukt i små elektronikkprosjekter Trianguleringssensorer)
-  **Måler avstand** 

-  **Ifrarøde lys** 

-  **Refleksjon** 

-  **Konvertering til analog** 

-  **Spenning fått fra vinkelen av PSD** 
<!--
You can have `style` tag in markdown to override the style for the current page.
Learn more: https://sli.dev/features/slide-scope-style
-->

<style>
h1 {
  background-color: #2B90B6;
  background-image: linear-gradient(45deg, #4EC5D4 10%, #146b8c 20%);
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
level: 2
---

# IR avstandssensor brukt i større prosjekter


## Forskjell (IR avstandssensor (Trianguleringssensor) vs Tid)

|                                                     |                             |
| --------------------------------------------------- | --------------------------- |
| <kbd>Måler avstand med spenning fra vinkelen</kbd>                | Måler tiden brukt til lyset reflekterer tilbake     |
| <kbd>Nøyaktig korte avstander, ikke lange</kbd> | Veldig nøyaktig både store og små distanser|
| <kbd>Billig, simpel</kbd>                                       | Dyr og avansert              |
| <kbd>Påvirkes av mørke farger eller glass</kbd>                                     | Mindre påvirket av farge og lys |

<!--
https://sli.dev/guide/animations.html#click-animation
-->

---
transition: slide-right
level: 2
---

# Signaltypen

![](https://i.ytimg.com/vi/I1AhW6_HQpI/maxresdefault.jpg)

<!--
Gir sensoren fra seg et analogt eller digitalt signal? 

Forklar hvorfor det er enten analogt eller digitalt. Hva betyr det i praksis for denne sensoren?
-->

---
layout: iframe
url: http://127.0.0.1:5500/embeds/ir.html
---

# Signaltypen



---
layout: image-right
image: https://cover.sli.dev
---

# Generelt om signal

Use code snippets and get the highlighting directly, and even types hover!

<!--
Notes can also sync with clicks

[click] This will be highlighted after the first click

[click] Highlighted with `count = ref(0)`

[click:3] Last click (skip two clicks)
-->

---
level: 2
---

# Praktiske bruksområder 
<br/> 

- Robotikk - For eksempel i lego league

<br/> 


- Bilkjøring - Forparkeringsassistanse eller blindsoneovervåking.

<br/> 


- Droner - For å unngå kollisjoner under landing eller under flyging i områder med mange hindringer

---
theme: default
---

# Oppsumering

<iframe src="https://pokernow.club"></iframe>
