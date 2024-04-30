import pandas as pd

# loop through and read and merge all files with the format "- copy(2).csv"
# into one dataframe
df = pd.DataFrame()
df = pd.read_csv("Orissa_ec_form2data - Copy.csv")
for i in range(2, 19):
    df = df.append(pd.read_csv(f"Orissa_ec_form2data - Copy ({i}).csv"))

df.to_csv("merged_form2data.csv", index=False)

df = pd.DataFrame()
df = pd.read_csv("Orissa_ec_maindata - Copy.csv")
for i in range(2, 19):
    df = df.append(pd.read_csv(f"Orissa_ec_maindata - Copy ({i}).csv"))

df.to_csv("merged_maindata.csv", index=False)

df = pd.DataFrame()
df = pd.read_csv("Orissa_ec_timelinedata - Copy.csv")
for i in range(2, 19):
    df = df.append(pd.read_csv(f"Orissa_ec_timelinedata - Copy ({i}).csv"))

df.to_csv("merged_timelinedata.csv", index=False)