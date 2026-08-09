# Data Dictionary — Sweet Stash

## 1. Player Entity (`Player` Class)

| Variable / Attribute | Data Type | Format / Range | Description | Validation / Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `cash_balance` | Float | >= 0.00 | Current available funds for trading and purchasing shares. | Cannot be negative. |
| `candy_inventory` | Dictionary | `{String: Integer}` | Quantities of each candy type currently held. | Quantities >= 0. |
| `empire_wealth` | Float | >= 0.00 | Calculated sum of cash balance, inventory value, and district shares. | Dynamic property. |
| `total_suspicion` | Integer | 0 to 100 | Cumulative heat level across all regions. | Clamped between 0 and 100. |
| `min_suspicion_floor` | Integer | >= 0 | Minimum heat floor permanently raised after prison escapes. | Cannot decrease once raised. |



## 2. Region / Location Entity (`Region` Class)

| Variable / Attribute | Data Type | Format / Range | Description | Validation / Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `name` | String | Max 20 chars | Unique identifier for a region (e.g., `'Gandy'`, `'Newark'`). | Non-empty string key. |
| `market_prices` | Dictionary | `{String: Float}` | Buying/selling prices for sweets stocked in the area. | Values must be > 0.00. |
| `security_presence` | Integer | 1 to 3 | Local law enforcement level influencing guard encounters. | Integer between 1 and 3. |
| `share_price` | Float | > 0.00 | Infrastructure investment cost per regional share. | Fixed float value > 0.00. |
| `stock` | List | `[String]` | Types of candy produced and sold in this region. | Must match catalog keys. |



## 3. Non-Player Character Entity (`NPC` Class)

| Variable / Attribute | Data Type | Format / Range | Description | Validation / Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `name` | String | Max 30 chars | Identifier for the character (e.g., `'Warden Vane'`, `'Old John'`). | Non-empty string. |
| `role` | String | Max 30 chars | Functional role within the narrative/game loop. | Valid descriptor. |
| `suspicion_impact` | Integer | -20 to 20 | Modifier applied to overall heat when interacting with the NPC. | Integer range. |



## 4. Game Control Variables (`GameEngine` State)

| Variable / Attribute | Data Type | Format / Range | Description | Validation / Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `day` | Integer | >= 1 | Global turn counter tracking progression. | Integer >= 1. |
| `win_threshold` | Float | 1000.00 | Target `empire_wealth` required to trigger victory. | System constant (> 0.00). |
| `max_jail_days` | Integer | 5 | Limit of days spent in dungeon before execution sequence
