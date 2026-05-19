import sqlite3
import pandas as pd
import os

def clean_data():
    print("Starting Data Cleaning Pipeline...")
    
    # 1. Load Data
    try:
        df_restaurants = pd.read_csv('data/restaurants.csv')
        df_engagements = pd.read_csv('data/engagements.csv')
    except FileNotFoundError:
        print("Data files not found. Please run data_generator.py first.")
        return
        
    print(f"Raw Restaurants count: {len(df_restaurants)}")
    print(f"Raw Engagements count: {len(df_engagements)}")
    
    # Create SQLite in-memory DB
    conn = sqlite3.connect(':memory:')
    
    # Write to SQL
    df_restaurants.to_sql('raw_restaurants', conn, index=False)
    df_engagements.to_sql('raw_engagements', conn, index=False)
    
    # 2. SQL Cleaning Queries
    # Cleaning criteria:
    # - Remove engagements with null dates
    # - Ensure engagements have valid stars for reviews (1 to 5)
    # - For tips and check-ins, stars should be null/empty, we'll keep them as is but filter review anomalies.
    # - Remove restaurants with missing city names
    
    cleaning_query_restaurants = """
    CREATE TABLE clean_restaurants AS
    SELECT *
    FROM raw_restaurants
    WHERE city IS NOT NULL AND city != '';
    """
    
    cleaning_query_engagements = """
    CREATE TABLE clean_engagements AS
    SELECT *
    FROM raw_engagements
    WHERE engagement_date IS NOT NULL
      AND (
          (engagement_type = 'review' AND stars >= 1 AND stars <= 5)
          OR
          (engagement_type != 'review')
      );
    """
    
    conn.execute(cleaning_query_restaurants)
    conn.execute(cleaning_query_engagements)
    
    # 3. Export back to DataFrame
    df_clean_restaurants = pd.read_sql_query("SELECT * FROM clean_restaurants", conn)
    df_clean_engagements = pd.read_sql_query("SELECT * FROM clean_engagements", conn)
    
    print(f"Cleaned Restaurants count: {len(df_clean_restaurants)}")
    print(f"Cleaned Engagements count: {len(df_clean_engagements)}")
    
    # Calculate improvement metrics
    dirty_engagements_removed = len(df_engagements) - len(df_clean_engagements)
    dirty_restaurants_removed = len(df_restaurants) - len(df_clean_restaurants)
    
    print(f"Data quality improvement complete.")
    print(f"Removed {dirty_engagements_removed} anomalous engagement records.")
    print(f"Removed {dirty_restaurants_removed} anomalous restaurant records.")
    
    # Save cleaned data to disk for analysis step
    df_clean_restaurants.to_csv('data/clean_restaurants.csv', index=False)
    df_clean_engagements.to_csv('data/clean_engagements.csv', index=False)
    print("Cleaned datasets saved to 'data/clean_restaurants.csv' and 'data/clean_engagements.csv'.")
    
    conn.close()

if __name__ == '__main__':
    clean_data()
