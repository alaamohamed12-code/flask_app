from flask import Flask, request, render_template
import requests
from pytube import YouTube
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
app = Flask(__name__)

def fetch_youtube_video_info(video_url):
    try:
        url = video_url
        if 'youtube.com' in url:
            vid = url.split("?v=")[-1]
        elif 'youtu.be' in url:
            parsed_url = urlparse(url)
            vid = parsed_url.path[1:]
        print(vid)
        cookies = {
            '_ga': 'GA1.1.55845380.1719854884',
            '_ga_PSRPB96YVC': 'GS1.1.1719854884.1.1.1719854910.0.0.0',
        }

        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'dnt': '1',
            'origin': 'https://www.y2mate.com',
            'priority': 'u=1, i',
            'referer': f'https://www.y2mate.com/youtube/{vid}',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'k_query': url,
            'k_page': 'home',
            'hl': 'en',
            'q_auto': '0',
        }

        response = requests.post('https://www.y2mate.com/mates/en948/analyzeV2/ajax', cookies=cookies, headers=headers, data=data)
        video_info = response.json()
        vid = video_info['vid']

        
        
        if not video_info.get('links') or not video_info['links'].get('mp4'):
            return None

        full_data = {}
        full_data['platform'] = 'youtube'
        full_data['title'] = video_info['title']
        yt = YouTube(video_url)
        thumbnail_url = yt.thumbnail_url
        full_data['thumbnail'] = thumbnail_url

        for key, quality in video_info['links']['mp4'].items():
            print(key)
            print(quality)
            try:
                quality_cookies = {
                    '_ga': 'GA1.1.55845380.1719854884',
                    '_ga_PSRPB96YVC': 'GS1.1.1719854884.1.1.1719854910.0.0.0',
                }

                quality_headers = {
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'dnt': '1',
                    'origin': 'https://www.y2mate.com',
                    'priority': 'u=1, i',
                    'referer': f'https://www.y2mate.com/youtube/{vid}',
                    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
                    'x-requested-with': 'XMLHttpRequest',
                }

                quality_data = {
                    'vid': vid,
                    'k': quality['k'],
                }

                quality_response = requests.post('https://www.y2mate.com/mates/convertV2/index', cookies=quality_cookies, headers=quality_headers, data=quality_data)
                download_info = quality_response.json()
                print(quality_response.status_code())
                full_data[quality['q']] = download_info['dlink']
            except Exception as e:
                print(e)
                continue
        return full_data

    except Exception:
        return None


def fetch_video_info(video_url):
    try:
        cookies = {
            'pll_language': 'en',
            '_ga': 'GA1.1.136381888.1718849976',
            'xcnmo-offsetgxc': '1W8PoUXWEf',
            'cf_clearance': 'zU2ChO7fc2yubYtZacxWADnzWzhV_e7exgKVlQCV2Do-1718932029-1.0.1.1-BwjCGz.YMOSeSJuggGZ8HtKteAgoM8OFGQyu.vgVSTiQy8OSt1Tr5rUB98mWruORqhmoOMUIyjSm7YK8kun9Xw',
            '_ga_9JVBM9CZ41': 'GS1.1.1718929298.5.1.1718932415.5.0.0',
        }

        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'origin': 'https://viddownloader.online',
            'priority': 'u=1, i',
            'referer': 'https://viddownloader.online/',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        }

        data = {
            'url': video_url,
            'token': 'd7d25ebb7ee7720b96aa0a2af29b20f4781221e22588031c80665b463d0e57d3',
            'hash': 'aHR0cHM6Ly93d3cudGlrdG9rLmNvbV93ZWJhcHA9MSZzZW5kZXJfZGV2aWNlPXBj1093YWlvLWRs',
        }

        response = requests.post('https://viddownloader.online/wp-json/aio-dl/video-data/', cookies=cookies, headers=headers, data=data)
        json_response = response.json()
        if 'url' in json_response:
            video_info = {
                'platform': 'other',
                'title': json_response.get('title', 'No Title'),
                'thumbnail': json_response.get('thumbnail', ''),
                'keyword': json_response.get('url', video_url),
                'medias': json_response.get('medias', [])
            }
            return video_info

    except Exception as e:
        error_message = "An error occurred while fetching the video info."
        return render_template('index2.html', error_message=error_message)
    return None

def tiktok_video(video_url):
    try:

        cookies = {
            '_ga': 'GA1.1.1051799445.1718932873',
            '__gads': 'ID=e0663ca5c42588f6:T=1718932874:RT=1720133318:S=ALNI_Ma40gtQWWtI-UQOzUHqMj3zVi3tDA',
            '__eoi': 'ID=eac9e4dc05b084cc:T=1718932874:RT=1720133318:S=AA-AfjYoDhXAoxrlxZ7-1Uvk1NrA',
            'FCNEC': '%5B%5B%22AKsRol8NCARjXywzomkz71YSdl1gXol5KNYq4rEBiTT81UwlTSKnJHQ0ZBVYt4-hU-X8Jzm7xDGMEXCx0DnJ5fZ61m1CnRjChNu8sTtXqHI1Q-gsOLlpanCxg0WgvR9ePpXkB0s3ioFYcqPOWMb0Qexv9KriQjqXvw%3D%3D%22%5D%5D',
            '_ga_ZSF3D6YSLC': 'GS1.1.1719991267.2.1.1719991323.0.0.0',
        }

        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'dnt': '1',
            'hx-current-url': 'https://ssstik.io/en-1',
            'hx-request': 'true',
            'hx-target': 'target',
            'hx-trigger': '_gcaptcha_pt',
            'origin': 'https://ssstik.io',
            'priority': 'u=1, i',
            'referer': 'https://ssstik.io/en-1',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        }

        params = {
            'url': 'dl',
        }

        data = {
            'id': video_url,
            'locale': 'en',
            'tt': 'ZzVTcWNi',
        }

        response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)

        if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                a_tags = soup.find_all('a')
                hrefs = [a.get('href') for a in a_tags if a.get('href')]
                if len(hrefs) > 1:
                    hrefs = hrefs[:1] + hrefs[2:]

                img_tag = soup.find('img', class_='result_author')
                if img_tag:
                    img_src = img_tag.get('src')
                    img_alt = img_tag.get('alt')
                else:
                    img_src = None
                    img_alt = None

                # Find the div with the specified class
                div_element = soup.find('div', class_='pure-u-18-24 pd-lr')

                # Extract all h2 and p elements from the div
                if div_element:
                    h2_elements = div_element.find_all('h2')
                    h2_texts = [h2.get_text(strip=True) for h2 in h2_elements]
                    
                    p_elements = div_element.find_all('p')
                    p_texts = [p.get_text(strip=True) for p in p_elements]
                else:
                    h2_texts = []
                    p_texts = []

                # Save all outputs in a single list
                video_info = {}
                video_info['mp4'] = hrefs[0]
                video_info['mp3'] = hrefs[1]
                video_info['thumbnail'] = img_src
                video_info['auther'] = h2_texts
                video_info['title'] = p_texts              
                video_info['platform'] = 'tiktok'

                return video_info

    except Exception as e:
        error_message = "An error occurred while fetching the TikTok video info."
        return render_template('index2.html', error_message=error_message)

    return None

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/fetch', methods=['POST'])
def fetch():
    video_url = request.form['video_url']
    video_info = None

    if "tiktok.com" in video_url:
        video_info = tiktok_video(video_url)
    elif 'youtube.com' in video_url or 'youtu.be' in video_url:
        video_info = fetch_youtube_video_info(video_url)
    else:
        video_info = fetch_video_info(video_url)

    return render_template('index2.html', video_info=video_info)

if __name__ == '__main__':
    app.run(debug=True)
