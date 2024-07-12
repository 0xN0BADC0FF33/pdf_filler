# Klassenbuchscraper AiO Package
# version 0.8.0 ALPHA for 'pdf_filler' by mxwmnn
# Updated: 2024/03/21

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def loginUser(page, User, Pass):
    try:
        page.goto("https://lernplattform.gfn.de/login/index.php")
        page.fill('#username', User)
        page.fill('#password', Pass)
        page.click('.btn-primary')
        page.wait_for_load_state('networkidle')
        
        if "Ungültige Anmeldedaten. Versuchen Sie es noch einmal!" in page.content():
            raise Exception("Invalid credentials")
        
    except Exception as e:
        raise Exception(f"Login failed: {e}")

    try:
        page.goto("https://lernplattform.gfn.de/user/profile.php")
        page.wait_for_load_state('networkidle')
    except Exception as e:
        raise Exception(f"Page could not load with error: {e}")
    
    soup = BeautifulSoup(page.content(), 'html.parser')
    fullname_element = soup.select_one('div.page-header-headings h1.h2')
    if fullname_element:
        fullname = fullname_element.text.strip()
    else:
        raise Exception("Could not find user's full name")
    
    return fullname

def Kursmenu(page):
    Kurse = {}    
    page.goto('https://lernplattform.gfn.de/my/courses.php')
    page.wait_for_load_state('networkidle')
    
    # Check if the user is logged in
    if "Sie sind als Gast angemeldet" in page.content():
        raise Exception("User is not logged in properly")
    
    # Check if "Alle" is already selected
    alle_button = page.query_selector('button.dropdown-toggle:has-text("Alle")')
    if not alle_button:
        # If "Alle" is not selected, try to select it
        try:
            page.click('button[data-toggle="dropdown"][aria-haspopup="true"]')
            page.wait_for_selector('.dropdown-menu[data-show-active-item]', state='visible')
            page.click('.dropdown-menu[data-show-active-item] a[data-limit="0"]')
            page.wait_for_load_state('networkidle')
        except Exception as e:
            print(f"Warning: Error when trying to show all courses: {e}")
    
    # Ensure all courses are loaded
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_load_state('networkidle')
    
    soup = BeautifulSoup(page.content(), 'html.parser')
    
    # Look for the course view container
    course_view = soup.find('div', {'data-region': 'courses-view'})
    
    if not course_view:
        print("Warning: Course view container not found. The page structure might have changed.")
        return Kurse
    
    # Find all course cards
    course_cards = soup.find_all('div', class_='card dashboard-card')
    
    for card in course_cards:
        # Find the full course name
        full_course_name = card.find('span', class_='multiline')
        if full_course_name:
            kursname = full_course_name['title'].strip()
            
            # Find the course link
            course_link = card.find('a', class_='coursename')
            if course_link:
                href = course_link['href']
                
                # Check if the course name starts with "LF"
                if kursname.startswith("LF"):
                    Kurse[kursname] = href
    
    if not Kurse:
        print("Warning: No courses found. The user might not be enrolled in any courses.")
    
    return Kurse


def klassenbucher(page, Kurse):
    classbooks = {}
    for key, url in Kurse.items():
        page.goto(url)
        page.wait_for_load_state('networkidle')
        
        # Find the Klassenbuch link
        klassenbuch_link = None
        grid_sections = page.query_selector_all('div.grid-section.card')
        for section in grid_sections:
            title = section.query_selector('.card-header')
            if title and 'Klassenbuch' in title.inner_text():
                klassenbuch_link = section.query_selector('a.grid-section-inner')
                break
        
        if not klassenbuch_link:
            print(f"Warning: Klassenbuch link not found for course {key}")
            continue
        
        klassenbuch_url = klassenbuch_link.get_attribute('href')
        page.goto(klassenbuch_url)
        page.wait_for_load_state('networkidle')
        

        anzeigen_link = page.query_selector('a.courseindex-link[href*="/mod/attendance/view.php"]')
        if not anzeigen_link:
            print(f"Warning: Anzeigen link not found for course {key}")
            continue
        
        anzeigen_url = anzeigen_link.get_attribute('href')
        anzeigen_url += '&view=5'
        
        # Navigate to the Anzeigen page
        page.goto(anzeigen_url)
        page.wait_for_load_state('networkidle')
        
        # Extract the data from the table
        table = page.query_selector('.boxaligncenter')
        if not table:
            print(f"Warning: Data table not found for course {key}")
            continue
        
        daten = table.query_selector_all('.datecol')
        desc = table.query_selector_all('.desccol')
        
        classbook = {}
        for datum, description in zip(daten, desc):
            Datum = datum.inner_text()
            Desc = description.inner_text()
            cleanedDesc = Desc.replace("\n", "; ")
            classbook[Datum] = cleanedDesc
        
        classbooks[key] = classbook
    
    return classbooks

def main(benutzer, passwort):
    with sync_playwright() as p:
        browser = p.chromium.connect("ws://localhost:9222")
        page = browser.new_page()
        
        fullname = loginUser(page, benutzer, passwort)
        Kurse = Kursmenu(page)
        output = klassenbucher(page, Kurse)
        browser.close()
        return output

if __name__ == '__main__':
    # Assuming credentials are passed as environment variables or command-line arguments
    import os
    benutzer = os.environ.get('USERNAME')
    passwort = os.environ.get('PASSWORD')
    if not benutzer or not passwort:
        raise ValueError("USERNAME and PASSWORD must be set as environment variables")
    result = main(benutzer, passwort)
    print(result)  # Or handle the result as needed2