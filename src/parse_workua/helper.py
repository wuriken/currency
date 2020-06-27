import json
import re
import sqlite3


def clean_html(str_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', str(str_html))
    return cleantext.replace('\n', '. ').replace("'", '').replace("`", '')


def clean_space(tmp_str):
    return str(tmp_str).replace('\n', '').replace('  ', '')


def get_str_from_list(list_html):
    res = ''
    for item in list_html:
        res += str(item)
    return res


def insert_data_into_db(company, address, vacancy, description):
    conn = sqlite3.connect("vacancy.db")
    cursor = conn.cursor()
    sql = f"INSERT INTO vacancy VALUES ('{company}', '{address}', '{vacancy}', '{description}')"
    cursor.execute(sql)
    conn.commit()


def save_vacancy_to_json(dict_map):
    conn = sqlite3.connect('vacancy.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute('''
    SELECT * from vacancy
    ''').fetchall()
    conn.commit()
    conn.close()
    if dict_map:
        with open('export.json', 'w') as file:
            json.dump([dict(ix) for ix in rows], file, ensure_ascii=False, indent=4)
