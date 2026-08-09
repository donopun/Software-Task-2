# Testing Strategies & Test Cases — Sweet Stash

## Manual Test Matrix

| Test ID | Feature Tested | Input / Action | Expected Result | Pass / Fail |
| :--- | :--- | :--- | :--- | :--- |
| **TC01** | Player Movement | Select a valid region (e.g., move from `Gandy` to `Newark`). | `current_region` updates to `Newark`, market prices reload, and suspicion slightly drops. | **Pass** |
| **TC02** | Invalid Input Handling | Type a letter string (e.g., `"abc"`) or negative integer into a numeric menu prompt. | System catches the `ValueError`, prints a prompt error, and re-asks without crashing the game loop. | **Pass** |
| **TC03** | Buying Candy (Normal) | Purchase 5 units of candy with sufficient `cash_balance`. | Cash decreases by total cost, `candy_inventory` count increases by 5, and local heat increases. | **Pass** |
| **TC04** | Buying Candy (Insufficient Funds) | Attempt to buy 50 units of candy costing more cash than available. | Transaction is rejected with an "Insufficient Funds" warning; balances remain unchanged. | **Pass** |
| **TC05** | Selling Candy | Sell 3 units of candy currently held in inventory. | Inventory drops by 3, `cash_balance` increases by the regional market payout, and heat increments. | **Pass** |
| **TC06** | Blacksmith Gear Purchase | Purchase a weapon (e.g., `Rusty Sugar Tongs`) from the Blacksmith menu. | `cash_balance` decreases by weapon cost and player's `equipped_weapon` updates with higher accuracy/power. | **Pass** |
| **TC07** | Guard Combat & Bribe | Select `Bribe ($20.00)` or `Strike` during a guard patrol encounter. | Bribing deducts $20 and ends combat safely; striking rolls accuracy against guard count. | **Pass** |
| **TC08** | Prison Breakout & Floor Persistence | Successfully lockpick cell door (Option 1) during a jail stay. | Player escapes dungeon, and `min_suspicion_floor` permanently increases by +15. | **Pass** |
| **TC09** | Dungeon Time Out (Loss Condition) | Select Option 3 (`Wait out the day`) for 5 consecutive days in jail. | Warden Vane executes the terminal execution sequence and the program exits via `sys.exit()`. | **Pass** |
| **TC10** | Share Purchase | Purchase 1 share of local infrastructure in `Gandy`. | `shares_owned` for `Gandy` increases by 1, cash decreases by share price, and `empire_wealth` updates. | **Pass** |
| **TC11** | Win Condition Threshold | Reach or exceed $1,000.00 total `empire_wealth`. | Main loop terminates and renders custom victory screen based on total escapes and guard kills. | **Pass** |
