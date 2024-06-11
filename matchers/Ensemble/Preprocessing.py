import pandas as pd

def convert_dates(date):
    for fmt in ('%d.%m.%Y', '%Y-%m-%d'):
        try:
            return pd.to_datetime(date, format=fmt).strftime('%Y-%m-%d')
        except ValueError:
            pass
    raise ValueError(f"Date format of {date} not recognized")

def exclude_urls(df, url_pattern):
    return df[~df['url'].str.startswith(url_pattern)]

def filter_by_date(df, start_date, end_date, date_column='date'):

    df[date_column] = pd.to_datetime(df[date_column], format='%Y-%m-%d')
    
    # Filter the DataFrame
    mask = (df[date_column] >= start_date) & (df[date_column] <= end_date)
    return df[mask]

def exclude_instagram_articles(articles):
    a = exclude_urls(articles, "https://scontent-fra3-1.cdninstagram.com/")
    a = exclude_urls(a, "https://scontent-fra3-2.cdninstagram.com/")
    a = exclude_urls(a, "https://scontent-fra5-1.cdninstagram.com/")
    a = exclude_urls(a, "https://scontent-fra5-2.cdninstagram.com/")
    return a