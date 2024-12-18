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

    n = len(chosen_nicknames)
    if n < 3:
        return "팀을 생성할 충분한 인원이 없습니다!", 400

    # 팀 당 인원 수 설정
    team_size = 3
    max_teams = 8

    if n >= team_size * max_teams:
        # 정확히 24명을 선택하여 8팀 생성
        selected_people = random.sample(chosen_nicknames, team_size * max_teams)
        num_teams = max_teams
    else:
        # 가능한 만큼 팀 생성
        selected_people = random.sample(chosen_nicknames, n)
        num_teams = n // team_size

    # 참가자 무작위로 섞기
    random.shuffle(selected_people)

    # 팀 생성
    teams = [selected_people[i*team_size:(i+1)*team_size] for i in range(num_teams)]

    # 나머지 참가자 처리 (반드시 팀에 포함)
    remainder = len(selected_people) % team_size
    if remainder != 0 and n >= team_size * max_teams:
        for i in range(remainder):
            teams[i % num_teams].append(selected_people[num_teams*team_size + i])

    return render_template('teams.html', teams=teams)

if __name__ == '__main__':
    app.run(debug=True)
