import json

# 1. 원본 데이터 준비
data = """
참여 3번 / 월석 
참여 1번 / 츤구미
참여 3번 / 땡컨07

참여 1번 / 보랏빛
참여 3번 /  SoulJJW
참여 1번 / 스바루와에밀리아

참여 2번 / 호랑이코털
참여 1번 / 저돌맹진우디르
참여 3번 / 뉴질랜드
참여 1번 / 건랜스
참여 1번 /  꼬마 고양이 누코
참여 1번 / 무지성청소부
참여 1번 /  김하련
참여 3번 / 모스트아니면던짐
참여 2번 / 백절불굴
참여 3번 / 카하

참여 3번 / 모히또s
참여 3번 / 먀캬롱
참여 1번 / 하이롤링
참여 1번 / 민시아
참여 1번 / 허송하
참여 1번 / 재리임
참여 3번 / 비오는어느여름날
참여 1번 / 시셀루
참여 3번 / 박힘
참여 1번 / 이롯치유튜브구독
참여 3번 / 홍유진
참여 3번 / 묭루
참여 1번 / fonias
참여 3번 / 모라도리
참여 1번 / 마주치면박살
참여 3번 / OIF
참여 3번 / 흑조롱이
참여 1번 / 각보이면걍박음
참여 2번 / 코힐
참여 1번 / 홍재원개패기
참여 3번 / 활활타는청년
참여 2번 / 네온아잘좀하자
참여 3번 / 생각없이하는중
참여 3번 / stellarcium
참여 2번 / 아비게일포탈구멍
참여 1번 / 죽이면그만이야
참여 3번 / 주라미
참여 3번 / sorasakihina
참여 3번 / kmdkm
참여 2번 / 정치의신문재1인
참여 3번 / 다람씨
참여 3번 / oblivio
참여 3번 / GeForceNow실비아
참여 3번 / 배수
참여 2번 / whatabout
참여 3번 / 아이리 kanna
참여 1번 / 소아성도착증
참여 3번 / 지켜줘요
참여 1번 / 아디나의오물풍선
참여 1번 / 애정결핍
참여 1번 / 우이0
참여 1번 / 이승무스톰레이지
참여 3번 / 여운울
참여 3번 / 찡하
참여 1번 / 스이

참여 3번 / 라푸태온

참여 3번 / 하누씌
참여 1번 / Shealke
참여 2번 / KuroPenguin
참여 1번 / summer12512
참여 1번 / ペトナナ
참여 1번 / 보빔열발전기
참여 1번 / 방찌
참여 3번 / 구미대권은현
참여 2번 / 코이
참여 3번 / grimheart
참여 2번 / sandart
참여 1번 / 가젯
참여 1번 / 돔공연축하해스이
참여 1번 / 건전한닉네임3697
참여 2번 / 원사이클

참여 3번 / 나도잘할래
참여 1번 / 단단우
참여 3번 / Oliverslife
참여 1번 / imS2
참여 2번 / 장화13
참여 3번 / 가너
참여 3번 / 아싸루코가타
참여 3번 / pengzzo
참여 1번 / 절명이
참여 3번 / fallguy1843 
참여 1번 / 네오구리
참여 3번 / 유리프
참여 1번 /  매사에긍정
참여 3번 / 앤티오
참여 2번 /  我爱你姜海琳
참여 1번/ mallage
참여 3번 / ArkD
참여 3번 / 김네코
참여 2번 / 딸기몽쉘
참여 3번 / 天魔1
참여 3번 / 해삼속연가시
참여 1번 / 인도태
참여 1번 / iNEkANNA
참여 1번 / 점점늙고있어
참여 1번 / 무기좀제발
참여 2번 / 밥동주
참여 1번 / 따비서우내
참여 2번 / 난ap가좋아요
참여 3번 / 공찌
참여 2번 / 어재여비
참여 1번 / 바론대포미니언
참여 2번 / 이리는개과
참여 3번 / Ishmael2
참여 1번 / 박젺
참여 3번 / 제니누나나죽어
참여 1번 / 김상명
참여 1번 / 맬리를
참여 3번 / 이지희
참여 1번 / 카람빗
참여 3번 / 쪼잔

참여 3번 / 제주집킬러
참여 3번 / 따오
참여 3번 / 타르라스
참여 1번 / Haku6
참여 3번 / 은발병약미소녀
참여 1번 / Blache
참여 2번 / Roza
참여 3번 / 포카포카
참여 3번 / SKBB
참여 1번 / unfae
참여 1번 / 큰호빵
참여 1번 / 까영
참여 1번 / 이상향
참여 2번 / 징징벅

참여 3번 / 50cm자
참여 3번 / Ra1N29
참여 1번 / 한유설
참여 3번 / 퐁송
참여 1번 / 정령신사탱커
참여 1번 / 핑아
참여 3번 / Juxtap0sition
참여 3번 / 사리엘이에영
참여 3번 / ha2e
참여 3번/ 안녕난스노우맨
참여 3번 / 햄스터
참여 3번 / 이세돌막내비챤
참여 1번 / 대가25
참여 2번 / 어둠의이리단

"""

lines = [line.strip() for line in data.split('\n') if line.strip()]
processed_lines = []
for line in lines:
    # "참여" 단어 제거
    line = line.replace("참여", "").strip()
    # "X번/닉네임" 형태를 "X번 / 닉네임" 형태로 정리
    line = line.replace("번/", "번 / ")
    parts = line.split('/')
    if len(parts) == 2:
        category_part = parts[0].strip()  # "1번", "2번", "3번"
        nickname = parts[1].strip()
        processed_line = f"{category_part} / {nickname}"
        processed_lines.append(processed_line)

# 2. 카테고리별 딕셔너리 생성
categories = {
    "1번": [],
    "2번": [],
    "3번": []
}

for pline in processed_lines:
    # "X번 / 닉네임"
    cpart, nick = pline.split('/')
    cpart = cpart.strip()
    nick = nick.strip()
    if cpart in categories:
        categories[cpart].append(nick)

# 3. JSON 파일로 저장
with open('categories.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)