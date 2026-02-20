class Yatzee:
    def __init__(self, rolls):
        self.uppercategories = {
            "Aces": ["Sum all 1s", 1, "-"],
            "Twos": ["Sum all 2s", 2, "-"],
            "Threes": ["Sum all 3s", 3, "-"],
            "Fours": ["Sum all 4s", 4, "-"],
            "Fives": ["Sum all 5s", 5, "-"],
            "Sixes": ["Sum all 6s", 6, "-"],
            "Bonus": ["If total over 63, +35", 35, "-"],
        }
        self.lowercategories = {
            "Chance": ["Sum all dice", "Sum", "-"],
            "Three of a kind": ["Sum all if 3 of a kind", "Sum", "-"],
            "Four of a kind": ["Sum all if 4 of a kind", "Sum", "-"],
            "Full house": ["+25 if 3 and 2 of kinds", 25, "-"],
            "Small straight": ["+30 if 4 in sequence", 30, "-"],
            "Large straight": ["+40 if 5 in sequence", 40, "-"],
            "Yahtzee": ["+50 if all dice match", 50, "-"],
        }
        self.dice = sorted(rolls)
        self.upperscore = 0
        self.lowerscore = 0

   
    def set_dice(self, rolls):
        """Supply the current five dice values.

        The GUI should call this at the start of each scoring attempt; the
        list is stored sorted because many scoring helpers rely on order.
        """
        self.dice = sorted(rolls)

    def score_category(self, category):
        """Score the current dice in the named category."""
        if not isinstance(category, str):
            raise ValueError("category must be a string")
        cat = category.capitalize()
        if cat in self.uppercategories:
            self.upperscorecalculator(cat)
        elif cat in self.lowercategories:
            kind = self.lowercategories[cat][1]
            if kind == "Sum":
                self.kinds(cat)
            elif cat in ("Large straight", "Small straight"):
                self.straights(cat)
            else:
                self.specialcases(cat)
        else:
            raise ValueError(f"unknown category '{category}'")

    def get_lines(self):
        """Return list of (category_or_None, display_text) for rendering."""
        result = []
        result.append((None, "Upper Section"))
        for name in self.uppercategories:
            desc, _, pts = self.uppercategories[name]
            result.append((name, f"{name:18} {desc:25} {pts}"))
        result.append((None, ""))
        result.append((None, "Lower Section"))
        for name in self.lowercategories:
            desc, _, pts = self.lowercategories[name]
            result.append((name, f"{name:18} {desc:25} {pts}"))
        total = self.totalscore(self.uppercategories) + self.totalscore(
            self.lowercategories
        )
        result.append((None, f"Total: {total}"))
        return result

 
    def run(self):
        # (unchanged) CLI loop
        for i in range(13):
            self.insertnewdice()
            if self.dice == []:
                break
            self.poytakirja()
            print(self.dice)
            self.dice.sort()
            chosencategory = input(
                "Which category would you like to score in? "
            ).capitalize()
            if chosencategory in self.uppercategories:
                self.upperscorecalculator(chosencategory)
            elif self.lowercategories[chosencategory][1] == "Sum":
                self.kinds(chosencategory)
            elif chosencategory == "Full house" or chosencategory == "Yahtzee":
                self.specialcases(chosencategory)
            elif (
                chosencategory == "Large straight"
                or chosencategory == "Small straight"
            ):
                self.straights(chosencategory)
        self.poytakirja()
        print("Gameover!")

    def upperscorecalculator(self, category):
        self.cheatcheck(category, self.uppercategories)
        self.uppercategories[category][2] = 0
        for i in self.dice:
            if int(i) == self.uppercategories[category][1]:
                self.uppercategories[category][2] += int(i)
        if self.totalscore(self.uppercategories) >= 63:
            self.uppercategories["Bonus"][2] = 35

    def straights(self, category):
        """Score a small or large straight correctly.

        The previous implementation counted a simple run and treated duplicates
        as breaks; real Yatzy looks for any run of four (small) or five (large)
        **distinct** consecutive values.  Use set membership checks.
        """
        self.cheatcheck(category, self.lowercategories)
        self.lowercategories[category][2] = 0
        vals = set(self.dice)
        if category == "Small straight":
            # three possible small-straight runs
            for seq in ([1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]):
                if all(x in vals for x in seq):
                    self.lowercategories[category][2] = 30
                    break
        else:  # Large straight
            if vals.issuperset({1, 2, 3, 4, 5}) or vals.issuperset({2, 3, 4, 5, 6}):
                self.lowercategories[category][2] = 40

    def kinds(self, category):
        self.cheatcheck(category, self.lowercategories)
        self.lowercategories[category][2] = 0
        if category == "Three of a kind":
            for i in self.dice:
                if self.dice.count(i) >= 3:
                    self.lowercategories[category][2] = sum(self.dice)
        elif category == "Four of a kind":
            for i in self.dice:
                if self.dice.count(i) >= 4:
                    self.lowercategories[category][2] = sum(self.dice)
        elif category == "Chance":
            self.lowercategories[category][2] = sum(self.dice)

    def specialcases(self, category):
        if (
            category == "Yahtzee"
            and self.lowercategories[category][2] != "-"
            and self.lowercategories[category][2] != 0
        ):
            if self.dice.count(self.dice[0]) >= 5:
                self.lowercategories[category][2] += 100
                return
        self.cheatcheck(category, self.lowercategories)
        self.lowercategories[category][2] = 0
        if category == "Yahtzee":
            if self.dice.count(self.dice[0]) >= 5:
                self.lowercategories[category][2] = 50
        if category == "Full house":
            if (
                self.dice.count(self.dice[0]) >= 2
                and self.dice.count(self.dice[4]) >= 3
                or self.dice.count(self.dice[0]) >= 3
                and self.dice.count(self.dice[4]) >= 2
            ):
                self.lowercategories[category][2] = 25

    def cheatcheck(self, chosen, category):
        if category[chosen][2] != "-" or chosen == "Bonus":
            raise Exception(
                "Sorry, you're playing the game wrong, please start over"
            )

    # ------------------------------------------------------------------
    # convenience/query helpers
    # ------------------------------------------------------------------
    def remaining_categories(self):
        """Return list of category names that are still unfilled.
        Bonus is excluded since it is not chosen by the player.
        """
        cats = []
        for name, data in self.uppercategories.items():
            if name != "Bonus" and data[2] == "-":
                cats.append(name)
        for name, data in self.lowercategories.items():
            if data[2] == "-":
                cats.append(name)
        return cats

    def is_complete(self):
        """Return True when all thirteen scoring boxes have been filled."""
        return len(self.remaining_categories()) == 0

    def insertnewdice(self):
        result = input("Uudet nopat: ")
        self.dice = [int(i) for i in result]

    def totalscore(self, categories):
        self.score = 0
        for i in categories:
            if categories[i][2] != "-":
                self.score += categories[i][2]
        return self.score

    def poytakirja(self):
        self.formatline()
        print("Upper Section")
        self.formatline()
        print(f"{'Category':18} {'Point Calculation':25} Points Earned")
        self.formatline()
        for i in self.uppercategories:
            print(
                f"{i:18} {self.uppercategories[i][0]:25} {self.uppercategories[i][2]}"
            )
        self.formatline()
        print(
            f"{'Upper Total':42}{self.totalscore(self.uppercategories)}"
        )
        self.formatline()
        print("")
        self.formatline()
        print("Lower Section")
        self.formatline()
        print(f"{'Category':18} {'Point Calculation':25} Points Earned")
        self.formatline()
        for i in self.lowercategories:
            print(
                f"{i:18} {self.lowercategories[i][0]:25} {self.lowercategories[i][2]}"
            )
        self.formatline()
        print(
            f"{'Lower Total':45}{self.totalscore(self.lowercategories)}"
        )
        self.formatline()
        print(
            f"{'Total':45}{self.totalscore(self.lowercategories)+self.totalscore(self.uppercategories)}"
        )
        self.formatline()

    def formatline(self):
        print("-" * 61)



if __name__ == "__main__":
    game = Yatzee("11666")
    game.run()