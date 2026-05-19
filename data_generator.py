import pandas as pd
import numpy as np
import uuid
import datetime
import random
import os

def generate_data(num_restaurants=2200, num_engagements=55000):
    print("Generating synthetic data for Restaurant Engagement Analysis...")
    np.random.seed(42)
    random.seed(42)

    # 1. Generate Restaurants
    restaurant_ids = [str(uuid.uuid4()) for _ in range(num_restaurants)]
    categories = ['Italian', 'Mexican', 'Fast Food', 'Fine Dining', 'Cafe', 'Asian', 'Bar', 'Dessert']
    
    restaurants_data = []
    for rid in restaurant_ids:
        # Base quality of restaurant (influences avg stars and wait times)
        base_quality = np.random.normal(3.5, 0.8)
        base_quality = max(1.0, min(5.0, base_quality))
        
        restaurants_data.append({
            'restaurant_id': rid,
            'name': f"Restaurant_{str(rid)[:8]}",
            'category': random.choice(categories),
            'city': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego']),
            'true_quality': base_quality
        })
        
    df_restaurants = pd.DataFrame(restaurants_data)
    
    # Intentionally insert some dirty data in restaurants
    # Drop some cities
    df_restaurants.loc[np.random.choice(df_restaurants.index, 50), 'city'] = np.nan
    
    # 2. Generate Engagements (Reviews, Tips, Check-ins)
    engagements_data = []
    engagement_types = ['review', 'tip', 'check-in']
    
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    
    # We want retaining customers. Consistent monthly engagement -> higher retention.
    # We'll create some "consistent" users, and some "sporadic" users.
    num_users = 10000
    user_ids = [str(uuid.uuid4()) for _ in range(num_users)]
    
    # Tag 20% of users as 'highly consistent'
    consistent_users = set(random.sample(user_ids, int(num_users * 0.2)))
    
    for _ in range(num_engagements):
        user_id = random.choice(user_ids)
        restaurant = random.choice(restaurants_data)
        rid = restaurant['restaurant_id']
        quality = restaurant['true_quality']
        
        # Determine date
        if user_id in consistent_users:
            # Consistent users have more evenly distributed dates, higher volume
            random_number_of_days = random.randrange(days_between_dates)
            eng_date = start_date + datetime.timedelta(days=random_number_of_days)
        else:
            # Sporadic users tend to flock around holidays or weekends
            random_number_of_days = random.randrange(days_between_dates)
            eng_date = start_date + datetime.timedelta(days=random_number_of_days)
            
        # Determine engagement type
        eng_type = np.random.choice(engagement_types, p=[0.7, 0.1, 0.2]) # 70% reviews, 10% tips, 20% check-ins
        
        stars = np.nan
        if eng_type == 'review':
            stars = np.random.normal(quality, 0.5)
            stars = round(max(1.0, min(5.0, stars)))
            
            # Inject anomalies (stars out of bounds, e.g., > 5 or <= 0)
            if random.random() < 0.02:
                stars = random.choice([-1, 0, 6, 7, 10])
                
        # Inject null dates (anomalies)
        date_str = eng_date.strftime('%Y-%m-%d')
        if random.random() < 0.01:
            date_str = None
            
        engagements_data.append({
            'engagement_id': str(uuid.uuid4()),
            'restaurant_id': rid,
            'user_id': user_id,
            'engagement_type': eng_type,
            'stars': stars,
            'engagement_date': date_str
        })
        
    df_engagements = pd.DataFrame(engagements_data)
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df_restaurants.drop(columns=['true_quality']).to_csv('data/restaurants.csv', index=False)
    df_engagements.to_csv('data/engagements.csv', index=False)
    
    print(f"Generated {len(df_restaurants)} restaurants.")
    print(f"Generated {len(df_engagements)} engagements.")
    print("Files saved to 'data/restaurants.csv' and 'data/engagements.csv'.")

if __name__ == "__main__":
    generate_data()
