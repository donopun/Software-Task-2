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
