import openai
import requests
from PIL import Image
from io import BytesIO
from rembg import remove

# Установите ваш API ключ OpenAI
openai.api_key = ''

def generate_images(description, n=2):
    """
    Задача 1: Генерация изображений по описанию
    """
    response = openai.Image.create(
        prompt=description,
        n=n,
        size="256x256"
    )
    return [item['url'] for item in response['data']]

def enhance_description(description):
    """
    Задача 2: Улучшение описания с помощью ChatGPT
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative assistant that enhances image descriptions."},
            {"role": "user", "content": f"Enhance this image description to make it more detailed and interesting: {description}"}
        ]
    )
    return response.choices[0].message['content']

def generate_enhanced_images(description, n=2):
    """
    Комбинация задач 1 и 2
    """
    enhanced_description = enhance_description(description)
    return generate_images(enhanced_description, n)

def generate_image_variation(image_path):
    """
    Задача 3: Генерация вариации изображения
    """
    with open(image_path, "rb") as image_file:
        response = openai.Image.create_variation(
            image=image_file,
            n=1,
            size="1024x1024"
        )
    return response['data'][0]['url']

def edit_image_background(image_path, prompt):
    """
    Задача 4: Редактирование фона изображения
    """
    # Удаление фона
    with open(image_path, "rb") as image_file:
        input_image = Image.open(image_file)
        output_image = remove(input_image)
    
    # Сохранение изображения без фона
    temp_path = "temp_no_bg.png"
    output_image.save(temp_path, format="PNG")
    
    # Редактирование изображения с помощью DALL-E
    with open(temp_path, "rb") as image_file:
        response = openai.Image.create_edit(
            image=image_file,
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
    
    return response['data'][0]['url']

# Пример использования функций
if __name__ == "__main__":
    # Задача 1 и 2
    description = "A cat sitting on a moon"
    urls = generate_enhanced_images(description)
    print("Enhanced image URLs:", urls)
    
    # Задача 3
    variation_url = generate_image_variation("path/to/your/image.jpg")
    print("Variation URL:", variation_url)
    
    # Задача 4
    edited_url = edit_image_background("path/to/your/portrait.jpg", "Add a fantasy landscape background")
    print("Edited image URL:", edited_url)
