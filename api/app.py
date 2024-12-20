from flask import Flask, render_template, request, redirect, url_for
import random
import json
import os

# Flask 앱 초기화
app = Flask(
    __name__,
    template_folder="../templates",  # 템플릿 경로
    static_folder="../static"        # 정적 파일 경로
)

# JSON 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'categories.json')

# JSON 파일 로드 함수
def load_categories():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# 초기 데이터 로드
categories = load_categories()

@app.route('/')
def home():
    """
    메인 페이지: 카테고리와 데이터를 전달
    """
    category_list = list(categories.keys())  # ["1번", "2번", "3번"]
    return render_template('index.html', categories=categories, category_list=category_list)

@app.route('/generate_teams', methods=['POST'])
def generate_teams():
    """
    팀 생성 페이지: 선택된 카테고리에서 팀 구성
    """
    selected_category = request.form.get('category')  # 선택된 카테고리
    chosen_nicknames = categories.get(selected_category, [])  # 해당 카테고리의 닉네임 목록

    n = len(chosen_nicknames)
    if n < 3:
        return "팀을 생성할 충분한 인원이 없습니다!", 400

    # 팀 구성 로직
    team_size = 3  # 한 팀당 인원 수
    max_teams = 8  # 최대 팀 수

    if n >= team_size * max_teams:
        selected_people = random.sample(chosen_nicknames, team_size * max_teams)
        num_teams = max_teams
    else:
        selected_people = chosen_nicknames
        num_teams = n // team_size

    # 참가자 무작위 섞기
    random.shuffle(selected_people)

    # 팀 나누기
    teams = [selected_people[i * team_size:(i + 1) * team_size] for i in range(num_teams)]

    # 잔여 인원 분배
    remainder = len(selected_people) % team_size
    if remainder != 0:
        for i, person in enumerate(selected_people[-remainder:]):
            teams[i % num_teams].append(person)

    return render_template('teams.html', teams=teams, selected_category=selected_category)

@app.route('/add_data', methods=['POST'])
def add_data():
    """
    선택된 카테고리에 닉네임 추가
    """
    global categories  # 전역 변수 업데이트를 위해 global 사용
    category = request.form.get('category')  # 선택된 카테고리
    nicknames = request.form.get('nicknames')  # 입력된 닉네임들

    # 닉네임들을 "/" 기준으로 분리
    nickname_list = [name.strip() for name in nicknames.split('/') if name.strip()]

    # 선택된 카테고리에 추가
    if category in categories:
        categories[category].extend(nickname_list)

        # 중복 제거
        categories[category] = list(set(categories[category]))

        # JSON 파일 업데이트
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)

        # JSON 파일을 다시 읽어 categories 변수 업데이트
        categories = load_categories()

        return redirect(url_for('home'))  # 메인 페이지로 리디렉션
    else:
        return "잘못된 카테고리 선택", 400
    
@app.route('/delete_data', methods=['POST'])
def delete_data():
    """
    선택된 닉네임 삭제
    """
    global categories
    category = request.form.get('category')
    nickname = request.form.get('nickname')

    if category in categories and nickname in categories[category]:
        categories[category].remove(nickname)

        # JSON 파일 업데이트
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)

        # JSON 파일 다시 로드
        categories = load_categories()

        return redirect(url_for('home'))
    else:
        return "잘못된 요청입니다.", 400


if __name__ == '__main__':
    app.run(debug=True)
