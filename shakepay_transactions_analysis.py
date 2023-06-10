### AUTEUR : ALEXANDRE ROUSSEAU
### LIEU : SHERBROOKE, QC


class Shakepay_transactions:
    purchase_queue = []
    sale_queue = []
    sale_per_year = {}

    def __init__(self):
        self.Analyse_Transaction()
        self.Format_Sale_Queue()
        self.Format_Purchase_Queue()
        self.Create_Dict()
        self.Calcul_Tax()

    ### Fonction permettant d'ouvrir le fichier "transactions_summary.csv" à partir du répertoire courat et créer deux
    ### listes. Soit deux listes contenant un nombre de btc et le prix unitaire lors de la transaction.
    def Analyse_Transaction(self):
        # indice des colonnes
        date = 1
        amount_debited = 2
        amount_credited = 4
        buy_sell_rate = 6
        direction = 7
        file = open("transactions_summary.csv", "r")
        for line in file:
            list = line.split(',')
            match list[direction]:
                case '"purchase"':
                    self.purchase_queue.append([list[amount_credited], list[buy_sell_rate]])
                case '"sale"':
                    self.sale_queue.append([list[date], list[amount_debited], list[buy_sell_rate]])

    ### Fonction permettant de convertir l'année, le nombre et le prix unitaire du btc de chaines en nombres.
    def Format_Sale_Queue(self):
        date = 0
        amount_debited = 1
        buy_sell_rate = 2
        for i in range(len(self.sale_queue)):
            self.sale_queue[i][date] = int(self.sale_queue[i][date].split('-')[0].split('"')[1])
            self.sale_queue[i][amount_debited] = float(self.sale_queue[i][amount_debited])
            self.sale_queue[i][buy_sell_rate] = float(self.sale_queue[i][buy_sell_rate].split('"')[1])


    ### Fonction permettant de convertir le nombre et le prix unitaire du btc de chaines en nombres.
    def Format_Purchase_Queue(self):
        amount_credited = 0
        buy_sell_rate = 1
        for i in range(len(self.purchase_queue)):
            self.purchase_queue[i][buy_sell_rate] = float(self.purchase_queue[i][buy_sell_rate].split('"')[1])
            self.purchase_queue[i][amount_credited] = float(self.purchase_queue[i][amount_credited])

    ### Fonction permettant de créer un dicitonnaire contenant la vente total de btc pour chaque année
    def Create_Dict(self):
        for i in range(len(self.sale_queue)):
            if self.sale_queue[i][0] in self.sale_per_year:
                self.sale_per_year[self.sale_queue[i][0]][0] += self.sale_queue[i][1]
                self.sale_per_year[self.sale_queue[i][0]][1] += self.sale_queue[i][2] * self.sale_queue[i][1]
            else:
                self.sale_per_year[self.sale_queue[i][0]] = [self.sale_queue[i][1], self.sale_queue[i][2] * self.sale_queue[i][1]]
        for year in self.sale_per_year:
            self.sale_per_year[year][1] /= self.sale_per_year[year][0]

    ### Affiche dans la console le montant dû à l'impôt
    def Calcul_Tax(self):
        total_to_pay = []
        i = 0
        for year in self.sale_per_year:
            total_to_pay.append([year, 0])
            while self.sale_per_year[year][0] != 0:
                if self.purchase_queue[0][0] > self.sale_per_year[year][0]:
                    total_to_pay[i][1] += (self.sale_per_year[year][0] * (self.sale_per_year[year][1] - self.purchase_queue[0][1]))
                    self.purchase_queue[0][0] -= self.sale_per_year[year][0]
                    self.sale_per_year[year][0] = 0
                else:
                    total_to_pay[i][1] += (self.purchase_queue[0][0] * (self.sale_per_year[year][1] - self.purchase_queue[0][1]))
                    self.sale_per_year[year][0] -= self.purchase_queue.pop(0)[0]
            i += 1
        print(total_to_pay)

x = Shakepay_transactions()

