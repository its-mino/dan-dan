from flask import Flask, render_template, request, redirect
import json
import requests
import random
import player
import string
import uuid
import time

app = Flask(__name__)

rooms = {}

with open('default_list.txt', 'r') as f:
    default_list = f.read()

def get_list(decklist):
    with open('art_links.json', 'r') as f:
        art_links = json.loads(f.read())
    l = []
    decklist = decklist.split('\n')
    for line in decklist:
        if line == '':
            continue
        splits = line.split(' ')
        for i in range(int(splits[0])):
            card_name = ' '.join(splits[1:])
            if card_name in art_links:
                l.append(art_links[card_name])
            else:
                r = requests.get('https://api.scryfall.com/cards/named?exact='+card_name)            
                data = r.json()            
                l.append(data['image_uris']['small'])
                art_links[card_name] = data['image_uris']['small']
    try:
        with open('art_links.json', 'w') as f:
            f.write(json.dumps(art_links))
    except:
        pass

    return l

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/check_code/<code>')
def check_code(code):
    if code not in rooms:
        return 'Invalid Code'
    else:
        return 'ok'

@app.route('/createroom')
def createroom():
    roomcode = ''
    for i in range(4):
        roomcode += random.choice(string.ascii_letters).upper()

    while roomcode in rooms:
        roomcode = ''
        for i in range(4):
            roomcode += random.choice(string.ascii_letters).upper()

    decklist = get_list(default_list)
    random.shuffle(decklist)

    rooms[roomcode] = {'deck': decklist, 'graveyard': [], 'stack': [], 'deck_string': default_list, 'creation_date':int(time.time()), 'p1': player.Player(), 'p2': player.Player()}
    return roomcode+'/1'

@app.route('/update_deck/<code>', methods=['POST'])
def update_deck(code):
   deckstring = request.form['decklist']
   decklist = get_list(deckstring)
   random.shuffle(decklist)
   rooms[code]['deck'] = decklist
   rooms[code]['graveyard'] = []
   rooms[code]['stack'] = []
   rooms[code]['deck_string'] = deckstring
   rooms[code]['p1'].reset()
   rooms[code]['p2'].reset()
   return 'success'

@app.route('/shuffle/<code>')
def shuffle(code):
    random.shuffle(rooms[code]['deck'])
    return 'success'

@app.route('/play/<code>/<player>')
def play(code, player):
    if code not in rooms:
        return 'Invalid Room Code'
    return render_template('play.html', code=code, player=player)

@app.route('/delete_room/<code>')
def delete_room(code):
    del rooms[code]

@app.route('/get_hand/<code>/<player>')
def get_hand(code, player):
    hand = rooms[code]['p'+player].getHand()
    return render_template('hand.html', hand = hand)

@app.route('/get_stack/<code>/<player>')
def get_stack(code, player):
    stack = rooms[code]['stack']
    return render_template('stack.html', stack = stack, player = player)

@app.route('/get_decklist/<code>')
def get_decklist(code):
    return rooms[code]['deck_string']

@app.route('/draw/<code>/<player>/<amount>')
def draw(code, player, amount):
    player = rooms[code]['p'+player]
    for i in range(int(amount)):
        player.addCardToHand(rooms[code]['deck'].pop(0))
    return 'success'

@app.route('/mill/<code>/<amount>')
def mill(code, amount):
    graveyard = rooms[code]['graveyard']
    deck = rooms[code]['deck']
    for i in range(int(amount)):
        graveyard.append(deck.pop())
    return 'success'

@app.route('/view_graveyard/<code>')
def view_graveyard(code):
    graveyard = rooms[code]['graveyard']
    with open('art_links.json', 'r') as f:        
        art_links = json.loads(f.read())
    names_graveyard = []
    for card in graveyard:
        for name, link in art_links.items():
            if card == link:
                names_graveyard.append({'name':name.replace('\'', ';'), 'url':card})
    return render_template('list.html', cards = names_graveyard, source='graveyard')

@app.route('/view_deck/<code>')
def view_deck(code):
    deck = rooms[code]['deck']
    with open('art_links.json', 'r') as f:        
        art_links = json.loads(f.read())
    names_deck = []
    for card in deck:
        for name, link in art_links.items():
            if card == link:
                names_deck.append({'name':name.replace('\'', ';'), 'url':card})
    return render_template('list.html', cards = names_deck, source='deck')

@app.route('/count_grave/<code>')
def count_grave(code):    
    graveyard = rooms[code]['graveyard']
    return str(len(graveyard))

@app.route('/count_hand/<code>/<player>')
def count_hand(code, player):    
    player_num = (1 if player == 2 else 1)
    hand = rooms[code]['p'+str(player_num)].getHand()
    return str(len(hand))

@app.route('/count_deck/<code>')
def count_deck(code):    
    deck = rooms[code]['deck']    
    return str(len(deck))

@app.route('/add_to_battlefield/<code>/<player>', methods=['POST'])
def add_to_battlefield(code, player):
    card = request.form['url']
    if 'http' not in card:
        card.replace(';', '\'')
        with open('art_links.json', 'r') as f:        
            art_links = json.loads(f.read())
        card = art_links[card]
    player = rooms[code]['p'+player]
    player.addCardToBattlefield({'card':card, 'tapped':False})
    return 'success'

@app.route('/tap/<code>/<player>', methods=['POST'])
def toggle_tap(code, player):
    card = request.form['url']
    battlefield = rooms[code]['p'+player].getBattlefield()
    for card2 in battlefield:
        if card == card2['card']:
            card2['tapped'] = not card2['tapped']
            return 'success'

@app.route('/add_to_hand/<code>/<player>', methods=['POST'])
def add_to_hand(code, player):
    card = request.form['url']
    player = rooms[code]['p'+player]
    player.addCardToHand(card)
    return 'success'

@app.route('/get_battlefield/<code>/<player>')
def get_battlefield(code, player):    
    b1 = rooms[code]['p1'].getBattlefield()
    b2 = rooms[code]['p2'].getBattlefield()
    if player == '1':
        return render_template('battlefield.html', cards = b1, cards2 = b2)
    else:
        return render_template('battlefield.html', cards = b2, cards2 = b1)

@app.route('/remove_from_battlefield/<code>/<player>', methods=['POST'])
def remove_from_battlefield(code, player):
    card = request.form['url']
    player = rooms[code]['p'+player]
    player.removeCardFromBattlefield(card)
    return 'success'

@app.route('/remove_from_hand/<code>/<player>', methods=['POST'])
def remove_from_hand(code, player):
    card = request.form['url']
    player = rooms[code]['p'+player]
    player.removeCardFromHand(card)
    return 'success'

@app.route('/add_to_stack/<code>/<player>', methods=['POST'])
def add_to_stack(code, player):
    card = request.form['url']
    stack = rooms[code]['stack']
    stack.append({'card':card, 'owner':player})
    return 'success'

@app.route('/remove_from_stack/<code>/<player>', methods=['POST'])
def remove_from_stack(code, player):
    card = request.form['url']
    stack = rooms[code]['stack']
    for i, c in enumerate(stack):
        if c['owner'] == player and c['card'] == card:
            target = i
    del stack[target]
    return 'success'
            
@app.route('/add_to_deck/<code>', methods=['POST'])
def add_to_deck(code):
    card = request.form['url']
    deck = rooms[code]['deck']
    deck.insert(0, card)
    return 'success'

@app.route('/add_to_graveyard/<code>', methods=['POST'])
def add_to_graveyard(code):
    card = request.form['url']
    graveyard = rooms[code]['graveyard']
    graveyard.insert(0, card)
    return 'success'

@app.route('/remove_from_graveyard/<code>', methods=['POST'])
def remove_from_graveyard(code):
    card = request.form['url']
    card.replace(';', '\'')
    graveyard = rooms[code]['graveyard']
    with open('art_links.json', 'r') as f:            
        art_links = json.loads(f.read())        
    card = art_links[card]
    graveyard.remove(card)
    return 'success'

@app.route('/remove_from_deck/<code>', methods=['POST'])
def remove_from_deck(code):
    card = request.form['url']
    card.replace(';', '\'')
    with open('art_links.json', 'r') as f:            
        art_links = json.loads(f.read())        
    card = art_links[card]
    deck = rooms[code]['deck']
    deck.remove(card)
    return 'success'
