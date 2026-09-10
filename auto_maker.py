import os
import urllib.parse
import random
import shutil

# 1. 🎯 [집사남] 전용 10개 핵심 항목
ITEMS = [
    "볼라드", "논슬립패드", "반사경", "아스콘부분보수", "주차금지봉", 
    "차량진입판", "카스토퍼", "코너보호대", "차선규제봉", "표지판설치"
]

TEMPLATE_FILE = "template.html"
OUTPUT_DIR = "완성본"

# 2. 🧠 항목별 Jipsanam(집사남) 친화적 DB
ITEM_DB = {
    "볼라드": {"desc": "스텐볼라드 파손 교체 및 신규 앙카/매립 설치를 안전하게 진행해 드립니다.", "keywords": "진입 차단, 보행자 보호", "aliases": ["볼라드", "스텐볼라드", "주차단속봉"]},
    "논슬립패드": {"desc": "미끄러운 실내외 계단에 알루미늄 논슬립 패드를 들뜸 없이 꼼꼼하게 시공합니다.", "keywords": "계단 미끄럼방지, 낙상 예방", "aliases": ["논슬립패드", "계단논슬립"]},
    "반사경": {"desc": "창고 출입구, 주차장 등 사각지대 사고 예방을 위해 최적의 각도로 거울을 설치합니다.", "keywords": "사각지대, 볼록거울", "aliases": ["반사경", "도로반사경", "안전거울"]},
    "아스콘부분보수": {"desc": "노후화되어 파인 포트홀을 새 아스콘으로 평탄하게 땜빵 보수해 드립니다.", "keywords": "포트홀 보수, 평탄화 작업", "aliases": ["아스콘부분보수", "아스팔트보수", "바닥땜빵"]},
    "주차금지봉": {"desc": "가게 앞, 개인 주차 공간을 확실히 지킬 수 있는 자물쇠형 접이식 봉을 설치합니다.", "keywords": "지정 주차구역, 튼튼한 고정", "aliases": ["주차금지봉", "접이식주차봉", "주차차단봉"]},
    "차량진입판": {"desc": "높은 경계석 단차 때문에 통행이 불편한 진입로에 부드러운 차량 진입판을 시공합니다.", "keywords": "단차 턱낮춤, 충격 흡수", "aliases": ["차량진입판", "경계석진입판", "턱낮춤"]},
    "카스토퍼": {"desc": "상가 앞 주차 구역에 차량 규격에 맞춰 국산 고강도 스토퍼를 단단하게 고정해 드립니다.", "keywords": "주차장 안전, 튼튼한 앙카", "aliases": ["카스토퍼", "주차블럭", "주차스토퍼"]},
    "코너보호대": {"desc": "주차장 기둥과 차량 보호를 위해 시인성 뛰어난 새 코너가드로 튼튼하게 교체합니다.", "keywords": "모서리가드, 긁힘 방지", "aliases": ["코너보호대", "주차장코너가드", "기둥보호대"]},
    "차선규제봉": {"desc": "관공서, 상가 앞 고질적인 불법 주정차 방지를 위해 탄성 좋은 시선유도봉을 시공합니다.", "keywords": "불법주차 방지, 차선 분리", "aliases": ["차선규제봉", "시선유도봉", "탄력봉"]},
    "표지판설치": {"desc": "주차구역 안내 등 각종 지주형 표지판을 강풍에도 끄떡없이 단단하게 매립해 드립니다.", "keywords": "표지판 매립, 규격 준수", "aliases": ["표지판설치", "표지판매립", "안내판설치"]},
}

# 3. 📸 완벽 맞춤형 갤러리 10개 (jipsanam_1 ~ 10, 정확한 제목과 3줄 설명)
BEFORE_AFTER_GALLERY = [
    {"item": "볼라드", "html": '<div class="photo-item"><div class="before-after-wrap"><div class="img-box"><span class="img-label label-before">시공 전</span><img src="jipsanam_1_before.webp" alt="스텐볼라드 파손" loading="lazy"></div><div class="img-box"><span class="img-label label-after">시공 후</span><img src="jipsanam_1_after.webp" alt="스텐볼라드 교체" loading="lazy"></div></div><div class="photo-text-wrap"><div class="photo-title">📍 전용 차량 진입방지 매립이동식 스텐볼라드 파손 교체</div><div class="photo-desc">차량 충돌로 훼손된 기존 볼라드를 철거하고,<br>내구성이 뛰어난 스텐볼라드로 튼튼하게 교체 시공하여<br>외부 차량의 무단 진입을 완벽히 차단했습니다.</div></div></div>'},
    {"item": "논슬립패드", "html": '<div class="photo-item"><div class="before-after-wrap"><div class="img-box"><span class="img-label label-before">시공 전</span><img src="jipsanam_2_before.webp" alt="미끄러운 실내계단" loading="lazy"></div><div class="img-box"><span class="img-label label-after">시공 후</span><img src="jipsanam_2_after.webp" alt="논슬립패드 설치" loading="lazy"></div></div><div class="photo-text-wrap"><div class="photo-title">📍 꼬마빌딩 실내계단 논슬립패드 설치</div><div class="photo-desc">비와 눈으로 미끄러운 꼬마빌딩 실내 계단에<br>접착력이 우수한 고강도 알루미늄 논슬립패드를 설치해<br>보행자의 낙상 사고를 예방하는 환경을 조성했습니다.</div></div></div>'},
    {"item": "반사경", "html": '<div class="photo-item"><div class="before-after-wrap"><div class="img-box"><span class="img-label label-before">시공 전</span><img src="jipsanam_3_before.webp" alt="창고 입구 사각지대" loading="lazy"></div><div class="img-box"><span class="img-label label-after">시공 후</span><img src="jipsanam_3_after.webp" alt="벽부형 반사경 설치" loading="lazy"></div></div><div class="photo-text-wrap"><div class="photo-title">📍 창고 입구 벽부형 반사경 설치</div><div class="photo-desc">지게차와 화물차 이동이 잦은 창고 출입구 사각지대에<br>시인성 좋은 벽부형 반사경을 최적의 각도로 설치하여<br>충돌 사고 위험을 확실하게 낮췄습니다.</div></div></div>'},
    {"item": "차량진입판", "html": '<div class="photo-item"><div class="before-after-wrap"><div class="img-box"><span class="img-label label-before">시공 전</span><img src="jipsanam_4_before.webp" alt="아파트 진입로 단차" loading="lazy"></div><div class="img-box"><span class="img-label label-after">시공 후</span><img src="jipsanam_4_after.webp" alt="차량진입판 설치" loading="lazy"></div></div><div class="photo-text-wrap"><div class="photo-title">📍 아파트 진입로 단차 차량진입판 설치</div><div class="photo-desc">경계석 단차가 높아 통행이 불편했던 아파트 진입로에<br>충격 흡수에 탁월한 고무 재질의 차량진입판을 시공하여<br>차량 하부 긁힘 없는 부드러운 진출입이 가능해졌습니다.</div></div></div>'},
    {"item": "아스콘부분보수", "html": '<div class="photo-item"><div class="before-after-wrap"><div class="img-box"><span class="img-label label-before">시공 전</span><img src="jipsanam_5_before.webp" alt="바닥 파손 포트홀" loading="lazy"></div><div class="img-box"><span class="img-label label-after">시공 후</span><img src="jipsanam_5_after.webp" alt="아스콘 부분보수" loading="lazy"></div></div><div class="photo-text-wrap"><div class="photo-title">📍 오피스텔 주차장 진입로 바닥 파손 아스콘 부분보수</div><div class="photo-desc">노후화되어 심하게 파인 주차장 진입로 바닥을<br>새 아스콘으로 평탄화 및 꼼꼼하게 땜빵 보수하여<br>차량의 덜컹거림과 타이어 손상 위험을 해결했습니다.</div></div></div>'},
    {"item": "코너보호대", "html": '<div class="photo-item"><div class="before-after-wrap"><div class="img-box"><span class="img-label label-before">시공 전</span><img src="jipsanam_6_before.webp" alt="지하주차장 코너 파손" loading="lazy"></div><div class="img-box"><span class="img-label label-after">시공 후</span><img src="jipsanam_6_after.webp" alt="코너보호대 파손 교체" loading="lazy"></div></div><div class="photo-text-wrap"><div class="photo-title">📍 아파트 지하주차장 코너보호대 파손 교체</div><div class="photo-desc">주차 중 잦은 접촉으로 찢어진 기존 코너가드를 철거 후,<br>시인성이 뛰어난 새 고강도 코너보호대로 교체 부착하여<br>건물 벽면과 입주민의 차량을 동시에 보호합니다.</div></div></div>'},
    {"item": "표지판설치", "html": '<div class="photo-item"><div class="before-after-wrap"><div class="img-box"><span class="img-label label-before">시공 전</span><img src="jipsanam_7_before.webp" alt="상가 전용 주차장 표지판 없음" loading="lazy"></div><div class="img-box"><span class="img-label label-after">시공 후</span><img src="jipsanam_7_after.webp" alt="표지판 매립 설치" loading="lazy"></div></div><div class="photo-text-wrap"><div class="photo-title">📍 상가 전용 주차장 표지판 매립</div><div class="photo-desc">지정 주차 구역 안내를 확실히 명시하기 위해<br>바닥을 깊게 천공하고 고강도 시멘트를 타설하는 매립 시공으로<br>강풍에도 흔들림 없는 지주형 표지판을 세웠습니다.</div></div></div>'},
    {"item": "차선규제봉", "html": '<div class="photo-item"><div class="before-after-wrap"><div class="img-box"><span class="img-label label-before">시공 전</span><img src="jipsanam_8_before.webp" alt="불법주정차 관공서 입구" loading="lazy"></div><div class="img-box"><span class="img-label label-after">시공 후</span><img src="jipsanam_8_after.webp" alt="차선규제봉 설치" loading="lazy"></div></div><div class="photo-text-wrap"><div class="photo-title">📍 관공서 입구 차선규제봉 설치</div><div class="photo-desc">고질적인 불법 주정차 방지 및 명확한 차선 분리를 위해<br>복원력이 우수한 폴리우레탄 차선규제봉(시선유도봉)을<br>정확한 간격과 튼튼한 앙카 작업으로 고정했습니다.</div></div></div>'},
    {"item": "카스토퍼", "html": '<div class="photo-item"><div class="before-after-wrap"><div class="img-box"><span class="img-label label-before">시공 전</span><img src="jipsanam_9_before.webp" alt="카스토퍼 미설치 주차장" loading="lazy"></div><div class="img-box"><span class="img-label label-after">시공 후</span><img src="jipsanam_9_after.webp" alt="카스토퍼 설치 완료" loading="lazy"></div></div><div class="photo-text-wrap"><div class="photo-title">📍 상가 앞 주차장 카스토퍼 설치</div><div class="photo-desc">주차 시 후면 벽체와의 충돌을 완벽하게 막기 위해<br>주차 구역 라인에 국산 3구 고강도 카스토퍼를<br>차량 규격에 맞춰 안전하고 단단하게 고정했습니다.</div></div></div>'},
    {"item": "주차금지봉", "html": '<div class="photo-item"><div class="before-after-wrap"><div class="img-box"><span class="img-label label-before">시공 전</span><img src="jipsanam_10_before.webp" alt="무단주차 가게 앞" loading="lazy"></div><div class="img-box"><span class="img-label label-after">시공 후</span><img src="jipsanam_10_after.webp" alt="주차금지봉 설치" loading="lazy"></div></div><div class="photo-text-wrap"><div class="photo-title">📍 가게 앞 주차금지봉 설치</div><div class="photo-desc">가게 앞 무단 주차로 인한 영업 방해를 차단하기 위해<br>누구나 손쉽게 접고 펼 수 있는 자물쇠형 주차금지봉을 시공하여<br>상가 전용 주차 공간을 확실하게 확보했습니다.</div></div></div>'}
]

# 4. 리뷰 모음
ALL_REVIEWS = [
    '<div class="review-card"><div class="star-rating">★★★★★</div><p class="review-text">"1개만 교체하는 거라 미안했는데, 너무 친절하게 수평까지 딱 맞춰주셨습니다."</p><div class="review-author">- 화성 빌라 입주민</div></div>',
    '<div class="review-card"><div class="star-rating">★★★★★</div><p class="review-text">"상가 앞 단차가 심해서 차량진입판 의뢰했는데 들뜸 하나 없이 깔끔하게 깔아주셨어요."</p><div class="review-author">- 용인 상가 사장님</div></div>',
    '<div class="review-card"><div class="star-rating">★★★★★</div><p class="review-text">"사각지대 반사경 위치를 전문가답게 딱 잡아주셔서 이제 주차하기 편안합니다."</p><div class="review-author">- 수원 원룸 건물주</div></div>',
    '<div class="review-card"><div class="star-rating">★★★★★</div><p class="review-text">"아스콘 파인 곳 소량 보수도 깔끔하게 해주시고 주변 정리까지 완벽했습니다."</p><div class="review-author">- 안양 오피스텔 관리소장님</div></div>',
    '<div class="review-card"><div class="star-rating">★★★★★</div><p class="review-text">"우리 주차장 자리에 외부차량이 자꾸 대서 주차금지봉 달았는데 스트레스 싹 날아갔어요."</p><div class="review-author">- 분당 xx이자카야 사장님</div></div>'
]

def create_pages():
    try:
        print("🚀 [집사남 전용] HTML 복제 공장 가동을 시작합니다!\n")
        current_folder = os.path.dirname(os.path.abspath(__file__))
        os.chdir(current_folder)
        
        if os.path.exists(OUTPUT_DIR):
            if os.path.basename(OUTPUT_DIR) == "완성본":
                shutil.rmtree(OUTPUT_DIR)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        target_file = None
        for name in ["지역리스트.txt", "지역리스트"]:
            if os.path.exists(name):
                target_file = name
                break

        if target_file is None:
            print("❌ '지역리스트.txt' 파일이 없습니다!")
            return
            
        with open(target_file, "r", encoding="utf-8") as f:
            raw_regions = [line.strip() for line in f.readlines() if line.strip()]
            regions = list(dict.fromkeys(raw_regions))

        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()

        total_count = 0

        for region in regions:
            for item in ITEMS:
                safe_region = region.replace(" ", "_")
                safe_item = item.replace(" ", "_").replace("/", "_")
                file_name = f"{safe_region}_{safe_item}.html"
                file_path = os.path.join(OUTPUT_DIR, file_name)
                
                seed_val = f"{region}_{item}"
                rng = random.Random(seed_val)
                
                item_info = ITEM_DB.get(item, {"desc": "꼼꼼하고 안전하게 시공합니다.", "keywords": "소량시공, 맞춤시공", "aliases": [item]})
                related_keywords_str = ", ".join(item_info["aliases"])
                
                # 타깃 키워드와 매칭되는 갤러리를 가장 1번으로 빼기
                matching_blocks = [g["html"] for g in BEFORE_AFTER_GALLERY if g["item"] == item]
                filler_blocks = [g["html"] for g in BEFORE_AFTER_GALLERY if g["item"] != item]
                rng.shuffle(filler_blocks)
                
                final_gallery_blocks = matching_blocks + filler_blocks
                final_gallery_html = "".join(final_gallery_blocks[:10]) 
                
                rng.shuffle(ALL_REVIEWS)
                reviews_html = "".join(ALL_REVIEWS[:5])
                
                custom_html = html_content.replace("{지역명}", region)
                custom_html = custom_html.replace("{시공항목}", item)
                custom_html = custom_html.replace("{DB_설명}", item_info["desc"])
                custom_html = custom_html.replace("{DB_키워드}", item_info["keywords"])
                custom_html = custom_html.replace("{연관검색어}", related_keywords_str)
                custom_html = custom_html.replace("{스마트_갤러리}", final_gallery_html)
                custom_html = custom_html.replace("{스마트_리뷰}", reviews_html)
                
                safe_url_name = urllib.parse.quote(file_name)
                target_url = f"https://jipsanam.github.io/{safe_url_name}" 
                custom_html = custom_html.replace("{CANONICAL_URL}", target_url)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(custom_html)
                
                total_count += 1
                
        print(f"\n🎉 [집사남] 총 {total_count}개의 HTML 파일이 완벽하게 생성되었습니다!")
        
    except Exception as e:
        print("\n❌ 에러 발생:", e)
        
    input("\n엔터 키를 누르면 창이 닫힙니다...")

if __name__ == "__main__":
    create_pages()