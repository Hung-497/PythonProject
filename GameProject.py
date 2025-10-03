import mysql.connector
import sys, time
sys.stdout.reconfigure(line_buffering=True)
import random

connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='demogame',
         user='root',
         password='maria',
         autocommit=True,
         auth_plugin="mysql_native_password",
         use_pure=True
)

## this is a function for defining random airports in r rows

def get_airport(db_conf): #random 30 airports for the game
    sql = """SELECT ident, name, municipality
             FROM airport
             WHERE continent = 'EU'
               AND type = 'large_airport'
             ORDER by RAND() LIMIT 30;"""
    con = mysql.connector.connect(**db_conf)
    cur = con.cursor(dictionary=True)
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    con.close()
    return {r["ident"]: r for r in rows}

def ascii_art(db_conf): #pick 5 ascii art from goals (ordered by id for determinism)
    sql = """select name, code from goals order by id limit 5 """
    con = mysql.connector.connect(**db_conf)
    cur = con.cursor(dictionary=True)
    cur.execute(sql)
    arts = cur.fetchall()
    cur.close()
    con.close()
    return arts

# ---- Core game ----

def start_game(db_conf):

    # Map
    airport = get_airport(db_conf)
    idents = list(airport.keys()) #return a view of all the keys in the dict

    # Choose 5 code spots
    arts = ascii_art(db_conf)
    random.shuffle(idents) #shuffle all the codes in 30 airports
    code_positions = {}
    for ident, art in zip(idents[:5], arts):
        code_positions[ident] = art

    # Player state
    start = random.choice(idents)   #Pick a random airport to spawn
    game = {
        "airports": airport,
        "idents": idents,
        "code_positions": code_positions,
        "start": start,
        "cur":start,
        "found": set(),
        "visited": {start},
        "attempts_left": 21,
        "max_attempts": 21
    }
    return game
def move(game, dest_ident):
    if dest_ident not in game["airports"]:
        return f"This airport {dest_ident} is not on the map!"
    if dest_ident == game["cur"]:
        return "You are already at that airport." # for duplicate ident

    game["attempts_left"] -= 1 # consume 1 attempt for 1 move
    game["cur"] = dest_ident
    game["visited"].add(dest_ident)

    msg = f"You are now at {dest_ident} - {game["airports"][dest_ident]["name"]} - {game["airports"][dest_ident]["municipality"] or ''}"
    # Reveal code if present and not already found
    if dest_ident in game["code_positions"] and dest_ident not in game["found"]:
       art = game["code_positions"][dest_ident]
       print(f"The computers in {game["airports"][dest_ident]["name"]} completely read the code. It is decrypted and gradually destroyed a part of 'Red Death'. Keep Fighting!!")
       msg += f" | >>> CODE FOUND: {art['name']} ({len(game['found']) +1}/5) <<<\n"
       msg += (art["code"] or "")
       game["found"].add(dest_ident)
    return msg

def is_win(game):
    return len(game["found"]) == 5

def fmt(game, ident):
    row = game["airports"][ident]
    mini = row.get("municipality") or ""
    return f"{ident} - {row['name']} - {mini}"

# ---- CLI runner ----
def run_cli(db_conf):
    from Intro import show_intro
    show_intro()
    g = start_game(db_conf) # The core game
    start_ident = g["start"]
    name = input("Type the player name: ").upper()
    input("\n\033[32mPress Enter to start the game...\033[0m")
    print("The world is falling apart, piece by piece.")
    print("A strange new 'red hole' has opened somewhere out in the cosmos, quietly erasing the code that holds reality together.")
    print("Languages grow simpler, memories fade, and entire systems vanish overnight. Nobody knows how to stop it.")
    print(f"But somehow, {name}, you’ve woken up in the middle of it all—with nothing but a letter, a few cryptic clues, and a map that might lead to the last surviving computers.")
    print("If there’s any hope left, the hope is you.")
    input("\n\033[32mPress Enter to accept the mission...\033[0m")
    print(f"{name}. You now are at {fmt(g, start_ident)}")
    print("Commands: list (show airports) | go <IDENT> | quit")

    # Main loop
    while not is_win(g) and g["attempts_left"] > 0:
        cur_ident = g["cur"]
        print(f"Codes found: {len(g['found'])}/5 | Days left: {g["attempts_left"]}/{g["max_attempts"]} | Current location: {fmt(g, cur_ident)}")
        cmd = input("Choose your next destination: ").strip().upper().split()
        if not cmd:
            continue

        c = cmd[0].lower()

        if c == "list":
            remaining = []    # Build a list of unvisited airports
            for i in g["idents"]:
                if i not in g["visited"]:
                    remaining.append(i)

            count = len(remaining)

            if count > 0:
                print(f"You only have {count} airports remaining:")
                for ident in sorted(remaining): # show IDENT – NAME – MUNICIPALITY one per line
                    print("  " + fmt(g, ident))
            else:
                print("(No more unvisited airports)")
        elif c == "go" and len(cmd) >= 2:
            print(move(g,cmd[1]))
        elif c == "quit":
            break
        else:
            print("Invalid command.")
    if is_win(g):
        from Goodend import show_good_end
        show_good_end()
        print("You have visited:")
        for ident in sorted(g["visited"]):
            print("  " + fmt(g, ident))
    elif g["attempts_left"] <= 0:
        from Badend import show_bad_end
        show_bad_end()
    else:
        print(">>> GAME ENDED! <<<")





