#-*- coding:utf-8 -*-
import discord
import requests
import asyncio
import json
from parse import *
import operator
from threading import Thread
import os


client = discord.Client()
game = discord.Game("명령어 '전적' 입력")

# Key: 닉네임(소문자)
# Value: 출력이름
names = {
    "mde_f0rza": "포르자",
    "mde_no7.son": "클랜장",
    "mde_liketoshy": "샤이",
    "mde_partyman": "파티맨",
    "mde_queen": "퀸",
    "mde_pang-yo": "빵요",
    "mde_fbi_ssd": "스스디",
    "mde_durexx": "콘돔",
    "mde_bibigo": "비비고",
    "mde_mighty": "마이티",
    "mde_seok": "석",
    "mde_rose": "로즈",
    "mde_sia": "시아",
    "mde_jk": "히토미",
    "mde_nozaaaaaa": "노자",
    "mde_haagendazs": "다즈",
    "mde_chatterbox": "채터박스",
    "mde_leoparddddd": "레오파드",
    "mde_worst": "워스트",
    "mde_redpingki": "터틀",
    "n.chovy": "엔초비",
    "mde_legendary":"레전더리",
    "mde_bomberris":"봄베리",
    "mde_zemma_ping9":"제마",
    "mde_sun2880":"썬",
    "mde_uonigogi":"우니고기",
    "mde_booringgame":"부링게임",
    "do_not_touch_it" : "쉴드",
    "master_caveira" : "마카배",
    "mde_dolbyis" : "돌비",
    "mde_honkonteemo" : "홍콩티모"
    "mde_yuda" : "유다"
}

# Thread Worker
def fetch_player(nickname, result):
    base_url = "https://r6tab.com/api/search.php?platform=uplay&search="
    player = json.loads(requests.get(base_url + nickname).text)
    result.append(player)

# Fetch all players using thread
def fetch_players():
    threads = []
    result = []
    nicknames = list(names.keys()) # 전적 검색할 닉네임 배열

    for i in range(0, len(nicknames)):
        thread = Thread(target=fetch_player, args=(nicknames[i], result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(result)
    return result

#디스코드 봇 부분
@client.event
async def on_ready():
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(status=discord.Status.online,activity=game) #봇상태


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    while True:
        # 플레이어 정보 리스트 받아옴
        players = fetch_players()
        # mmr로 정렬
        sorted_players = sorted(players, key=lambda player: -player['results'][0]['p_currentmmr'])
        # 출력 시작
        output = "MDE 클랜 MMR 순위\n\n"
        embed = discord.Embed()
        embed.set_footer(text="시즌 종료시 1위는 클랜장 제외하고 치킨 기프티콘!")
        for index in range(0, len(sorted_players)):
            rank = index + 1 # 순위
            player = sorted_players[index] # 플레이어 정보
            player_nickname = player['results'][0]['p_name'].lower() # 플레이어 닉네임(소문자)
            player_realname = names[player_nickname] # 플레이어 출력이름
            player_mmr = player['results'][0]['p_currentmmr'] # 플레이어 점수
            output += "%d.[%s](%d점)\n" % (rank, player_realname, player_mmr)

        await message.channel.send("```md\n%s\n```" % output,embed=embed)
        await asyncio.sleep(7200)

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
