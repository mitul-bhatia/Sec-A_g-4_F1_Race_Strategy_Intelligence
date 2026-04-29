# The Story of Our Project: F1 Race Strategy Intelligence

Welcome! You asked for a clear, simple, "A to Z" story about everything we've built in this repository. Imagine this is a guide for someone who has never watched a race and has never written a line of code.

Here is the journey of how we turned 76 years of messy racing logs into a "Strategy Cheat Code" for F1 teams.

---

## Chapter 1: What is Formula 1? (The 2-Minute Version)
Imagine 20 of the world's fastest cars racing around a track for about 90 minutes. To understand our project, you only need to know **three things**:

1.  **The Start (The Grid):** On the day before the race, drivers do a "speed test" (Qualifying). The fastest driver starts at the front (called "Pole Position"). It's much easier to win if you start at the front.
2.  **The Pit Stop:** F1 tires are high-tech, but they melt like butter when they get hot. During the race, cars must pull over into a "Pit Stop" to get fresh tires. This takes about 2 to 3 seconds. If the crew is slow, the driver loses time and other cars pass them.
3.  **The Tracks:** Some tracks are like narrow hallways (hard to pass), and some are like wide highways (easy to pass).

---

## Chapter 2: The Hero of our Story (Our "Client")
In F1, there are "Big Teams" (like Ferrari and Red Bull) with billions of dollars. Then there are **"Mid-Field Teams"** (the teams that usually finish 4th to 7th).

Our project is designed for the **Mid-Field Team Manager**. They can't outspend the big teams, so they have to outsmart them using **Data**. They want to know: *"If we only have a limited budget, should we spend it on making the car faster in qualifying, or training our pit crew to be 0.5 seconds faster?"*

---

## Chapter 3: The Raw Material (The Data)
We used the **Ergast F1 Database**. It is a giant collection of every single thing that has happened in F1 since 1950.
*   **14 Tables:** One table for race results, one for pit stop times, one for driver names, one for track locations, etc.
*   **The Mess:** The data is messy. If a driver's engine blew up, the data might just say `\N`. If a race was in 1960, the timing might be recorded differently than in 2024.

---

## Chapter 4: The Construction Site (The 6 Notebooks)

We built our solution in 6 clear steps, located in the `notebooks/` folder:

### Phase 1: Ingesting (Notebook 01)
We brought all 14 tables into our "digital workshop." We looked at the data to make sure nothing was missing and that we understood how all the tables connected to each other.

### Phase 2: The Deep Clean (Notebook 02)
This was the hardest part. We:
*   Fixed the `\N` errors.
*   Converted time (like "1 minute 20 seconds") into pure numbers (80,000 milliseconds) so we could do math.
*   Labeled every crash and engine failure so we could track "Reliability."
*   **Output:** We created a single, perfect file called `master_fact.csv`.

### Phase 3: The First Discoveries (Notebook 03 - EDA)
We started drawing pictures (charts). We found that for mid-field teams, finishing the race is half the battle. We also saw that on some tracks, the guy who starts 1st almost always wins, while on other tracks, it's a total lottery.

### Phase 4: The Mathematical Proof (Notebook 04 - Statistics)
We didn't want to just "guess" based on charts. We used math to prove our theories:
*   **The Power of the Start:** We proved that for every 1 spot better you start on the grid, you are likely to score significantly more points.
*   **The Pit Stop Secret:** We proved that teams with the fastest pit crews actually gain more positions during the race than slow ones.
*   **Sorting the Tracks (AI):** We used an AI algorithm (K-Means) to group all tracks into 3 types:
    1.  **Qualifying-Dominant:** (Like Monaco). Don't bother with fancy pit strategies; just start at the front!
    2.  **Strategy-Dominant:** (Like Brazil). You can start at the back and still win if your pit stops are perfect.
    3.  **Mixed:** A balance of both.

### Phase 5: Preparing for the Boss (Notebook 05 - Tableau Prep)
A team manager doesn't want to look at code. They want a beautiful dashboard. We took our complex math and "shined it up" into a format that a software called **Tableau** can understand. We even created a "Data Dictionary" to explain what every single number means.

### Phase 6: The Strategy Cheat Code (Notebook 06 - Track Analysis)
This is the "Final Boss" of our notebooks. For every single track in the world, we generated a **Strategy Card**. It answers:
*   *Should we use Soft (fast/short-life) or Hard (slow/long-life) tires?*
*   *Exactly which lap should we pull over for our pit stop?*
*   *How many pit stops are mathematically optimal for this specific track?*

---

## Chapter 5: The Final Result
By the end of this project, we have built a **Decision Engine**. 

Instead of a team manager "feeling" like they should stop on Lap 20, they can look at our data and see: *"Historically, at this track, teams that stop on Lap 18 have a 20% higher chance of finishing in the Top 5."*

We turned historical "trivia" into **Winning Strategy.**
.
