import pandas as pd

file_name = 'prz.xlsx'

datam100 = pd.read_excel(file_name, usecols='B:K', skiprows=2, nrows=15)
datam75 = pd.read_excel(file_name, usecols='M:V', skiprows=2, nrows=15)
datam50 = pd.read_excel(file_name, usecols='X:AK', skiprows=2, nrows=15)
datam25 = pd.read_excel(file_name, usecols='AI:AR', skiprows=2, nrows=15)
datag100 = pd.read_excel(file_name, usecols='B:K', skiprows=19, nrows=15)
datag75 = pd.read_excel(file_name, usecols='M:V', skiprows=19, nrows=15)
datag50 = pd.read_excel(file_name, usecols='X:AK', skiprows=19, nrows=15)
datag25 = pd.read_excel(file_name, usecols='AI:AR', skiprows=19, nrows=15)

motor_strings = []

for index, row in datam100.iterrows():
    for col in range(1, len(row)):
        if pd.notna(row[col]):
            for rpm in range(100, 10001, 100):
                if rpm < len(datam100):
                    motor_strings.append(f'Motor_100_{row[col]}_{rpm}_{datam100.iloc[index, col]}')

for index, row in datam100.iterrows():
    for col in range(1, len(row)):
        if pd.notna(row[col]) and row[col] == 56.5:
            for rpm in range(100, 10001, 100):
                if rpm < len(datam100):
                    motor_strings.append(f'Motor_100_{row[col]}_{rpm}_{datam100.iloc[index, col]}')

print(motor_strings)
