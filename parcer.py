"""_============================================================_ИМПОРТИРУЕМ_НЕОБХОДИМЫЕ_БИБЛИОТЕКИ_============================================================_"""
import time # Для работы с временными задержками
import json # Для работы с форматом JSON
from selenium import webdriver # Для автоматизации браузера
from selenium.webdriver.common.by import By # Для поиска элементов на странице
from selenium.webdriver.support.ui import WebDriverWait # Для ожидания загрузки элементов
from selenium.webdriver.support import expected_conditions as EC # Для условий ожидания
from bs4 import BeautifulSoup # Для парсинга HTML-кода
"""_===================================================_СОЗДАНИЕ_ЭКЗЕМпЛЯРА_ВЕБ-ДРАЙВЕРА_ДЛЯ_БРАУЗЕРА_CHROME_===================================================_"""
driver = webdriver.Chrome()
"""_======================================================_ФУНКЦИЯ_ДЛЯ_ЗАГРУЗКИ_СТРАНИЦЫ_ПО_УКАЗАННОМУ_URL_=====================================================_"""
def load_page(url):
    driver.get(url) # Открываем страницу по указанному URL
    time.sleep(3) # Ждем 3 секунды, чтобы страница успела загрузиться
"""_===========================================================_ФУНКЦИЯ_ДЛЯ_ПОЛУЧЕНИЯ_КАТЕГОРИЙ_ТОВАРОВ_========================================================_"""
def get_categories():
    try:
        # Ожидаем, пока все элементы категорий станут доступными
        categories_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//ul[@class='sp-site-nav-mainlist']//li[@data-cid]") # XPath для поиска элементов категорий
            )
        )
    except Exception as e:
        # Если произошла ошибка, выводим сообщение и возвращаем пустой список
        print(f"Ошибка при загрузке категорий: {e}")
        return []

    categories = [] # Список для хранения категорий

    for category_element in categories_elements: # Проходим по всем найденным элементам категорий
        category_name = category_element.text.strip() # Получаем текст категории и убираем лишние пробелы
        category_url = category_element.find_element(By.XPATH, "..").get_attribute("data-href") # Получаем URL категории
        category_id = category_element.get_attribute("data-cid") # Получаем уникальный идентификатор категории
        categories.append((category_name, category_url, category_id)) # Добавляем категорию в список

    return categories # Возвращаем список категорий
"""_================================================_ФУНКЦИЯ_ДЛЯ_ПОЛУЧЕНИЯ_ПОДКАТЕГОРИЙ_ПО_ИДЕНТИФИКАТОРУ_КАТЕГОРИИ_============================================_"""
def get_subcategories(category_id):
    try:
        # Ожидаем, пока все элементы подкатегорий станут доступными
        subcategories_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, f"//ul[@data-pcid='{category_id}']//li//a/span") # XPath для поиска подкатегорий
            )
        )
    except Exception as e:
        # Если произошла ошибка, выводим сообщение и возвращаем пустой список
        print(f"Ошибка при загрузке подкатегорий для категории {category_id}: {e}")
        return []

    subcategories = [] # Список для хранения подкатегорий

    for element in subcategories_elements: # Проходим по всем найденным элементам подкатегорий
        span_element = element.get_attribute('innerHTML').strip() # Получаем HTML-код элемента
        soup = BeautifulSoup(span_element, 'html.parser') # Парсим HTML-код с помощью BeautifulSoup

        for small in soup.find_all('small'): # Находим все элементы  и удаляем их
            small.decompose()

        subcategory_url = element.find_element(By.XPATH, "..").get_attribute("href") # Получаем URL подкатегории
        subcategories.append((soup.get_text().strip(), subcategory_url)) # Добавляем подкатегорию в список

    return subcategories # Возвращаем список подкатегорий
"""_=======================================================_ФУНКЦИЯ_ДЛЯ_ПОЛУЧЕНИЯ_ТОВАРОВ_ПО_URL_ПОДКАТЕГОРИИ_===================================================_"""
def get_products(subcategory_url):
    load_page(subcategory_url) # Загружаем страницу подкатегории
    try:
        # Ожидаем, пока блок с товарами станет доступным
        products_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sp-product-list")) # Класс для контейнера товаров
        )
        products_elements = products_container.find_elements(By.CLASS_NAME, "sp-product-item") # Находим все элементы товаров

    except Exception:
        # Если произошла ошибка, просто возвращаем пустой список
        return []

    products = [] # Список для хранения товаров

    for product_element in products_elements: # Проходим по всем найденным элементам товаров
        title = product_element.find_element(By.CSS_SELECTOR,  ".sp-product-item__title a").text.strip() # Получаем название товара и убираем лишние пробелы
        code = product_element.find_element(By.CSS_SELECTOR, ".sp-product-item__code span").text.strip() # Получаем код товара и убираем лишние пробелы
        price = product_element.find_element(By.CSS_SELECTOR, ".sp-price-kit__price").text.strip() # Получаем цену товара и убираем лишние пробелы

        products.append((title, code, price)) # Добавляем информацию о товаре в список

    return products # Возвращаем список товаров
"""_=======================================================================_ОСНОВНАЯ_ФУНКЦИЯ_===================================================================_"""
def main():
    base_url = 'https://stroyparkdiy.ru' # Базовый URL сайта
    category_url = '/catalog/potolochnyie-i-stenovyie-pokryitiya' # URL категории товаров
    load_page(base_url + category_url) # Загружаем страницу категории

    categories = get_categories() # Получаем список категорий
    data = {"categories": []} # Структура для хранения данных о категориях и их подкатегориях

    for name, url, category_id in categories:  # Проходим по всем категориям
        category_data = { # Создаем структуру для хранения данных конкретной категории
            "name": name, # Название категории
            "url": url, # URL категории
            "subcategories": [] # Список для хранения подкатегорий
        }

        print(f"Категория: {name}, URL: {url}")

        # Получаем подкатегории для текущей категории
        subcategories = get_subcategories(category_id) # Получаем список подкатегорий
        for sub_name, sub_url in subcategories: # Проходим по всем подкатегориям
            subcategory_data = { # Создаем структуру для хранения данных конкретной подкатегории
                "name": sub_name, # Название подкатегории
                "url": sub_url, # URL подкатегории
                "products": [] # Список для хранения товаров подкатегории
            }

            print(f"Подкатегория: {sub_name}, URL: {sub_url}")

            # Получаем товары для каждой подкатегории
            products = get_products(sub_url) # Получаем список товаров

            if not products: # Если товары не найдены
                subcategory_data[
                    "products"] = "Это каталог и в нем нет товаров"  # Пишем сообщение о пустом каталоге

                print(f"Это каталог, в нем нет товаров")

            else: # Если товары найдены
                for product_title, product_code, product_price in products: # Проходим по всем товарам
                    subcategory_data["products"].append({ # Добавляем информацию о товаре в подкатегорию
                        "title": product_title, # Название товара
                        "code": product_code, # Код товара
                        "price": product_price # Цена товара
                    })

                    print(f"Товар: {product_title}, Код: {product_code}, Цена: {product_price}")

            category_data["subcategories"].append(subcategory_data) # Добавляем подкатегорию в категорию

        data["categories"].append(category_data) # Добавляем категорию в общий список данных

    # Записываем данные в файл
    with open('data.json', 'w', encoding='utf-8') as f: # Открываем файл для записи
        json.dump(data, f, ensure_ascii=False, indent=4) # Записываем данные в формате JSON

    driver.quit() # Закрываем браузер
"""_=======================================================================_ЗАПУСК_ПРОГРАММЫ_===================================================================_"""
if __name__ == "__main__": # Проверяем, запущена ли эта программа как основная
    main() # Запускаем основную функцию
"""_============================================================================================================================================================_"""