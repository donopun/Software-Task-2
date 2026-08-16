import os
import random
import sys


def clear_screen():
    """Clears the terminal screen for a clean interface."""
    os.system("cls" if os.name == "nt" else "clear")


# =============================================================================
# NPC CLASS
# =============================================================================
class NPC:

    def __init__(self, name, role, suspicion_impact=0):
        self.name = name
        self.role = role
        self.suspicion_impact = suspicion_impact

    def interact_warden(self, day, jail_day, max_days):
        taunts = [
            '"Five days, kid. Pay the bail or become part of the brickwork."',
            (
                '"No cash, no lockpick skills? Bold strategy for a small-time'
                ' smuggler."'
            ),
            '"The Crown doesn\'t care about your sugar syndicate. Neither do I."',
            (
                '"You look lighter than your ledger. That\'s a bad combination'
                ' in here."'
            ),
            (
                '"Every smuggler thinks they\'re special until the iron door'
                ' swings shut."'
            ),
        ]
        print(f"\n{self.name} steps up to the bars, keys jingling.")
        print(f"{random.choice(taunts)}")
        print(f"--- Day {day} (Jail Day {jail_day}/{max_days}) ---\n")


# =============================================================================
# REGION CLASS
# =============================================================================
class Region:

    def __init__(self, name, security_presence, share_price, stock):
        self.name = name
        self.security_presence = security_presence  # Security Tier 1-3
        self.share_price = share_price
        self.stock = stock
        self.market_prices = {}

    def update_market_prices(self, candy_catalog):
        self.market_prices.clear()
        for candy in self.stock:
            base = candy_catalog[candy]["base"]
            fluctuation = random.uniform(0.85, 1.25)
            self.market_prices[candy] = max(4, round(base * fluctuation, 2))


# =============================================================================
# PLAYER CLASS
# =============================================================================
class Player:

    def __init__(self):
        self.cash_balance = 160.0
        self.candy_inventory = {
            "Sour Worms": 0,
            "Fudge": 0,
            "Choco-Bricks": 0,
            "Jawbreakers": 0,
            "Royal Truffles": 0,
        }
        self.total_suspicion = 0
        self.min_suspicion_floor = 0
        self.shares_owned = {}
        self.hp = 100
        self.max_hp = 100
        self.jail_hits = 0
        self.equipped_weapon = None

        # Stat tracking for dynamic endings
        self.guards_defeated = 0
        self.prison_escapes = 0

    @property
    def empire_wealth(self):
        """Calculates total net worth (Cash + Inventory + Shares)."""
        inv_val = sum(count * 20.0 for count in self.candy_inventory.values())
        share_val = sum(count * 50.0 for count in self.shares_owned.values())
        return self.cash_balance + inv_val + share_val

    def trade_candy(self, current_region):
        clear_screen()
        print(f"--- Market in {current_region.name} ---")
        print("=" * 45)
        print(f" CASH BALANCE: ${self.cash_balance:.2f}")
        print(
            " TOTAL SUSPICION:"
            f" {self.total_suspicion}/100 (Floor: {self.min_suspicion_floor})"
        )
        print(" YOUR INVENTORY:")
        for item, count in self.candy_inventory.items():
            print(f"   * {item}: {count}")
        print("=" * 45)

        print("\nLOCAL MARKET PRICES:")
        for candy, price in current_region.market_prices.items():
            print(f"- {candy}: ${price:.2f}")

        print("\n1. Buy Sweets")
        print("2. Sell Sweets")
        print("3. Return")

        choice = input("Select option (1-3): ").strip()
        if choice not in ["1", "2"]:
            return

        candy_name = input("Enter Candy Name: ").strip().title()
        if candy_name not in current_region.market_prices:
            print("\nThat item is not traded in this district.")
            input("Press Enter to continue...")
            return

        try:
            quantity = int(input("Enter Quantity: ").strip())
            if quantity <= 0:
                print("\nQuantity must be greater than zero.")
                input("Press Enter to continue...")
                return
        except ValueError:
            print("\nInvalid quantity. Enter numerical values only.")
            input("Press Enter to continue...")
            return

        unit_price = current_region.market_prices[candy_name]

        if choice == "1":  # Buy
            total_cost = unit_price * quantity
            if self.cash_balance >= total_cost:
                self.cash_balance -= total_cost
                self.candy_inventory[candy_name] += quantity
                print(
                    f"\nAcquired {quantity} x {candy_name} for"
                    f" ${total_cost:.2f}."
                )
                self.apply_heat(quantity)
            else:
                print("\nYour wallet is empty. The dealer turns away.")

        elif choice == "2":  # Sell
            if self.candy_inventory[candy_name] >= quantity:
                total_earned = unit_price * quantity
                self.cash_balance += total_earned
                self.candy_inventory[candy_name] -= quantity
                print(
                    f"\nOffloaded {quantity} x {candy_name} for"
                    f" ${total_earned:.2f}."
                )
                self.apply_heat(quantity)
            else:
                print("\nYou don't possess that much stock.")

        input("Press Enter to continue...")

    def apply_heat(self, quantity):
        heat_add = 2 if quantity <= 3 else (4 if quantity <= 10 else 8)
        self.total_suspicion = min(100, self.total_suspicion + heat_add)
        print(f"  [Heat +{heat_add}] Suspicion: {self.total_suspicion}/100")


# =============================================================================
# WEAPON DATA
# =============================================================================
class Weapon:

    def __init__(self, name, price, accuracy, power, flavor):
        self.name = name
        self.price = price
        self.accuracy = accuracy
        self.power = power
        self.flavor = flavor


WEAPONS = [
    Weapon(
        "Soggy Licorice Whip",
        30,
        0.80,
        1,
        "Stings enough to make a rookie guard reconsider his career choices.",
    ),
    Weapon(
        "Rusty Sugar Tongs",
        70,
        0.85,
        2,
        "Heavy, sharp, and smelling of stale caramel and poor decisions.",
    ),
    Weapon(
        "Hard-Tack Stunner",
        130,
        0.90,
        3,
        "Stale bread wrapped around a rock. Crude, effective.",
    ),
    Weapon(
        "The Tooth-Extractor",
        220,
        0.95,
        4,
        "A brutal piece of brass hardware from the old dentist guild.",
    ),
]


# =============================================================================
# BOSS CLASS
# =============================================================================
class Boss:

    def __init__(self, player_wealth):
        self.name = "Old John"
        self.role = "Grid Architect"
        # Scales stats dynamically off player net worth
        self.max_hp = int(150 + (player_wealth * 0.25))
        self.hp = self.max_hp
        self.base_damage = int(12 + (player_wealth * 0.02))

    def get_health_bar(self):
        bar_length = 20
        filled = int((self.hp / self.max_hp) * bar_length)
        bar = "[" + "=" * filled + " " * (bar_length - filled) + "]"
        return f"{bar} {self.hp}/{self.max_hp} HP"


# =============================================================================
# GAME ENGINE CLASS
# =============================================================================
class GameEngine:

    def __init__(self):
        self.player = Player()
        self.day = 1

        self.candy_catalog = {
            "Sour Worms": {"base": 8},
            "Fudge": {"base": 20},
            "Choco-Bricks": {"base": 42},
            "Jawbreakers": {"base": 85},
            "Royal Truffles": {"base": 160},
        }

        self.regions = {
            "Gandy": Region("Gandy", 1, 45, ["Sour Worms", "Fudge"]),
            "Twixbury": Region("Twixbury", 1, 45, ["Sour Worms", "Fudge"]),
            "Nougate": Region("Nougate", 1, 40, ["Fudge", "Choco-Bricks"]),
            "Simber": Region("Simber", 1, 50, ["Sour Worms", "Choco-Bricks"]),
            "Caramoor": Region(
                "Caramoor", 2, 55, ["Fudge", "Choco-Bricks", "Jawbreakers"]
            ),
            "Choc Block": Region(
                "Choc Block", 2, 60, ["Choco-Bricks", "Jawbreakers"]
            ),
            "Newark": Region(
                "Newark", 3, 65, ["Jawbreakers", "Royal Truffles"]
            ),
            "L'darestary": Region(
                "L'darestary", 3, 70, ["Jawbreakers", "Royal Truffles"]
            ),
        }

        self.current_region = self.regions["Gandy"]
        self.warden = NPC("Warden Vane", "Head Warden")
        self.john = NPC("Old John", "Underground Supplier")

        self.update_all_region_markets()

    def update_all_region_markets(self):
        for reg in self.regions.values():
            reg.update_market_prices(self.candy_catalog)

    def show_intro_lore(self):
        clear_screen()
        print("=" * 65)
        print(" SWEET STASH: UNDERGROUND CANDY EMPIRE ")
        print("=" * 65)
        print("""
CONTEXT & ORIGINS:
Mass production made sweets absurdly cheap, hooking whole kingdoms overnight. 
Fearing civil collapse, the aristocracy banned candy production, rationing sugar 
and branding sweet traders as criminals. Common folk view traders as vigilantes 
bringing flavor back into a dull world.

EXILE FROM MOUNTAIN VILLAGE:
Flunking every apprenticeship in Mountain Village, you wandered into an 
abandoned waterway and met John. He handed you your first taste of sweet 
contraband and introduced you to the grid. 

Leaving stray crumbs in your room exposed you. Your zealously anti-sugar parents 
cast you out on the spot. With nowhere left to go, you followed John to Gandy 
to build your own operation. In a market flooded with rivals, watch your back—and 
keep an eye on John. Nothing comes free.
-----------------------------------------------------------------
GUIDE:
1. Trade sweets across regions to grow your empire's wealth.
2. High suspicion triggers guard encounters.
3. Visit Blacksmiths for combat gear. Bribe or fight off patrols.
4. If jailed, lockpick or pay bail within 5 days.
""")
        print("=" * 65)
        input("Press Enter to step onto the grid...")

    def check_guard_encounter(self):
        heat = self.player.total_suspicion
        spawn_chance = 0.15 if heat < 25 else (0.45 if heat < 60 else 0.75)

        if random.random() < spawn_chance:
            num_guards = 1 if heat < 60 else random.randint(2, 3)
            print(
                f"\n GUARD PATROL! {num_guards} Crown Guard(s) spotted your"
                " stash!"
            )
            input("Press Enter to engage...")
            self.resolve_combat(num_guards)

    def resolve_combat(self, num_guards):
        while num_guards > 0 and self.player.jail_hits < 5:
            clear_screen()
            print("--- COMBAT INITIATED ---")
            print(
                f"Guards: {num_guards} | HP: {self.player.hp}/100 | Jail"
                f" Strikes: {self.player.jail_hits}/5"
            )
            w_name = (
                self.player.equipped_weapon.name
                if self.player.equipped_weapon
                else "Bare Fists"
            )
            print(f"Equipped: {w_name}\n")
            print("1. Strike")
            print("2. Bribe ($20.00)")

            choice = input("Select: ").strip()
            if choice == "1":
                acc = (
                    self.player.equipped_weapon.accuracy
                    if self.player.equipped_weapon
                    else 0.55
                )
                power = (
                    self.player.equipped_weapon.power
                    if self.player.equipped_weapon
                    else 1
                )

                if random.random() <= acc:
                    defeated = min(num_guards, power)
                    num_guards -= defeated
                    self.player.guards_defeated += defeated
                    print(
                        f"\n Direct hit! Knocked out {defeated} guard(s)."
                    )
                else:
                    dmg = random.randint(5, 10) * num_guards
                    self.player.hp -= dmg
                    self.player.jail_hits += 1
                    print(
                        f"\n Strike missed! Guards hit back for {dmg} damage."
                        f" Strike {self.player.jail_hits}/5."
                    )
                input("Press Enter to continue...")

            elif choice == "2":
                if self.player.cash_balance >= 20.0:
                    self.player.cash_balance -= 20.0
                    print(
                        "\n You slipped cash into the guard's pocket and"
                        " stepped into the alley."
                    )
                    input("Press Enter to continue...")
                    return
                else:
                    print(
                        "\nYour pockets are empty. The guards scoff at your"
                        " attempt."
                    )
                    input("Press Enter to continue...")

        if self.player.jail_hits >= 5:
            self.enter_dungeon()
        else:
            clear_screen()
            print(" Patrol cleared! You melted into the shadows.")
            input("Press Enter to continue...")

    def enter_dungeon(self):
        jail_days = 0
        max_days = 5

        while jail_days < max_days:
            clear_screen()
            print(" ARRESTED! Thrown into the municipal cells.")
            jail_days += 1
            self.day += 1

            self.warden.interact_warden(self.day, jail_days, max_days)

            print("1. Lockpick door (50% chance)")
            print("2. Pay bail ($40.00)")
            print("3. Wait out the day")

            choice = input("Select: ").strip()

            if choice == "1":
                if random.random() <= 0.50:
                    print(
                        "\n The mechanism clicks! You broke out before Vane"
                        " returned."
                    )
                    self.player.jail_hits = 0
                    self.player.prison_escapes += 1

                    self.player.min_suspicion_floor += 15
                    self.player.total_suspicion = max(
                        self.player.total_suspicion,
                        self.player.min_suspicion_floor + 20,
                    )

                    print(
                        "  WANTED OUTLAW! Permanent suspicion floor raised to"
                        f" {self.player.min_suspicion_floor}."
                    )
                    input("Press Enter to continue...")
                    return
                else:
                    print(
                        "\n Lockpick snapped. Warden Vane chuckles down the"
                        " hallway."
                    )
                    input("Press Enter to continue...")

            elif choice == "2":
                if self.player.cash_balance >= 40.0:
                    self.player.cash_balance -= 40.0
                    print(
                        "\n Bail processed. Vane pocketed your purse with a"
                        " smirk."
                    )
                    self.player.jail_hits = 0
                    self.player.total_suspicion = max(
                        15, self.player.min_suspicion_floor
                    )
                    input("Press Enter to continue...")
                    return
                else:
                    print(
                        '\n"That\'s short of $40," Vane says flatly. "Try again'
                        ' when you have money."'
                    )
                    input("Press Enter to continue...")

            elif choice == "3":
                print("\nYou sit on damp straw, watching time run out.")
                input("Press Enter to continue...")

        clear_screen()
        print("=" * 65)
        print(" TIME'S UP IN THE DUNGEON.")
        print("=" * 65)
        print("\nWarden Vane unlocks the iron door, shaking his head.")
        print('"Five days, no cash, no escape. Unfortunate."')
        print("\nGuards escort you up stone stairs toward the courtyard.")
        print("The Crown waste no resources on bankrupt smugglers.")
        print("\n EXECUTED BY CROWN DECREE. ITS OVER FOR YOU.")
        print("=" * 65)
        sys.exit()

    def blacksmith_menu(self):
        clear_screen()
        print("--- LOCAL BLACKSMITH ---")
        for i, w in enumerate(WEAPONS, 1):
            print(
                f"{i}. {w.name} - ${w.price} | Acc: {int(w.accuracy*100)}% |"
                f" Defeats: {w.power} guard(s)"
            )
            print(f'    -- "{w.flavor}"')
        print("5. Leave\n")

        choice = input("Select gear (1-4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            w = WEAPONS[int(choice) - 1]
            if self.player.cash_balance >= w.price:
                self.player.cash_balance -= w.price
                self.player.equipped_weapon = w
                print(f"\n Equipped {w.name}.")
            else:
                print(
                    '\n The blacksmith eyes your thin purse. "No credit here."'
                )
            input("Press Enter to continue...")

    def trigger_boss_encounter(self):
        """Secret cheat encounter with scaling difficulty and scripted boss sequence."""
        boss = Boss(self.player.empire_wealth)

        clear_screen()
        print("=" * 65)
        print(" ... ")
        print(" ... ")
        print(" ... ")
        print("=" * 65)
        print("\nYou step behind the abandoned distillery, expecting a shipment.")
        print(
            "Old John leans against the damp brickwork, tossing a heavy brass"
            " key."
        )
        print('\n"You got greedy kid," John says, spitting onto the cobbles.')
        print('"Suddenly, he lunges at you with a cane."')
        print(
            '"I built this pipeline. I won\'t let a stray like you blow it'
            ' up."'
        )
        print("=" * 65)
        input("Press Enter to initiate battle...")

        # Turn-based RPG Loop
        turn = 1
        while boss.hp > 0 and self.player.hp > 0:
            clear_screen()
            # Scripted interruption when John is near defeat
            if boss.hp <= boss.max_hp * 0.15:
                print("=========================================================")
                print("            *** ENEMY TURN - INTERRUPT ***               ")
                print("=========================================================")
                print(f" {boss.name.upper()} {boss.get_health_bar()}")
                print(
                    f" PLAYER     "
                    f" [{'=' * int((self.player.hp/self.player.max_hp)*20)}]"
                    f" {self.player.hp}/{self.player.max_hp} HP"
                )
                print(
                    "=========================================================\n"
                )
                print(
                    "Old John drops his cane. He doesn't bleed. He doesn't"
                    " flinch."
                )
                print(
                    "He wipes a speck of dust off his coat and looks you dead"
                    " in the eye.\n"
                )
                print('"You think you could win?" John says.')
                print(
                    "\nBefore you can pull your weapon, John moves faster than"
                    " breath."
                )
                print("A heavy iron cosh catches you across the temple.")
                print("The grid blurs. The cobbles rush up to meet your face.")
                print("\n[ CRITICAL DAMAGE: 9999 ]")
                self.player.hp = 0
                input("\nPress Enter...")
                break

            # RPG Battle UI Display
            print("=========================================================")
            print(f" TURN {turn} - BOSS ENGAGEMENT")
            print("=========================================================")
            print(f" {boss.name.upper()} ({boss.role})")
            print(f" {boss.get_health_bar()}")
            print("-" * 57)

            p_bar = int((self.player.hp / self.player.max_hp) * 20)
            print(" PLAYER STATUS")
            print(
                f" [{('=' * p_bar).ljust(20)}] {self.player.hp}/{self.player.max_hp}"
                " HP"
            )
            w_name = (
                self.player.equipped_weapon.name
                if self.player.equipped_weapon
                else "Fists"
            )
            print(f" Weapon: {w_name}")
            print("=========================================================")
            print("1. Weapon Strike")
            print("2. Desperate Pocket Sand")
            print("3. Attempt Retraction")
            print("---------------------------------------------------------")

            action = input("Execute command (1-3): ").strip()

            if action == "1":
                acc = (
                    self.player.equipped_weapon.accuracy
                    if self.player.equipped_weapon
                    else 0.50
                )
                pwr = (
                    self.player.equipped_weapon.power * 15
                    if self.player.equipped_weapon
                    else 10
                )

                if random.random() <= acc:
                    damage = random.randint(pwr, pwr + 12)
                    boss.hp -= damage
                    print(
                        f"\n> You landed a hit with {w_name} for {damage}"
                        " damage."
                    )
                else:
                    print(
                        "\n> You swung wildly. John parried it effortlessly."
                    )

            elif action == "2":
                damage = random.randint(3, 8)
                boss.hp -= damage
                print(
                    f"\n> You threw pocket grit. John grunts, taking {damage}"
                    " raw damage."
                )

            elif action == "3":
                print(
                    '\n> John laughs dryly. "Nobody walks away from the grid."'
                )

            # Boss Attack Counter
            if boss.hp > boss.max_hp * 0.15:
                john_dmg = random.randint(
                    boss.base_damage - 3, boss.base_damage + 5
                )
                self.player.hp -= john_dmg
                print(
                    "> Old John counters with a reinforced cane strike for"
                    f" {john_dmg} damage."
                )
                turn += 1
                input("\nPress Enter to next turn...")

        # Scripted Game Over / Epilogue
        clear_screen()
        print("=" * 65)
        print(" GRID ERASURE - TERMINAL LOSS, ITS OVER ")
        print("=" * 65)
        print(
            "\nYou wake up face down in freezing water. Your coat is gone. So is"
            " your identity."
        )
        print("Your ledger is ash. Your stock is gone. Your purse is empty.")
        print(
            "You take a moment to recuperate, still on edge after the encounter"
        )
        print("under a flickering streetlamp, lighting a thin cigar.")
        print("John returns an ominous glare")
        print('"Now you\'re just a loose end."')
        print("Usually I would deflower you.")
        print("But that is only for those worthy enough...")
        print("\nTwo figures step out from the alley shadows.")
        print("Canvas sacks cover your head as rope binds your wrists.")
        print("They drag you down steep stone steps into absolute darkness.")
        print(
            "A heavy iron door slams shut, locking with the finality of a tomb."
        )
        print(
            "Whatever depraved things happen to you is out of your control"
            " now..."
        )
        print("\n--- YOU NEVER EXISTED ---")
        print("=" * 65)
        sys.exit()

    def display_victory(self):
        clear_screen()
        print("=" * 65)
        print(" KING OF THE SUGAR GRID - VICTORY ")
        print("=" * 65)
        print("\nYou stand on the balcony of your Newark estate, swirling")
        print(
            "spiced cherry syrup with an empire net worth reading"
            f" ${self.player.empire_wealth:,.2f}.\n"
        )
        print("-" * 65)

        escapes = self.player.prison_escapes
        if escapes == 0:
            print(" TITLE: THE UNTOUCHABLE GHOST")
            print("The Magistrates don't have a mugshot on file.")
            print("You built a syndicate without touching a dungeon wall.")
        elif escapes <= 2:
            print(" TITLE: THE SLIPPERY SMUGGLER")
            print(f"Your {escapes} breakout(s) are tavern folklore.")
            print(
                "Guards attempted to lock you behind iron; you picked the cell"
                " locks and walked out."
            )
        elif escapes <= 4:
            print(" TITLE: THE DUNGEON PHANTOM")
            print(
                f"With {escapes} jailbreaks recorded, wardens sweated whenever"
                " you were brought in."
            )
            print(
                "You treated high-security cells like a lounge, lockpicking out"
                " in minutes."
            )
        else:
            print(" TITLE: ARCHITECT OF THE REVOLVING DOOR")
            print(f"RECORD SET: {escapes} ESCAPES.")
            print("The Royal High Council gave up trying to keep you imprisoned.")
            print(
                f"After escape #{escapes}, Warden Vane resigned in humiliation."
                " Dungeon staff"
            )
            print(
                "converted your old cell into a public museum dedicated to"
                " your runs."
            )
            print("Iron bars are useless when the prisoner owns the kingdom.")

        print("-" * 65)
        defeated = self.player.guards_defeated
        if defeated == 0:
            print(" COMBAT: PACIFIST MASTERMIND")
            print(
                "No guards took hits from you. Bribes and alleyways kept your"
                " hands clean."
            )
        elif defeated <= 5:
            print(" COMBAT: STREET BRAWLER")
            print(
                f"With {defeated} guards knocked out, garrisons gave your trade"
                " routes a wide berth."
            )
        else:
            print(" COMBAT: ENFORCER OF THE ALLEYWAYS")
            print(
                f"A trail of {defeated} knocked-out guards left no doubt who"
                " ruled the grid."
            )
            print(
                "You dismantled Crown authority and broke patrol units to"
                " pieces."
            )

        print("=" * 65)
        print("""
Old John dropped by yesterday. He left a crate of Sour Worms on your desk, 
took a pull from his pipe, and tipped his hat before fading into the rain.

You ran the entire kingdom's grid.

--- GAME OVER: YOU WIN ---
""")
        print("=" * 65)
        input("Press Enter to exit...")

    def start_game_loop(self):
        self.show_intro_lore()

        while True:
            clear_screen()
            current_wealth = self.player.empire_wealth

            if current_wealth >= 1000.0:
                self.display_victory()
                break

            print("=" * 50)
            print(" SWEET STASH: UNDERGROUND CANDY EMPIRE ")
            print("=" * 50)
            print(f"Day {self.day} | Location: {self.current_region.name}")
            print(
                f"Cash: ${self.player.cash_balance:.2f} | Net Worth:"
                f" ${current_wealth:.2f}"
            )
            print(
                f"Suspicion: {self.player.total_suspicion}/100 (Floor:"
                f" {self.player.min_suspicion_floor})"
            )
            print(f"Inventory: {self.player.candy_inventory}")
            w_name = (
                self.player.equipped_weapon.name
                if self.player.equipped_weapon
                else "Bare Fists"
            )
            print(f"Weapon: {w_name}")
            print("-" * 50)
            print("1. Trade Candy (Local Market)")
            print("2. Visit Blacksmith")
            print("3. Travel to District")
            print("4. Buy District Share ($50.00)")
            print("5. Quit\n")

            choice = input("Select (1-5): ").strip()

            # CHEAT CODE TRIGGER
            if choice == "666" or choice.lower() == "john":
                self.trigger_boss_encounter()

            elif choice == "1":
                self.player.trade_candy(self.current_region)
                self.check_guard_encounter()

            elif choice == "2":
                self.blacksmith_menu()

            elif choice == "3":
                clear_screen()
                print("--- District Map ---")
                region_keys = list(self.regions.keys())
                for i, r_name in enumerate(region_keys, 1):
                    reg = self.regions[r_name]
                    stock_list = ", ".join(reg.stock)
                    print(
                        f"{i}. {r_name} (Security: Tier"
                        f" {reg.security_presence}) - Sweets: [{stock_list}]"
                    )

                try:
                    t_choice = int(
                        input("\nSelect destination (number): ").strip()
                    )
                    if 1 <= t_choice <= len(region_keys):
                        selected_name = region_keys[t_choice - 1]
                        self.current_region = self.regions[selected_name]
                        self.day += 1
                        self.update_all_region_markets()
                        self.player.total_suspicion = max(
                            self.player.min_suspicion_floor,
                            self.player.total_suspicion - 3,
                        )
                        print(
                            f"\nArrived in {self.current_region.name}."
                            " Suspicion lowered."
                        )
                    else:
                        print("\nInvalid district number.")
                except ValueError:
                    print("\nEnter numerical choices only.")
                input("Press Enter to continue...")

            elif choice == "4":
                reg_name = self.current_region.name
                cost = self.current_region.share_price
                if self.player.cash_balance >= cost:
                    self.player.cash_balance -= cost
                    self.player.shares_owned[reg_name] = (
                        self.player.shares_owned.get(reg_name, 0) + 1
                    )
                    print(f"\nPurchased 1 Share in {reg_name}!")
                else:
                    print("\nNot enough cash balance to acquire shares.")
                input("Press Enter to continue...")

            elif choice == "5":
                print("Exiting game loop.")
                break


if __name__ == "__main__":
    game = GameEngine()
    game.start_game_loop()
