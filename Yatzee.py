class Yatzee():
    def __init__(self, rolls):
        self.uppercategories = {"Aces": ["Sum all 1s",1,"-"],
                    "Twos": ["Sum all 2s",2,"-"],
                    "Threes": ["Sum all 3s",3,"-"],
                    "Fours": ["Sum all 4s",4,"-"],
                    "Fives": ["Sum all 5s",5,"-"],
                    "Sixes": ["Sum all 6s",6,"-"],
                    "Bonus": ["If total over 63, +35",35,"-"],}
        self.lowercategories = {"Chance": ["Sum all dice","Sum","-"],
                    "Three of a kind": ["Sum all if 3 of a kind","Sum","-"],
                    "Four of a kind": ["Sum all if 4 of a kind","Sum","-"],
                    "Full house": ["+25 if 3 and 2 of kinds",25,"-"],
                    "Small straight": ["+30 if 4 in sequence",30,"-"],
                    "Large straight": ["+40 if 5 in sequence",40,"-"],
                    "Yahtzee": ["+50 if all dice match",50,"-"]}
        self.dice = rolls
        self.upperscore = 0
        self.lowerscore = 0

    def run(self):
        for i in range(13):
            self.insertnewdice()
            if self.dice == []:
                break
            self.poytakirja()
            print(self.dice)
            self.dice.sort()
            chosencategory = input("Which category would you like to score in? ").capitalize()
            
            #Tässä tehdään ylävalikot, jossa lasketaan vaan samanlaiset nopat.
            if chosencategory in self.uppercategories:
                self.upperscorecalculator(chosencategory)

            #Tässä tehdään "keskivalikot", eli ne jotka laskevat kaikkien noppien Summan, jos heitto sopii kategoriaan.
            elif self.lowercategories[chosencategory][1] == "Sum":
                self.kinds(chosencategory)


            #Tässä tehdään alavalikot, joissa lisätään aina sama luku, kunhan heitto sopii.
            #Eka tehdään Yahtzee tai Full House.
            elif chosencategory == "Full house" or chosencategory == "Yahtzee":
                self.specialcases(chosencategory)

            #Tässä tehdään suorat.
            elif chosencategory == "Large straight" or chosencategory == "Small straight":
                self.straights(chosencategory)

        self.poytakirja()
        print("Gameover!")
        #self.scoreprinter()



#Tämän sisällä on kaikki laskulogiikka.
    #Ylä kategoriat on helppo laskea tällä.
    def upperscorecalculator(self, category):
        self.cheatcheck(category, self.uppercategories)
        self.uppercategories[category][2] = 0
        for i in self.dice:
            if int(i) == self.uppercategories[category][1]:
                self.uppercategories[category][2] += int(i)
        if self.totalscore(self.uppercategories) >= 63:
            self.uppercategories["Bonus"][2] = 35
        #print(self.uppercategories)
        #print(self.lowercategories)

    def straights(self, category):
        self.cheatcheck(category, self.lowercategories)
        self.lowercategories[category][2] = 0
        #Täällä hoidetaan Large ja Small Straight
        length = 1
        for i in range(len(self.dice)-1):
            if self.dice[i] == self.dice[i+1]-1:
                length += 1
        print(length)
        print(category)
        if category == "Small straight" and length >= 4:
                    self.lowercategories[category][2] = 30
        elif category == "Large straight" and length >= 5:
                    self.lowercategories[category][2] = 40

    def kinds(self, category):
        self.cheatcheck(category, self.lowercategories)
        self.lowercategories[category][2] = 0
        #Täällä hoidetaan 3 and 4 of a kind, ja samalla Chance, koska toimii samalla lailla.
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
        self.cheatcheck(category, self.lowercategories)
        self.lowercategories[category][2] = 0
        #Täällä hoidetaan Yahtzee ja Full House, jotka ovat vähän erikoisia
        if category == "Yahtzee":
            if self.dice.count(self.dice[0]) >= 5:
                self.lowercategories[category][2] = 50
        if category == "Full house":
            if self.dice.count(self.dice[0]) >= 2 and self.dice.count(self.dice[4]) >= 3 or self.dice.count(self.dice[0]) >= 3 and self.dice.count(self.dice[4]) >= 2 :
                self.lowercategories[category][2] = 25

    def cheatcheck(self, chosen, category):
        if category[chosen][2] != "-" or chosen == "Bonus":
            raise Exception("Sorry, you're playing the game wrong, please start over")
#Tämän sisällä on kaikki laskulogiikka.


#Tämän sisällä on "Käyttäjäpuoli"
    def insertnewdice(self):
        # Sisäisiä testejä varten
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
        print(f"{"Category":18} {"Point Calculation":25} Points Earned")
        self.formatline()
        for i in self.uppercategories:
            print(f"{i:18} {self.uppercategories[i][0]:25} {self.uppercategories[i][2]}")
        self.formatline()
        print(f"{"Upper Total":42}{self.totalscore(self.uppercategories)}")
        self.formatline()
        print("")
        self.formatline()
        print("Lower Section")
        self.formatline()
        print(f"{"Category":18} {"Point Calculation":25} Points Earned")
        self.formatline()
        for i in self.lowercategories:
            print(f"{i:18} {self.lowercategories[i][0]:25} {self.lowercategories[i][2]}")
        self.formatline()
        print(f"{"Lower Total":45}{self.totalscore(self.lowercategories)}")
        self.formatline()
        print(f"{"Total":45}{self.totalscore(self.lowercategories)+self.totalscore(self.uppercategories)}")
        self.formatline()

    def formatline(self):
        print("-"*61)


game = Yatzee("11666")
game.run()




    #def scoreprinter(self):
        #score = self.upperscore + self.lowerscore
        # Jos saa tarpeeksi pisteitä ylävalikosta, tulee lisä pisteitä
        #if self.upperscore > 5:
            #score += 35
        #print(score)