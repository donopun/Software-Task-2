# Designing Characters and Environment

## Characters

Protag - You are kicked out of your village for eating candy and now you decide to run a candy empire, being a vigilante that gives sweet treats to everyone that wants. Surprisingly enough, this practice is quite prevalant (hence you finding the candy in thef irst place), so you must compete with rival establishments to serve the best candy

Your Parents - Briefly shown, they are zealous towards candy and somewhat heartbroken but mostly furious that you are eating candy.

John - He introduces you as a supplier to where you can produce and get some candy. He lets you enter the market and trade candy to people and advises you certain tips. It's best to be suspicious of this guy, as there's no such thing as a free lunch, let alone a free candy.

## Environment

Context - In this world, mass production of candy and sweets were discovered rather early. Due to massive portions of the peasant class beocming addicted to cheap sweets, all the reigning kingdoms decided to brutally ban candy, causing an undercover trade of 'vigilantes' - or demonic betrayers of the peace of the realm according to the aristocracy.

Mountain Village - This is your hometown. You were a 'cultured' student, according to your parents, but really you were flunking your apprenticeships and miserably failed actually mastering a craft. This caused great tension inside your household, so you started hanging around the outskirts and you found john in an abandoned waterway. He offers you some candy, and you oblige. Seeing that you have nothing better to do, you ask him how to start selling candy and he introduces you to a market. Once returning, you made the blunder of leaving some candy crumbs in your living quarters, as to which your parents find. You underestimated how badly they hate candy, and considering your utter uselessness you were abruptly exiled.

Gandy - This is the main city bordering your town. John shows you the ropes and you start moving some small time trades, after this, you are mostly left to your own devices.

Newark - This is the premier proto-industrial area for making candy. You can buy directly from suppliers outside of the market here, if you are a big time dealer, but mostly the area is fiercely guarded and trying to not provoke an army ruining their empire. 

Various other areas - Other areas like L'darestary, Simber, Twixbury, Nougate, Choc Block and Caramoor are where you constantly travel to and make your empire. Once you get rich enough, you can buy shares of these areas and make a physical empire, and eventually draw the attention of the authorities.

## Rationale

For the protagonist, I tried to make it slightly relatable that he was in a miserable situation to leave his family, while still exciting the player with some household conflicts in a short and punchy way to establish the motivations and gameplay itself. Also, I started here to develop the balance between parody and realistically parallelling actual illegial trades in real life, creating a concise and engaging story for players.

## Development & OOP Implementation

### Building the Game Logic
After getting the story down, I started writing the Python code using OOP classes to keep everything organized instead of dumping it into one massive script.

1. **Player Class:** Stores all the main stats like `cash_balance`, `candy_inventory`, `empire_wealth`, and `total_suspicion`. This keeps track of whether you are winning or about to get caught by authorities.
2. **Region Class:** Manages each town (`Gandy`, `Newark`, `Twixbury`, etc.). Every location gets its own `market_prices`, `security_presence`, `share_price`, and connected paths for traveling.
3. **NPC Class:** Handles characters like John and the local guards, tracking suspicion levels and whether an NPC sells wholesale candy.


## Problems & Solutions During Coding

### Issue 1: Game Crashing on Inputs
* **The Problem:** Typing letters instead of numbers or entering negative values into menus broke the code with a `ValueError` and crashed the whole game loop.
* **The Solution:** Wrapped input prompts with `try/except` blocks and `if/else` checks. Invalid inputs now trigger a quick error message and ask you to try again without stopping the program.

### Issue 2: Messy Variable Scope
* **The Problem:** Functions inside the player code tried to modify global variables directly, which got chaotic when moving between regions.
* **The Solution:** Passed object references straight into methods, like passing the current `Region` object into `Player.trade_candy()`. This kept variables neatly self-contained within their respective classes.



## Testing & Reflection

- **Market Balancing:** Adjusted price ranges across regions so moving between towns like Newark and Gandy actually pays off and makes taking on extra suspicion worth it.
- **Final Thoughts:** Moving to an OOP setup made managing all the separate pieces like prices, cash, and shares much cleaner than running standard linear code.




