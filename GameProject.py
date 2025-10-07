import mysql.connector
import time
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

# ---- Fixed airports, hints and letter parts ----
FIXED_CODE_AIRPORTS = ["LIRF", "GCTS", "LFPG", "EHEH", "DDDF"]

FIXED_HINTS = {
    "LIRF": "Gelato can taste sweet. :)",
    "GCTS": "Les Fleurs du Petit Garçon",
    "LFPG": "Eheh :)",
    "EHEH": "ERROR 504: Data packet lost  Driver mismatch detected  Database access denied   File structure corrupted",
    # DDDF has no hint (final)
}

letter_parts = {
    "LIRF": "You have a great chance to save the world.",
    "GCTS": "Do what you can!.",
    "LFPG": "There are still computers left, scattered around the EU that can help you",
    "EHEH": "to remember who you are.",
    "DDDF": "But don’t get too excited, since I tricked you; the secret base, the key, my password - remember?",
}

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

# ---- Core game ----

def start_game(db_conf):

    # Map
    airport = get_airport(db_conf)

    # Fixed airports and their hints
    code_positions = {icao: FIXED_HINTS.get(icao, "") for icao in FIXED_CODE_AIRPORTS}

    fixed_municipalities = {
        "LIRF": "Rome",
        "GCTS": "Tenerife",
        "LFPG": "Paris",
        "EHEH": "Eindhoven",
        "DDDF": "Frankfurt"
    }
    idents = list(airport.keys()) #return a view of all the keys in the dict

    # Ensure fixed airports are included
    for icao in FIXED_CODE_AIRPORTS:
        if icao not in airport:
            airport[icao] = {"ident": icao, "name": f"Special Airport {icao}", "municipality": ""}

    # Player state
    start = random.choice(idents)
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

def show_letter_so_far(game):
    parts = [letter_parts[i] for i in FIXED_CODE_AIRPORTS if i in game["found"]]
    if parts:
        print("\n>>> Letter so far:\n" + " ".join(parts) + "\n")

def move(game, dest_ident):
    if dest_ident not in game["airports"]:
        return f"This airport {dest_ident} is not on the map!"
    if dest_ident == game["cur"]:
        return "You are already at that airport."
    show_letter_so_far(game)
    game["attempts_left"] -= 1
    game["cur"] = dest_ident
    game["visited"].add(dest_ident)
    msg = f"You are now at {dest_ident} - {game['airports'][dest_ident]['name']} - {game['airports'][dest_ident]['municipality'] or ''}"

    # Reveal letter part for the special airport
    if dest_ident in letter_parts and dest_ident not in game["found"]:
        part = letter_parts[dest_ident]
        msg += f"\n\n>>> Letter fragment discovered:\n\"{part}\" <<<"
        hint = game["code_positions"].get(dest_ident, "")
        if hint:
            msg += f"\n\n>>> A computer flickers:\n\"{hint}\" <<<"
        game["found"].add(dest_ident)

        # If all letter parts are found
    if len(game["found"]) == len(FIXED_CODE_AIRPORTS):
        msg += "\n>>> The letter is now complete! <<<\n"
    return msg

def is_win(game):
    return len(game["found"]) == len(FIXED_CODE_AIRPORTS)

def fmt(game, ident):
    row = game["airports"][ident]
    mini = row.get("municipality") or ""
    return f"{ident} - {row['name']} - {mini}"

# ---- CLI runner ----
def run_cli(db_conf):
    from Intro import show_intro
    show_intro()
    g = start_game(db_conf)  # The core game
    start_ident = g["start"]  # Now start_ident exists
    name = input("Type the player name: ").capitalize()
    input("\n\033[32mPress Enter to start the game...\033[0m")
    print("The world is falling apart, piece by piece.")
    print("A strange new 'red hole' has opened somewhere out in the cosmos, quietly erasing the code that holds reality together.")
    print("Languages grow simpler, memories fade, and entire systems vanish overnight. Nobody knows how to stop it.")
    print(f"But somehow, {name}, you’ve woken up in the middle of it all—with nothing but a letter and a few cryptic clues that might lead to the last surviving computers.")
    print("If there’s any hope left, the hope is you.")
    input("\n\033[32mPress Enter to continue...\033[0m")
    print("You need to find the computers at each airport to piece together the letter and remember who you are. Each computer you find will give you a part of the letter and a clue to the next location.")
    print("Your journey begins now...")
    input("\n\033[32mPress Enter to accept the mission...\033[0m")
    print(f"{name}. You now are at {fmt(g, start_ident)}")
    print("Commands: list (show airports) | go <IDENT> | quit")

# Winning situation
    def show_good(letter_parts):
        print("\n--- MISSION COMPLETE ---\n")
        time.sleep(1)

        print("You have visited all the airports and decoded every hint.")
        time.sleep(1)

        print("The letter finally makes sense. You remember… it was you who caused the system error.")
        time.sleep(1)

        print("You caused the Red Death, but you are the only one who could fix it.")
        time.sleep(1)

        print("\n>>> Letter is now completed <<<\n")
        time.sleep(1)

        # Show the letter gradually
        for part in letter_parts.values():
            print(part)
            time.sleep(1)

        print("\nIt’s painful, yes. But for the first time in weeks, you feel clarity.")
        time.sleep(1)

        print("The Red Death recedes a little, just enough to stop immediate destruction.")
        time.sleep(1)

        print("You sit on a bench in the empty airport lounge, reflecting.")
        time.sleep(1)

        print("You have won not by reversing everything, but by understanding, remembering, and acting.")
        time.sleep(1)

        print("\n>>> End of letter <<<\n")
        time.sleep(1)

# Losing situation
    def show_bad(letter_parts):
        print("\n--- TIME IS UP ---\n")
        time.sleep(1)

        print("You didn’t manage to decode all the hints in time.")
        time.sleep(1)

        print("The Red Death continues its work, erasing memories and simplifying everything.")
        time.sleep(1)

        print("Fragments of the world you knew remain, but the full picture is lost.")
        time.sleep(1)

        print("\n>>> Letter partially decoded <<<\n")
        time.sleep(1)

        # Show what the player managed to find
        for part in letter_parts.values():
            print(part)
            time.sleep(1)

        print("\nA familiar face appears—the ice cream seller from Italy.")
        time.sleep(1)

        print("He hands you a cone and smiles gently.")
        time.sleep(1)

        print('"Sometimes," he says, "there are battles you can’t win no matter how hard you try. But even then… there’s beauty in small moments."')
        time.sleep(1)

        print("You take a bite, feeling the sweetness, and a quiet calm.")
        time.sleep(1)

        print("On that bench, you rest, exhausted but alive.")
        time.sleep(1)

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
        show_good(letter_parts)
        print("You have visited:")
        for ident in sorted(g["visited"]):
            print("  " + fmt(g, ident))
    elif g["attempts_left"] <= 0:
        from Badend import show_bad_end
        show_bad_end()
        show_bad(letter_parts)
    else:
        print(">>> GAME ENDED! <<<")