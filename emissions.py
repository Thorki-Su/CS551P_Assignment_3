from flask import Flask, render_template, abort
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
    try:
        countries = Country.query.order_by(Country.name).all()
    except Exception as e:
        print(f"reading database error: {e}")
        abort(500)
    return render_template('homepage.html', countries=countries)

@app.route('/country/<int:country_id>')
def country_detail(country_id):
    countries = Country.query.order_by(Country.name).all()
    country = Country.query.get_or_404(country_id)
    emissions = EmissionData.query.filter_by(country_id=country.id).order_by(EmissionData.year).all()
    years = [e.year for e in emissions]
    values = [e.emission for e in emissions]

    plot_path = os.path.join(PLOT_DIR, f"{country.name.replace(' ', '_')}.png")
    try:
        if not os.path.exists(plot_path):
            plt.figure(figsize=(10, 5))
            plt.plot(years, values, marker='o')
            plt.title(f"{country.name} CO₂ Emissions")
            plt.xlabel("Year")
            plt.ylabel("Emissions (metric tons per capita)")
            plt.tight_layout()
            plt.savefig(plot_path)
            plt.close()
    except Exception as e:
        print(f"Error in creating the chart: {e}")
        return render_template("country.html",
                               countries=countries,
                               country=country,
                               error="Error in creating the chart, please try later.")

    return render_template("country.html",
                           countries=countries,
                           country=country,
                           image_file=f"/{plot_path}")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)