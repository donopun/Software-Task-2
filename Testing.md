# Testing Strategies & Test Cases - Sweet Stash

## Test Cases

| Test ID | Feature Tested | Input / Action | Expected Result | Pass / Fail |
| :--- | :--- | :--- | :--- | :---: |
| **TC01** | Player Movement | Select a valid adjacent region (e.g., move from `Gandy` to `Newark`). | `current_location` updates to `Newark` and the local price menu reloads. | Pass |
| **TC02** | Invalid Location Choice | Select a region that is not connected to the current location. | Game displays an error message and stays in the current region. | Pass |
| **TC03** | Buying Candy (Normal) | Purchase 5 units of candy with sufficient `cash_balance`. | Cash decreases by total cost, and `candy_inventory` count increases by 5. | Pass |
| **TC04** | Buying Candy (Insufficient Funds) | Attempt to buy 50 units of candy costing more cash than available. | Transaction is rejected with an "Insufficient Funds" warning; balances remain unchanged. | Pass |
| **TC05** | Selling Candy | Sell 3 units of candy currently held in inventory. | Inventory drops by 3, and `cash_balance` increases by the local regional payout. | Pass |
| **TC06** | Invalid Input Handling | Type a letter string (e.g., `"abc"`) or negative integer into a numeric menu prompt. | System catches the `ValueError`, prints a prompt error, and re-asks without crashing. | Pass |
| **TC07** | Share Purchase | Purchase 1 share of local infrastructure in `Gandy`. | `player_shares_owned` increases by 1, cash decreases by share price, and `empire_wealth` updates. | Pass |
| **TC08** | Suspicion Limit (Loss Condition) | Accumulate suspicion level to 100 via risky trading / authority interactions. | `game_over` flag sets to `True` and triggers the arrest/loss ending screen. | Pass |
| **TC09** | Win Condition Threshold | Reach or exceed the target `empire_wealth` milestone. | `game_over` flag sets to `True` and triggers the "Empire Solidified" victory screen. | Pass |
