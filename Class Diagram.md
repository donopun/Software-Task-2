+-------------------------------------------------------------------------+
|                               GameEngine                                |
+-------------------------------------------------------------------------+
| - day: int                                                              |
| - candy_catalog: dict                                                   |
| - regions: dict[str, Region]                                            |
| - current_region: Region                                                |
| - warden: NPC                                                           |
| - john: NPC                                                             |
| - player: Player                                                        |
+-------------------------------------------------------------------------+
| + update_all_region_markets(): void                                     |
| + show_intro_lore(): void                                               |
| + check_guard_encounter(): void                                         |
| + resolve_combat(num_guards: int): void                                 |
| + enter_dungeon(): void                                                 |
| + blacksmith_menu(): void                                               |
| + display_victory(): void                                               |
| + start_game_loop(): void                                               |
+-------------------------------------------------------------------------+
       |                                |                            |
       | 1                              | 1..* | 1..*
       v                                v                            v
+-----------------------------+  +------------------------+  +---------------+
|           Player            |  |         Region         |  |      NPC      |
+-----------------------------+  +------------------------+  +---------------+
| - cash_balance: float       |  | - name: str            |  | - name: str   |
| - candy_inventory: dict     |  | - security_presence:int|  | - role: str   |
| - total_suspicion: int      |  | - share_price: float   |  | - suspicion_  |
| - min_suspicion_floor: int  |  | - stock: list[str]     |  |   impact: int |
| - shares_owned: dict        |  | - market_prices: dict  |  +---------------+
| - hp: int                   |  +------------------------+  | + interact_   |
| - jail_hits: int            |  | + update_market_       |  |   warden()    |
| - equipped_weapon: Weapon   |  |   prices(): void       |  +---------------+
| - guards_defeated: int      |  +------------------------+
| - prison_escapes: int       |
| - empire_wealth: float (prop|
+-----------------------------+
| + trade_candy(region): void |
| + apply_heat(qty: int): void|
+-----------------------------+
       |
       | 0..1
       v
+-----------------------------+
|           Weapon            |
+-----------------------------+
| - name: str                 |
| - price: float              |
| - accuracy: float           |
| - power: int                |
| - flavor: str               |
+-----------------------------+
