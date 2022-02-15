import csv
import os

import nsepy
import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import config
import kite_automation_config
import time


def get_historic_data_by_symbol_days(stock_name,days):
    today = datetime.date.today()
    start = today + datetime.timedelta(-days)
    stock_data = nsepy.get_history(symbol = stock_name,start=start,end=today)
    return stock_data

driver = None
def get_driver():
    global driver
    if driver is None:
        driver = webdriver.Chrome(kite_automation_config.PATH)
    return driver


def login_kite_in_browser():
    driver = get_driver()
    driver.maximize_window()

    driver.get(kite_automation_config.KITE_LOGIN_URL)

    print(driver.title)

    time.sleep(kite_automation_config.DELAY_IN_SEC)

    element_user_name = driver.find_element(By.XPATH, kite_automation_config.KITE_USER_ID_XPATH)

    if element_user_name.is_displayed():
        element_user_name.send_keys(kite_automation_config.KITE_LOGIN)

    element_password = driver.find_element(By.XPATH, kite_automation_config.KITE_PASSWORD_XPATH)

    if element_password.is_displayed():
        element_password.send_keys(kite_automation_config.KITE_PASSWORD)

    element_login_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_LOGIN_BUTTON_XPATH)
    if element_login_btn.is_displayed():
        element_login_btn.click()

    time.sleep(kite_automation_config.DELAY_IN_SEC)

    element_pin = driver.find_element(By.XPATH, kite_automation_config.KITE_PIN_XPATH)
    if element_pin.is_displayed():
        element_pin.send_keys(kite_automation_config.KITE_PIN)

    element_continue_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_CONTINUE_BTN_XPATH)
    if element_continue_btn.is_displayed():
        element_continue_btn.click()

def delete_gtt_order():
    driver = get_driver()
    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_order_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_ORDERS_MENU_XPATH)
    if element_order_btn.is_displayed():
        element_order_btn.click()

    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_gtt_menu_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_GTT_MENU_XPATH)
    if element_gtt_menu_btn.is_displayed():
        element_gtt_menu_btn.click()

    #time.sleep(kite_automation_config.DELAY_IN_SEC)
    achain = ActionChains(driver)
    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_gtt_hover_locator = driver.find_element(By.XPATH,kite_automation_config.KITE_GTT_ORDER_HOVER_SELECTOR_XPATH)
    achain.move_to_element(element_gtt_hover_locator).perform()
    time.sleep(kite_automation_config.DELAY_IN_SEC)
    if element_gtt_hover_locator.is_displayed():
        element_gtt_order_hover_del_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_GTT_ORDER_HOVER_DELETE_XPATH)
        if element_gtt_order_hover_del_btn.is_displayed():
            element_gtt_order_hover_del_btn.click()
            time.sleep(kite_automation_config.DELAY_IN_SEC)
            element_gtt_del_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_GTT_ORDER_DELETE_BTN_XPATH)
            if element_gtt_del_btn.is_displayed():
                element_gtt_del_btn.click()
                time.sleep(kite_automation_config.DELAY_IN_SEC)
                element_gtt_del_btn_popup = driver.find_element(By.XPATH,
                                                          kite_automation_config.KITE_GTT_ORDER_DELETE_BTN_FROM_POPUP_XPATH)
                if element_gtt_del_btn_popup.is_displayed():
                    element_gtt_del_btn_popup.click()


def check_exists_by_xpath(xpath):
    driver = get_driver()
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def delete_all_gtt_orders():
    driver = get_driver()
    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_order_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_ORDERS_MENU_XPATH)
    if element_order_btn.is_displayed():
        element_order_btn.click()

    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_gtt_menu_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_GTT_MENU_XPATH)
    if element_gtt_menu_btn.is_displayed():
        element_gtt_menu_btn.click()

    time.sleep(kite_automation_config.DELAY_IN_SEC)
    if check_exists_by_xpath(kite_automation_config.KITE_GTT_DOWNLOAD_CSV_BTN_XPATH):
        element_download_gtt_orders_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_GTT_DOWNLOAD_CSV_BTN_XPATH)
        if element_download_gtt_orders_btn.is_displayed():
            element_download_gtt_orders_btn.click()

        time.sleep(kite_automation_config.DELAY_IN_SEC)
        #Read the gtt-list.csv file from downloads directory
        gtt_file = r'C:\Users\Rohit Pant\Downloads\gtt-list.csv'
        with open(gtt_file) as file:
            reader = csv.reader(file)
            for i in range(1,len(list(reader))):
                delete_gtt_order()

        #Delete the gtt_file
        os.remove(gtt_file)

def place_buy_order(sym, gtt_order_price):
    driver = get_driver()
    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_order_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_ORDERS_MENU_XPATH)
    if element_order_btn.is_displayed():
        element_order_btn.click()

    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_gtt_menu_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_GTT_MENU_XPATH)
    if element_gtt_menu_btn.is_displayed():
        element_gtt_menu_btn.click()

    time.sleep(kite_automation_config.DELAY_IN_SEC)
    if check_exists_by_xpath(kite_automation_config.KITE_NEW_GTT_BTN_XPATH):
        element_new_gtt_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_NEW_GTT_BTN_XPATH)
        if element_new_gtt_btn.is_displayed():
            element_new_gtt_btn.click()
    else :
        element_new_gtt_btn_pop_up = driver.find_element(By.XPATH, kite_automation_config.KITE_NEW_GTT_BTN_FROM_POPUP_XPATH)
        if element_new_gtt_btn_pop_up.is_displayed():
            element_new_gtt_btn_pop_up.click()

    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_search_stock_text = driver.find_element(By.XPATH, kite_automation_config.KITE_SEARCH_STOCK_XPATH)
    if element_search_stock_text.is_displayed():
        element_search_stock_text.send_keys(sym)

    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_search_stock_result_text = driver.find_element(By.XPATH, kite_automation_config.KITE_SEARCH_STOCK_RESULT_XPATH)
    if element_search_stock_result_text.is_displayed():
        element_search_stock_result_text.click()

    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_create_gtt_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_CREATE_GTT_BTN_XPATH)
    if element_create_gtt_btn.is_displayed():
        element_create_gtt_btn.click()

    #I/p for GTT
    trigger_price = format_num_filter(gtt_order_price)
    buy_price = format_num_filter(1.005*gtt_order_price)
    quantity = get_quantity_of_stock_for_buy(buy_price)

    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_gtt_trigger_price = driver.find_element(By.XPATH, kite_automation_config.KITE_GTT_TRIGER_PRICE_XPATH)
    if element_gtt_trigger_price.is_displayed():
        element_gtt_trigger_price.clear()
        element_gtt_trigger_price.send_keys(trigger_price)

    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_gtt_buy_price = driver.find_element(By.XPATH, kite_automation_config.KITE_GTT_ORDER_PRICE_XPATH)
    if element_gtt_buy_price.is_displayed():
        element_gtt_buy_price.clear()
        element_gtt_buy_price.send_keys(buy_price)

    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_gtt_order_price = driver.find_element(By.XPATH, kite_automation_config.KITE_GTT_ORDER_QTY_XPATH)
    if element_gtt_order_price.is_displayed():
        element_gtt_order_price.clear()
        element_gtt_order_price.send_keys(quantity)

    time.sleep(kite_automation_config.DELAY_IN_SEC)
    element_gtt_order_sub_btn = driver.find_element(By.XPATH, kite_automation_config.KITE_GTT_ORDER_SUBMIT_BTN_XPATH)
    if element_gtt_order_sub_btn.is_displayed():
        element_gtt_order_sub_btn.click()


    return None

def get_quantity_of_stock_for_buy(gtt_buy_price):
    money_available_per_trade = config.TOTAL_MONEY_PER_TRADE
    #quantity = round(money_available_per_trade/buy_price_usdt, 5)
    print(money_available_per_trade/gtt_buy_price)
    quantity = int(format_num_filter(money_available_per_trade/gtt_buy_price))
    print(f' Quantity for this trade is {quantity}')
    return quantity

def format_num_filter(number):
    return round(number, 0)

sym_where_we_have_position=set()