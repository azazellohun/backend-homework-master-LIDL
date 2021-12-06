# Backend Position Házi Feladat

A alábbi feladatban egy egyszerűsített, esemény-vezérelt raktárkezelő rendszer két komponensét kell implementálnod. Az egyszerűség kedvéért, kétféle eseménnyel kell dolgoznod:

* készletfeltöltés - új készlet érkezik a boltba (event_type: "incoming")
* eladás - a boltban lévő termékből x db-ot eladtak (event_type: "sale")

## A rendszer felépítése:
---

* Importer alkalmazás:
  * szerepe: adatok felolvasása, feldolgozása, publisholása
* Kafka
  * szerepe: feldolgozott adatok továbbítása

Az alkalmazás egy adott mappában CSV fájlokat keres és szerializált formátumban elküldi az `events` nevű Kafka topic-ra.


Példa egy sorra:
```
transaction_id,event_type,date,store_number,item_number,value
7c71fb42-1f5e-45e1-be16-7d4d772d1aab,sale,2018-12-03T23:57:40Z,9,8,116
```

Példa CSV fájlokat `data` mappában megtalálod.

### Megjegyzés

> Néha előfordulhatnak hibás formátumú CSV-k, melyekben egy vagy több érték hiányzik, esetleg bizonyos értékek típusa eltér. Ilyen esetekben az alkalmazás logoljon hibát, de indokolatlanul ne álljon meg a működése. Egyetlen sorban szereplő hiba ne vezessen egy egész fájl elvesztéséhez.

> Lehetnek olyan sorok a CSV fájlokban, amelyek esetén a dátum mező formátuma eltérő módon van reprezentálva. Az ilyen esetekben alakítsd a dátumokat azonos formátumra. Példa: 18 12 03 MON 23:57:40 - 2018-12-03T23:57:40Z

## Technikai követelmények
---

* A project legyen verzió követve `git` alkalmazasaval
* Az alkalmazáshoz legyen megfelelő teszt suite, akár `pytest`, akár a standard python `unittest` modul
* Az alkalmazás legyen elindítható lokálisan, konténerizált formában (docker-compose)


## Hogyan használd

Poetry telepítése: https://python-poetry.org/docs/#installation

```
poetry install
```

* `docker-compose version >= 1.29.2`
* `python version >= 3.8`
* `poetry version >= 1.1.7`

### Megjegyzés

> A projektben előre definiáltunk számodra egy minimális docker-compose.yaml fájlt. Ebben konfigurálásra került egy `zookeeper` és egy `kafka` container. Topic-ot nem kell kreálnod, mivel a rendszer automatikusan készít egyet, amennyiben arra üzenet érkezik (KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true). Amennyiben nem dockerben futtatod a kódodat, a kafka-t a `localhost:9094`-en éred el, docker környezetben az `app-network`-ben pedig `kafka:9094`-en.
