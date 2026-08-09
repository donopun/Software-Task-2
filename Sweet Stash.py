import random
import sys

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
        self.shares = {}
        self.hp = 100
        self.jail_hits = 0
        self.weapon = None
        self.current_town = "Gandy"

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
    Weapon("Soggy Licorice Whip", 30, 0.80, 1, "Stings just enough to make a rookie guard reconsider his career."),
    Weapon("Rusty Sugar Tongs", 70, 0.85, 2, "Heavy, sharp, and smells like stale caramel."),
    Weapon("Hard-Tack Stunner", 130, 0.90, 3, "Stale bread wrapped around a rock. Simple and effective."),
    Weapon("The Tooth-Extractor", 220, 0.95, 4, "A brutal piece of brass hardware left over from the old dentist guild.")
]

TOWNS = {
    "Gandy": {
        "security": 1, 
        "share_price": 45, 
        "stock": ["Sour Worms", "Fudge"]
    },
    "Twixbury": {
        "security": 1, 
        "share_price": 45, 
        "stock": ["Sour Worms", "Fudge"]
    },
    "Nougate": {
        "security": 1, 
        "share_price": 40, 
        "stock": ["Fudge", "Choco-Bricks"]
    },
    "Simber": {
        "security": 1, 
        "share_price": 50, 
        "stock": ["Sour Worms", "Choco-Bricks"]
    },
    "Caramoor": {
        "security": 2, 
        "share_price": 55, 
        "stock": ["Fudge", "Choco-Bricks", "Jawbreakers"]
    },
    "Choc Block": {
        "security": 2, 
        "share_price": 60, 
        "stock": ["Choco-Bricks", "Jawbreakers"]
    },
    "Newark": {
        "security": 3, 
        "share_price": 65, 
        "stock": ["Jawbreakers", "Royal Truffles"]
    },
    "L'darestary": {
        "security": 3, 
        "share_price": 70, 
        "stock": ["Jawbreakers", "Royal Truffles"]
    }
}

CANDY_CATALOG = {
    "Sour Worms": {"base": 8, "tier": 1},
    "Fudge": {"base": 20, "tier": 1},
    "Choco-Bricks": {"base": 42, "tier": 2},
    "Jawbreakers": {"base": 85, "tier": 3},
    "Royal Truffles": {"base": 160, "tier": 4}
}

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
        added_sus = 1 if quantity <= 3 else (2 if quantity <= 10 else 4)
        self.player.suspicion = min(100, self.player.suspicion + added_sus)
        
        print(f"⚠️  [Suspicion +{added_sus}] Total Heat: {self.player.suspicion}/100")
        self.check_guard_encounter()

    def check_guard_encounter(self):
        sus = self.player.suspicion
        if sus < 35:
            spawn_chance = 0.0
        elif sus < 65:
            spawn_chance = 0.25
        else:
            spawn_chance = 0.55

        if random.random() < spawn_chance:
            num_guards = 1 if sus < 65 else random.randint(2, 3)
            print(f"\n🚨 GUARD ALERT! {num_guards} Town Guard(s) spotted your contraband!")
            self.start_combat(num_guards)

    def start_combat(self, num_guards):
        print("\n⚔️  COMBAT INITIATED!")
        while num_guards > 0 and self.player.jail_hits < 5:
            print(f"\nGuards: {num_guards} | HP: {self.player.hp}/100 | Jail Strikes: {self.player.jail_hits}/5")
            print(f"Weapon: {self.player.weapon.name if self.player.weapon else 'Bare Fists'}")
            print("1. Attack")
            print("2. Bribe ($20)")
            
            choice = input("Select: ").strip()
            
            if choice == "1":
                acc = self.player.weapon.accuracy if self.player.weapon else 0.55
                power = self.player.weapon.power if self.player.weapon else 1
                
                if random.random() <= acc:
                    num_guards -= power
                    num_guards = max(0, num_guards)
                    print(f"💥 Direct hit! Knocked out {power} guard(s)!")
                else:
                    print("❌ Missed!")
                    dmg = random.randint(5, 10) * num_guards
                    self.player.hp -= dmg
                    self.player.jail_hits += 1
                    print(f"🗡️  Guards hit back for {dmg} damage! Arrest Strike {self.player.jail_hits}/5!")

            elif choice == "2":
                if self.player.cash >= 20:
                    self.player.cash -= 20
                    print("💰 You bribed the guard and slipped away.")
                    return
                else:
                    print("Not enough cash!")

        if self.player.jail_hits >= 5:
            self.go_to_jail()
        else:
            print("🎉 Guards defeated! You escaped into the alleyway.")

    def go_to_jail(self):
        print("\n🔒 ARRESTED! Placed in the municipal dungeons.")
        jail_days = 0
        time_limit = 5

        while jail_days < time_limit:
            jail_days += 1
            self.day += 1
            print(f"\n--- Day {self.day} (Jail Day {jail_days}/{time_limit}) ---")
            print("1. Lockpick door (50% chance)")
            print("2. Pay bail ($40)")
            print("3. Wait")

            choice = input("Select: ").strip()

            if choice == "1":
                if random.random() <= 0.50:
                    print("🔓 Picked the lock! You broke out!")
                    self.player.jail_hits = 0
                    self.player.suspicion = 10
                    return
                else:
                    print("❌ Failed lockpick attempt.")
            elif choice == "2":
                if self.player.cash >= 40:
                    self.player.cash -= 40
                    print("🔑 Paid your bail. You are released!")
                    self.player.jail_hits = 0
                    self.player.suspicion = 10
                    return
                else:
                    print("Not enough cash for bail!")

        print("\n💀 EXECUTED BY TOWN AUTHORITY. GAME OVER.")
        sys.exit()

    def blacksmith_menu(self):
        print("\n🗡️  --- LOCAL BLACKSMITH ---")
        for i, w in enumerate(WEAPONS, 1):
            print(f"{i}. {w.name} - ${w.price} | Acc: {int(w.accuracy*100)}% | Defeats: {w.power} guard(s)")
            print(f"   └─ \"{w.flavor}\"")
        print("5. Leave")

        choice = input("Buy (1-4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            w = WEAPONS[int(choice) - 1]
            if self.player.cash >= w.price:
                self.player.cash -= w.price
                self.player.weapon = w
                print(f"✅ Bought and equipped {w.name}!")
            else:
                print("❌ Not enough money!")

    def main_loop(self):
        print("="*50)
        print("🍬 SWEET STASH: UNDERGROUND CANDY EMPIRE 🍬")
        print("="*50)
        
        while True:
            net_worth = self.player.calculate_net_worth(self.prices)
            if net_worth >= 1000:
                print(f"\n🏆 VICTORY! Net Worth hit ${net_worth:.2f}! Your empire dominates the kingdom!")
                break

            print(f"\n--- Day {self.day} | Location: {self.player.current_town} ---")
            print(f"Cash: ${self.player.cash:.2f} | Net Worth: ${net_worth:.2f} | Suspicion: {self.player.suspicion}/100")
            print(f"Inventory: {self.player.inventory}")
            print(f"Weapon: {self.player.weapon.name if self.player.weapon else 'Bare Fists'}")
            print("-" * 50)
            print("1. Trade Candy (Local Market)")
            print("2. Visit Blacksmith")
            print("3. Travel to Next Town")
            print("4. Buy Town Shares ($50)")
            print("5. Quit")

            choice = input("Enter choice (1-5): ").strip()

            if choice == "1":
                print(f"\n--- Market in {self.player.current_town} ---")
                for c in TOWNS[self.player.current_town]["stock"]:
                    print(f"- {c}: ${self.prices[c]:.2f}")
                
                action = input("\n1. Buy | 2. Sell: ").strip()
                candy_input = input("Candy Name: ").strip().title()
                
                if candy_input in self.prices:
                    qty = int(input("Quantity: ") or 0)
                    if qty <= 0:
                        continue
                        
                    if action == "1":
                        cost = self.prices[candy_input] * qty
                        if self.player.cash >= cost:
                            self.player.cash -= cost
                            self.player.inventory[candy_input] += qty
                            print(f"Bought {qty} x {candy_input}!")
                            self.add_suspicion(qty)
                        else:
                            print("Not enough cash!")
                            
                    elif action == "2":
                        if self.player.inventory[candy_input] >= qty:
                            earned = self.prices[candy_input] * qty
                            self.player.cash += earned
                            self.player.inventory[candy_input] -= qty
                            print(f"Sold {qty} x {candy_input} for ${earned:.2f}!")
                            self.add_suspicion(qty)
                        else:
                            print("Not enough inventory!")
                else:
                    print("That item is not produced or traded in this town!")

            elif choice == "2":
                self.blacksmith_menu()

            elif choice == "3":
                print("\n--- Map Travel ---")
                towns = list(TOWNS.keys())
                for i, t in enumerate(towns, 1):
                    stock_str = ", ".join(TOWNS[t]["stock"])
                    print(f"{i}. {t} (Sec: {TOWNS[t]['security']}) - Sells: [{stock_str}]")
                t_choice = input("Select destination: ").strip()
                
                if t_choice.isdigit() and 1 <= int(t_choice) <= len(towns):
                    self.player.current_town = towns[int(t_choice) - 1]
                    self.day += 1
                    self.update_prices()
                    self.player.suspicion = max(0, self.player.suspicion - 6)
                    print(f"Traveled to {self.player.current_town}. (Suspicion reduced -6)")

            elif choice == "4":
                t = self.player.current_town
                price = TOWNS[t]["share_price"]
                if self.player.cash >= price:
                    self.player.cash -= price
                    self.player.shares[t] = self.player.shares.get(t, 0) + 1
                    print(f"Bought 1 Share in {t}!")
                else:
                    print("Not enough cash!")

            elif choice == "5":
                print("Exiting game.")
                break

if __name__ == "__main__":
    game = Game()
    game.main_loop()
