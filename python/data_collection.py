import os
# os.chdir(path = "C:/Users/msi/Desktop/work/study/soccer_data_analysis" )

import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import numpy as np

# =============================================================================
# -- driver start
# =============================================================================
def base_page( driver_dir, url ):
    driver = webdriver.Chrome( driver_dir )
    
    # start page
    driver.get( url )
    
    # page of players
    driver.find_element_by_css_selector("button.btn_nav").click()
    driver.find_elements_by_css_selector("nav.menu > ul > li")[7].click()
    
    # page of national players
    if driver.find_elements_by_css_selector("tr > td") == []:
        time.sleep( 1 )
    driver.find_elements_by_css_selector("tr > td")[0].click()
    
    return( driver )

# =============================================================================
# -- crawling basic information
# =============================================================================
def basic_info(  driver_dir: str
               , url: str = "http://www.kfamatch.or.kr/svc/man/selectMainInfo.do"
               , max_page: int = 37 ):
    # base page
    driver = base_page( driver_dir, url = url )
    
    # player name and position
    player_name_list, position_list = [], []

    for page in range( max_page ):
        # go to page
        page_next = page % 10
        
        driver.find_elements_by_css_selector("a.num")[ page_next ].click()
        
        ## --START: crawling 10 players
        # player name & position
        time.sleep( 1 )
        player_name_css = driver.find_elements_by_css_selector("p.subject")
        player_name = [name.text for name in player_name_css]
        
        position_css = driver.find_elements_by_css_selector("p.summary")
        position = [name.text for name in position_css if name.text != "선수 에 대한 검색 결과 입니다."]
        
        player_name_list.append( player_name )
        position_list.append( position )
        
        if page_next == 9:
            driver.find_elements_by_css_selector("a.btn")[2].click()
            time.sleep( 1 )
    
    driver.close()
    
    player_name_list = np.array( sum( player_name_list, [] ) )
    position_list = np.array( sum( position_list, [] ) )
    
    return( player_name_list, position_list )

# =============================================================================
# -- crawling stat, detail stat
# =============================================================================
def get_stat(  driver_dir: str
             , player_name_list: np.array
             , position_list: np.array
             , url: str = "http://www.kfamatch.or.kr/svc/man/selectMainInfo.do"
             ):
    # define some parameter
    # id of stat
    stat_id = [  "appCnt", "goalCnt", "smemCnt", "shotCnt"
               , "subCnt", "onTgCnt", "fullCnt", "miStCnt"
               , "appTime", "passCnt", "yCardCnt", "pSucRte"
               , "rCardCnt", "assistCnt"
               ]
    # column name
    column_name = {  "stat_kor": ["출전경기", "득점", "선발출전", "슈팅", "교체출전", "유효슈팅", "풀타임", "중거리 슈팅", "출전시간", "패스", "경고", "패스성공율", "퇴장", "어시스트"]
                   , "stat": ["appCnt", "goalCnt", "smemCnt", "shotCnt", "subCnt", "onTgCnt", "fullCnt", "miStCnt", "appTime", "passCnt", "yCardCnt", "pSucRte", "rCardCnt", "assistCnt"]
                   , "detail_kor": ["장거리패스", "중거리패스", "단거리패스", "전체 슈팅수", "ON TARGET", "OFF TARGET", "크로스 횟수", "킬패스 횟수", "돌파 횟수", "태클 횟수", "가로채기 횟수", "패스차단 횟수"]
                   , "detail": ["lgPsCnt", "miPsCnt", "stPsCnt", "totShot", "onTarget", "offTarget", "crosCnt", "kPasCnt", "fliOnCnt", "tackleCnt", "interceptCnt", "passcutCnt"]}
    
    # preprocessing
    except_player = [ "박철우" ]
    
    # except player & position(GK)
    position_list = position_list[ ~np.isin( player_name_list, except_player ) ]
    player_name_list = player_name_list[ ~np.isin( player_name_list, except_player ) ]

    player_name_list = player_name_list[ position_list != "GK" ]
    position_list = position_list[ position_list != "GK" ]
    
    ## -- START: Crawling
    # driver
    driver = webdriver.Chrome( driver_dir )
    
    # main page
    driver.get( url )
    
    stat_list, detail_list = [], []
    for player, position in zip(player_name_list, position_list):
        # player page
        driver.find_element_by_css_selector("div.search_box > div.input_box > input").send_keys( player )
        driver.find_element_by_css_selector("button.btn_search").click()
        time.sleep( 1 )
    
        position_check = [value.text for value in driver.find_elements_by_css_selector("p.summary")]
        idx = np.where( np.array(position_check) == position )[0][0]
        
        driver.find_elements_by_css_selector("div.list > ul > li > a")[idx - 1].click()

        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "menuForm"))
            )
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "contents_container"))
            )
        finally:
            pass
        # stat_css = driver.find_elements_by_css_selector("div.p_cont > div.row_top > div.right_a > div.stats > dl > dd")
        detail_css = driver.find_elements_by_css_selector("div.txt > dl > dd")
        detail = [stat.text for stat in detail_css]
        
        stat = list()
        for id_ in stat_id:
            stat.append( driver.find_element(By.ID, id_).text )
    
        driver.back()
        driver.find_element_by_css_selector("div.search_box > div.input_box > input").clear()
        
        stat_list.append( stat )
        detail_list.append( detail )
    
    driver.close()
    ## -- END: Crawling
    
    stat   = pd.DataFrame( stat_list, columns = column_name["stat_kor"] )
    detail = pd.DataFrame( detail_list, columns = column_name["detail_kor"] )
    df = pd.concat(objs = [stat, detail], axis = 1)
    df.insert( loc = 0, column = "이름", value = player_name_list )
    df.insert( loc = 1, column = "포지션", value = position_list )
    
    return( df )
