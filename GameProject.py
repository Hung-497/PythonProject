import mysql.connector
import random

connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='demogame',
         user='root',
         password='Giahung@!497',
         autocommit=True,
         auth_plugin="mysql_native_password",
         use_pure=True
)

def get_airport(db_conf): #random 30 airports for the game
    sql = """SELECT ident, name, municipality
             FROM airport
             WHERE continent = 'EU'
               AND type = 'large_airport'
             ORDER by RAND() LIMIT 30;"""
    con = mysql.connector.connect(**db_conf)
    cur = con.cursor(dictionary=True)   # each row is a dict
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
        "airports": airport,                # dict: ident -> row {'ident','name','municipality'}
        "idents": idents,                   # list of the 30 idents, shuffled
        "code_positions": code_positions,   # dict: ident -> {'name','code'}  (5 entries)
        "start": start,                     # starting ident
        "cur":start,                        # starting ident
        "found": set(),                     # idents where a code was found
        "visited": {start},                 # idents the player has visited
        "attempts_left": 21,                # moves remaining
        "max_attempts": 21
    }
    return game
def move(game, dest_ident):
    if dest_ident not in game["airports"]:
        return f"This airport {dest_ident} is not on the map!"
    if dest_ident == game["cur"]:
        return "You are already at that airport." # for duplicate ident

    game["attempts_left"] -= 1        # consume 1 attempt for 1 move
    game["cur"] = dest_ident          # update posi
    game["visited"].add(dest_ident)   # mark visited location

    msg = f"You are now at {dest_ident} - {game["airports"][dest_ident]["name"]} - {game["airports"][dest_ident]["municipality"] or ''}"
    # Reveal code if present and not already found
    if dest_ident in game["code_positions"] and dest_ident not in game["found"]:
       art = game["code_positions"][dest_ident]
       print(f"Congratulation, the computers in {game["airports"][dest_ident]["name"]} completely read the code. It is decrypted and gradually destroyed a part of 'Red Death'. Keep Fighting!!")
       msg += f" | >>> CODE FOUND: {art['name']} ({len(game['found']) +1}/5) <<<\n"
       msg += (art["code"] or "")
       game["found"].add(dest_ident)
    else:
        print(f"Unfortunately, the computers in {game["airports"][dest_ident]["name"]} are broken. Go to the next destination.")
    return msg

def is_win(game):   # win condition
    return len(game["found"]) == 5

def fmt(game, ident):   # show clearly ident - name - muni
    row = game["airports"][ident]
    mini = row.get("municipality") or ""
    return f"{ident} - {row['name']} - {mini}"

# ---- CLI runner ----
def run_cli(db_conf):   # interface loop
    from Intro import show_intro
    show_intro()
    g = start_game(db_conf) # The core game
    start_ident = g["start"]
    name = input("Type the player name: ").upper()
    input("\n\033[32mPress Enter to start the game...\033[0m")
    print(f"Our Milky Way contains a database of humankind's knowledge and its very existence. But humanity now faces adversity from an evil called ‘Red Death’, which is in its evil mission to eliminate humankind. \nThe intelligence agencies of the world get a tip-off that the world has 21 days before ‘Red Death’ succeeds in its evil mission. But humanity could be saved, and there is always a greater good that \nfaces the evil. There are 5 codes hidden around the large airports in the EU, which will save our world if all are found and decrypted. Since there is anarchy and governments don't trust each other, \nthey won't cooperate. Here you are our Hero, {name}, a spy belonging to a secret Spy agency under the government named 'IPM', who takes it upon themselves to save the world. They chose you and \nentrusted you to save our world.")
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
                for ident in sorted(remaining): # show ident - name - muni
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





