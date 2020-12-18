import pytest
from selene.support.shared import browser
from selene import by, be, have
from random import choices
from string import ascii_letters


@pytest.fixture(scope='session')
def setup():
    browser.config.browser_name = 'firefox'
    yield
    browser.quit()


def test_add_contact(setup):
    # open homepage
    browser.open("http://192.168.64.2/addressbook/index.php")
    # login
    browser.element(by.name('user')).type('admin')
    browser.element(by.name('pass')).type('secret')
    browser.element('input[value=\'Login\']').click()
    # add new contact
    browser.element(by.link_text('add new')).click()
    lastname = ''.join(choices(ascii_letters, k=10))
    browser.element(by.name('lastname')).type(lastname)
    browser.element(by.name('bday')).element(by.xpath('//option[. = \'6\']')).click()
    browser.element(by.name('bmonth')).element(by.xpath('//option[. = \'July\']')).click()
    browser.element(by.name('byear')).type('1990')
    browser.element(by.name('submit')).click()
    # check contact is present
    browser.element(by.link_text('home')).click()
    browser.all(by.name('entry')).filtered_by_their('td:nth-child(2)', have.exact_text(lastname)).should(have.size(1))
    # check contact birthday
    browser.all(by.name('entry')).element_by(have.exact_text(lastname)).element('img[alt=\'Details\']').click()
    browser.element('#content').should(have.text('Birthday 6. July 1990'))
    # delete contact
    browser.element(by.link_text('home')).click()
    browser.all(by.name('entry')).element_by(have.exact_text(lastname)).element(by.name('selected[]')).click()
    browser.element('input[value=\'Delete\']').click()
    browser.switch_to.alert.accept()
    # check contact deleted
    browser.element(by.link_text('home')).click()
    browser.all(by.name('entry')).filtered_by_their('td:nth-child(2)', have.exact_text(lastname)).should(have.size(0))
    # logout
    browser.element(by.link_text('Logout')).click()
    browser.element(by.name('user')).should(be.present)

