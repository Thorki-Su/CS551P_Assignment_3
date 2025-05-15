from models import db, Country, EmissionData
from emissions import app
import pandas as pd

with app.app_context():
    db.drop_all()
    db.create_all()

    df = pd.read_excel('data/data_upload.xlsx')
    for _, row in df.iterrows():
        country = Country(
            name=row['Country Name'],
            code=row['Country Code'],
            region=row['Region'],
            income_group=row['IncomeGroup']
        )
        db.session.add(country)
        db.session.flush()

        for year in range(1990, 2021):
            value = row.get(str(year))
            if pd.notna(value):
                data = EmissionData(year=year, emission=value, country_id=country.id)
                db.session.add(data)
    
    db.session.commit()
    print("data uploaded successfully")