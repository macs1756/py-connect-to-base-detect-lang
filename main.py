import psycopg2
from langdetect import detect
from datetime import datetime

def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

# Підключення до бази даних
connection = psycopg2.connect(
    dbname="vapping2",
    user="postgres",
    password="admin",
    host="127.0.0.1",
    port="4444"
)

cursor = connection.cursor()

# Виконуємо запит для вибірки всіх записів з таблиці
# cursor.execute("""
#     SELECT cke.textarea, r.id 
#     FROM public.reviews_components rc 
#     JOIN public.reviews r ON rc.entity_id = r.id 
#     JOIN public.components_content_ck_editors cke ON rc.component_id = cke.id 
#     WHERE r.locale = 'de' 
#     AND rc.component_type = 'content.ck-editor'
# """)

cursor.execute("""
   SELECT cke.textarea, r.id 
    FROM public.news_components rc 
    JOIN public.news r ON rc.entity_id = r.id 
    JOIN public.components_content_ck_editors cke ON rc.component_id = cke.id 
    WHERE r.locale = 'de' 
    AND rc.component_type = 'content.ck-editor'
""")


records = cursor.fetchall()

# Перевіряємо кожен запис на англійську мову та зберігаємо як текст, так і ID
english_records = [(record[1], record[0]) for record in records if is_english(record[0])]

# Отримуємо поточний час для створення унікального імені файлу
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"english_records_{timestamp}.txt"

# Записуємо результати у файл
with open(filename, "w") as file:
    for product_id, text in english_records:
        file.write(f"ID: {product_id}, Text: {text}\n")

# Виводимо кількість записів англійською мовою
print(f"{len(english_records)} записів англійською мовою.")
print(f"Результати збережено у файл {filename}.")

# Закриваємо підключення до бази даних
cursor.close()
connection.close()
