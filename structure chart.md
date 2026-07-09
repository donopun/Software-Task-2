# Structure Chart - Sweet Stash

## 1. System Module Flow Hierarchy

* **[1.0] MAIN CONTROL (main.py)**
  * **[1.1] INITIALISE GAME STATE**
    * *Action:* Instantiate Player, Regions, and NPCs
  * **[1.2] SETUP ENVIRONMENT**
    * *Action:* Create Map Connections & Regional Layouts
  * **[1.3] CORE GAMEPLAY LOOP (Repeats until Win/Loss is True)**
    * **Phase 1: Environmental Assessment**
      * ├─► Read Location
      * ├─► Get Prices
      * └─► Get Security
    * **Phase 2: Input Processing**
      * ├─► Player.move()
      * ├─► Player.trade_candy()
      * └─► Player.buy_shares()
    * **Phase 3: State Evaluation**
      * ├─► NPC Ticks
      * └─► Alerts
    * **Phase 4: Terminal Condition Check**
      * ├─► Check Wealth
      * └─► Check Suspicion
