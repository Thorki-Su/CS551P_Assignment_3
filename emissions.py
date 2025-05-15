from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
DATA_FILE = 'data/data_upload.xlsx'
PLOT_DIR = 'static/plots'

df_raw = pd.read_excel(DATA_FILE)
df = df_raw.melt(
    id_vars=["Country Name"],
    value_vars=[str(year) for year in range(1990, 2021)],
    var_name="Year",
    value_name="Emissions"
)
df['Year'] = df['Year'].astype(int)

os.makedirs(PLOT_DIR, exist_ok=True)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/countries')
def country_list():
    countries = sorted(df['Country Name'].unique())
    return render_template('countries.html', countries=countries)

@app.route('/country/<country_name>')
def country_detail(country_name):
    country_data = df[df['Country Name'] == country_name].sort_values(by='Year')

    safe_name = country_name.replace(" ", "_")
    plot_path = os.path.join(PLOT_DIR, f"{safe_name}.png")

    if not os.path.exists(plot_path):
        plt.figure(figsize=(10, 5))
        plt.plot(country_data['Year'], country_data['Emissions'], marker='o')
        plt.title(f"{country_name} - CO₂ Emissions (1990–2020)")
        plt.xlabel("Year")
        plt.ylabel("Emissions")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()

    return render_template('country.html', country=country_name, image_file=f"/{plot_path}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)