import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2_Project.settings')

import django
django.setup()

import uuid

from codenamez.models import *
from django.contrib.auth.models import User

from random import randint

def populate():
  words = ["africa","agent","air","alien","alps","amazon","ambulance","america","angel","antarctica","apple","arm","atlantis","australia","aztec","back","ball","band","bank","bar","bark","bat","battery","beach","bear","beat","bed","beijing","bell","belt","berlin","bermuda","berry","bill","block","board","bolt","bomb","bond","boom","boot","bottle","bow","box","bridge","brush","buck","buffalo","bug","bugle","button","calf","canada","cap","capital","car","card","carrot","casino","cast","cat","cell","centaur","center","chair","change","charge","check","chest","chick","china","chocolate","church","circle","cliff","cloak","club","code","cold","comic","compound","concert","conductor","contract","cook","copper","cotton","court","cover","crane","crash","cricket","cross","crown","cycle","czech","dance","date","day","death","deck","degree","diamond","dice","dinosaur","disease","doctor","dog","draft","dragon","dress","drill","drop","duck","dwarf","eagle","egypt","embassy","engine","england","europe","eye","face","fair","fall","fan","fence","field","fighter","figure","file","film","fire","fish","flute","fly","foot","force","forest","fork","france","game","gas","genius","germany","ghost","giant","glass","glove","gold","grace","grass","greece","green","ground","ham","hand","hawk","head","heart","helicopter","himalayas","hole","hollywood","honey","hood","hook","horn","horse","horseshoe","hospital","hotel","ice","ice cream","india","iron","ivory","jack","jam","jet","jupiter","kangaroo","ketchup","key","kid","king","kiwi","knife","knight","lab","lap","laser","lawyer","lead","lemon","leprechaun","life","light","limousine","line","link","lion","litter","loch ness","lock","log","london","luck","mail","mammoth","maple","marble","march","mass","match","mercury","mexico","microscope","millionaire","mine","mint","missile","model","mole","moon","moscow","mount","mouse","mouth","mug","nail","needle","net","new york","night","ninja","note","novel","nurse","nut","octopus","oil","olive","olympus","opera","orange","organ","palm","pan","pants","paper","parachute","park","part","pass","paste","penguin","phoenix","piano","pie","pilot","pin","pipe","pirate","pistol","pit","pitch","plane","plastic","plate","platypus","play","plot","point","poison","pole","police","pool","port","post","pound","press","princess","pumpkin","pupil","pyramid","queen","rabbit","racket","ray","revolution","ring","robin","robot","rock","rome","root","rose","roulette","round","row","ruler","satellite","saturn","scale","school","scientist","scorpion","screen","scuba diver","seal","server","shadow","shakespeare","shark","ship","shoe","shop","shot","sink","skyscraper","slip","slug","smuggler","snow","snowman","sock","soldier","soul","sound","space","spell","spider","spike","spine","spot","spring","spy","square","stadium","staff","star","state","stick","stock","straw","stream","strike","string","sub","suit","superhero","swing","switch","table","tablet","tag","tail","tap","teacher","telescope","temple","theater","thief","thumb","tick","tie","time","tokyo","tooth","torch","tower","track","train","triangle","trip","trunk","tube","turkey","undertaker","unicorn","vacuum","van","vet","wake","wall","war","washer","washington","watch","water","wave","web","well","whale","whip","wind","witch","worm","yard"]
  users = [
    {   
      "username": "test1",
      "password": "test1",
      "email": "test1@django.com",
      "is_staff": True,
      "profile": {
        "ipaddress": "127.0.0.1",
        "games_won": randint(0, 1000),
        "games_lost": randint(0, 1000),
        "games_played": randint(0, 1000),
        "ranking": randint(500, 2000) } 
    },
    {   
      "username": "test2",
      "password": "test2",
      "email": "test2@django.com",
      "is_staff": True,
      "profile": {
        "ipaddress": "127.0.0.2",
        "games_won": randint(0, 1000),
        "games_lost": randint(0, 1000),
        "games_played": randint(0, 1000),
        "ranking": randint(500, 2000) } 
    },
    {   
      "username": "test3",
      "password": "test3",
      "email": "test3@django.com",
      "is_staff": True,
      "profile": {
        "ipaddress": "127.0.0.3",
        "games_won": randint(0, 1000),
        "games_lost": randint(0, 1000),
        "games_played": randint(0, 1000),
        "ranking": randint(500, 2000) } 
    },
    {   
      "username": "test4",
      "password": "test4",
      "email": "test4@django.com",
      "is_staff": True,
      "profile": {
        "ipaddress": "127.0.0.4",
        "games_won": randint(0, 1000),
        "games_lost": randint(0, 1000),
        "games_played": randint(0, 1000),
        "ranking": randint(500, 2000) } 
    }]

  games = [
    { "id": "3ba2df11-7b57-469c-9019-48da3dfaa200",
      "name": "Demo",
      "max_players": 4 }
  ]

  for i,game in enumerate(games):
    games[i]['object'] = add_game(game['id'], game['name'], game['max_players'])

  for i,user in enumerate(users):
    u = add_user(user['username'], user['password'], user['email'], user['is_staff'])
    add_user_profile(u, user['profile']['ipaddress'], user['profile']['games_won'], user['profile']['games_lost'], user['profile']['games_played'], user['profile']['ranking'])
    if i == 0:
      add_user_to_game(u, games[0]['object'], time.time(), is_admin=True)
    else:
      add_user_to_game(u, games[0]['object'], time.time() + (i*1000))

  for word in words:
    add_word(word)

  for u in User.objects.all():
    print("[User]: {0}".format(str(u)))

  for g in Game.objects.all():
    print("[Game]: {0}".format(str(g)))
  
  for player in GamePlayer.objects.all():
    print("[Player]: {0}".format(str(player)))

def add_word(word):
  w = WordList.objects.get_or_create(word=word)[0]
  w.save()

def add_user(username, password, email, is_staff):
  u = User.objects.get_or_create(username=username)[0]
  u.set_password(password)
  u.email = email
  u.is_staff = is_staff
  u.is_superuser = is_staff
  u.save()
  return u

def add_user_profile(user, ipaddress, games_won, games_lost, games_played, ranking):
  up = UserProfile.objects.get_or_create(user=user, ipaddress=ipaddress)[0]
  up.games_won = games_won
  up.games_lost = games_lost
  up.games_played = games_played
  up.ranking = ranking
  up.save()

def add_game(id, name, max_players):
  g = Game.objects.get_or_create(id=uuid.UUID(id), name=name, max_players=max_players)[0]
  g.save()
  return g

def add_user_to_game(user, game, joined, is_admin=False):
  if is_admin:
    game.owner = user
    game.save()

  player = GamePlayer.objects.get_or_create(game=game, user=user)[0]
  player.joined = joined
  player.is_admin = is_admin
  player.save()

if __name__ == '__main__':
  print("Starting CodenameZ population script...")
  populate()
