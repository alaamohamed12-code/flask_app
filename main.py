from flask import Flask, request, render_template, jsonify
import requests
from pytube import YouTube
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

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
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return None

        video_info = response.json()
        vid = video_info['vid']
        if not video_info.get('links') or not video_info['links'].get('mp4'):
            return None

        full_data = {
            'platform': 'youtube',
            'title': video_info['title']
        }
        yt = YouTube(video_url)
        full_data['thumbnail'] = yt.thumbnail_url

        for key, quality in video_info['links']['mp4'].items():
            try:
                quality_headers = headers.copy()
                quality_data = {
                    'vid': vid,
                    'k': quality['k'],
                }
                quality_response = requests.post('https://www.y2mate.com/mates/convertV2/index', headers=quality_headers, data=quality_data)
                if quality_response.status_code != 200:
                    print(f"Error: Received status code {quality_response.status_code} for quality {quality['q']}")
                    continue
                download_info = quality_response.json()
                full_data[quality['q']] = download_info['dlink']
            except Exception as e:
                print(f"Error fetching quality {quality['q']}: {e}")
                continue
        return full_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def fetch_video_info(video_url):
    try:
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'origin': 'https://viddownloader.online',
            'referer': 'https://viddownloader.online/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        }

        data = {
            'url': video_url,
            'token': 'd7d25ebb7ee7720b96aa0a2af29b20f4781221e22588031c80665b463d0e57d3',
            'hash': 'aHR0cHM6Ly93d3cudGlrdG9rLmNvbV93ZWJhcHA9MSZzZW5kZXJfZGV2aWNlPXBj1093YWlvLWRs',
        }

        response = requests.post('https://viddownloader.online/wp-json/aio-dl/video-data/', headers=headers, data=data)
        json_response = response.json()
        print(f"Video Info: {json_response}")
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
        error_message = f"An error occurred while fetching the video info: {e}"
        print(error_message)
        return render_template('index2.html', error_message=error_message)
    return None

def tiktok_video(video_url):
    try:
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
            'referer': 'https://ssstik.io/en-1',
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

        response = requests.post('https://ssstik.io/abc', params=params, headers=headers, data=data)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.find_all('a')
            hrefs = [a.get('href') for a in a_tags if a.get('href')]
            if len(hrefs) > 1:
                hrefs = hrefs[:1] + hrefs[2:]

            img_tag = soup.find('img', class_='result_author')
            img_src = img_tag.get('src') if img_tag else None

            div_element = soup.find('div', class_='pure-u-18-24 pd-lr')
            h2_texts = [h2.get_text(strip=True) for h2 in div_element.find_all('h2')] if div_element else []
            p_texts = [p.get_text(strip=True) for p in div_element.find_all('p')] if div_element else []

            video_info = {
                'mp4': hrefs[0],
                'mp3': hrefs[1],
                'thumbnail': img_src,
                'auther': h2_texts,
                'title': p_texts,
                'platform': 'tiktok'
            }

            return video_info

    except Exception as e:
        error_message = f"An error occurred while fetching the TikTok video info: {e}"
        print(error_message)
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
