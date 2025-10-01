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

def get_airports_30(db_conf):
    """Return dict[ident] = row for 30 random, valid airports."""
    con = mysql.connector.connect(**db_conf)
    cur = con.cursor(dictionary=True)
    cur.execute(
        """
        SELECT ident, name, municipality
        FROM airport
        WHERE type = 'large_airport'
          AND continent = 'EU'
        ORDER BY RAND()
        LIMIT 30
        """
    )
    rows = cur.fetchall()
    cur.close()
    con.close()
    return {r["ident"]: r for r in rows}

def load_ascii_art_5(db_conf):
    """Pick 5 ascii arts from goals table (ordered by id for determinism)."""
    con = mysql.connector.connect(**db_conf)
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT name, code FROM goals ORDER BY id LIMIT 5")
    arts = cur.fetchall()
    cur.close()
    con.close()
    return arts  # list of dicts: {'name': ..., 'code': ...}

# ---- Core game ----

class FlightGame:
    def __init__(self, db_conf):
        # Map
        self.airports = get_airports_30(db_conf)
        self.idents = list(self.airports.keys())

        # Choose 5 code spots
        arts = load_ascii_art_5(db_conf)  # [{'name','code'} * 5]
        random.shuffle(self.idents)
        self.code_positions = {}  # ident -> {'name':..., 'code':...}
        for ident, art in zip(self.idents[:5], arts):
            self.code_positions[ident] = art

        # Player state
        self.start = random.choice(self.idents)
        self.cur = self.start
        self.found_idents = set()   # airports where code was found
        self.visited = {self.start} # track visited for 'list' command

    def move(self, dest_ident: str):
        if dest_ident not in self.airports:
            return f"Airport {dest_ident} is not on the map!"
        self.cur = dest_ident
        self.visited.add(dest_ident)

        r = self.airports[dest_ident]
        msg = f"You are now at {self.fmt(dest_ident)}"
        # Reveal code if present & not yet collected
        if dest_ident in self.code_positions and dest_ident not in self.found_idents:
            art = self.code_positions[dest_ident]
            msg += f" | >>> CODE FOUND: {art['name']} ({len(self.found_idents) + 1}/5) <<<\n"
            # In ASCII art đúng như DB lưu (giữ newline/spacing)
            msg += (art['code'] or '')
            self.found_idents.add(dest_ident)
        return msg

    def is_win(self):
        return len(self.found_idents) == 5

    def fmt(self, ident: str) -> str:
        row = self.airports[ident]
        return f"{ident} - {row['name']} - {row.get('municipality') or ''}"
# ---- CLI runner ----

def run_cli(db_conf):
    from Intro import show_intro
    show_intro()
    g = FlightGame(db_conf)
    print(f"You are now at {g.fmt(g.start)}")
    print("Commands: list (show *unvisited* airports), go <IDENT>, quit")

    while not g.is_win():
        print(f"\nCodes found: {len(g.found_idents)}/5 | Current location: {g.cur}")
        cmd = input("> ").strip().split()
        if not cmd:
            continue
        c = cmd[0].lower()
        if c == "list":
            remaining = [i for i in g.idents if i not in g.visited]
            count = len(remaining)
            if count > 0:
                print(f"You only have {count} airports remaining:")
                print(", ".join(sorted(remaining)))
            else:
                print("(No more unvisited airports)")
        elif c == "go" and len(cmd) >= 2:
            print(g.move(cmd[1]))
        elif c == "quit":
            break
        else:
            print("Invalid command.")
    if g.is_win():
        print(">>> WIN! You found all 5 codes. <<<")
        print(f'U have visited{g.visited}')

