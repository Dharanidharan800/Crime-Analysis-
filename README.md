# Crime-Analysis-
NetLogo Model - Agent Based Crime Analysis 
Overview:
This simulation models a simple environment with criminals, police, and public agents. Some public agents may become CIs who help the police track down criminals.
The goal is to explore how community participation (through informants) and police deployment affect criminal activities.
The main objective of the simulation is to demonstrate how criminal activity will be affected by community informants and law enforcement.

Agent Types:
1. Criminals – Move in groups, hide when scared, and can be arrested.
2. Police – Patrol fixed zones and arrest nearby criminals.
3. Public – Ordinary citizens; some can become CIs and alert the police.

Features:
1. Criminals wander in gangs, hide after many arrests, and may respawn randomly.
2. Police patrol would arrest criminals if they are within close radius and would respond to CI alerts if they are in different zones.
3. CIs would trigger reinforcements if they detect criminals and.
4. Simulation ends if all criminals are either arrested or hide.

Key Variables:
globals:
- alert-location: Where a CI saw a criminal.
- reinforcement-request: Whether backup is needed.
- hideouts: Yellow patches for criminals to hide.
- hideout-timer: Tracks how long no criminals have been seen.

Code Usage(with NetLogo)
1. Open the simulation in NetLogo.
2. Check for "use-informants" it should be turned ON if CI functionality needed.
3. Press the "setup" button to initialize the environment.
4. Press "go" to run the simulation.

Code Usage(With Python Integration)
1. Open the python code and Make sure all packages are installed and pyNetLogo is connected.
2. Run the code
3. Code will run simulations, collect data, and generate plots.

Modes of Use:
- Standalone: The simulation can be run entirely within the NetLogo GUI.
- Python Integration: This simulation can also be controlled and analyzed using Python (e.g., through the pyNetLogo package)which can be used for data collection or plotting or analysis.

Requirements(With NetLogo):
- NetLogo = 6.2.0 

Requirments(With Python)
- NetLogo = 6.2.0
- Python = 3.7 (if using integration)
- pyNetLogo (for Python-to-NetLogo bridge)
- JAVA 
- Jpype to connect NetLogo to python
- Libraries like Matplotlib, Pandas, Seaborn for data collection, plotting etc..

Future Improvements (Optional):
1. Behavioral Profiling: Give criminals different behavioral patterns like aggressive, stealthy, or opportunistic, affecting how they move or react to police.
2. Criminal Networks: Simulate criminal gangs with internal hierarchy and communication between them.
3. CI Trust & Cooldown System: Add a “trust” level to CIs; repeated false alarms reduce trust and delay reinforcement (saves resources)
4. Citizen Reactions: Let public turtles run away or change direction when near criminals instead of arrest events for more realistic view.
