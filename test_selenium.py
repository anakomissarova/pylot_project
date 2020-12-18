import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from random import choices
from string import ascii_letters


@pytest.fixture(scope='session')
def driver():
    wd = webdriver.Firefox()
    wd.implicitly_wait(5)
    yield wd
    wd.quit()


def test_add_contact(driver):
    # open homepage
    driver.get("http://192.168.64.2/addressbook/index.php")
    # login
    driver.find_element(By.NAME, "user").send_keys("admin")
    driver.find_element(By.NAME, "pass").send_keys("secret")
    driver.find_element(By.XPATH, "//input[@value=\'Login\']").click()
    # add new contact
    driver.find_element(By.LINK_TEXT, "add new").click()
    lastname = ''.join(choices(ascii_letters, k=10))
    driver.find_element(By.NAME, "lastname").send_keys(lastname)
    driver.find_element(By.NAME, "bday").find_element(By.XPATH, "//option[. = '6']").click()
    driver.find_element(By.NAME, "bmonth").find_element(By.XPATH, "//option[. = 'July']").click()
    driver.find_element(By.NAME, "byear").send_keys("1990")
    driver.find_element(By.NAME, "submit").click()
    # check contact is present
    driver.find_element(By.LINK_TEXT, "home").click()
    contacts = driver.find_elements(By.NAME, "entry")
    new_contact_num = 0
    for contact in contacts:
        if contact.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text == lastname:
            new_contact_num += 1
    assert new_contact_num == 1
    # check contact birthday
    new_contact = contacts[0]
    new_contact_id = contacts[0].find_element(By.NAME, "selected[]").get_attribute('id')
    for contact in contacts:
        if lastname in contact.text:
            new_contact = contact
            new_contact_id = contact.find_element(By.NAME, "selected[]").get_attribute('id')
            break
    new_contact.find_element(By.CSS_SELECTOR, 'img[alt=\'Details\']').click()
    assert 'Birthday 6. July 1990' in driver.find_element(By.CSS_SELECTOR, '#content').text
    # delete contact
    driver.find_element(By.LINK_TEXT, "home").click()
    driver.find_element(By.NAME, 'entry')
    driver.find_element(By.ID, new_contact_id).click()
    driver.find_element(By.CSS_SELECTOR, "input[value='Delete']").click()
    driver.switch_to.alert.accept()
    # check contact deleted
    driver.find_element(By.LINK_TEXT, "home").click()
    contacts = driver.find_elements(By.NAME, "entry")
    new_contact_num = 0
    for contact in contacts:
        if contact.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text == lastname:
            new_contact_num += 1
    assert new_contact_num == 0
    # logout
    driver.find_element(By.LINK_TEXT, "Logout").click()
    driver.find_element(By.NAME, 'user')