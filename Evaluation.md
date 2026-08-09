# Project Evaluation - Sweet Stash

## 1. Success Criteria Review

| Requirement / Goal | Met? | Explanation |
| :--- | :---: | :--- |
| **Object-Oriented Architecture** | Yes | Built using clear `Player`, `Region`, and `NPC` classes with encapsulated attributes and methods. |
| **Dynamic Economy System** | Yes | Market prices update across different towns, giving players a real reason to move around and trade strategically. |
| **Risk vs. Reward System** | Yes | Higher-value trade zones come with higher guard security, forcing players to balance profit against their total suspicion level. |
| **Win and Loss Conditions** | Yes | Clear termination triggers: reaching the empire wealth milestone wins the game, while hitting 100 suspicion triggers an arrest. 5 days in jail leads to game over. |
| **User Input & Error Handling** | Yes | Input validation prevents invalid entries (strings or negative numbers) from crashing the game execution loop. |

---

## 2. Project Strengths

- **OOP Design:** Grouping data into distinct objects made managing player assets, regional prices, and NPC stats much cleaner than using unstructured arrays or global variables.
- **Engaging Mechanics:** The balance between managing cash, buying regional shares, and keeping suspicion low creates a fun gameplay loop that matches the original story concept.
- **Robustness:** The application handles unexpected user inputs smoothly without terminating or corrupting saved state data.
- ** Creativity:** A genuine and light hearted adventure of subtle cynical undertones

---

## 3. Future Improvements

- **Save & Load Functionality:** Adding JSON or text file saving so players can pause and resume their progress later instead of finishing in one session.
- **Expanded Map & Random Events:** Adding more regional events (like sudden guard raids or market crashes in specific towns) to make playthroughs more unpredictable.
- **GUI Version:** Porting the text-based terminal interface over to Pygame or Tkinter for visual map navigation and graphics.
