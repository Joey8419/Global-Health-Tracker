# Handles the database queries
import pandas as pd
from global_health_tracker.models import db, Outbreak
from datetime import datetime, timedelta


def load_data_from_csv(csv_path='Outbreaks.csv'):
    data = pd.read_csv(csv_path)

    # Assuming columns in the CSV match the model fields
    data = data.rename(columns=lambda x: x.lower().replace(' ', '_'))

    # Create and configure the database
    db.create_all()

    # Load data into the database
    for index, row in data.iterrows():
        outbreak = Outbreak(**row.to_dict())
        db.session.add(outbreak)

    db.session.commit()


# Gets disease outbreaks from the last 10 years
def get_disease_outbreaks_last_10_years(country):
    current_year = datetime.now.year
    ten_years_ago = current_year - 10
    return Outbreak.query.filter_by(country=country).filter(Outbreak.year >= ten_years_ago).all()


# Gets past searches by User
def get_user_search_history(user_id):
    # Assuming there is a UserSearchHistory model with user_id, search_term, timestamp fields
    return UserSearchHistory.query.filter_by(user_id=user_id).order_by(UserSearchHistory.timestamp.desc()).all()


# Adds user search history
def add_user_search_history(user_id, search_term):
    # Assuming there is a UserSearchHistory model
    search_history = UserSearchHistory(user_id=user_id, search_term=search_term)
    db.session.add(search_history)
    db.session.commit()

# run this script to load data from CSV to the database
def load_data_from_csv(csv_path='Outbreaks.csv')
    data = pd.read_csv(csv_path)

    # Assuming columns in the CSV match the model fields
    data = data.rename(columns=lambda x: x.lower().replace(' ', '_'))

    # Create and configure the database
    db.create_all()

    # Load data into the database
    for index, row in data.iterrows():
        outbreak = Outbreak(**row.to_dict())
        db.session.add(outbreak)

    db.session.commit()
