# Overview
A prototype of text based rpg based adventure game inspired by Gregory Yob's Hunt the Wumpus using OOP in pyhton.
### Credits
* A student project created by Johnny Chan for Year 11 Software engineering course
* Teacher Mr McFarlane

### Game name: Sweet Stash
# Idea Implementation
Through python, the game incorporates a ubiqudous OOP system throughout with deep character immersion and a sophosicated rpg style text based game to create an enjoyable and replayable interactive experience.
## Gameplay Cycle & Core Loop

The execution architecture of "Sweet Stash" runs on a continuous operational loop driven by user input, evaluating state variables across character and region objects until a terminal win/loss condition is satisfied. The core gameplay loop is structured into four distinct, recurring phases:


```

```

### 1. Environmental Assessment & Market Analysis
At the initiation of each turn, the system queries the `Region` object corresponding to the `Player.current_location` reference. The engine processes the internal `Region.market_prices` and local `security_presence` metrics. The player is presented with a text-based interface displaying the current economic data, regional risks, and adjacent directional vectors available for travel.

### 2. Input Processing & Action Execution
The game loop transitions into a polling state, waiting for user input to trigger an operational method. The user's input string is validated and mapped to one of three primary behavioral tracks:
* **Traversal:** Invoking `Player.move()` to change spatial coordinates to an adjacent region object.
* **Commerce:** Invoking `Player.trade_candy()` to liquidate candy inventory or acquire wholesale supplies from local `NPC` instances.
* **Expansion:** Invoking `Player.buy_shares()` to invest capital directly into the regional market infrastructure.

### 3. State Evaluation & NPC Response
Once the player's action modifies the system state, the engine updates dependent object variables globally. During this phase, neighboring `NPC` instances execute their tick routines. If the player's trade volume or illegal activity breaches the environmental thresholds, the system modifies `NPC.suspicion_level` and triggers secondary events, such as calling `NPC.alert_guards()` to scale local security variables.

### 4. Terminal Condition Check
Before restarting the loop, the engine evaluates the global game state against the project's success and failure parameters:
* **Win Condition (Empire Solidified):** Triggers if `Player.empire_wealth` achieves the target threshold and ownership shares are acquired across all major industrial regions (e.g., Newark and Gandy).
* **Loss Condition (Exile/Apprehension):** Triggers if regional threat parameters or suspicion variables maximize, leading to a terminal intercept sequence that concludes program execution.

```
