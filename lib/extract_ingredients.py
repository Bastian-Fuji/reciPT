import config
from openai import OpenAI
import base64

client = OpenAI(api_key=config.OPENAI_API_KEY)

def encode_image(image_path): # 画像をbase64にエンコード
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def parse_ingredients(ingredients_text): # 出力結果の整形
        ingredients_list = [line.strip('- ').strip() for line in ingredients_text.split('\n') if line.strip()]
        return ingredients_list

def get_ingredients_list(image_path): # ChatGPTのAPIを使用して画像から材料リストを抽出
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": [
                {"type": "text", "text": "Please list the specific ingredients contained in this image in Japanese only and in short words. Output a list of ingredients."},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.0,
    )

    res = response.choices[0].message.content
    ingredients_list = parse_ingredients(res)
    return ingredients_list
