
                                   │
                                   ▼
                       [ INITIALISE GAME STATE ]
                       (Instantiate Player, Regions, NPCs)
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         │                                                   │
         ▼                                                   ▼
[ SETUP ENVIRONMENT ]                                [ CORE GAMEPLAY LOOP ]
(Create Map/Connections)                           (Runs until Win/Loss is True)
                                                             │
         ┌───────────────────────┬───────────────────────────┴───────────┐
         │                       │                           │           │
         ▼                       ▼                           ▼           ▼
   [ PHASE 1 ]             [ PHASE 2 ]                 [ PHASE 3 ]  [ PHASE 4 ]
  ENVIRONMENTAL               INPUT                       STATE       TERMINAL
   ASSESSMENT              PROCESSING                  EVALUATION    CONDITION
       │                       │                           │            │
       ├─► Read Location       ├─► Player.move()           ├─► NPC Ticks├─► Check Wealth
       ├─► Get Prices          ├─► Player.trade_candy()    └─► Alerts   └─► Check Suspicion
       └─► Get Security        └─► Player.buy_shares()
