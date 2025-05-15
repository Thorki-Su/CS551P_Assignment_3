from flask import Flask, render_template
from models import db, Country, EmissionData
import os
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emissions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

PLOT_DIR = 'static/plots'
os.makedirs(PLOT_DIR, exist_ok=True)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/countries')
def country_list():
    countries = Country.query.order_by(Country.name).all()
    return render_template('countries.html', countries=countries)

@app.route('/country/<int:country_id>')
def country_detail(country_id):
    country = Country.query.get_or_404(country_id)
    emissions = EmissionData.query.filter_by(country_id=country.id).order_by(EmissionData.year).all()
    years = [e.year for e in emissions]
    values = [e.emission for e in emissions]

    plot_path = os.path.join(PLOT_DIR, f"{country.name.replace(' ', '_')}.png")
    if not os.path.exists(plot_path):
        plt.figure(figsize=(10, 5))
        plt.plot(years, values, marker='o')
        plt.title(f"{country.name} CO₂ Emissions")
        plt.xlabel("Year")
        plt.ylabel("Emissions")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()

    return render_template("country.html",
                           country=country,
                           image_file=f"/{plot_path}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)