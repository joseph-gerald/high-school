---
# try also 'default' to start simple
theme: seriph
# random image from a curated Unsplash collection by Anthony
# like them? see https://unsplash.com/collections/94734566/slidev
background: https://images.unsplash.com/photo-1760159201329-521cd85a5bf9?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=2070
# some information about your slides (markdown enabled)
title: TREX GAME
info: |
  ## Slidev Starter Template
  Ac

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

# T-Rex Game

Input gjennom en trådløs integrasjon av akselerometerdata.

<!--
The last comment block of each slide will be treated as slide notes. It will be visible and editable in Presenter Mode along with the slide. [Read more in the docs](https://sli.dev/guide/syntax.html#notes)
-->

---
transition: slide-down
---

# Opprinnelige Ideen (pitch)
<br>

- Spill - Lage noe gøy

<br>
<br>
<br>


- Ikke overkomplisert - Prosjekt innenfor vårt nivå

<br>
<br>
<br>

- Gøy prosjekt - Noe som er gøy å lage

<br>
<br>


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
Først ville vi lage en bil eller en drone, men etter vi fant ut tidsmangelen bestemte vi oss på et mer realistisk prosjekt som også var gøy. Vi fikk også litt feedback om prosjekt ideen av pål som sa at det var et bra første prosjekt å lage vårt design. ​
-->

---
transition: slide-up
level: 2
---

# Byggeprosessen​

|                                                     |                             |
| --------------------------------------------------- | --------------------------- |
| <kbd>Problemer med 3d printing</kbd>                  | Feil målinger|
| <kbd>Problem med lodding</kbd>   | ødeleggelse av accelerometer|
| <kbd>Problem med kode</kbd>                                       | Neste slide|

<img src="https://up.jooo.tech/a9c2" class="max-h-48">

<!--
Vi begynte prosjektet ved å lage et prosjekt på tinkercad som skulle ha riktige målinger slik at arduinonen vår kunne passe inni I tillegg til å festes til buksen slik at produktet vårt kunne brukes uten å holdes fysisk. Etter 3d printingen var ferdig møtte vi på problemet som var at breadboardet var større enn vi hadde kalkulert for, så bare arduinoet passet. Et annet problem gjaldt circuiten vår som brukte en acccelerometer som ikke hadde blitt loddet riktig som gjorde at den ikke funket. Vi fikk en ny en og prøvde å lodde den riktig men klarte å gjøre at loddetinnet traff flere pins på accelerometeren og funka ikke igjen. På det tredje forsøket gjorde vi mer research på selve loddingen og fikk den endelig til å funke. ​
-->

---
image: https://cover.sli.dev
---

# Problemer med koden​

Gjennom prosjektet


````md magic-move {lines: true}
```cpp {*|1-3|6-8|11-12}
#include <WiFiS3.h>      // Manages the WiFi module on the R4
#include <WiFiClient.h>  // Use standard client for unencrypted HTTP connections
#include <Wire.h>        // For I2C communication with MPU6050

// --- WiFi Credentials ---
char ssid[] = "YOUR_WIFI_SSID";
char pass[] = "YOUR_WIFI_PASSWORD";
int status = WL_IDLE_STATUS;

// --- Server Details (UPDATED) ---
const char server[] = "10.18.8.252"; // Your server's local IP address
const int port = 3000;               // Your server's port
```

```cpp
void sendServerRequest(const char* path) {
  // Use client.connect() with the IP address and port
  if (client.connect(server, port)) {
    Serial.print("Requesting path: ");
    Serial.println(path);
    
    // Make an HTTP GET request.
    client.print("GET ");
    client.print(path);
    client.println(" HTTP/1.1");
    client.print("Host: "); // The Host header is part of the HTTP standard
    client.print(server);
    client.print(":");
    client.println(port);
    client.println("Connection: close");
    client.println(); // End of headers
  } else {
    // If the connection fails, print an error.
    // Check that the Arduino is on the same WiFi network as the server!
    Serial.println("Connection to server failed!");
  }
```

```cpp
void holdSpace() {
  sendServerRequest("/hold/space");
}

void holdDown() {
  sendServerRequest("/hold/down");
}
```

Non-code blocks are ignored.

```cpp
void setup() {
  Serial.begin(9600);
  while (!Serial);

  // --- MPU6050 Initialization ---
  Wire.begin();
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
  
  // --- Connect to WiFi ---
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    while (true);
  }
  
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }

  Serial.println("\nConnected to WiFi!");
  Serial.print("Arduino IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.println("---------------------");
}
```

```cpp
void loop() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 14, true);

  // Read raw data from MPU6050
  AcX = Wire.read() << 8 | Wire.read();
  AcY = Wire.read() << 8 | Wire.read();
  AcZ = Wire.read() << 8 | Wire.read();
  Tmp = Wire.read() << 8 | Wire.read();
  GyX = Wire.read() << 8 | Wire.read();
  GyY = Wire.read() << 8 | Wire.read();
  GyZ = Wire.read() << 8 | Wire.read();

  // Convert to real-world units
  Ay = AcY / 16384.0 * 9.81;

  // Print results to Serial Monitor
  Serial.print("Y-Acceleration: ");
  Serial.print(Ay, 2);
  Serial.println(" m/s²");

  // --- JUMP DETECTION LOGIC ---
  if (!isSpaceHeld && Ay > JUMP_THRESHOLD) {
    Serial.println("JUMP DETECTED! Holding space...");
    holdSpace();
    isSpaceHeld = true;
  } 
  else if (isSpaceHeld && Ay < RELEASE_THRESHOLD) {
    Serial.println("Jump ended. Releasing space...");
    releaseSpace();
    isSpaceHeld = false;
  }

  delay(100);
}
```


```cpp
  // --- JUMP DETECTION LOGIC ---
  if (!isSpaceHeld && Ay > JUMP_THRESHOLD) {
    Serial.println("JUMP DETECTED! Holding space...");
    holdSpace();
    isSpaceHeld = true;
  } 
  else if (isSpaceHeld && Ay < RELEASE_THRESHOLD) {
    Serial.println("Jump ended. Releasing space...");
    releaseSpace();
    isSpaceHeld = false;
  }

  delay(100);
}
```
````

<!--
Notes can also sync with clicks

[click] This will be highlighted after the first click

[click] Highlighted with `count = ref(0)`

[click:3] Last click (skip two clicks)
-->


---
---

# Teknisk beskrivelse​

<img src="https://up.jooo.tech/ec68">

<img
  v-click
  class="absolute top-24 left-40 w-20 opacity-100"
  src="https://static.vecteezy.com/system/resources/previews/044/291/818/non_2x/cartoon-arrow-pointing-down-png.png"
  alt=""
/>

<!--
Produktet vårt er en ny måte å spille google sitt t-rex spill som er ved å bruke en accelerometer som plukker opp på accelerasjon og bruker det til å hoppe. I vårt tilfelle plukker accelerometeren opp på skarpe endringer I y-verdien og tar det som et tegn til å trykke spacebar på keyboardet slik at t-rexen hopper. Accelerometeren er sensoren brukt I prosjektet, og er egentlig den eneste komponenten brukt annet enn kabler og batteri.
-->


---
layout: iframe
url: https://www.trex-game.skipser.com/
class: px-20
---

# Live Demo​

---

# Det viktigste vi lærte​

<br>
<br>

- Hvordan å lodde

<br>
<br>

- Kalkulere 3d printing størrelser

<br>
<br>

- Hvordan å gjøre relevant research

<!--
Vi har lært hvordan å lodde uten å ødelegge komponentene, hvordan å kalkulere størrelsen til 3d printingen bedre og hvordan å 3d printe generellt, I tillegg til hvordan å gjøre relevant research angående produktet vi prøver å lage og hvilken ressurser er nyttige, for eksempel – projecthub.arduino.
-->

---

# Om vi hadde uendelig tid

<br>
<br>

- prøvd å utvikle bedre kode

<br>
<br>

- raskere system

<br>
<br>


- bedre 3d printing

<!--
Om vi hadde uendelig tid hadde vi garantert prøvd å utvikle et system som er bedre på å plukke opp endringer I y aksen, og prøvd å finne en måte å registrere det kjapt nok slik at t-rex bevegelsen og bevegelsen til person er I sync. Vi hadde også gjort 3d printingen om igjen I tillegg til å sjekke om andre komponenter kunne forbedre effektiviteten av produktet.
-->

---
