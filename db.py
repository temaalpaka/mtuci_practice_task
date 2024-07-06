import sqlite3

conn = sqlite3.connect("mtuci_practice_task_db.db")

sql = "CREATE TABLE vacancy (vacancy_id TEXT, vacancy_url TEXT, vacancy_title TEXT, company_name TEXT, vacancy_experience TEXT, vacancy_description_list_item TEXT)"
sql = "SELECT * FROM vacancy"

sql = "CREATE TABLE resume (resume_id TEXT, resume_url TEXT, resume_block_title_position TEXT, bloko_header_2 TEXT, resume_personal_gender TEXT, resume_personal_age TEXT)"
sql = "SELECT * FROM resume"

sql = "CREATE TABLE comparison (vacancy_id TEXT, resume_id TEXT)"
sql = "SELECT * FROM comparison"

cursor = conn.cursor()

cursor.execute(sql)

res = cursor.fetchall()

conn.close()