# -*- coding: utf-8 -*-
import sys
import os

# libフォルダをモジュール検索パスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash
import lib.extract_ingredients as extract_ingredients
import lib.get_recipes as get_recipes

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.secret_key = 'your_secret_key'  # フラッシュメッセージのためにシークレットキーを設定

# ファイルの保存フォルダを作成
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return redirect(url_for('show_recipes', image_path=file_path))
    else:
        flash('許可されていないファイル形式です。')
        return redirect(url_for('index'))

@app.route('/recipes')
def show_recipes():
    try:
        image_path = request.args.get('image_path')
        ingredients_list = extract_ingredients.get_ingredients_list(image_path) # 画像から材料リストを抽出
        if os.path.exists(image_path):
            os.remove(image_path)
        recipes = get_recipes.fetch_recipes(ingredients_list) # 材料リストを使用してレシピを取得
        return render_template('recipes.html', recipes=recipes)
    except Exception as e:
        return str(e)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
