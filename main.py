import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def open_chatgpt_and_authorize():
    USER_EMAIL = input("Введите ваш email: ")
    USER_PASSWORD = input("Введите ваш пароль: ")

    driver = uc.Chrome()

    try:
        driver.get("https://chat.openai.com")

        send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='login-button']")))
        send_button.click()

        email_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#email-input")))

        # Ввод email с задержкой
        for char in USER_EMAIL:
            email_input.send_keys(char)
            time.sleep(0.1)
        print("Email введён.")

        time.sleep(1)

        email_continue_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.continue-btn:not([disabled])")))
        email_continue_button.click()

        password_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#password")))

        # Ввод пароля с задержкой
        for char in USER_PASSWORD:
            password_input.send_keys(char)
            time.sleep(0.1)
        print("Пароль введён.")

        time.sleep(1)

        password_continue_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-action-button-primary='true']")))
        password_continue_button.click()

        code_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input._codeInput_p12g4_28")))

        # Получение кода из консоли
        code = input("Введите код из приложения: ")

        # Ввод кода с задержкой
        for char in code:
            code_input.send_keys(char)
            time.sleep(0.1)
        print("Код введён.")

        time.sleep(1)

        code_continue_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button._continueButton_p12g4_42")))
        code_continue_button.click()

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ProseMirror[contenteditable='true']")))

        # Цикл для продолжения работы
        previous_responses = []  # Список для всех предыдущих ответов
        while True:
            # Получение запроса от пользователя
            input_text = input("Введите текст для ChatGPT (или 'exit' для завершения): ")

            # Если введено "exit", выходим из цикла и завершаем работу
            if input_text.lower() == "exit":
                print("Завершаем работу парсера.")
                break

            input_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "prompt-textarea")))

            # Вводим текст в поле
            input_field.send_keys(input_text)

            send_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='send-button']")))
            send_button.click()

            time.sleep(15)

            response_message = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[data-message-author-role='assistant'] div.markdown.prose.w-full.break-words.dark\\:prose-invert.light")))

            response_text = response_message.text
            print(f"Ответ от ChatGPT: {response_text}")

            # Проверяем, не повторяется ли ответ
            if response_text in previous_responses:
                print("Ответ повторяется, ищем другой ответ...")
                other_responses = driver.find_elements(By.CSS_SELECTOR,"div[data-message-author-role='assistant'] div.markdown.prose.w-full.break-words.dark\\:prose-invert.light")
                for response in other_responses:
                    new_response_text = response.text
                    if new_response_text not in previous_responses:
                        response_text = new_response_text
                        print(f"Новый ответ от ChatGPT: {response_text}")
                        break

            previous_responses.append(response_text)

    except Exception as e:
        print(f"Ошибка во время авторизации или работы с ChatGPT: {e}")
    finally:
        driver.quit()

open_chatgpt_and_authorize()