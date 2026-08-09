# Class Diagram & Object Architecture

The system is structured using Object-Oriented Programming (OOP) across five primary classes to encapsulate game state, regional data, combat mechanics, and character interactions:

* **`GameEngine`:** Manages execution flow, dynamic market recalibration, combat logic, and win/loss terminal state evaluations.
* **`Player`:** Tracks inventory, cash, global suspicion, minimum suspicion floor, combat stats, and calculates dynamic net worth.
* **`Region`:** Stores local candy stocks, security levels, share costs, and dynamic market prices.
* **`NPC`:** Handles non-player characters (e.g., Warden Vane, Old John) and contextual dialogue interactions.
* **`Weapon`:** Stores stats for offensive gear obtainable at the blacksmith (accuracy, power, flavor text).

<img width="432" height="558" alt="Screenshot 2026-08-09 at 11 50 20 pm" src="https://github.com/user-attachments/assets/997d53dd-6f01-49ad-aefc-ed9c676fb56d" />




