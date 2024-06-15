import pandas as pd
import matplotlib.pyplot as plt
import math

# Zmiana opcji biblioteki Pandas tak, aby wyświetlić wszystkie kolumny
pd.set_option('display.max_columns', None)

# Wczytanie pliku Excel do DataFrame
df = pd.read_excel('Procent obrotu dla tłumaczy od lutego 2020.xlsx')

# Wyświetlenie DataFrame'a w celu zlokalizowania poszukiwanych danych
print(df)

# Nazwy arkuszy w pliku Excel zapisujemy do zmiennej
sheet_names = pd.ExcelFile('Procent obrotu dla tłumaczy od lutego 2020.xlsx').sheet_names

pct_turnover = []
date = []

# W pętli for wczytujemy po kolei każdy z akruszy pliku Excel i z każdego z nich wyciągamy wartość procentu obrotu
# w danym miesiącu oraz datę, które dodajemy do zadeklarowanych list
for sheet_name in sheet_names:
    loop_df = pd.read_excel('Procent obrotu dla tłumaczy od lutego 2020.xlsx', sheet_name=sheet_name)
    # Odczytujemy wartość komórki z wiersza nr 5 i kolumny nr 9, w której znajduje się informacja o procencie obrotu
    pct_turnover.append(loop_df.iloc[4, 8])
    if sheet_name.split()[0] == 'STYCZEŃ':
        date.append(sheet_name.split()[1] + '-' + '01')
    elif sheet_name.split()[0] == 'LUTY':
        date.append(sheet_name.split()[1] + '-' + '02')
    elif sheet_name.split()[0] == 'MARZEC':
        date.append(sheet_name.split()[1] + '-' + '03')
    elif sheet_name.split()[0] == 'KWIECIEŃ':
        date.append(sheet_name.split()[1] + '-' + '04')
    elif sheet_name.split()[0] == 'MAJ':
        date.append(sheet_name.split()[1] + '-' + '05')
    elif sheet_name.split()[0] == 'CZERWIEC':
        date.append(sheet_name.split()[1] + '-' + '06')
    elif sheet_name.split()[0] == 'LIPIEC':
        date.append(sheet_name.split()[1] + '-' + '07')
    elif sheet_name.split()[0] == 'SIERPIEŃ':
        date.append(sheet_name.split()[1] + '-' + '08')
    elif sheet_name.split()[0] == 'WRZESIEŃ':
        date.append(sheet_name.split()[1] + '-' + '09')
    elif sheet_name.split()[0] == 'PAŹDZIERNIK':
        date.append(sheet_name.split()[1] + '-' + '10')
    elif sheet_name.split()[0] == 'LISTOPAD':
        date.append(sheet_name.split()[1] + '-' + '11')
    elif sheet_name.split()[0] == 'GRUDZIEŃ':
        date.append(sheet_name.split()[1] + '-' + '12')

data = {'date': date,
        'pct_turnover': pct_turnover}
new_df = pd.DataFrame(data)
print(new_df)
new_df_sorted = new_df.sort_values(by='date')

new_df_sorted.index = pd.to_datetime(new_df_sorted['date'], format='%Y-%m')

del new_df_sorted['date']

plt.plot(new_df_sorted.index, new_df_sorted['pct_turnover'])
plt.ylabel('Procent obrotu')
plt.xlabel('Okres')
# Obracamy daty na osi X, aby były łatwiejsze do odczytania
plt.xticks(rotation=45)
plt.subplots_adjust(bottom=0.2)
plt.title('Procent obrotu na przestrzeni miesięcy')
plt.show()

# Podział danych do uczenia maszynowego
# Bierzemy 80% danych do treningu. 20% zostaje do testów.
train = new_df_sorted.head(math.ceil(len(sheet_names) * 0.8))
test = new_df_sorted.tail(math.ceil(len(sheet_names) * 0.2))

y = train['pct_turnover']
