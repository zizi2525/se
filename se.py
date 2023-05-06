import requests 
import json
from fastapi import FastAPI, Response
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import pytz
from tinydb import TinyDB, Query
import uvicorn
app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db = TinyDB('db.json')
channel = Query()
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/today")
def get_today():
    #swap
    #r= requests.get("https://6kora.koooora-online.com/p/matches-today.html")
    #soup = BeautifulSoup(r.content, 'html.parser')
    #matches = soup.find_all('div', {"id": "today"})
    #matches = matches[0].find_all('div', {"class": "match-container"})
    r= requests.get("https://kooora.alkoora.live/")
    soup = BeautifulSoup(r.content, 'html.parser')
    matches = soup.find_all('div', {"id": "today"})
    matches = matches[0].find_all('div', {"class": "match-event"})
    
    matches_list = []

    for match in matches:
        match_dict = {}
        match_dict['match_url'] = match.find('a')['href'].split('/')[-1]
        match_dict['match_url0'] = match.find('a')['href']
        match_dict['team1'] = match.find('div', {"class": "right-team"}).find('div', {"class": "team-name"}).text
        match_dict['team1logo'] = match.find('div', {"class": "right-team"}).find('div', {"class": "team-logo"}).find('img')['data-img']
        match_dict['team2'] = match.find('div', {"class": "left-team"}).find('div', {"class": "team-name"}).text
        match_dict['team2logo'] = match.find('div', {"class": "left-team"}).find('div', {"class": "team-logo"}).find('img')['data-img']
        match_ended = match.find('div', {"class": "match-center"}).find('div', {"class": "date"})['data-gameends']
        match_started = match.find('div', {"class": "match-center"}).find('div', {"class": "date"})['data-start']
        match_dict['match_ended'] = match_ended
        match_dict['match_started'] = match_started
        db.search(channel.id == match_dict['match_url'])
        if len(db.search(channel.id == match_dict['match_url'])) == 0:

          db.insert({"id":match_dict['match_url'],"url": match_dict['match_url0']})
        



        
        start_time = datetime.fromisoformat(match_started)
        end_time = datetime.fromisoformat(match_ended)

        tz = pytz.timezone('gmt')

        start_time_local = start_time.astimezone(tz)
        end_time_local = end_time.astimezone(tz)

        start_time_str_local = start_time_local.strftime('%H:%M')
        end_time_str_local = end_time_local.strftime('%H:%M')

        dif = timedelta(minutes=15)

        match_status =""
        status =""
        time_now = datetime.now(tz)
  
        print(start_time_local  > time_now +dif)
        print(time_now)

       
        if start_time_local > time_now:
            match_status = "لم تبدأ بعد"
            status = False
        elif end_time_local < time_now:
            match_status = "انتهت"
            match_dict['score'] = match.find('div', {"class": "match-center"}).find('div', {"class": "match-timing"}).find('div', {"id": "result"}).text
            status = "ended"
        else:
            if start_time_local  > time_now +dif:
             match_status = "بعد قليل"
            else:
             match_status = " مباشر"
             match_dict['score'] = match.find('div', {"class": "match-center"}).find('div', {"class": "match-timing"}).find('div', {"id": "result"}).text
             status = True
            


        match_dict['match_status'] = match_status
        match_dict['status'] = status
        


       
        match_dict['date'] = start_time_str_local
        match_dict['commentary'] = match.find('div', {"class": "match-info"}).find('ul').find_all('li')[0].text
        match_dict['channel'] = match.find('div', {"class": "match-info"}).find('ul').find_all('li')[1].text
        match_dict['league'] = match.find('div', {"class": "match-info"}).find('ul').find_all('li')[2].text
       

        
        matches_list.append(match_dict)
    return matches_list
@app.get("/api/yesterday")
def get_yesterday():
    #swap
    #r= requests.get("https://6kora.koooora-online.com/p/yesterday-matches.html")
    #soup = BeautifulSoup(r.content, 'html.parser')
    #matches = soup.find_all('div', {"id": "yes-match"})
    #print(matches)
    #matches = soup.find_all('div', {"class": "match-container"})
  
    r= requests.get("https://kooora.alkoora.live/p/yesterday-matches.html")
    soup = BeautifulSoup(r.content, 'html.parser')
    #matches = soup.find_all('div', {"id": "today"})
    matches = soup.find_all('div', {"class": "match-event"})
    
    matches_list = []

    for match in matches:
        match_dict = {}
        match_dict['match_url'] = match.find('a')['href'].split('/')[-1]
        match_dict['match_url0'] = match.find('a')['href']
        match_dict['team1'] = match.find('div', {"class": "right-team"}).find('div', {"class": "team-name"}).text
        match_dict['team1logo'] = match.find('div', {"class": "right-team"}).find('div', {"class": "team-logo"}).find('img')['data-img']
        match_dict['team2'] = match.find('div', {"class": "left-team"}).find('div', {"class": "team-name"}).text
        match_dict['team2logo'] = match.find('div', {"class": "left-team"}).find('div', {"class": "team-logo"}).find('img')['data-img']
        match_ended = match.find('div', {"class": "match-center"}).find('div', {"class": "date"})['data-gameends']
        match_started = match.find('div', {"class": "match-center"}).find('div', {"class": "date"})['data-start']
        match_dict['match_ended'] = match_ended
        match_dict['match_started'] = match_started
        db.search(channel.id == match_dict['match_url'])
        if len(db.search(channel.id == match_dict['match_url'])) == 0:

          db.insert({"id":match_dict['match_url'],"url": match_dict['match_url0']})
        



        
        start_time = datetime.fromisoformat(match_started)
        end_time = datetime.fromisoformat(match_ended)

        tz = pytz.timezone('gmt')

        start_time_local = start_time.astimezone(tz)
        end_time_local = end_time.astimezone(tz)

        start_time_str_local = start_time_local.strftime('%H:%M')
        end_time_str_local = end_time_local.strftime('%H:%M')

        dif = timedelta(minutes=15)

        match_status =""
        status =""
        time_now = datetime.now(tz)
  
        print(start_time_local  > time_now +dif)
        print(time_now)

       
        if start_time_local > time_now:
            match_status = "لم تبدأ بعد"
            status = False
        elif end_time_local < time_now:
            match_status = "انتهت"
            match_dict['score'] = match.find('div', {"class": "match-center"}).find('div', {"class": "match-timing"}).find('div', {"id": "result"}).text
            status = "ended"
        else:
            if start_time_local  > time_now +dif:
             match_status = "بعد قليل"
            else:
             match_status = "بث مباشر"
             match_dict['score'] = match.find('div', {"class": "match-center"}).find('div', {"class": "match-timing"}).find('div', {"id": "result"}).text
             status = True
            


        match_dict['match_status'] = match_status
        match_dict['status'] = status
        


       
        match_dict['date'] = start_time_str_local
        match_dict['commentary'] = match.find('div', {"class": "match-info"}).find('ul').find_all('li')[0].text
        match_dict['channel'] = match.find('div', {"class": "match-info"}).find('ul').find_all('li')[1].text
        match_dict['league'] = match.find('div', {"class": "match-info"}).find('ul').find_all('li')[2].text   
   
        matches_list.append(match_dict)
    return matches_list

@app.get("/api/tomorrow")
def get_tomorrow():
    #swap
    #r= requests.get("https://6kora.koooora-online.com/p/yesterday-matches.html")
    #soup = BeautifulSoup(r.content, 'html.parser')
    #matches = soup.find_all('div', {"id": "yes-match"})
    #print(matches)
    #matches = soup.find_all('div', {"class": "match-container"})
  
    r= requests.get("https://kooora.alkoora.live/p/tomorrow-matches.html")
    soup = BeautifulSoup(r.content, 'html.parser')
    #matches = soup.find_all('div', {"id": "today"})
    matches = soup.find_all('div', {"class": "match-event"})
    
    matches_list = []

    for match in matches:
        match_dict = {}
        match_dict['match_url'] = match.find('a')['href'].split('/')[-1]
        match_dict['match_url0'] = match.find('a')['href']
        match_dict['team1'] = match.find('div', {"class": "right-team"}).find('div', {"class": "team-name"}).text
        match_dict['team1logo'] = match.find('div', {"class": "right-team"}).find('div', {"class": "team-logo"}).find('img')['data-img']
        match_dict['team2'] = match.find('div', {"class": "left-team"}).find('div', {"class": "team-name"}).text
        match_dict['team2logo'] = match.find('div', {"class": "left-team"}).find('div', {"class": "team-logo"}).find('img')['data-img']
        match_ended = match.find('div', {"class": "match-center"}).find('div', {"class": "date"})['data-gameends']
        match_started = match.find('div', {"class": "match-center"}).find('div', {"class": "date"})['data-start']
        match_dict['match_ended'] = match_ended
        match_dict['match_started'] = match_started
        db.search(channel.id == match_dict['match_url'])
        if len(db.search(channel.id == match_dict['match_url'])) == 0:

          db.insert({"id":match_dict['match_url'],"url": match_dict['match_url0']})
        



        
        start_time = datetime.fromisoformat(match_started)
        end_time = datetime.fromisoformat(match_ended)

        tz = pytz.timezone('gmt')

        start_time_local = start_time.astimezone(tz)
        end_time_local = end_time.astimezone(tz)

        start_time_str_local = start_time_local.strftime('%H:%M')
        end_time_str_local = end_time_local.strftime('%H:%M')

        dif = timedelta(minutes=15)

        match_status =""
        status =""
        time_now = datetime.now(tz)
  
        print(start_time_local  > time_now +dif)
        print(time_now)

       
        if start_time_local > time_now:
            match_status = "لم تبدأ بعد"
            status = False
        elif end_time_local < time_now:
            match_status = "انتهت"
            match_dict['score'] = match.find('div', {"class": "match-center"}).find('div', {"class": "match-timing"}).find('div', {"id": "result"}).text
            status = "ended"
        else:
            if start_time_local  > time_now +dif:
             match_status = "بعد قليل"
            else:
             match_status = " مباشر"
             match_dict['score'] = match.find('div', {"class": "match-center"}).find('div', {"class": "match-timing"}).find('div', {"id": "result"}).text
             status = True
            


        match_dict['match_status'] = match_status
        match_dict['status'] = status
        


       
        match_dict['date'] = start_time_str_local
        match_dict['commentary'] = match.find('div', {"class": "match-info"}).find('ul').find_all('li')[0].text
        match_dict['channel'] = match.find('div', {"class": "match-info"}).find('ul').find_all('li')[1].text
        match_dict['league'] = match.find('div', {"class": "match-info"}).find('ul').find_all('li')[2].text   
   
        matches_list.append(match_dict)
    return matches_list   
@app.get("/api/{match_id}")
def get_cdn(match_id):
  try :
    name = db.search(channel.id == match_id)[0]['url']


    r= requests.get(name)
    soup = BeautifulSoup(r.content, 'html.parser')
    matches = soup.find_all('iframe')[0]['src']
    r = requests.get(matches)
    return {"cdn":matches,
            "title":soup.find_all('h1')[0].text

            }
  except:
    return {"cdn":"not found"}
  

@app.get("/api/player/{match_id}")
def get_player(match_id):
   r = requests.get("https://online.alkoora.live/albaplayer/"+match_id+"/")

   print("https://online.alkoora.live/albaplayer/"+match_id+"/")
   soup = BeautifulSoup(r.content, 'html.parser')
   matches = soup.find_all('iframe')[0]['src']
   r= requests.get(matches)
   soup = BeautifulSoup(r.content, 'html.parser')
   script = soup.find_all('script')[7].text
   script = script.split("player = new Clappr.Player(")[1]
   script = script.split(");")[0]
   source = script.split("source:")[1]
   source = source.split("}")[0]
   source = source.split(",")[0]
   source = source.split("'")[1]

   
   
   

   
   print(source)
   return {"cdn":matches}
    
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)    
  


   



  


      

      

 




