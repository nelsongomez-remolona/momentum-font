# Antarctic meteorites — what the catalogue reveals

**Data:** The Meteoritical Society "Meteorite Landings" catalogue — **45,716**
records with name, classification, mass, fall/found status, year, and
coordinates. Mirror: NASA Open Data / [figshare](https://rochester.figshare.com/articles/dataset/Meteorite_Landings/26462452).
Analysis: [`analyze_meteorites.py`](./analyze_meteorites.py) (`python3 analyze_meteorites.py`).

**Antarctic subset** = records south of 60°S **or** carrying a known Antarctic
collection-field name (Allan Hills, Yamato, Queen Alexandra Range, …): **30,646**.

> ⚠️ **Data caveat:** this snapshot effectively ends **~2013**. The collapse in the
> 2010s row is the *catalogue* ending, not meteorites running out.

---

## The surprising findings

### 1. Two out of every three meteorites on Earth were found in Antarctica
**30,646 of 45,716 catalogued meteorites (67%) come from Antarctica** — a continent
with no permanent population, where humans have physically searched a vanishingly
small fraction of the surface. A place almost nobody goes has produced the majority
of the world's space rocks.

### 2. Essentially no one has ever *seen* one fall there
Meteorites are classed "**Fell**" (witnessed) or "**Found**." Elsewhere, 1,090 were
seen to fall. In Antarctica: **effectively zero (17 of 30,646)** — because there's no
one there to watch. Every Antarctic meteorite is a *found* object, recovered from ice
long after it landed.

### 3. Antarctic meteorites are ~20× smaller than the rest
**Median mass 14 g in Antarctica vs 277 g elsewhere.** Everywhere else, meteorites are
noticed because they're big enough to spot by luck. On Antarctic blue ice, teams walk
transects and pick up **every dark pebble**, so the catalogue captures the tiny ones
the rest of the world never records. The size difference is a *sampling* signature, not
a physics one.

### 4. The ice is a natural conveyor belt that concentrates them
A handful of "**stranding surfaces**" dominate — ice flows toward mountains, stalls, and
sublimating wind strips the snow away, leaving meteorites piled on exposed blue ice:

| Field | Meteorites |
|---|---:|
| Yamato Mountains (Japan program) | 7,269 |
| Queen Alexandra Range | 3,461 |
| Grove Mountains | 2,502 |
| Elephant Moraine | 2,190 |
| Miller Range | 2,068 |
| Allan Hills | 1,756 |

Six spots account for a large share of all 30,000+. The continent doesn't just preserve
meteorites — its ice actively *gathers* them into a few natural collecting basins.

### 5. Antarctica handed us the Moon and Mars
The catalogue holds **119 Martian and 165 lunar meteorites** — rocks blasted off other
worlds by impacts, later falling to Earth. The most scientifically famous ones are
Antarctic finds:
- **Allan Hills 84001** — the Mars meteorite that sparked the 1996 "life on Mars" debate.
- **ALHA A77005 / EETA79001** — early Martian meteorites that let us *identify* Mars as a source (their trapped gas matched Viking's Mars-atmosphere measurements).
- **ALHA 81005** — the **first recognized lunar meteorite** (1982).

(Most *catalogued* lunar/Martian stones are actually hot-desert finds from NW Africa,
but Antarctica delivered the pioneers that made the whole field possible.)

### 6. The find rate maps the history of one science program
Antarctic finds by decade: **18 (1960s) → 4,626 → 6,369 → 8,931 → 10,334 (2000s)**.
That curve *is* the growth of systematic searching — the US **ANSMET** program (from 1976)
and the Japanese Yamato/Asuka expeditions. Before humans went looking, the number was
essentially zero; the "meteorite richness" of Antarctica is as much about **who searched**
as about the ice.

---

## The one-line insight
Antarctica isn't where most meteorites *land* — they fall evenly worldwide — it's where
the ice **preserves, transports, and concentrates** them, and where systematic teams
**collect the small ones everyone else misses**. The 67% figure is a story about *ice
dynamics and human effort*, and it's how we ended up holding pieces of Mars and the Moon.
