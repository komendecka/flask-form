from flask import Flask, render_template, request
import csv
import requests
import pickle

app = Flask(__name__)

response = requests.get('http://api.nbp.pl/api/exchangerates/tables/C?format=json')
data = response.json()
rates = data[0]['rates']

# filename = 'exchange_rates.pkl'
#
# with open(filename, 'wb') as file:
#     pickle.dump(data, file)
#
# print("Dane zostały zapisane do pliku binarnego za pomocą Pickle.")

# Tworzenie pliku CSV
filenameRates = 'rates.csv'

with open(filenameRates, 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['currency', 'code', 'bid', 'ask'])  # Nagłówki kolumn

    for rate in rates:
        currency = rate['currency']
        code = rate['code']
        bid = rate['bid']
        ask = rate['ask']
        writer.writerow([currency, code, bid, ask])

print("Plik CSV został utworzony.")


@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    currency = request.form.get('currency')
    qty = float(request.form.get('qty')) if request.form.get('qty') else 0.0
    rates = {}

    with open('rates.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            rates[row['code']] = float(row['bid'])

    if currency in rates:
        rate = rates[currency]
        cost = qty * rate
        return render_template('result.html', cost=cost)
    else:
        return render_template('result.html', error='Nieznana waluta')

if __name__ == "__main__":
    app.run(debug=True)
