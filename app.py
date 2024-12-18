from flask import Flask, render_template, request, redirect, url_for
import random, json

app = Flask(__name__)

# 앱 시작 시 categories.json 불러오기 (전처리 과정을 통해 이미 생성한 파일)
with open('categories.json', 'r', encoding='utf-8') as f:
    categories = json.load(f)
    # categories = { "1번": [...], "2번": [...], "3번": [...] }

@app.route('/')
def home():
    # 카테고리 키 (1번, 2번, 3번)를 select 박스에서 보여주기 위해 전달
    category_list = list(categories.keys())  # ["1번", "2번", "3번"]
    return render_template('index.html', categories=categories, category_list=category_list)

@app.route('/generate_teams', methods=['POST'])
def generate_teams():
    selected_category = request.form.get('category')
    # 'category' 값이 '1번', '2번', '3번' 중 하나라고 가정
    # 선택한 카테고리의 닉네임들을 가져오기
    chosen_nicknames = categories.get(selected_category, [])

    if len(chosen_nicknames) < 24:
        return "Not enough nicknames in this category to generate 8 teams!", 400

    selected_people = random.sample(chosen_nicknames, 24)
    random.shuffle(selected_people)
    teams = [selected_people[i:i + 3] for i in range(0, 24, 3)]

    return render_template('teams.html', teams=teams)

if __name__ == '__main__':
    app.run(debug=True)
