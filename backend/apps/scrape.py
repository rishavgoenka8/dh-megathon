from linkedin_scraper import actions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import re
import os
from time import sleep
from random import randint

def gradual_scroll(driver, scroll_by_pixels=400, wait_time=1):
    """
    Scroll the webpage gradually.

    :param driver: Selenium WebDriver instance.
    :param scroll_by_pixels: Amount to scroll by in pixels. Default is 400 pixels.
    :param wait_time: Time to wait after each scroll. Default is 0.5 seconds.
    """
    current_scroll_position, new_scroll_position = 0, 0
    ctr = 0
    while True:
        ctr+=1
        current_scroll_position = new_scroll_position
        driver.execute_script(f"window.scrollBy(0, {scroll_by_pixels});")
        sleep(0.5*randint(wait_time, wait_time*2))
        new_scroll_position = driver.execute_script("return window.scrollY;")

        if new_scroll_position == current_scroll_position or ctr >30:
            break

def scrapePosts(post_url, driver):    
    driver.get(post_url)
    try:
        gradual_scroll(driver)
        # WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "end-of-page")))
    except Exception as e:
        pass 
    soup = BeautifulSoup(driver.page_source, 'lxml')
    posts = soup.find_all('li', class_='profile-creator-shared-feed-update__container')
    print(len(posts))
    post_dict ={'posts':[]}
    for item in posts:
        try:
            el=item.find('span', class_='break-words').text.strip()
            print(el)
            post_dict['posts'].append(el)
        except Exception as e:
            print(e)
    with open('posts-1.json', 'w') as f:
        json.dump(post_dict, f)
    return post_dict

def getSoup(url, driver, flag=0, ctr=0):
    driver.get(url)
    try:
        if flag == 0:
            WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, "display-flex ph5 pv3")))
        else:
            WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, "pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column")))
    except Exception as e:
        print(e)
        pass
    soup = BeautifulSoup(driver.page_source, 'lxml')
    with open(f'soup-{ctr}.html', 'w') as f:
        f.write(soup.prettify())
    return soup, ctr+1


def remove_consecutive_duplicates(text):
    lines = text.split("\n")
    deduped_lines = [re.search(r'(.+)(\1)+', line).group(1).strip() if re.search(r'(.+)(\1)+', line) else line.strip() for line in lines]
    return "\n".join(deduped_lines)


def clean_data(data):
    cleaned_text = remove_consecutive_duplicates(data[0])
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    cleaned_text = re.sub(r'\n+', '\n', cleaned_text).strip()
    return cleaned_text


def postProcess(array, key):
    if key == "skills":
        raw_data = " ".join(array).split("Endorse")
        formatted_skills = []
        unique_skills = set()
        for item in raw_data:
            item = item.strip()
            if item:
                skill = re.sub(r'\n+', '\n', item).split('\n')[0]
                skill = skill.replace("Endorse", "").strip()  # Remove "Endorse" from skill
                endorsements = re.findall(r'\d+ endorsements', item)
                if skill not in unique_skills:
                    sk = remove_consecutive_duplicates(skill)
                    formatted_skills.append(sk.strip())
                    unique_skills.add(sk)
        return formatted_skills
    elif key == "projects":
        raw_data = " ".join(array).split("Show project")
        formatted_projects = []
        for item in raw_data:
            item = item.strip()
            if item:
                lines = item.split('\n')
                project_name = lines[0].strip()
                duration_match = re.search(r'(\w+ \d+ - \w+ \d+)', item)
                project_duration = duration_match.group(0) if duration_match else "N/A"
                org_match = re.search(r'Associated with (.+)', item)
                org = org_match.group(1).strip() if org_match else "N/A"
                formatted_projects.append({
                    "Project Name": project_name,
                    "Duration": project_duration,
                    "Associated Organization": org
                })
        return formatted_projects
    else:
        return clean_data(array)
    return array


def scrape(linkedin_url):
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	driver = webdriver.Chrome(options=options)
	
	email = os.environ.get('LINKEDIN_EMAIL')
	password = os.environ.get('LINKEDIN_PASSWORD')
	actions.login(driver, email, password, timeout=60)
	
	ctr = 0
	soup, ctr = getSoup(linkedin_url, driver, ctr=ctr)
	
	with open('soup.html', 'w') as f:
			f.write(soup.prettify())
	
	div = soup.find('div', {'class': 'ph5 pb5'})
	name = div.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).text.strip()
	headline = div.find('div', {'class': 'text-body-medium break-words'}).text.strip()
	profile_details = {'name': name, 'headline': headline}
	
	try:
			about_section = soup.find('div', {'class': 'display-flex ph5 pv3'})
			span_element = about_section.find('span')
			about_info = ' '.join(span_element.get_text(separator=' ').strip().split()) if span_element else ''
			profile_details['about'] = about_info
	except Exception as e:
			print(e, "About Not Found.")
	
	subpages = ['skills', 'education', 'experience', 'projects']
	for subsection in subpages:
			profile_details[subsection] = []
			soup, ctr = getSoup(linkedin_url + "details/" + subsection, driver, flag=1, ctr=ctr)
			items = soup.find_all('li', {'class': 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
			for item in items:
					outp = item.text.strip()
					profile_details[subsection].append(postProcess([outp], subsection))
	post_url = f"{linkedin_url}recent-activity/all/"
	print(post_url)
	posts_details=scrapePosts(post_url, driver)
	driver.quit()
	return profile_details, posts_details