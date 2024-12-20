from flask import Flask, render_template, request, redirect, url_for
import random, json
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# 앱 시작 시 categories.json 불러오기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'categories.json')

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    categories = json.load(f)

@app.route('/')
def home():
    category_list = list(categories.keys())  # 카테고리 목록 전달
    return render_template('index.html', category_list=category_list)

@app.route('/generate_teams', methods=['POST'])
def generate_teams():
    selected_category = request.form.get('category')
    chosen_nicknames = categories.get(selected_category, [])

    n = len(chosen_nicknames)
    if n < 3:
        return "팀을 생성할 충분한 인원이 없습니다!", 400

    team_size = 3
    max_teams = 8

    if n >= team_size * max_teams:
        selected_people = random.sample(chosen_nicknames, team_size * max_teams)
        num_teams = max_teams
    else:
        selected_people = random.sample(chosen_nicknames, n)
        num_teams = n // team_size

    random.shuffle(selected_people)
    teams = [selected_people[i*team_size:(i+1)*team_size] for i in range(num_teams)]

    remainder = len(selected_people) % team_size
    if remainder != 0:
        for i, person in enumerate(selected_people[-remainder:]):
            teams[i % num_teams].append(person)

    return render_template('teams.html', teams=teams)

if __name__ == '__main__':
    app.run(debug=True)
