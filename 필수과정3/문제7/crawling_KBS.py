import urllib.request
from bs4 import BeautifulSoup

def get_kbs_headlines():
    url = 'http://news.kbs.co.kr/news/pc/main/main.html'
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
    
    soup = BeautifulSoup(html, 'html.parser')
    title_tags = soup.find_all('p', class_='title')

    headlines = []
    for tag in title_tags:
        for br in tag.find_all('br'):
            br.replace_with('\n')

        text = tag.get_text(strip=True)
        if not text:
            continue

        if text.startswith('공유'):
            break

        headlines.append(text)

    return headlines

def get_weather():
    url = 'https://weather.com/ko-KR/weather/today/l/4cd22b2121525036e716bd8c994548ec12a793c5c9763af6f9a10c538f7a2a4b'
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')

    soup = BeautifulSoup(html, 'html.parser')
    temp_tag = soup.find('span', {'data-testid': 'TemperatureValue'})

    if temp_tag:
        return temp_tag.get_text(strip=True)
    else:
        return None

if __name__ == '__main__':
    headlines = get_kbs_headlines()
    print('KBS 뉴스 헤드라인:')
    for i, hl in enumerate(headlines, start=1):
        print(f'{i}. {hl}')

    temp = get_weather()
    print()
    if temp:
        print(f'구로구 현재 기온: {temp}')
    else:
        print('구로구 날씨 정보를 가져올 수 없습니다.')
