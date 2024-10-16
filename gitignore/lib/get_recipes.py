import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote

RAKUTEN_BASE_URL = "https://recipe.rakuten.co.jp" # 楽天レシピのURL

def create_search_recipes_url(ingredients): # 検索用のURLの作成
    query = quote(" ".join(ingredients)) # 材料をスペース区切って結合
    return f"{RAKUTEN_BASE_URL}/search/{query}"

def validate_recipe(recipe): # バリデーション
    if 'url' in recipe and 'image' in recipe and 'title' in recipe:
        return True
    return False

def fetch_recipes(ingredients): # レシピの取得
    url = create_search_recipes_url(ingredients)
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    recipes = []

    for element in soup.select('.recipe_ranking__item'):
        image = element.select_one(".recipe_ranking__item img")['src'] # 画像
        title = element.select_one('.recipe_ranking__recipe_title').text # タイトル
        url = element.select_one('.recipe_ranking__item a')['href'] # URL

        full_url = urljoin(RAKUTEN_BASE_URL, url) if url else None
        
        new_recipe = {'url': full_url, 'image': image, 'title': title}
        
        if validate_recipe(new_recipe):
            recipes.append(new_recipe)
        else:
            print(f"Invalid recipe: {new_recipe}")
    
    return recipes
