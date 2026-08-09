import os
import random
import sys

def clear_screen():
    """Clears the terminal screen for a clean interface."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_lore_and_guide():
    """Displays the intro story and beginner's guide before the game begins."""
    clear_screen()
    print("=" * 65)
    print("🍬 WELCOME TO SWEET STASH: UNDERGROUND CANDY EMPIRE 🍬")
    print("=" * 65)
    print("""
THE LORE & ORIGINS:
When mass production made sweets absurdly cheap, whole kingdoms hooked 
themselves on sugar overnight. Fearing civil breakdown, the Crown clamped 
down hard—banning private production, rationing sugar, and branding sweet 
traders as rogue criminals. To the common folk, those traders are 
vigilantes bringing flavor back into a dull world.

YOU & YOUR EXILE:
Growing up in Mountain Village, you were expected to master an honest trade, 
but you flunked every single apprenticeship you tried. Aimless and restless, 
you spent your days wandering the outskirts until you stumbled into an old, 
abandoned waterway and met John. He handed you your first taste of candy 
and introduced you to the local underground market.

That taste was your downfall. Leaving a few stray crumbs in your room was all 
it took for your zealously anti-sugar parents to catch on. Heartbroken by your 
betrayal and fed up with your lack of direction, they cast you out on the spot.

With nowhere else to go, you followed John to Gandy. He showed you how to move 
your first few small-time batches before stepping back to let you build your 
own operation. In a market flooded with rival dealers, stay sharp—and keep a 
close eye on John. In this line of work, nothing comes free.

-----------------------------------------------------------------
BEGINNER'S GUIDE & SMUGGLER RULES:
1. TRADING CANDY:
   - Different towns produce and stock different types of sweets!
   - Buy low in production towns and travel to sell high in wealthy towns.
   
2. SUSPICION & HEAT (⚠️) [HARD MODE]:
   - Trading adds steep suspicion. Larger deals attract heavy heat.
   - Low Heat (<25): Mild guard patrols (15% encounter rate).
   - Mid Heat (25-59): Frequent patrols (45% encounter rate).
   - High Heat (60+): Heavy lockdown (75% encounter rate).
   - Tip: Escaping prison permanently raises your minimum suspicion floor!

3. WEAPONS & COMBAT (⚔️):
   - Visit the Blacksmith to buy weapons with better accuracy & power.
   - If guards attack, you can fight back or bribe them ($20).
   - Taking 5 hits in combat gets you ARRESTED.

4. DUNGEON & JAILBREAK (🔒):
   - If arrested, you have 5 days to lockpick your cell or pay bail ($40).
   - The Warden checks cells on Day 5. Bribes or lockpicks are your only way out.
""")
    print("=" * 65)
    input("Press Enter to begin your empire...")

def show_victory_screen(net_worth, guards_defeated, prison_escapes):
    """Displays dynamic ending lore based on player stats with unique escape titles."""
    clear_screen()
    print("=" * 65)
    print("🍬 KING OF THE SUGAR GRID — VICTORY 🍬")
    print("=" * 65)
    print(f"\nYou stand on the top balcony of your sprawling Newark estate, swirling")
    print(f"a glass of spiced cherry syrup with a ledger reading ${net_worth:,.2f}.\n")

    print("-" * 65)
    # Dynamic Escape Narrative Tiers
    if prison_escapes == 0:
        print("👑 TITLE EARNED: THE UNTOUCHABLE GHOST")
        print("The Crown Magistrates don't have a mugshot of you on file.")
        print("You built a multi-thousand dollar sugar syndicate without touching")
        print("a dungeon wall. The guards spent years chasing shadows while you built an empire.")

    elif prison_escapes <= 2:
        print("🔓 TITLE EARNED: THE SLIPPERY SMUGGLER")
        print(f"Your {prison_escapes} prison breakout(s) are legendary tavern folklore.")
        print("The guards attempted to lock you up behind cold iron,")
        print("you picked their locks with rusted sugar tongs and walked right out the front gate.")

    elif prison_escapes <= 4:
        print("🌀 TITLE EARNED: THE DUNGEON PHANTOM")
        print(f"With {prison_escapes} jailbreaks under your belt, the wardens started sweating")
        print("every time you were brought in. You treated their high-security cells like a lounge,")
        print("lockpicking your way out before your cell door finished swinging shut.")

    else:
        print("🏰 TITLE EARNED: ARCHITECT OF THE REVOLVING DOOR")
        print(f"A WHOPPING {prison_escapes} ESCAPES!")
        print("The Royal High Council gave up trying to keep you imprisoned.")
        print(f"After escape #{prison_escapes}, the High Warden resigned in humiliation, and the dungeon")
        print("staff converted your old cell into a public museum dedicated to your legendary runs.")
        print("Iron bars are useless when the person inside owns the entire kingdom.")

    print("-" * 65)

    # Dynamic Guard Defeat Narrative Tiers
    if guards_defeated == 0:
        print("🕊️ COMBAT STYLE: PACIFIST MASTERMIND")
        print("Not a single guard took a hit from you. Smooth talk, crisp bribes, and ghosting")
        print("through alleyways kept your hands clean and the Crown's treasury drained.")
    elif guards_defeated <= 5:
        print("🥊 COMBAT STYLE: STREET BRAWLER")
        print(f"With {guards_defeated} guards knocked out across your runs, the local garrisons learned")
        print("to give your trade routes a wide berth whenever your carriage rolled into town.")
    else:
        print("💥 COMBAT STYLE: ENFORCER OF THE ALLEYWAYS")
        print(f"A trail of {guards_defeated} battered guards left no doubt who ruled the grid.")
        print("You dismantled Crown authority and broke their patrols to pieces.")

    print("=" * 65)
    print(f"""
Old John dropped by yesterday. He left a vintage crate of Sour Worms on your desk, 
took a slow pull from his pipe, and tipped his hat before fading back into the rain.

You ran the entire kingdom's grid.

--- GAME OVER: YOU WIN ---
""")
    print("=" * 65)
    input("Press Enter to exit the game...")

class Player:
    def __init__(self):
        self.cash = 160.0
        self.inventory = {
            "Sour Worms": 0,
            "Fudge": 0,
            "Choco-Bricks": 0,
            "Jawbreakers": 0,
            "Royal Truffles": 0
        }
        self.suspicion = 0
        self.min_suspicion = 0  # Dynamic minimum suspicion floor
        self.shares = {}
        self.hp = 100
        self.jail_hits = 0
        self.weapon = None
        self.current_town = "Gandy"
        
        # Track stats for custom endings
        self.guards_defeated = 0
        self.prison_escapes = 0

    def calculate_net_worth(self, market_prices):
        candy_val = sum(self.inventory[c] * market_prices.get(c, 0) for c in self.inventory)
        share_val = sum(count * 50 for count in self.shares.values())
        return self.cash + candy_val + share_val

class Weapon:
    def __init__(self, name, price, accuracy, power, flavor):
        self.name = name
        self.price = price
        self.accuracy = accuracy
        self.power = power
        self.flavor = flavor

WEAPONS = [
    Weapon("Soggy Licorice Whip", 30, 0.80, 1, "Stings just enough to make a rookie guard reconsider his career choices."),
    Weapon("Rusty Sugar Tongs", 70, 0.85, 2, "Heavy, sharp, and smells like stale caramel and poor decisions."),
    Weapon("Hard-Tack Stunner", 130, 0.90, 3, "Stale bread wrapped around a rock. Simple, crude, effective."),
    Weapon("The Tooth-Extractor", 220, 0.95, 4, "A brutal piece of brass hardware left over from the old dentist guild.")
]

TOWNS = {
    "Gandy": {"security": 1, "share_price": 45, "stock": ["Sour Worms", "Fudge"]},
    "Twixbury": {"security": 1, "share_price": 45, "stock": ["Sour Worms", "Fudge"]},
    "Nougate": {"security": 1, "share_price": 40, "stock": ["Fudge", "Choco-Bricks"]},
    "Simber": {"security": 1, "share_price": 50, "stock": ["Sour Worms", "Choco-Bricks"]},
    "Caramoor": {"security": 2, "share_price": 55, "stock": ["Fudge", "Choco-Bricks", "Jawbreakers"]},
    "Choc Block": {"security": 2, "share_price": 60, "stock": ["Choco-Bricks", "Jawbreakers"]},
    "Newark": {"security": 3, "share_price": 65, "stock": ["Jawbreakers", "Royal Truffles"]},
    "L'darestary": {"security": 3, "share_price": 70, "stock": ["Jawbreakers", "Royal Truffles"]}
}

CANDY_CATALOG = {
    "Sour Worms": {"base": 8, "tier": 1},
    "Fudge": {"base": 20, "tier": 1},
    "Choco-Bricks": {"base": 42, "tier": 2},
    "Jawbreakers": {"base": 85, "tier": 3},
    "Royal Truffles": {"base": 160, "tier": 4}
}

# Cynical flavour text for flavor beats
RANDOM_EVENTS = [
    "A local official looks the other way. For a fee, of course.",
    "Someone left a half-eaten Fudge on the curb. You consider selling it anyway.",
    "A guard glares at you, then realizes he isn't paid enough to care.",
    "The rain smells like burnt sugar and bad luck.",
    "John told you loyalty is expensive. You're starting to see his point."
]

WARDEN_TAUNTS = [
    "\"Five days, kid. You either pay the tax or you become part of the brickwork.\"",
    "\"No cash, no lockpick skills? Bold strategy for a small-time smuggler.\"",
    "\"The Crown doesn't care about your little sugar dream. Neither do I.\"",
    "\"You look lighter than your ledger. That's a bad combination in here.\"",
    "\"Every smuggler thinks they're special until the iron swings shut.\""
]

class Game:
    def __init__(self):
        self.player = Player()
        self.prices = {}
        self.day = 1
        self.update_prices()

    def update_prices(self):
        self.prices.clear()
        available_candies = TOWNS[self.player.current_town]["stock"]
        for candy in available_candies:
            base_price = CANDY_CATALOG[candy]["base"]
            fluctuation = random.uniform(0.85, 1.25)
            self.prices[candy] = max(4, round(base_price * fluctuation, 2))

    def add_suspicion(self, quantity):
        added_sus = 2 if quantity <= 3 else (4 if quantity <= 10 else 8)
        self.player.suspicion = min(100, self.player.suspicion + added_sus)
        print(f"\n⚠️  [Suspicion +{added_sus}] Total Heat: {self.player.suspicion}/100 (Floor: {self.player.min_suspicion})")
        self.check_guard_encounter()

    def check_guard_encounter(self):
        sus = self.player.suspicion
        if sus < 25:
            spawn_chance = 0.15
        elif sus < 60:
            spawn_chance = 0.45
        else:
            spawn_chance = 0.75

        if random.random() < spawn_chance:
            num_guards = 1 if sus < 60 else random.randint(2, 3)
            print(f"\n🚨 GUARD ALERT! {num_guards} Town Guard(s) spotted your contraband!")
            input("Press Enter to enter combat...")
            self.start_combat(num_guards)

    def start_combat(self, num_guards):
        while num_guards > 0 and self.player.jail_hits < 5:
            clear_screen()
            print("⚔️  COMBAT INITIATED!")
            print(f"Guards: {num_guards} | HP: {self.player.hp}/100 | Jail Strikes: {self.player.jail_hits}/5")
            print(f"Weapon: {self.player.weapon.name if self.player.weapon else 'Bare Fists'}\n")
            print("1. Attack")
            print("2. Bribe ($20)")
            
            choice = input("Select: ").strip()
            
            if choice == "1":
                acc = self.player.weapon.accuracy if self.player.weapon else 0.55
                power = self.player.weapon.power if self.player.weapon else 1
                
                if random.random() <= acc:
                    defeated = min(num_guards, power)
                    num_guards -= defeated
                    self.player.guards_defeated += defeated
                    print(f"\n💥 Direct hit! Knocked out {defeated} guard(s)!")
                else:
                    dmg = random.randint(5, 10) * num_guards
                    self.player.hp -= dmg
                    self.player.jail_hits += 1
                    print(f"\n❌ Missed! Guards hit back for {dmg} damage! Arrest Strike {self.player.jail_hits}/5!")
                input("Press Enter to continue...")

            elif choice == "2":
                if self.player.cash >= 20:
                    self.player.cash -= 20
                    print("\n💰 You bribed the guard and slipped away.")
                    input("Press Enter to continue...")
                    return
                else:
                    print("\nNot enough cash! The guards laugh at your empty pockets.")
                    input("Press Enter to continue...")

        if self.player.jail_hits >= 5:
            self.go_to_jail()
        else:
            clear_screen()
            print("🎉 Guards defeated! You escaped into the alleyway.")
            input("Press Enter to continue...")

    def go_to_jail(self):
        jail_days = 0
        time_limit = 5

        while jail_days < time_limit:
            clear_screen()
            print("🔒 ARRESTED! Placed in the municipal dungeons.")
            jail_days += 1
            self.day += 1
            
            # Cynical Warden Interaction
            taunt = random.choice(WARDEN_TAUNTS)
            print(f"\nWarden Vane steps up to the bars, keys jingling.")
            print(f"{taunt}")
            print(f"\n--- Day {self.day} (Jail Day {jail_days}/{time_limit}) ---\n")
            print("1. Lockpick door (50% chance)")
            print("2. Pay bail ($40)")
            print("3. Wait out the day")

            choice = input("Select: ").strip()

            if choice == "1":
                if random.random() <= 0.50:
                    print("\n🔓 Picked the lock! You broke out before Vane could turn around!")
                    self.player.jail_hits = 0
                    self.player.prison_escapes += 1
                    
                    # Each escape permanently increases suspicion floor by +15
                    self.player.min_suspicion += 15
                    self.player.suspicion = max(self.player.suspicion, self.player.min_suspicion + 20)
                    
                    print(f"⚠️  WANTED OUTLAW! Permanent suspicion floor raised to {self.player.min_suspicion}!")
                    input("Press Enter to continue...")
                    return
                else:
                    print("\n❌ Lockpick snapped. Warden Vane chuckles from down the hall.")
                    input("Press Enter to continue...")
            elif choice == "2":
                if self.player.cash >= 40:
                    self.player.cash -= 40
                    print("\n🔑 Paid your bail. Vane takes your purse with a cynical smirk.")
                    self.player.jail_hits = 0
                    self.player.suspicion = max(15, self.player.min_suspicion)
                    input("Press Enter to continue...")
                    return
                else:
                    print("\n\"That's not $40,\" Vane says flatly. \"Try again when you're solvent.\"")
                    input("Press Enter to continue...")
            elif choice == "3":
                print("\nYou sit on the damp straw, watching time run out.")
                input("Press Enter to continue...")

        # Cynical Game Over Sequence
        clear_screen()
        print("=" * 65)
        print("🔒 TIME'S UP IN THE DUNGEON.")
        print("=" * 65)
        print("\nWarden Vane unlocks the heavy door, shaking his head.")
        print("\"Five days and not a coin or a decent escape plan. Unfortunate.\"")
        print("\nTwo heavy guards escort you up the stone stairwell toward the main courtyard.")
        print("The Crown doesn't waste resources on bankrupt smugglers.")
        print("\n💀 EXECUTED BY TOWN AUTHORITY. GAME OVER.")
        print("=" * 65)
        sys.exit()

    def blacksmith_menu(self):
        clear_screen()
        print("🗡️  --- LOCAL BLACKSMITH ---")
        for i, w in enumerate(WEAPONS, 1):
            print(f"{i}. {w.name} - ${w.price} | Acc: {int(w.accuracy*100)}% | Defeats: {w.power} guard(s)")
            print(f"    └─ \"{w.flavor}\"")
        print("5. Leave\n")

        choice = input("Buy (1-4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            w = WEAPONS[int(choice) - 1]
            if self.player.cash >= w.price:
                self.player.cash -= w.price
                self.player.weapon = w
                print(f"\n✅ Bought and equipped {w.name}!")
            else:
                print("\n❌ The blacksmith eyes your thin purse. \"No credit in this shop.\"")
            input("Press Enter to continue...")

    def main_loop(self):
        show_lore_and_guide()
        
        while True:
            clear_screen()
            net_worth = self.player.calculate_net_worth(self.prices)
            
            # Victory Condition
            if net_worth >= 1000:
                show_victory_screen(net_worth, self.player.guards_defeated, self.player.prison_escapes)
                break

            print("="*50)
            print("🍬 SWEET STASH: UNDERGROUND CANDY EMPIRE 🍬")
            print("="*50)
            print(f"Day {self.day} | Location: {self.player.current_town}")
            print(f"Cash: ${self.player.cash:.2f} | Net Worth: ${net_worth:.2f}")
            print(f"Suspicion: {self.player.suspicion}/100 (Min Floor: {self.player.min_suspicion})")
            print(f"Inventory: {self.player.inventory}")
            print(f"Weapon: {self.player.weapon.name if self.player.weapon else 'Bare Fists'}")
            
            # Subtle ambient flavor line
            if random.random() < 0.30:
                print(f"💬 \"{random.choice(RANDOM_EVENTS)}\"")
                
            print("-" * 50)
            print("1. Trade Candy (Local Market)")
            print("2. Visit Blacksmith")
            print("3. Travel to Next Town")
            print("4. Buy Town Shares ($50)")
            print("5. Quit\n")

            choice = input("Enter choice (1-5): ").strip()

            if choice == "1":
                clear_screen()
                print(f"--- Market in {self.player.current_town} ---")
                
                print("=" * 45)
                print(f"💼 CASH: ${self.player.cash:.2f}")
                print(f"⚠️  SUSPICION: {self.player.suspicion}/100 (Floor: {self.player.min_suspicion})")
                print("📦 YOUR CURRENT STOCK:")
                for item, count in self.player.inventory.items():
                    print(f"   • {item}: {count}")
                print("=" * 45)

                print("\nLOCAL MARKET PRICES:")
                for c in TOWNS[self.player.current_town]["stock"]:
                    print(f"- {c}: ${self.prices[c]:.2f}")
                
                action = input("\n1. Buy | 2. Sell: ").strip()
                candy_input = input("Candy Name: ").strip().title()
                
                if candy_input in self.prices:
                    try:
                        qty = int(input("Quantity: ") or 0)
                    except ValueError:
                        qty = 0
                        print("\nInvalid quantity! Enter numbers only.")

                    if qty > 0:
                        if action == "1":
                            cost = self.prices[candy_input] * qty
                            if self.player.cash >= cost:
                                self.player.cash -= cost
                                self.player.inventory[candy_input] += qty
                                print(f"\nBought {qty} x {candy_input}!")
                                self.add_suspicion(qty)
                            else:
                                print("\nNot enough cash!")
                                
                        elif action == "2":
                            if self.player.inventory[candy_input] >= qty:
                                earned = self.prices[candy_input] * qty
                                self.player.cash += earned
                                self.player.inventory[candy_input] -= qty
                                print(f"\nSold {qty} x {candy_input} for ${earned:.2f}!")
                                self.add_suspicion(qty)
                            else:
                                print("\nNot enough inventory!")
                else:
                    print("\nThat item is not produced or traded in this town!")
                input("\nPress Enter to continue...")

            elif choice == "2":
                self.blacksmith_menu()

            elif choice == "3":
                clear_screen()
                print("--- Map Travel ---")
                towns = list(TOWNS.keys())
                for i, t in enumerate(towns, 1):
                    stock_str = ", ".join(TOWNS[t]["stock"])
                    print(f"{i}. {t} (Sec: {TOWNS[t]['security']}) - Sells: [{stock_str}]")
                t_choice = input("\nSelect destination: ").strip()
                
                if t_choice.isdigit() and 1 <= int(t_choice) <= len(towns):
                    self.player.current_town = towns[int(t_choice) - 1]
                    self.day += 1
                    self.update_prices()
                    self.player.suspicion = max(self.player.min_suspicion, self.player.suspicion - 3)
                    print(f"\nTraveled to {self.player.current_town}. (Suspicion lowered, Floor: {self.player.min_suspicion})")
                    input("Press Enter to continue...")

            elif choice == "4":
                t = self.player.current_town
                price = TOWNS[t]["share_price"]
                if self.player.cash >= price:
                    self.player.cash -= price
                    self.player.shares[t] = self.player.shares.get(t, 0) + 1
                    print(f"\nBought 1 Share in {t}!")
                else:
                    print("\nNot enough cash!")
                input("Press Enter to continue...")

            elif choice == "5":
                print("Exiting game.")
                break

if __name__ == "__main__":
    game = Game()
    game.main_loop()
