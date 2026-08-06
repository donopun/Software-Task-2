import random

# ==========================================
# CLASS DEFINITIONS
# ==========================================

class Region:
    """
    Manages each town (Gandy, Newark, Twixbury, etc.). Every location gets its own 
    market_prices, security_presence, share_price, and connected paths for traveling.
    """
    def __init__(self, region_id, base_prices, security_presence, share_price, adjacent_vectors, allows_direct_supplier=False):
        self.region_id = region_id
        self.market_prices = base_prices.copy()
        self.security_presence = security_presence  # Range: 1 to 10
        self.share_price = share_price
        self.player_shares_owned = 0
        self.adjacent_vectors = adjacent_vectors  # List of connected region names
        self.allows_direct_supplier = allows_direct_supplier

    def update_market_prices(self):
        """Simulates dynamic market trends across the underground sweet trade."""
        for candy in self.market_prices:
            fluctuation = random.uniform(0.85, 1.25)  # +/- 15 to 25% price shifts
            self.market_prices[candy] = round(self.market_prices[candy] * fluctuation, 2)


class NPC:
    """
    Handles characters like John and the local guards, tracking suspicion levels 
    and whether an NPC sells wholesale candy.
    """
    def __init__(self, npc_id, assigned_region, is_supplier=False, discount_rate=0.8):
        self.npc_id = npc_id
        self.assigned_region = assigned_region
        self.suspicion_level = 0
        self.is_supplier = is_supplier
        self.discount_rate = discount_rate  # Wholesale supplier discount

    def alert_guards(self, security_level):
        """Calculates risk of increasing suspicion based on local guard presence."""
        risk_added = random.randint(1, security_level * 2)
        self.suspicion_level = min(100, self.suspicion_level + risk_added)
        return risk_added


class Player:
    """
    Stores all the main stats like cash_balance, candy_inventory, empire_wealth, 
    and total_suspicion. Keeps track of whether you're succeeding or about to get nabbed.
    """
    def __init__(self, name, starting_region="Gandy"):
        self.name = name
        self.current_location = starting_region
        self.cash_balance = 100.00
        self.candy_inventory = {"Fudge": 0, "Gummies": 0, "ChocoBars": 0, "Nougat": 0}
        self.empire_wealth = 100.00
        self.total_suspicion = 0

    def calculate_wealth(self, current_region_obj):
        """Calculates net worth based on cash, inventory value, and share ownership."""
        inventory_value = sum(
            qty * current_region_obj.market_prices.get(candy, 0)
            for candy, qty in self.candy_inventory.items()
        )
        share_value = current_region_obj.player_shares_owned * current_region_obj.share_price
        self.empire_wealth = round(self.cash_balance + inventory_value + share_value, 2)
        return self.empire_wealth

    def move(self, target_region):
        """Updates player location across kingdom travel vectors."""
        self.current_location = target_region
        print(f"\n[TRAVEL] You drag your feet into {target_region}. Another town, another set of guards to avoid.")

    def trade_candy(self, region, candy_type, quantity, is_buying):
        """Handles buying and selling of black-market sweet treats."""
        unit_price = region.market_prices.get(candy_type, 0)

        if is_buying:
            total_cost = unit_price * quantity
            if total_cost > self.cash_balance:
                print("\n[ERROR] You're broke. Try trading within your actual budget.")
                return False
            self.cash_balance -= total_cost
            self.candy_inventory[candy_type] += quantity
            print(f"\n[TRADE] Handed over ${total_cost:.2f} for {quantity}x {candy_type}. Hope it sells before it melts.")
        else:
            if self.candy_inventory.get(candy_type, 0) < quantity:
                print("\n[ERROR] You can't sell what you don't have. Nice try though.")
                return False
            total_earnings = unit_price * quantity
            self.cash_balance += total_earnings
            self.candy_inventory[candy_type] -= quantity
            print(f"\n[TRADE] Unloaded {quantity}x {candy_type} onto the locals for ${total_earnings:.2f}.")
        
        return True

    def buy_wholesale(self, supplier_npc, region, candy_type, quantity):
        """Direct supplier dealing in industrial zones like Newark."""
        base_price = region.market_prices.get(candy_type, 0)
        wholesale_price = round(base_price * supplier_npc.discount_rate, 2)
        total_cost = wholesale_price * quantity

        if total_cost > self.cash_balance:
            print("\n[ERROR] The factory cartel doesn't do hand-outs or IOUs. Come back with real cash.")
            return False

        self.cash_balance -= total_cost
        self.candy_inventory[candy_type] += quantity
        print(f"\n[DEAL] Bought {quantity}x {candy_type} off {supplier_npc.npc_id} @ ${wholesale_price:.2f}/unit (${total_cost:.2f} total). Definitely don't ask where they got it.")
        return True

    def buy_shares(self, region, quantity):
        """Acquires physical property shares in towns to build a physical candy empire."""
        total_cost = region.share_price * quantity
        if total_cost > self.cash_balance:
            print("\n[ERROR] You can't afford to buy out this town yet. Stick to small-time deals.")
            return False
        
        self.cash_balance -= total_cost
        region.player_shares_owned += quantity
        print(f"\n[EMPIRE] Bought {quantity} share(s) in {region.region_id} for ${total_cost:.2f}. You now legally own a piece of the place banning you.")
        return True


# ==========================================
# GAME INITIALISATION & STORY SETUP
# ==========================================

def display_prologue():
    """Prints narrative introduction reflecting the cynical backstory."""
    print("=" * 70)
    print("                  SWEET STASH: VIGILANTE CANDY EMPIRE            ")
    print("=" * 70)
    print("PROLOGUE:")
    print("You flunked every single apprenticeship in the Mountain Village.")
    print("Naturally, your parents were thrilled. While loafing around an abandoned")
    print("waterway, you met John—a sketchy guy who handed you a piece of banned candy.")
    print("\nYou ate it. It was delicious. You then made the genius mistake of leaving")
    print("fudge crumbs on your desk. Your zealot parents threw a historic rage fit")
    print("and kicked you out on the spot.")
    print("\nWith $100 in your pocket and John's dubious advice ringing in your ears,")
    print("you head into the realm to build a candy empire out of pure spite.")
    print("=" * 70)


def initialize_game():
    """Initialises kingdom regions, NPCs, and the player object."""
    regions = {
        "Gandy": Region("Gandy", {"Fudge": 5.0, "Gummies": 2.0, "ChocoBars": 8.0, "Nougat": 4.0}, security_presence=2, share_price=50.0, adjacent_vectors=["Newark", "Twixbury", "L'darestary"]),
        "Newark": Region("Newark", {"Fudge": 3.0, "Gummies": 1.5, "ChocoBars": 12.0, "Nougat": 3.0}, security_presence=8, share_price=120.0, adjacent_vectors=["Gandy", "Caramoor", "Nougate"], allows_direct_supplier=True),
        "Twixbury": Region("Twixbury", {"Fudge": 8.0, "Gummies": 4.0, "ChocoBars": 6.0, "Nougat": 5.0}, security_presence=4, share_price=75.0, adjacent_vectors=["Gandy", "Caramoor", "Simber"]),
        "Caramoor": Region("Caramoor", {"Fudge": 6.0, "Gummies": 3.0, "ChocoBars": 15.0, "Nougat": 7.0}, security_presence=5, share_price=150.0, adjacent_vectors=["Newark", "Twixbury", "Choc Block"]),
        "Nougate": Region("Nougate", {"Fudge": 4.0, "Gummies": 2.5, "ChocoBars": 10.0, "Nougat": 2.0}, security_presence=3, share_price=80.0, adjacent_vectors=["Newark", "Choc Block"]),
        "Choc Block": Region("Choc Block", {"Fudge": 7.0, "Gummies": 5.0, "ChocoBars": 18.0, "Nougat": 9.0}, security_presence=6, share_price=180.0, adjacent_vectors=["Caramoor", "Nougate"]),
        "L'darestary": Region("L'darestary", {"Fudge": 9.0, "Gummies": 3.5, "ChocoBars": 11.0, "Nougat": 6.0}, security_presence=3, share_price=95.0, adjacent_vectors=["Gandy", "Simber"]),
        "Simber": Region("Simber", {"Fudge": 5.5, "Gummies": 6.0, "ChocoBars": 14.0, "Nougat": 8.0}, security_presence=5, share_price=110.0, adjacent_vectors=["Twixbury", "L'darestary"])
    }

    npcs = {
        "John": NPC("John (Suspicious Contact)", "Gandy", is_supplier=True, discount_rate=0.85),
        "Newark_Wholesaler": NPC("Factory Syndicate", "Newark", is_supplier=True, discount_rate=0.65),
        "Guard": NPC("Royal Guards", "All", is_supplier=False)
    }

    display_prologue()
    player_name = input("\nEnter your vigilante trader alias: ").strip()
    if not player_name:
        player_name = "Exiled Flunkout"
    
    player = Player(player_name, "Gandy")
    return regions, npcs, player


# ==========================================
# MAIN EXECUTION LOOP
# ==========================================

def main():
    regions, npcs, player = initialize_game()
    WIN_THRESHOLD = 1000.00
    MAX_SUSPICION = 100

    game_over = False

    while not game_over:
        current_region = regions[player.current_location]
        current_region.update_market_prices()
        player.calculate_wealth(current_region)

        # Status Display
        print("\n" + "=" * 55)
        print(f"ALIAS: {player.name} | CURRENT TOWN: {current_region.region_id}")
        print(f"CASH: ${player.cash_balance:.2f} | NET WEALTH: ${player.empire_wealth:.2f}")
        print(f"SUSPICION: {player.total_suspicion}/{MAX_SUSPICION} | GUARD DENSITY: {current_region.security_presence}/10")
        print("-" * 55)
        print(f"Stash: {player.candy_inventory}")
        print(f"Local Prices: {current_region.market_prices}")
        print(f"Town Ownership: {current_region.player_shares_owned} shares (${current_region.share_price}/share)")
        print("=" * 55)

        # Menu
        print("\nWhat's the move?")
        print("1. Trade Candy (Market)")
        print("2. Travel to Another Town")
        print("3. Buy Market Infrastructure Shares")
        if current_region.allows_direct_supplier:
            print("4. Talk to Factory Syndicate (Direct Wholesale)")
            print("5. Give Up & Retire")
        else:
            print("4. Give Up & Retire")

        choice = input("\nSelect choice (1-5): ").strip()

        if choice == "1":
            action = input("Buy or Sell? (b/s): ").strip().lower()
            candy = input("Select candy (Fudge / Gummies / ChocoBars / Nougat): ").strip()
            
            if candy in current_region.market_prices:
                try:
                    qty = int(input("Enter quantity: "))
                    if qty > 0:
                        is_buying = (action == 'b')
                        if player.trade_candy(current_region, candy, qty, is_buying):
                            added_risk = npcs["Guard"].alert_guards(current_region.security_presence)
                            player.total_suspicion += added_risk
                            print(f"[SUSPICION] Guard eyes on you! Suspicion +{added_risk}.")
                    else:
                        print("[ERROR] Enter a positive number.")
                except ValueError:
                    print("[ERROR] That isn't a valid number.")
            else:
                print("[ERROR] Never heard of that candy in this market.")

        elif choice == "2":
            print(f"\nConnected towns from {current_region.region_id}: {current_region.adjacent_vectors}")
            dest = input("Enter destination: ").strip()
            if dest in current_region.adjacent_vectors:
                player.move(dest)
            else:
                print("[ERROR] There isn't a road leading there directly.")

        elif choice == "3":
            try:
                shares = int(input(f"Buy shares in {current_region.region_id} @ ${current_region.share_price}/share: "))
                if shares > 0:
                    player.buy_shares(current_region, shares)
                else:
                    print("[ERROR] Must buy at least 1 share.")
            except ValueError:
                print("[ERROR] Invalid number format.")

        elif choice == "4" and current_region.allows_direct_supplier:
            candy = input("Select wholesale candy (Fudge / Gummies / ChocoBars / Nougat): ").strip()
            if candy in current_region.market_prices:
                try:
                    qty = int(input("Enter wholesale quantity: "))
                    if qty > 0:
                        if player.buy_wholesale(npcs["Newark_Wholesaler"], current_region, candy, qty):
                            added_risk = npcs["Guard"].alert_guards(current_region.security_presence + 2)
                            player.total_suspicion += added_risk
                            print(f"[ALERT] Industrial guards noticed the bulk transaction! Suspicion +{added_risk}!")
                except ValueError:
                    print("[ERROR] Enter a valid integer.")

        elif (choice == "4" and not current_region.allows_direct_supplier) or choice == "5":
            print("\nYou decided the candy life wasn't for you after all. Game over.")
            game_over = True

        else:
            print("\n[ERROR] Invalid option.")

        # Check Win / Loss Conditions
        if player.total_suspicion >= MAX_SUSPICION:
            print("\n" + "!" * 60)
            print("GAME OVER! The Royal Guards caught you red-handed with a pocket full of gummies.")
            print("Your stash was seized, and you're serving time in the kingdom dungeons.")
            print("!" * 60)
            game_over = True
        elif player.empire_wealth >= WIN_THRESHOLD:
            print("\n" + "*" * 60)
            print("VICTORY! You bought up enough of the realm to become untouchable.")
            print(f"With ${player.empire_wealth:.2f} in empire wealth, even the aristocrats can't ban your sweets now.")
            print("*" * 60)
            game_over = True

if __name__ == "__main__":
    main()
