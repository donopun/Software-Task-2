# Class Diagram & Object Architecture

The system is structured using Object-Oriented Programming (OOP) across five primary classes to encapsulate game state, regional data, combat mechanics, and character interactions:

* **`GameEngine`:** Manages execution flow, dynamic market recalibration, combat logic, and win/loss terminal state evaluations.
* **`Player`:** Tracks inventory, cash, global suspicion, minimum suspicion floor, combat stats, and calculates dynamic net worth.
* **`Region`:** Stores local candy stocks, security levels, share costs, and dynamic market prices.
* **`NPC`:** Handles non-player characters (e.g., Warden Vane, Old John) and contextual dialogue interactions.
* **`Weapon`:** Stores stats for offensive gear obtainable at the blacksmith (accuracy, power, flavor text).

---

## Mermaid Diagram

```mermaid
classDiagram
    class GameEngine {
        +int day
        +dict candy_catalog
        +dict regions
        +Region current_region
        +NPC warden
        +NPC john
        +Player player
        +update_all_region_markets()
        +show_intro_lore()
        +check_guard_encounter()
        +resolve_combat(num_guards)
        +enter_dungeon()
        +blacksmith_menu()
        +display_victory()
        +start_game_loop()
    }

    class Player {
        +float cash_balance
        +dict candy_inventory
        +int total_suspicion
        +int min_suspicion_floor
        +dict shares_owned
        +int hp
        +int jail_hits
        +Weapon equipped_weapon
        +int guards_defeated
        +int prison_escapes
        +float empire_wealth
        +trade_candy(current_region)
        +apply_heat(quantity)
    }

    class Region {
        +string name
        +int security_presence
        +float share_price
        +list stock
        +dict market_prices
        +update_market_prices(candy_catalog)
    }

    class NPC {
        +string name
        +string role
        +int suspicion_impact
        +interact_warden(day, jail_day, max_days)
    }

    class Weapon {
        +string name
        +float price
        +float accuracy
        +int power
        +string flavor
    }

    GameEngine "1" -- "1" Player : manages
    GameEngine "1" -- "*" Region : contains
    GameEngine "1" -- "*" NPC : references
    Player "1" -- "0..1" Weapon : equips
    Player ..> Region : interacts with via trade_candy()
