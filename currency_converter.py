import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import CENTER,ttk
from PIL import Image, ImageTk
import pickle

URL = "https://www.nbp.pl/home.aspx?f=/kursy/kursya.html"

try:
    page = requests.get(URL, stream = True)
    soup = BeautifulSoup(page.content, "html.parser")
    with open('nbp.pickle', 'wb') as f:
        pickle.dump(page, f)
        f.close()

except (requests.ConnectionError) as exception:
    with open('nbp.pickle', 'rb') as f:
        page = pickle.load(f)
        f.close()
    soup = BeautifulSoup(page.content, "html.parser")


def sorting_rates(list_of_rates):
    global sorted_rates 
    global currency_names
    sorted_rates = []
    currency_names = []
    for i in range(0,len(list_of_rates),2):
        waluta = list_of_rates[i]
        kurs = list_of_rates[i+1]
        kurs = kurs.replace(',','.')
        if len(waluta) > 5:
            dzielnik = int(waluta[:-3])
            kurs = float(kurs)/dzielnik
        sorted_rates.append((waluta[-3:],float(kurs)))
        currency_names.append(waluta[-3:])

    sorted_rates += [("PLN", 1.0)]
    currency_names += ["PLN"]


def counter(rate_1, rate_2, money):
    for pack in sorted_rates:
        x,y = pack
        if x == rate_1:
            rate_1 = float(y)
        elif x == rate_2:
            rate_2 = float(y)
    result = float(money) * rate_1 / rate_2
    return round(result,2)

def convert():
    x = counter(combo1.get(),combo2.get(),value.get())
    result['text'] = x

full_rates =  soup.find_all("td", class_ = "right")
#print(full_rates)
rates = list(map(lambda kurs: kurs.get_text(), full_rates))
print(rates)
sorting_rates(rates)
#print(sorted_rates)

root = tk.Tk()
# tytuł okna
root.title('Your Personal Currency Converter')
# rozmiar okna
root.geometry('1030x775')
root.resizable(width=False, height=False)
#logo
logo = Image.open("logo.png")
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image = logo)
logo_label.image = logo
logo_label.grid()

#main
result = tk.Label(text = " ", height = 2, width = 60, padx = 13, pady = 30, anchor = CENTER)
result.place(x = 300, y = 300)

from_label = tk.Label(text = "From", height = 2, width = 5, padx = 0, pady = 0)
from_label.place(x = 300, y = 400)

combo1 = ttk.Combobox(width = 20, height = 10, justify = CENTER)
combo1['values'] = currency_names
combo1.place(x = 340, y = 400)

to_label = tk.Label(text = "To", height = 2, width = 5, padx = 0, pady = 0)
to_label.place(x = 550, y = 400)

combo2 = ttk.Combobox(width = 20, height = 10, justify = CENTER)
combo2['values'] = currency_names
combo2.place(x = 590, y = 400)

value = tk.Entry(width=63, justify=CENTER)
value.place(x = 300, y = 440)

button = tk.Button(text = "Convert", width =60, height = 5, command = convert)
button.place(x = 300, y = 480)

quit_button = tk.Button(text = "Quit", width = 60, height= 5, command = root.quit)
quit_button.place(x = 300, y = 550)

root.mainloop ()