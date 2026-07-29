# Data Dictionary - Sweet Stash

## 1. Player Entity (`Player` Class)

| Variable / Attribute | Data Type | Format / Range | Description | Validation / Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `name` | String | Max 30 chars | The identifier for the player character. | Non-empty string. |
| `current_location` | Object / String | Region reference | Tracks the player's current geographical location on the map. | Must match a valid `Region` key. |
| `cash_balance` | Float / Decimal | >= 0.00 | Current total funds available for trade and purchasing shares. | Cannot be negative. |
| `candy_inventory` | Dictionary | `{String: Integer}` | Key-value pairs mapping candy types to current stock quantities held by the player. | Quantities >= 0. |
| `empire_wealth` | Float / Decimal | >= 0.00 | Combined total value of cash balance, unsold inventory, and regional infrastructure shares owned. | Calculated property; updated on state evaluation. |
| `total_suspicion` | Integer | 0 to 100 | Cumulative regional authority awareness level across all locations. | Clamped between 0 and 100. |

## 2. Region / Location Entity (`Region` Class)

| Variable / Attribute | Data Type | Format / Range | Description | Validation / Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `region_id` | String | Max 20 chars | Unique identifier for a specific map region (e.g., `'Gandy'`, `'Newark'`, `'Twixbury'`). | Unique Primary Key. |
| `market_prices` | Dictionary | `{String: Float}` | Current local buying/selling prices for each candy item in the region. | Prices must be > 0.00. |
| `security_presence` | Integer | 1 to 10 | Numerical index representing the local law/guard presence severity in the area. | Integer between 1 and 10. |
| `share_price` | Float / Decimal | > 0.00 | Cost per share to invest capital in regional market infrastructure. | Cannot be <= 0.00. |
| `player_shares_owned` | Integer | >= 0 | Number of regional infrastructure shares owned by the player in this location. | Must be a non-negative integer. |
| `adjacent_vectors` | List | `[String]` | Directional paths/connections available to adjacent regions for traversal. | Elements must match existing `region_id` values. |

## 3. Non-Player Character Entity (`NPC` Class)

| Variable / Attribute | Data Type | Format / Range | Description | Validation / Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `npc_id` | String | Max 30 chars | Unique identifier for the NPC instance (e.g., `'John'`, `'Guard'`). | Non-empty string. |
| `assigned_region` | String | Region key | Specifies which region the NPC operates in. | Must reference a valid `region_id`. |
| `suspicion_level` | Integer | 0 to 100 | Metric tracking local authority awareness or NPC hostility toward the player. | Range 0 to 100. |
| `is_supplier` | Boolean | `True / False` | Flag determining whether the NPC can supply wholesale inventory. | Boolean value. |

## 4. Game Control Variables (`main.py` State)

| Variable / Attribute | Data Type | Format / Range | Description | Validation / Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `game_over` | Boolean | `True / False` | Flag indicating whether a terminal win/loss condition has been met. | Boolean value; defaults to `False`. |
| `win_threshold` | Float / Decimal | Dynamic target | The targeted `empire_wealth` required to achieve the "Empire Solidified" win condition. | Fixed system constant (> 0.00). |
| `max_suspicion_limit` | Integer | 100 | The threshold at which authority interception triggers the "Exile/Apprehension" loss condition. | Fixed system constant. |
