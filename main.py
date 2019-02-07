from selenium import webdriver
from selenium.webdriver.common.keys import Keys

SITE_PATH = "http://www.musicscore.co.kr/" #음악 다운로드 사이트
DRIVER_PATH = "./setup/chromedriver.exe" #크롬 드라이버 경로

mem_id = ""
mem_pwd = ""


## 검색 결과 리스트 출력
def __get_search_result_list__() :
    try:
        res_table_body = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div/table")
        rows = res_table_body.find_elements_by_css_selector("tr")

        search_result_list = []  # 검색 결과 리스트
        for row in rows:
            res = row.find_elements_by_css_selector("a")[1].text  # 노래제목 \n 가수
            temp = res.split("\n")  # [노래제목, 가수]
            temp.append(row.find_element_by_class_name("btn-primary"))  # [노래제목, 가수, 담기버튼]
            search_result_list.append(temp)
        return search_result_list
    except:  # 검색 결과가 없을 경우
        print("검색 결과가 없습니다.")
        driver.close()
        return None
while(True):
    print("\r\n\r\n------------------------------------------------")
    print("노래 제목을 입력해 주세요.\r\n종료하려면 '종료'를 입력하세요.")
    music_name = input("입력:")
    music_name = music_name.replace(" ","")
    if music_name == "종료":
        break


    driver = webdriver.Chrome(DRIVER_PATH)
    login_page = SITE_PATH + "member/login.asp"
    driver.get(login_page)

    id_elem = driver.find_element_by_id("mem_id")
    pwd_elem = driver.find_element_by_id("mem_passwd")
    login_submit_btn = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/form/button")

    id_elem.clear()
    pwd_elem.clear()

    id_elem.send_keys(mem_id)
    pwd_elem.send_keys(mem_pwd)
    login_submit_btn.send_keys(Keys.ENTER)

    ## 노래 검색
    search_elem = driver.find_element_by_xpath("//*[@id=\"search_score\"]/fieldset/div/input")
    search_submit_btn = driver.find_element_by_xpath("//*[@id=\"search_score\"]/fieldset/div/span/button")

    search_elem.clear()
    search_elem.send_keys(music_name)
    search_submit_btn.send_keys(Keys.ENTER)

    res_list = __get_search_result_list__() #[[노래제목, 가수, 담기버튼],[노래제목, 가수, 담기버튼],...]
    if res_list == None :
        continue
    else :
        driver.minimize_window()
        print("#########노래 번호를 선택하세요############")
        num = 0
        for res in res_list :
            print(str(num)+"번"+" || "+res[0]+" || "+res[1])
            num+=1

        selected_idx = input("번호:")

        if "번" in selected_idx :
            selected_idx = selected_idx.replace("번","")
        # TODO : 2번까지밖에 없는데 3입력했을 경우 처리

        driver.maximize_window()

        #장바구니에 담기
        store_btn = res_list[int(selected_idx)][2] #'담기' 버튼
        store_btn.send_keys(Keys.ENTER)

        #장바구니로 이동
        driver.get("http://www.musicscore.co.kr/member/mybag.asp")

        #악보 구매
        try:
            buy_check_box = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[1]/input")
            buy_check_box.click()
            buy_btn = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/div[4]/div[1]/a")
            buy_btn.click()
            confirm_btn = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/div/div/div[3]/div[1]/form/button")
            confirm_btn.click()
        except :
            print("이미 구매한 악보입니다.")
            driver.close()
            continue

        #악보 프린트
        driver.get("http://www.musicscore.co.kr/member/aftersell.asp")
        download_search_elem = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/form/fieldset/div/input")
        download_search_elem.send_keys(music_name)
        download_search_elem.send_keys(Keys.ENTER)

        download_view_elem = driver.find_element_by_xpath("//*[@id=\"form_send1\"]/button")
        download_view_elem.click()
