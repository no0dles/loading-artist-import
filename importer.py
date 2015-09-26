import pymysql.cursors
import loadingartist
import config
from contextlib import contextmanager


@contextmanager
def get_db():
    connection = pymysql.connect(
        host=config.DB_HOST,
        db=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        charset=config.DB_CHARSET,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            yield connection, cursor
    finally:
        connection.commit()
        connection.close()


def import_rss_feed():
    with get_db() as (connection, cursor):
        comic_details = loadingartist.get_rss_items()
        for comic_detail in comic_details:
            import_comic_detail(cursor, comic_detail)


def import_archives():
    comics = loadingartist.get_archive_comics()

    with get_db() as (connection, cursor):
        for comic in comics:
            import_comic(cursor, comic)


def does_comic_exist(cursor, comic):
    sql = 'select count(*) cnt from comics where url = %s'
    cursor.execute(sql, (comic['url']))
    result = cursor.fetchone()

    return result['cnt'] > 0


def import_comic(cursor, comic):
    if does_comic_exist(cursor, comic):
        return

    comic_detail = loadingartist.get_comic_detail(comic['url'])
    import_comic_detail(cursor, comic_detail, False)


def import_comic_detail(cursor, comic_detail, check_for_existing=True):
    if check_for_existing and does_comic_exist(cursor, comic_detail):
        return

    sql = 'insert into comics (url, thumb_url, img_url, date, title, author) values(%s, %s, %s, %s, %s, %s)'

    cursor.execute(sql, (comic_detail['url'], comic_detail['thumb_url'], comic_detail['img_url'],
                         comic_detail['date'], comic_detail['title'], comic_detail['author']))
