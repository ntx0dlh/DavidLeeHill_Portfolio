import pandas as pd
import os

CODE_PATH = "/home/imdavid/workplace/DavidLeeHill_Portfolio/dooropener/src/"

df = pd.read_csv(f"{CODE_PATH}testlog.txt", sep=" - ")
df.columns = ["timestamp", "event"]

df.info()

print(df["event"].value_counts())