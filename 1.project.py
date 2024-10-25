import pandas as pd
import os
import fsspec

# Функция для загрузки данных из файлов
def load_data(directory):
    data = []
    for filename in os.listdir(directory):
        if 'price' in filename and filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            # Поиск нужных столбцов
            name_col = next(
                (col for col in df.columns if col.lower() in ["название", "продукт", "товар", "наименование"]), None)
            price_col = next((col for col in df.columns if col.lower() in ["цена", "розница"]), None)
            weight_col = next((col for col in df.columns if col.lower() in ["фасовка", "масса", "вес"]), None)
            if name_col and price_col and weight_col:
                for _, row in df.iterrows():
                    data.append({
                        'Наименование': row[name_col],
                        'Цена': row[price_col],
                        'Вес': row[weight_col],
                        'Файл': filename,
                        'Цена за кг': row[price_col] / row[weight_col] if row[weight_col] else 0
                    })
    return pd.DataFrame(data)


# Функция для поиска товаров
def search_products(df, query):
    filtered = df[df['Наименование'].str.contains(query, case=False, na=False)]
    return filtered.sort_values('Цена за кг')


# Функция для сохранения в HTML
def save_to_html(df, output_file):
    df.to_html(output_file, index=False)


def main():
    directory = 'C://Users//Vitaly//Documents//Practikal_task//Analisator'  # Замените на свой путь
    df = load_data(directory)

    while True:
        user_input = input('Введите название товара для поиска (или "exit" для выхода): ')
        if user_input.lower() == 'exit':
            print("Работа закончена.")
            break
        results = search_products(df, user_input)
        if not results.empty:
            print(results[['Наименование', 'Цена', 'Вес', 'Файл', 'Цена за кг']])
            # Сохранение результатов в HTML файл
            save_to_html(results, 'results.html')
            print("Результаты сохранены в 'results.html'.")
        else:
            print('Товары не найдены.')


if __name__ == "__main__":
    main()


### Объяснение кода:
# 1.Загрузка данных: Загрузка CSV - файлов с различными наименованиями столбцов.
# 2. Поиск и сортировка: Функция поиска позволяет находить товары по запросу
# и сортирует их по цене за килограмм.
# 3. Интерфейс: Цикл для получения ввода от пользователя с возможностью выхода.
# 4. Сохранение в HTML: Результат поиска сохраняется в HTML - файл.
