import time
from bs4 import BeautifulSoup
from selenium import webdriver
from Station import Station


def updateCssSelector(cssSelector):
    i = 40
    number = ""
    while i < len(cssSelector):
        number += cssSelector[i]
        i += 1
        if cssSelector[i] == ')':
            i = len(cssSelector)

    oldNumber = number
    number = int(number)
    number += 1
    number = str(number)

    return cssSelector.replace(oldNumber, number, 1)

def getInfos(soup):
    station = Station()
    name = soup.find_all("h3", id="nome")[0].get_text()
    station.setName(name)

    address = ""
    divAddress = soup.find("div", id="div_Endereco")
    addressInfo = divAddress.find_all("p")
    for i in range(0, len(addressInfo), 1):
        address += addressInfo[i].get_text() + " "
    station.setAddress(address)

    characteristics = []
    divCharacteristics = soup.find("div", id="div_caracateristicas")
    nextDivs = divCharacteristics.find_next_siblings()
    for i in range(0, len(nextDivs), 1):
        if nextDivs[i].get("id") != "div_acessibilidade" and nextDivs[i].get("id") != "div_conveniencias":
            characteristics.append(nextDivs[i].find("p").get_text())
    station.setCharacteristics(characteristics)

    return station


error = True
while error:
    try:
        driver = webdriver.Firefox(executable_path="C:\\Users\\leona\\Documents\\GeckoDriver\\geckodriver.exe")
        driver.get("https://www.cptm.sp.gov.br/sua-viagem/Pages/Linhas.aspx")
        driver.maximize_window()
        for i in range(0, 2, 1):
            driver.find_element_by_class_name("leaflet-control-zoom-out").click()
            time.sleep(5)

        script = "window.scroll(400,400);"
        driver.execute_script(script)

        stations = []
        cssSelector = "svg.leaflet-zoom-animated > g:nth-child(1) > path:nth-child(1)"
        for i in range(1, 95, 1):
            driver.find_element_by_css_selector(cssSelector).click()
            time.sleep(1)

            script = "var btn = document.getElementsByClassName(\"btn btn-default\"); btn[0].scrollIntoView();"
            driver.execute_script(script)
            time.sleep(0.5)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            station = getInfos(soup)
            stations.append(station)

            driver.find_element_by_css_selector("#myModal > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > button:nth-child(1)").click()
            time.sleep(1)

            cssSelector = updateCssSelector(cssSelector)

        error = False
    except Exception as e:
        print(e)
        error = True

for s in stations:
    print(s.getName())
    print(s.getAddress())
    print(s.getCharacteristics())
    print("============================================================")
