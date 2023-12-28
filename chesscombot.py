import requests
import shutil
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os

def take_data(user):
    url = f'https://api.chess.com/pub/player/{user}'
    url_stats = f'https://api.chess.com/pub/player/{user}/stats'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    user = requests.get(url, headers=headers)
    user_stats = requests.get(url_stats, headers=headers)
    user_json = user.json()
    user_stats_json = user_stats.json()
    if 'code' in user_json.keys():
        return False
    else:
        if 'avatar' in user_json.keys():
            avatar_url = user_json['avatar']
        else:
            avatar_url = 'https://www.polmedis.pl/wp-content/uploads/2021/02/avatar-200x200-1.jpg'
        if 'name' in user_json.keys():
            name = user_json['name']
        else:
            name = 'Not provided'
        user_name = user_json['username']
        if 'title' in user_json.keys():
            title = user_json['title']
        else:
            title = 'None'
        country_code = user_json['country'][34:36]
        last_online = datetime.fromtimestamp(int(user_json['last_online']))
        last_online_string = last_online.strftime( "%d.%m.%Y" )
        joined = datetime.fromtimestamp(int(user_json['joined']))
        joined_string = joined.strftime( "%d.%m.%Y" )
        if 'chess_rapid' in user_stats_json.keys():
            rapid_rating = user_stats_json['chess_rapid']['last']['rating']
            rapid_wins = user_stats_json['chess_rapid']['record']['win']
            rapid_loses = user_stats_json['chess_rapid']['record']['loss']
            rapid_draws = user_stats_json['chess_rapid']['record']['draw']
            rapid_ratio = f"{rapid_wins}/{rapid_draws}/{rapid_loses}"
            rapid_string = f"{rapid_ratio}({rapid_rating})"
        else:
            rapid_string = "NONE"
        if 'chess_bullet' in user_stats_json.keys():
            bullet_rating = user_stats_json['chess_bullet']['last']['rating']
            bullet_wins = user_stats_json['chess_bullet']['record']['win']
            bullet_loses = user_stats_json['chess_bullet']['record']['loss']
            bullet_draws = user_stats_json['chess_bullet']['record']['draw']
            bullet_ratio = f"{bullet_wins}/{bullet_draws}/{bullet_loses}"
            bullet_string = f"{bullet_ratio}({bullet_rating})"
        else:
            bullet_string = 'NONE'
        if 'chess_blitz' in user_stats_json.keys():
            blitz_rating = user_stats_json['chess_blitz']['last']['rating']
            blitz_wins = user_stats_json['chess_blitz']['record']['win']
            blitz_loses = user_stats_json['chess_blitz']['record']['loss']
            blitz_draws = user_stats_json['chess_blitz']['record']['draw']
            blitz_ratio = f"{blitz_wins}/{blitz_draws}/{blitz_loses}"
            blitz_string = f"{blitz_ratio}({blitz_rating})"
        else:
            blitz_string = 'NONE'
        draw_img(avatar_url, name, user_name, title, country_code, last_online_string, joined_string, rapid_string, bullet_string, blitz_string)


def download_pictue(country):
    res = requests.get(f'https://flaglog.com/codes/standardized-rectangle-120px/{country}.png', stream = True)
    if res.status_code == 200:
        with open('./tmp/country.png','wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded:')
    else:
        print('Image Couldn\'t be retrieved')

def download_pfp(imglink):
    res = requests.get(imglink, stream = True)
    if res.status_code == 200:
        if os.path.isdir('./tmp/') == False:
            os.mkdir('./tmp/')
        with open('./tmp/pfp.jpg','wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded')
    else:
        print('Image Couldn\'t be retrieved')

def draw_img(avatar_url, name, user_name, title, country_code, lastonline, joined, rapid_string, bullet_string, blitz_string):
    download_pfp(avatar_url)
    download_pictue(country_code)
    font = ImageFont.truetype("segoeuib.ttf", size=20)
    font_stats = ImageFont.truetype("segoeuib.ttf", size=18)
    template = Image.open("pusty.png")
    pfp = Image.open("./tmp/pfp.jpg")
    flag = Image.open("./tmp/country.png").resize((22, 15))
    template.paste(pfp, (20,20))
    template.paste(flag, (230,27))
    os.remove('./tmp/pfp.jpg')
    os.remove('./tmp/country.png')
    draw = ImageDraw.Draw(template)
    draw.text((259,21), user_name, font=font, fill='black')
    draw.text((261,20), user_name, font=font, fill='white')
    draw.text((228,46), name, font=font, fill='black')
    draw.text((230,45), name, font=font, fill='white')
    draw.text((283,71), title, font=font, fill='black')
    draw.text((285,70), title, font=font, fill='white')
    draw.text((343,96), lastonline, font=font, fill='black')
    draw.text((345,95), lastonline, font=font, fill='white')
    draw.text((298,121), joined, font=font, fill='black')
    draw.text((300,120), joined, font=font, fill='white')
    draw.text((508,26), rapid_string, font=font_stats, fill='black')
    draw.text((510,25), rapid_string, font=font_stats, fill='white')
    draw.text((508,91), blitz_string, font=font_stats, fill='black')
    draw.text((510,90), blitz_string, font=font_stats, fill='white')
    draw.text((508,156), bullet_string, font=font_stats, fill='black')
    draw.text((510,155), bullet_string, font=font_stats, fill='white')
    template.save(f'{user_name}.png')

