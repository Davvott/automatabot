"""AutomataBot is ready"""
import requests
import random

URL = "https://api.noopschallenge.com/automatabot/rules"
URL_challenge = "https://api.noopschallenge.com/automatabot/challenges/new"
URL_post = "https://api.noopschallenge.com{}"


class AutomataBot:
    """Automata Class. Fetches rules and challenge and initializes from there. """
    def __init__(self):
        self.download = self.fetch_rules()
        self.rules = random.choice(self.download)
        self.challenge = self.fetch_challenge()
        self.challengepath = self.challenge['challengePath']

        self.name = self.challenge['challenge']['rules']['name']
        self.birth = self.challenge['challenge']['rules']['birth']
        self.survival = self.challenge['challenge']['rules']['survival']

        self.cells = self.challenge['challenge']['cells']
        self.generations = self.challenge['challenge']['generations']
        self.success = False
        self.rows = len(self.cells)
        self.cols = len(self.cells[0])

    def __str__(self):
        return "Name: {}, Birth: {}, Survival: {}, Life Span: {}, Cols: {}, Rows: {}\n{}".format(
            self.name, self.birth, self.survival, self.generations, self.cols, self.rows, self.challengepath)

    @staticmethod
    def fetch_rules():
        """You gotta know the rules to break them"""
        req = requests.get(URL)
        result = req.json()
        return result

    @staticmethod
    def fetch_challenge():
        """Ready!"""
        req = requests.get(URL_challenge)
        result = req.json()
        return result

    def next_state(self):
        """Parses next game state, returns a list of tile coordinates that will change for next_state
        Tk Grid takes care of flipping their color"""
        dead_cells = []
        live_cells = []
        alive_cells = self.get_alive_cells()  # returns list of pairs

        for j in range(self.rows):
            for i in range(self.cols):
                # Count your blessings
                alive_nei = self.count_neighbors(x=i, y=j, alive=alive_cells)  # returns int
                # Does it die?
                if alive_nei not in self.survival and [j, i] in alive_cells:  # dies
                    dead_cells.append([j, i])
                # Does it arise?
                elif alive_nei in self.birth and [j, i] not in alive_cells:  # birth
                    live_cells.append([j, i])
                else:
                    pass  # I will survive!

        # set cells to next state
        for cell in dead_cells:
            self.cells[cell[0]][cell[1]] = 0
        for cell in live_cells:
            self.cells[cell[0]][cell[1]] = 1

        self.generations -= 1
        if self.generations == 0:
            self.send_challenge_solution()

        flip_cells = dead_cells + live_cells
        return flip_cells

    def send_challenge_solution(self):
        """To win, or not to win. That is the challenge."""
        post = URL_post.format(self.challengepath)
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
