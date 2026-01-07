import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('data.csv')

df = df[df['Avstand (cm)'] != 0]

plt.figure(figsize=(10, 6))

plt.plot(df['Tid (s)'], df['Avstand (cm)'], color='blue', marker='o', linestyle='-')

plt.title('Avstand over Tid')
plt.xlabel('Tid (s)')
plt.ylabel('Avstand (cm)')
plt.grid(True)

plt.show()