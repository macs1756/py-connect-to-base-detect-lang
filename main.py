import psycopg2
from langdetect import detect
from datetime import datetime

def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

connection = psycopg2.connect(
    dbname="vapping2",
    user="postgres",
    password="admin",
    host="127.0.0.1",
    port="4444"
)

cursor = connection.cursor()


cursor.execute("""
   SELECT cke.textarea, r.id 
    FROM public.news_components rc 
    JOIN public.news r ON rc.entity_id = r.id 
    JOIN public.components_content_ck_editors cke ON rc.component_id = cke.id 
    WHERE r.locale = 'de' 
    AND rc.component_type = 'content.ck-editor'
""")


records = cursor.fetchall()

english_records = [(record[1], record[0]) for record in records if is_english(record[0])]

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"english_records_{timestamp}.txt"

with open(filename, "w") as file:
    for product_id, text in english_records:
        file.write(f"ID: {product_id}, Text: {text}\n")

print(f"{len(english_records)} records on english language")
print(f"Results save in {filename}.")

cursor.close()
connection.close()
