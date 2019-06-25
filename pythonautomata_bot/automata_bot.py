"""AutomataBot is ready"""
import requests
import random

DOMAIN = "https://api.noopschallenge.com"
RULES = "/automatabot/rules"
NEW = "/automatabot/challenges/new"


class AutomataBot:
    """Automata Class. Fetches rules and challenge and initializes from there. """
    def __init__(self, challenge=NEW):
        self.download = self.fetch_rules()
        self.rules = random.choice(self.download)

        self.challenge = self.fetch_challenge(challenge=challenge)
        try:
            self.challengepath = self.challenge['challengePath']
            self.name = self.challenge['challenge']['rules']['name']
            self.birth = self.challenge['challenge']['rules']['birth']
            self.survival = self.challenge['challenge']['rules']['survival']
            self.cells = self.challenge['challenge']['cells']
            self.generations = self.challenge['challenge']['generations']
        except KeyError:
            self.challengepath = ""
            self.name = self.challenge['rules']['name']
            self.birth = self.challenge['rules']['birth']
            self.survival = self.challenge['rules']['survival']
            self.cells = self.challenge['cells']
            self.generations = self.challenge['generations']
        self.rows = len(self.cells)
        self.cols = len(self.cells[0])
        self.success = False

    def __str__(self):
        return "Name: {}, Birth: {}, Survival: {}, Life Span: {}, Cols: {}, Rows: {}\n{}".format(
            self.name, self.birth, self.survival, self.generations, self.cols, self.rows, self.challengepath)

    @staticmethod
    def fetch_rules():
        """You gotta know the rules to break them"""
        url = DOMAIN + RULES
        req = requests.get(url)
        result = req.json()
        return result

    @staticmethod
    def fetch_challenge(challenge):
        """Ready!"""
        url = DOMAIN + challenge
        req = requests.get(url)
        result = req.json()
        return result

    def next_state(self):
        """Parses next game state, returns a list of tile coordinates that will change for next_state
        Tk Grid takes care of flipping their color"""
        dead_cells = []
        live_cells = []
        flip_cells = []
        alive_cells = self.get_alive_cells()  # returns list of pairs

        for j in range(self.rows):
            for i in range(self.cols):
                # Count your blessings
                alive_nei = self.count_neighbors(x=i, y=j, alive=alive_cells)  # returns int
                # Does it die?
                if alive_nei not in self.survival and self.cells[j][i] == 1:  # dies
                    flip_cells.append([j, i])
                # Does it arise?
                elif alive_nei in self.birth and self.cells[j][i] != 1:  # birth
                    flip_cells.append([j, i])
                else:
                    pass  # I will survive!

        # set cells to next state
        for y, x in flip_cells:
            self.cells[y][x] = 1 if self.cells[y][x] == 0 else 0

        self.generations -= 1
        if self.generations == 0:
            self.send_challenge_solution()

        # flip_cells = dead_cells + live_cells
        return flip_cells

    def send_challenge_solution(self):
        """To win, or not to win. That is the challenge."""
        post = DOMAIN + self.challengepath
        print(post)
        req = requests.post(post, json=self.cells)
        r = req.json()
        print(r)
        try:
            if r['result'] == 'correct':
                self.success = True
        except KeyError as error:
            print(error)

    def count_neighbors(self, x, y, alive):
        """Hey Neighbour, with x,y coords and list of live ones - counts surrounding neighbors
        Returns: account of alive_neighbors, get it?
        """
        # Index values for grid
        x_bound = self.cols
        y_bound = self.rows
        alive_neighbors = 0

        # Set Horizontal, Vertical, RDIAG, LDIAG directions
        for delta_x, delta_y in [(1, 0), (0, 1), (1, 1), (-1, 1)]:
            # Set delta for +- directions
            for delta in (1, -1):
                delta_x *= delta  # (1*1); (1+-1); (0*1); (0*-1) ...
                delta_y *= delta  # (0*1); (0*-1); (1*1); (1*-1) ...
                next_x = x + delta_x  # = 1; -1; 0; 0; ...
                next_y = y + delta_y  # = 0, 0; 1; -1; ...

                if 0 <= next_y <= y_bound and 0 <= next_x <= x_bound:
                    if [next_y, next_x] in alive:
                        alive_neighbors += 1

        return alive_neighbors

    def get_alive_cells(self):
        """Returns list of pairs of [[y, x],...]"""
        coords = []
        # iterate over entire initial
        for j, row in enumerate(self.cells):
            for i, col_el in enumerate(row):
                if col_el == 1:  # its alive
                    coords.append([j, i])  # append tuple coords

        return coords
