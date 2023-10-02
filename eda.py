import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

dtype_dict = {
    4: 'str', 6: 'str', 31: 'str', 33: 'str', 61: 'str',
    62: 'str', 63: 'str', 76: 'str', 79: 'str', 90: 'str',
    92: 'str', 94: 'str', 96: 'str', 114: 'str', 115: 'str', 121: 'str'
}

data = pd.read_csv("globalterrorismdb_0718dist.csv", encoding="latin1", dtype=dtype_dict)
Terror = pd.DataFrame(data)

print("Data has been successfully imported")

Terror = Terror[["iyear", "imonth", "iday", "country_txt", "region_txt", "provstate", "city",
                 "latitude", "longitude", "location", "summary", "attacktype1_txt",
                 "targtype1_txt", "gname", "motive", "weaptype1_txt", "nkill", "nwound", "addnotes"]]

# Rename columns
Terror.rename(columns={"iyear": "Year", "imonth": "Month", "iday": "Day", "country_txt": "Country",
                       "region_txt": "Region", "provstate": "Province/State", "city": "City",
                       "latitude": "Latitude", "longitude": "Longitude", "location": "Location",
                       "summary": "Summary", "attacktype1_txt": "Attack Type", "targtype1_txt": "Target Type",
                       "gname": "Group Name", "motive": "Motive", "weaptype1_txt": "Weapon Type",
                       "nkill": "Killed", "nwound": "Wounded", "addnotes": "Add Notes"}, inplace=True)

# # Fill missing values in "Killed" and "Wounded" columns with 0
Terror["Killed"] = Terror["Killed"].fillna(0)
Terror["Wounded"] = Terror["Wounded"].fillna(0)

Terror["Casualty"] = Terror["Killed"] + Terror["Wounded"]

# Explore the data
show = Terror.head()
print(show)

# Display information about the DataFrame
showdata = Terror.info()
print(showdata)

attacks = Terror["Year"].value_counts(dropna=False).sort_index().to_frame().reset_index()

# Rename columns
attacks.rename(columns={"index": "Year", "Year": "Attacks"}, inplace=True)

attacks.set_index("Attacks", inplace=True)

print(Terror.head())
attacks.plot(kind="bar", color="cornflowerblue", figsize=(15, 6), fontsize=13)
plt.title("Timeline of Attacks", fontsize=15)
plt.xlabel("Years", fontsize=15)
plt.ylabel("Number of Attacks", fontsize=15)
plt.show()

yc = Terror[["Year", "Casualty"]].groupby("Year").sum()
print(yc.head())

yc.plot(kind="bar",color="cornflowerblue",figsize=(15,6))
plt.title("Year wise Casualties",fontsize=13)
plt.xlabel("Years",fontsize=13)
plt.xticks(fontsize=12)
plt.ylabel("Number of Casualties",fontsize=13)
plt.show()

yk = Terror[["Year", "Killed"]].groupby("Year").sum()
yw = Terror[["Year", "Wounded"]].groupby("Year").sum()

fig1, ax1 = plt.subplots(figsize=(15, 6))
yk.plot(kind="bar", color="cornflowerblue", ax=ax1)
ax1.set_title("People Killed in each Year")
ax1.set_xlabel("Years")
ax1.set_ylabel("Number of People Killed")

plt.show()

fig2, ax2 = plt.subplots(figsize=(15, 6))
yw.plot(kind="bar", color="cornflowerblue", ax=ax2)
ax2.set_title("People Wounded in each Year")
ax2.set_xlabel("Years")
ax2.set_ylabel("Number of People Wounded")

plt.show()

reg=pd.crosstab(Terror.Year,Terror.Region)
reg.head()
color_dict = {
    'Africa': 'blue',
    'Central America & Caribbean': 'green',
    'Central Asia': 'red',
    'East Asia': 'purple',
    'Eastern Europe': 'orange',
    'Middle East & North Africa': 'brown',
    'North America': 'pink',
    'Oceania': 'gray',
    'South America': 'cyan',
    'South Asia': 'magenta',
    'Southeast Asia': 'lime',
    'Sub-Saharan Africa': 'teal',
    'Western Europe': 'olive'
}

ax = reg.plot(kind="area", stacked=False, alpha=0.5, figsize=(20, 10), colormap=plt.cm.colors.ListedColormap(list(color_dict.values())))

plt.title("Region wise attacks", fontsize=20)
plt.xlabel("Years", fontsize=20)
plt.ylabel("Number of Attacks", fontsize=20)

legend_labels = [plt.Line2D([0], [0], marker='o', color='w', label=label, markersize=10,
                            markerfacecolor=color_dict[label]) for label in color_dict.keys()]
plt.legend(handles=legend_labels, title="Regions", fontsize=12, title_fontsize=14)

plt.show()

regt=reg.transpose()
regt["Total"]=regt.sum(axis=1)
ra=regt["Total"].sort_values(ascending=False)
print(ra)



colors = [
    'blue', 'green', 'red', 'purple', 'orange', 'brown',
    'pink', 'gray', 'cyan', 'magenta', 'lime', 'teal', 'olive'
]

plt.figure(figsize=(15, 6))
plt.bar(ra.index, ra.values, color=colors)
plt.title("Total Attacks by Region", fontsize=16)
plt.xlabel("Region", fontsize=14)
plt.ylabel("Total Attacks", fontsize=14)
plt.xticks(rotation=55, ha="right")  
plt.tight_layout()
plt.show()

rc=Terror[["Region","Casualty"]].groupby("Region").sum().sort_values(by="Casualty",ascending=False)
print(rc)

rc.plot(kind="bar",color="purple",figsize=(15,6))
plt.title("Region wise Casualties",fontsize=13)
plt.xlabel("Regions",fontsize=13)
plt.xticks(fontsize=12)
plt.ylabel("Number of Casualties",fontsize=13)
plt.show()

rk=Terror[["Region","Killed"]].groupby("Region").sum().sort_values(by="Killed",ascending=False)
print(rk)

rw=Terror[["Region","Wounded"]].groupby("Region").sum().sort_values(by="Wounded",ascending=False)
print(rw)

fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

rk.plot(kind="bar",color="yellow",figsize=(15,6),ax=ax0)
ax0.set_title("People Killed in each Region")
ax0.set_xlabel("Regions")
ax0.set_ylabel("Number of People Killed")

rw.plot(kind="bar",color="green",figsize=(15,6),ax=ax1)
ax1.set_title("People Wounded in each Region")
ax1.set_xlabel("Regions")
ax1.set_ylabel("Number of People Wounded")

plt.show()

ct=Terror["Country"].value_counts().head(10)
print(ct)

cnc=Terror[["Country","Casualty"]].groupby("Country").sum().sort_values(by="Casualty",ascending=False)
print(cnc.head(10))

top_10_cnc = cnc.head(10)

# Create a bar plot
plt.figure(figsize=(15, 6))
top_10_cnc.plot(kind="bar", color="magenta")
plt.title("Top 10 Countries with the Highest Casualties", fontsize=13)
plt.xlabel("Countries", fontsize=13)
plt.xticks(rotation=45, fontsize=12)
plt.ylabel("Number of Casualties", fontsize=13)
plt.tight_layout()
plt.show()

cnk=Terror[["Country","Killed"]].groupby("Country").sum().sort_values(by="Killed",ascending=False)
print(cnk.head(10))

cnw=Terror[["Country","Wounded"]].groupby("Country").sum().sort_values(by="Wounded",ascending=False)
print(cnw.head(10))

fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Killed
cnk[:10].plot(kind="bar",color="chocolate",figsize=(15,6),ax=ax0)
ax0.set_title("People Killed in each Country")
ax0.set_xlabel("Countries")
ax0.set_ylabel("Number of People Killed")

#Wounded
cnw[:10].plot(kind="bar",color="indigo",figsize=(15,6),ax=ax1)
ax1.set_title("People Wounded in each Country")
ax1.set_xlabel("Countries")
ax1.set_ylabel("Number of People Wounded")

plt.show()

attc_city=Terror["City"].value_counts()[1:11]
print(attc_city)

attc_city.plot(kind="bar",color="palegreen",figsize=(15,6))
plt.title("City wise Attacks",fontsize=13)
plt.xlabel("Cities",fontsize=13)
plt.xticks(fontsize=12)
plt.ylabel("Number of Attacks",fontsize=13)
plt.show()

cas_city=Terror[["City","Casualty"]].groupby("City").sum().sort_values(by="Casualty",ascending=False).drop("Unknown")
print(cas_city.head(10))

cas_city[:10].plot(kind="bar",color="aqua",figsize=(15,6))
plt.title("City wise Casualties",fontsize=13)
plt.xlabel("Cities",fontsize=13)
plt.xticks(fontsize=12)
plt.ylabel("Number of Casualties",fontsize=13)
plt.show()

citi_kill=Terror[["City","Killed"]].groupby("City").sum().sort_values(by="Killed",ascending=False).drop("Unknown")
print(citi_kill.head(10))

citi_wound=Terror[["City","Wounded"]].groupby("City").sum().sort_values(by="Wounded",ascending=False).drop("Unknown")
citi_wound.head(10)

fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Killed
citi_kill[:10].plot(kind="bar",color="cornflowerblue",figsize=(15,6),ax=ax0)
ax0.set_title("People Killed in each City")
ax0.set_xlabel("Cities")
ax0.set_ylabel("Number of People Killed")

#Wounded
citi_wound[:10].plot(kind="bar",color="cornflowerblue",figsize=(15,6),ax=ax1)
ax1.set_title("People Wounded in each City")
ax1.set_xlabel("Cities")
ax1.set_ylabel("Number of People Wounded")

plt.show()

# this figure show killed and wounded in india countty

cities_in_india = Terror[Terror["Country"] == "India"]

citi_kill_in = cities_in_india[["City", "Killed"]].groupby("City").sum().sort_values(by="Killed", ascending=False)
citi_wound_in = cities_in_india[["City", "Wounded"]].groupby("City").sum().sort_values(by="Wounded", ascending=False)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(15, 6))

# Killed in India
citi_kill_in[:10].plot(kind="bar", color="khaki", ax=ax0)
ax0.set_title("People Killed in each City in India")
ax0.set_xlabel("Cities")
ax0.set_ylabel("Number of People Killed")

# Wounded in India
citi_wound_in[:10].plot(kind="bar", color="khaki", ax=ax1)
ax1.set_title("People Wounded in each City in India")
ax1.set_xlabel("Cities")
ax1.set_ylabel("Number of People Wounded")

plt.tight_layout()
plt.show()

# Group-wise attacks count
group = Terror["Group Name"].value_counts()[1:10]
print(group)

# Plotting group-wise attacks count
group.plot(kind="bar", color="slategrey", figsize=(15, 6))
plt.title("Group wise Attacks", fontsize=13)
plt.xlabel("Terrorist Groups", fontsize=13)
plt.xticks(fontsize=12)
plt.ylabel("Number of Attacks", fontsize=13)
plt.show()

# Group-wise killed count
group_kill = Terror[["Group Name", "Killed"]].groupby("Group Name").sum().sort_values(by="Killed", ascending=False).drop("Unknown")
print(group_kill.head(10))

# Group-wise wounded count (corrected)
group_wound = Terror[["Group Name", "Wounded"]].groupby("Group Name").sum().sort_values(by="Wounded", ascending=False).drop("Unknown")
group_wound.head(10)

# Creating subplots
fig = plt.figure()
ax0 = fig.add_subplot(1, 2, 1)
ax1 = fig.add_subplot(1, 2, 2)

# Killed
group_kill[:10].plot(kind="bar", color="burlywood", figsize=(15, 6), ax=ax0)
ax0.set_title("People Killed by each Group")
ax0.set_xlabel("Terrorist Groups")
ax0.set_ylabel("Number of people Killed")

# Wounded (corrected)
group_wound[:10].plot(kind="bar", color="goldenrod", figsize=(15, 6), ax=ax1)
ax1.set_title("People Wounded by each Group")
ax1.set_xlabel("Terrorist Groups")
ax1.set_ylabel("Number of people Wounded")

plt.show()

at=Terror["Attack Type"].value_counts()
print(at)

at.plot(kind="bar",color="hotpink",figsize=(15,6))
plt.title("Types of Attacks",fontsize=13)
plt.xlabel("Attack Types",fontsize=13)
plt.xticks(fontsize=12)
plt.ylabel("Number of Attacks",fontsize=13)
plt.show()

# Attack type in india 

# Filter data for attacks in India
attacks_in_india = Terror[Terror["Country"] == "India"]

# Count the attack types in India
attack_types_in_india = attacks_in_india["Attack Type"].value_counts()

# Plot the attack types in India
attack_types_in_india.plot(kind="bar", color="orange", figsize=(15, 6))
plt.title("Types of Attacks in India", fontsize=13)
plt.xlabel("Attack Types", fontsize=13)
plt.xticks(fontsize=12, rotation=45)
plt.ylabel("Number of Attacks", fontsize=13)
plt.show()

attck_cas=Terror[["Attack Type","Casualty"]].groupby("Attack Type").sum().sort_values(by="Casualty",ascending=False)
print(attck_cas)

attck_cas.plot(kind="bar",color="peru",figsize=(15,6))
plt.title("Casualties in each Attack",fontsize=13)
plt.xlabel("Attack Types",fontsize=13)
plt.xticks(fontsize=12)
plt.ylabel("Number of Casualties",fontsize=13)
plt.show()
attck_cas = Terror[["Attack Type", "Killed", "Wounded"]].groupby("Attack Type").sum().sum(axis=1).sort_values(ascending=False)

attack_kill=Terror[["Attack Type","Killed"]].groupby("Attack Type").sum().sort_values(by="Killed",ascending=False)
print(attack_kill)

attack_wound=Terror[["Attack Type","Wounded"]].groupby("Attack Type").sum().sort_values(by="Wounded",ascending=False)
print(attack_wound)

fig=plt.figure()
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

#Killed
attack_kill.plot(kind="bar",color="cyan",figsize=(15,6),ax=ax0)
ax0.set_title("People Killed in each Attack Type")
ax0.set_xlabel("Attack Types")
ax0.set_ylabel("Number of people Killed")

#Wounded
attack_wound.plot(kind="bar",color="red",figsize=(15,6),ax=ax1)
ax1.set_title("People Wounded in each Attack Type")
ax1.set_xlabel("Attack Types")
ax1.set_ylabel("Number of people Wounded")
plt.show()

target_type=Terror["Target Type"].value_counts()
print(target_type)

target_type.plot(kind="bar",color="palegreen",figsize=(15,6))
plt.title("Types of Targets",fontsize=13)
plt.xlabel("Target Types",fontsize=13)
plt.xticks(fontsize=12)
plt.ylabel("Number of Attacks",fontsize=13)
plt.show()

trtyp_cas=Terror[["Target Type","Casualty"]].groupby("Target Type").sum().sort_values(by="Casualty",ascending=False)
print(trtyp_cas)

trtyp_cas.plot(kind="bar",color="navy",figsize=(15,6))
plt.title("Casualties in each Target Attack",fontsize=13)
plt.xlabel("Target Types",fontsize=13)
plt.xticks(fontsize=12)
plt.ylabel("Number of Casualties",fontsize=13)
plt.show()

gca=Terror[["Group Name","Country"]].value_counts().drop("Unknown")
print(gca.head(10))

gca.head(10).plot(kind="bar",color="cornflowerblue",figsize=(15,6))
plt.title("Countries with most attacks by a particular Group",fontsize=13)
plt.xlabel("(Terrorist Group,Country)",fontsize=13)
plt.xticks(fontsize=12)
plt.ylabel("Number of Attacks",fontsize=13)
plt.show()

gcc=Terror[["Group Name","Country","Casualty"]].groupby(["Group Name","Country"],axis=0).sum().sort_values(by="Casualty",ascending=False).drop("Unknown").head(10)
print(gcc)

gcc.plot(kind="bar",color="steelblue",figsize=(15,6))
plt.title("Countries with most casualties by a particular Group",fontsize=13)
plt.xlabel("(Terrorist Group,Country)",fontsize=13)
plt.xticks(fontsize=12)
plt.ylabel("Number of Casualties",fontsize=13)
plt.show()

casualty=Terror.loc[:,"Casualty"].sum()
print("Total number of Casualties due to Terrorist Attacks from 1970 to 2017 across the world :\n",casualty)

kill=Terror.loc[:,"Killed"].sum()
print("Total number of people killed due to Terrorist Attacks from 1970 to 2017 across the world :\n",kill)

wound=Terror.loc[:,"Wounded"].sum()
print("Total number of people killed due to Terrorist Attacks from 1970 to 2017 across the world :\n",wound)