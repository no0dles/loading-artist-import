# loading-artist-import

Import comic meta data from http://loadingartist.com into MySQL database

## 1. Install
```
pip install -r requirements.txt
```

## 2. Configure
Create a new database with the create script "create_database.sql" and add your credentials of your database in the "config.py" file.

## 3. Run

### Import by web archive
This will import the archive back to 2011.
```
python manage.py archive
```

### Import by RSS feed
This will import the latest data from the official RSS feed.
```
python manage.py rss
```
