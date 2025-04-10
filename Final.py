#!D:/miniconda/Finalae/python.exe
# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# %%
import pyNetLogo

netlogo = pyNetLogo.NetLogoLink(gui=True)
netlogo.load_model(r"C:\Users\Dharanidharan\Desktop\Computing final project\Crime analysis.nlogo")
netlogo.command('setup')

# %%
import time 

scenarios = [3, 5, 8, 10]
criminal_scenarios = [15]  

info_options = [True, False]

combined_logs = []  
summary_logs = []    

for police_count in scenarios:
    for initial_criminals in criminal_scenarios:
        for use_info in info_options:
            netlogo.command(f"set use-informants {str(use_info).lower()}")
            netlogo.command(f"set initial-police {police_count}")
            netlogo.command(f"set initial-criminals {initial_criminals}")
            netlogo.command("setup")

            
            initial_ci = netlogo.report('initial-ci-count')
            ticks = 0
            tick_data = []

            while not netlogo.report('hideout-timer >= 20') and ticks < 2000:
                netlogo.command("go")
                current_ci = netlogo.report('count turtles with [role = "ci"]')

                tick_data.append({
                    "Tick": ticks,
                    "Initial_Police": police_count,
                    "Initial_Criminals": initial_criminals,
                    "Info_Status": "With Info" if use_info else "No Info",
                    "CI_Count": current_ci,
                    "CI_Growth_Tickwise": current_ci - initial_ci,
                    "Arrested_Criminals": netlogo.report('count turtles with [role = "criminal" and arrested?]'),
                    "Hiding_Criminals": netlogo.report('count turtles with [role = "criminal" and hiding?]'),
                    "Active_Criminals": netlogo.report('count turtles with [role = "criminal" and not arrested? and not hiding?]')
                })

                ticks += 1

            final_ci = tick_data[-1]["CI_Count"]
            criminals = netlogo.report('count turtles with [role = "criminal"]')
            arrested = netlogo.report('count turtles with [role = "criminal" and arrested?]')
            hiding = netlogo.report('count turtles with [role = "criminal" and hiding?]')
            active = netlogo.report('count turtles with [role = "criminal" and not arrested? and not hiding?]')
            police = netlogo.report('count turtles with [role = "police"]')

            for row in tick_data:
                row["Initial_CI_Count"] = initial_ci
                row["Final_CI_Count"] = final_ci
                row["CI_Growth"] = final_ci - initial_ci
                row["Criminals_Total"] = criminals
                row["Criminals_Arrested"] = arrested
                row["Criminals_Hiding"] = hiding
                row["Criminals_Active"] = active
                row["Police_Total"] = police

            combined_logs.extend(tick_data)

            summary_logs.append({
                "Initial_Police": police_count,
                "Initial_Criminals": initial_criminals,
                "Info_Status": "With Info" if use_info else "No Info",
                "Initial_CI_Count": initial_ci,
                "Final_CI_Count": final_ci,
                "CI_Growth": final_ci - initial_ci,
                "Criminals_Total": criminals,
                "Criminals_Arrested": arrested,
                "Criminals_Hiding": hiding,
                "Criminals_Active": active,
                "Police_Total": police
            })

            print(f"Done: Police={police_count}, Criminals={initial_criminals}, Info={'ON' if use_info else 'OFF'}")
            time.sleep(1)


# %%

df_full = pd.DataFrame(combined_logs)
df_full = df_full[[
    "Tick", "Initial_Police", "Info_Status", "Initial_CI_Count", "CI_Count",
    "Final_CI_Count", "CI_Growth_Tickwise", "CI_Growth",
    "Criminals_Total", "Criminals_Arrested", "Criminals_Hiding", "Criminals_Active",
    "Arrested_Criminals", "Hiding_Criminals", "Active_Criminals", "Police_Total"
]]


df_full.to_csv(r"C:\Users\Dharanidharan\Desktop\Computing final project\Dataset generated\tickwise.csv", index=False)
print("Data saved to tickwise.csv")




# %%
df_summary = pd.DataFrame(summary_logs)[[
    "Initial_Police", "Info_Status", "Initial_CI_Count", "Final_CI_Count", "CI_Growth",
    "Criminals_Total", "Criminals_Arrested", "Criminals_Hiding", "Criminals_Active", "Police_Total"
]]
df_summary.to_csv(r"C:\Users\Dharanidharan\Desktop\Computing final project\Dataset generated\summary.csv", index=False)
print("Data saved to summary.csv")


# %%

df = pd.read_csv(r"C:\Users\Dharanidharan\Desktop\Computing final project\Dataset generated\tickwise.csv")
sns.set(style="whitegrid", font_scale=1.3)
plt.figure(figsize=(14, 7))


sns.lineplot(
    data=df_full,
    x="Tick",
    y="CI_Growth_Tickwise",
    hue="Initial_Police",       
    style="Info_Status",        
    dashes={"With Info": "", "No Info": (4, 2)},
    linewidth=2.5,
    markers=False,
    palette="tab10"
)

# Titles and labels
plt.title("CI Growth Over Time\n(Solid = With Info, Dashed = No Info)", fontsize=16)
plt.xlabel("Simulation Time (Ticks)", fontsize=13)
plt.ylabel("CI Growth (Relative to Initial)", fontsize=13)

plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.grid(True, linestyle="--", alpha=0.6)

# Legend
plt.legend(title="Police Count / Info Usage", title_fontsize=12, fontsize=11, loc="upper left")

plt.tight_layout()
plt.show()



# %%

df = pd.read_csv(r"C:\Users\Dharanidharan\Desktop\Computing final project\Dataset generated\summary.csv")

df['Arrest_Rate'] = df['Criminals_Arrested'] / df['Criminals_Total']

sns.set(style="whitegrid", font_scale=1.2)

plt.figure(figsize=(12, 6))  
sns.barplot(
    data=df,
    x='Initial_Police',
    y='Arrest_Rate',
    hue='Info_Status',
    palette='Set2',
    dodge=True,
    width=0.4  
)

plt.title("Arrest Rate vs Police Count (With vs Without Informants)", fontsize=14)
plt.xlabel("Initial Police", fontsize=12)
plt.ylabel("Arrest Rate", fontsize=12)
plt.ylim(0, 1)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.legend(title="Informant Use", loc='upper right', fontsize=10, title_fontsize=11)

plt.tight_layout(pad=2.0)
plt.show()



# %%
#Correlation Heatmap of All Numerical Variables
numeric_cols = df.select_dtypes(include='number')

plt.figure(figsize=(10, 8))
sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap of Simulation Variables")
plt.tight_layout()
plt.show()


# %%
netlogo.kill_workspace()

# %%



