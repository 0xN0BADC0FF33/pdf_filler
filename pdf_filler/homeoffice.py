# Credit to @1sgp for the body. now improved to use playwright docker container to remove buggy selenium in docker.

from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from playwright.sync_api import sync_playwright

ondays = [
    "2023/06/19",
    "2023/06/20",
    "2023/06/21",
    "2023/06/22",
    "2023/06/23",
    "2023/06/26",
    "2023/06/27",
    "2023/06/28",
    "2023/06/29",
    "2023/06/30",
    "2023/07/03",
    "2023/07/04",
    "2023/07/05",
    "2023/07/06",
    "2023/07/07",
    "2023/07/10",
    "2023/07/11",
    "2023/07/12",
    "2023/07/13",
    "2023/07/14",
    "2023/07/17",
    "2023/07/18",
    "2023/07/19",
    "2023/07/20",
    "2023/07/21",
    "2023/08/07",
    "2023/08/08",
    "2023/08/09",
    "2023/08/10",
    "2023/08/11",
    "2023/08/14",
    "2023/08/16",
    "2023/08/17",
    "2023/08/18",
    "2023/08/21",
    "2023/08/22",
    "2023/08/23",
    "2023/08/24",
    "2023/08/25",
    "2023/08/28",
    "2023/08/29",
    "2023/08/30",
    "2023/08/31",
    "2023/09/01",
    "2023/09/04",
    "2023/09/05",
    "2023/09/06",
    "2023/09/07",
    "2023/09/08",
    "2023/09/11",
    "2023/09/12",
    "2023/09/13",
    "2023/09/14",
    "2023/09/15",
    "2023/09/18",
    "2023/09/19",
    "2023/09/20",
    "2023/09/21",
    "2023/09/22",
    "2023/09/25",
    "2023/09/26",
    "2023/09/27",
    "2023/09/28",
    "2023/09/29",
    "2023/10/02",
    "2023/10/04",
    "2023/10/05",
    "2023/10/06",
    "2023/10/09",
    "2023/10/10",
    "2023/10/11",
    "2023/10/12",
    "2023/10/13",
    "2023/10/16",
    "2023/10/17",
    "2023/10/18",
    "2023/10/19",
    "2023/10/20",
    "2023/10/23",
    "2023/10/24",
    "2023/10/25",
    "2023/10/26",
    "2023/10/27",
    "2023/10/30",
    "2023/11/02",
    "2023/11/03",
    "2023/11/06",
    "2023/11/07",
    "2023/11/08",
    "2023/11/09",
    "2023/11/10",
    "2023/11/13",
    "2023/11/14",
    "2023/11/15",
    "2023/11/16",
    "2023/11/17",
    "2023/11/20",
    "2023/11/21",
    "2023/11/22",
    "2023/11/23",
    "2023/11/24",
    "2023/11/27",
    "2023/11/28",
    "2023/11/29",
    "2023/11/30",
    "2023/12/01",
    "2023/12/04",
    "2023/12/05",
    "2023/12/06",
    "2023/12/07",
    "2023/12/08",
    "2023/12/11",
    "2023/12/12",
    "2023/12/13",
    "2023/12/14",
    "2023/12/15",
    "2023/12/18",
    "2023/12/19",
    "2023/12/20",
    "2023/12/21",
    "2023/12/22",
    "2024/01/08",
    "2024/01/09",
    "2024/01/10",
    "2024/01/11",
    "2024/01/12",
    "2024/01/15",
    "2024/01/16",
    "2024/01/17",
    "2024/01/18",
    "2024/01/19",
    "2024/01/22",
    "2024/01/23",
    "2024/01/24",
    "2024/01/25",
    "2024/01/26",
    "2024/01/29",
    "2024/01/30",
    "2024/01/31",
    "2024/02/01",
    "2024/02/02",
    "2024/02/05",
    "2024/02/06",
    "2024/02/07",
    "2024/02/08",
    "2024/02/09",
    "2024/02/12",
    "2024/02/13",
    "2024/02/14",
    "2024/02/15",
    "2024/02/16",
    "2024/02/19",
    "2024/02/20",
    "2024/02/21",
    "2024/02/22",
    "2024/02/23",
    "2024/02/26",
    "2024/02/27",
    "2024/02/28",
    "2024/02/29",
    "2024/03/01",
    "2024/03/04",
    "2024/03/05",
    "2024/03/06",
    "2024/03/07",
    "2024/03/11",
    "2024/03/12",
    "2024/03/13",
    "2024/03/14",
    "2024/03/15",
    "2024/03/18",
    "2024/03/19",
    "2024/03/20",
    "2024/03/21",
    "2024/03/22",
    "2024/04/08",
    "2024/04/09",
    "2024/04/10",
    "2024/04/11",
    "2024/04/12",
    "2024/04/15",
    "2024/04/16",
    "2024/04/17",
    "2024/04/18",
    "2024/04/19",
    "2024/04/22",
    "2024/04/23",
    "2024/04/24",
    "2024/04/25",
    "2024/04/26",
    "2024/04/29",
    "2024/04/30",
    "2024/05/02",
    "2024/05/03",
    "2024/05/06",
    "2024/05/07",
    "2024/05/08",
    "2024/05/10",
    "2024/05/13",
    "2024/05/14",
    "2024/05/15",
    "2024/05/16",
    "2024/05/17",
    "2024/05/21",
    "2024/05/22",
    "2024/05/23",
    "2024/05/24",
    "2024/05/27",
    "2024/05/28",
    "2024/05/29",
    "2024/05/31",
    "2024/06/03",
    "2024/06/04",
    "2024/06/05",
    "2024/06/06",
    "2024/06/07",
    "2024/06/10",
    "2024/06/11",
    "2024/06/12",
    "2024/06/13",
    "2024/06/14",
    "2024/06/17",
    "2024/06/18",
    "2024/06/19",
    "2024/06/20",
    "2024/06/21",
    "2024/06/24",
    "2024/06/25",
    "2024/06/26",
    "2024/06/27",
    "2024/06/28",
    "2024/07/01",
    "2024/07/02",
    "2024/07/03",
    "2024/07/04",
    "2024/07/05",
    "2024/07/08",
    "2024/07/09",
    "2024/07/10",
    "2024/07/11",
    "2024/07/12",
    "2024/07/15",
    "2024/07/16",
    "2024/07/17",
    "2024/07/18",
    "2024/07/19",
    "2024/08/05",
    "2024/08/06",
    "2024/08/07",
    "2024/08/08",
    "2024/08/09",
    "2024/08/12",
    "2024/08/13",
    "2024/08/14",
    "2024/08/16",
    "2024/08/19",
    "2024/08/20",
    "2024/08/21",
    "2024/08/22",
    "2024/08/23",
    "2024/08/26",
    "2024/08/27",
    "2024/08/28",
    "2024/08/29",
    "2024/08/30",
    "2024/09/02",
    "2024/09/03",
    "2024/09/04",
    "2024/09/05",
    "2024/09/06",
    "2024/09/09",
    "2024/09/10",
    "2024/09/11",
    "2024/09/12",
    "2024/09/13",
    "2024/09/16",
    "2024/09/17",
    "2024/09/18",
    "2024/09/19",
    "2024/09/20",
    "2024/09/21"
]


class link:
    login = "https://lernplattform.gfn.de/login/index.php"
    home = "https://lernplattform.gfn.de/"
    zestarted = "https://lernplattform.gfn.de/?starten=1"
    zestopped = "https://lernplattform.gfn.de/?stoppen=1"
    anwesi = "https://lernplattform.gfn.de/local/anmeldung/anwesenheit.php"


def login_user(page, User, Pass):
    page.goto(link.login)
    page.fill('#username', User)
    page.fill('#password', Pass)
    page.click('.btn-primary')
    page.wait_for_load_state('networkidle')
    return "Ungültige Anmeldedaten" not in page.content() and "Invalid login" not in page.content()

def Homecalculator(page):
    page.goto(link.anwesi)
    page.wait_for_load_state('networkidle')
    
    content = page.content()
    soup = bs(content, 'html.parser')
    fullname = soup.find("h1").text
    done = []
    hometage = 0
    orttage = 0
    gesamttage = len(ondays)
    emptystr = "--:--"
    Tagebuecher = {}
    tbody = soup.find('tbody')
    eintraege = tbody.find_all("tr") if tbody else []
    
    if eintraege and (
        eintraege[0].find_all("td")[3].text == emptystr
        and eintraege[0].find_all("td")[5].text == emptystr
    ):
        eintraege.pop(0)
    
    for eintrag in eintraege:
        tds = eintrag.find_all("td")
        date = dt.strftime(dt.strptime(tds[0].text, "%d.%m.%Y"), "%Y/%m/%d")
        if date not in ondays:
            continue
        done.append(date)
        loc = "home" if tds[1].text.strip() == "🏠" else "standort"
        start = tds[2].text
        end = tds[3].text
        start = tds[4].text if tds[4].text != emptystr else start
        end = tds[5].text if tds[5].text != emptystr else end
        if loc == "home":
            hometage += 1
        else:
            orttage += 1
        Tagebuch = {"Ort": loc, "Start": start, "Ende": end}
        Tagebuecher[date] = Tagebuch
    donetage = hometage + orttage
    todotage = len(ondays) - donetage
    homepercent = (hometage / donetage) * 100
    ortpercent = (orttage / donetage) * 100
    totalhomepercent = (hometage / gesamttage) * 100
    totalortpercent = (orttage / gesamttage) * 100
    homeneeded = 137 - hometage
    officeneeded = 143 - orttage
    print(fullname)
    return fullname, {"Tagegesamt": f"{gesamttage} Tage"} | {
        "Tagevorrueber": f"{donetage} Tage"
    } | {"Tageverbleibend": f"{todotage} Tage"} | {
        "HomeofficeNeed": f"{homeneeded} Tage"
    } | {
        "StandortNeed": f"{officeneeded} Tage"
    } | {
        "Standort": f"{orttage} Tage"
    } | {
        "Homeoffice": f"{hometage} Tage"
    } | {
        "HomeofficeProDone": f"{homepercent:.0f}%"
    } | {
        "HomeofficeProTotal": f"{totalhomepercent:.0f}%"
    } | {
        "StandortProDone": f"{ortpercent:.0f}%"
    } | {
        "StandortProTotal": f"{totalortpercent:.0f}%"
    }


def getUsername(page):
    page.goto(link.home)
    page.wait_for_load_state('networkidle')
    soup = bs(page.content(), 'html.parser')
    return soup.find("span", {"id": "actionmenuaction-1"}).text

def main(benutzer, passwort):
    with sync_playwright() as p:
        browser = p.chromium.connect("ws://localhost:9222")
        page = browser.new_page()
        if login_user(page, benutzer, passwort):
            fullname, home = Homecalculator(page)
            browser.close()
            return fullname, home
        else:
            browser.close()
            return None, None

# If running the script directly
if __name__ == "__main__":
    # You'll need to provide username and password here
    fullname, home = main("your_gfn_username", "your_gfn_password")
    if fullname and home:
        print(f"Full Name: {fullname}")
        print("Home Office Data:", home)
    else:
        print("Login failed or data retrieval error.")