#citim automatul

import copy

class Automat:

    def __init__(self):

        self.stari = list()
        self.alfabet = list()
        self.matriceTranzitii = list()
        self.stareInit = ""
        self.stariFinale = list()
        self.subsets = dict()

        

    def readAutomat(self, fisier):

        with open(fisier, "r", encoding="utf-8") as fisierautomat:
            self.stari = [x for x in fisierautomat.readline().split()]
            self.alfabet = [x for x in fisierautomat.readline().strip('\n')]

            #initializam matricea de tranzitii
            self.matriceTranzitii = [["" for x in range(len(self.alfabet))] for i in range(len(self.stari))] 
            
            self.aux = fisierautomat.readlines()
            for i in range(len(self.aux) - 2):
                l = [x for x in self.aux[i].strip('\n').split()]

                #verificam daca am facut o greseala de redactare
                if l[0] not in self.stari:
                    raise ValueError(f"Starea {l[0]} nu este definita!")
                if l[2] not in self.stari:
                    raise ValueError(f"Starea {l[2]} nu este definita!")
                if l[1] not in self.alfabet and l[1] != 'λ':
                    raise ValueError(f"Litera {l[1]} nu este definita!")
                

                #print(stari.index(l[0]))
                #print(stari.index(l[2]))

                self.matriceTranzitii[self.stari.index(l[0])][self.alfabet.index(l[1])] = l[2]

            self.stareInit = self.aux[-2].strip('\n')
            self.stariFinale = [x for x in self.aux[-1].split()]
            self.subsets["A0"] = {x for x in self.stari}
            self.subsets["B0"] = {x for x in self.stariFinale}
            #print(self.subsets["A0"])
            for x in self.stariFinale:
                self.subsets["A0"].remove(x)
                

        return
    
    def splitStates(self):
        
        cSubsets = copy.deepcopy(self.subsets)
        nSubsets = dict()
        while cSubsets != nSubsets:
            nSubsets = copy.deepcopy(cSubsets)
            cSubsets = dict() 

            for multime in nSubsets.keys():
                #print(multime)
                for elem in nSubsets[multime]:
                    #print(elem)
                    #print()
                    nMult = ""
                    for tElem in self.matriceTranzitii[self.stari.index(elem)]:
                        #print(tElem)
                        for tMult in nSubsets.keys():
                            if tElem in nSubsets[tMult]:
                                nMult += tMult

                    if nMult not in cSubsets.keys():
                        cSubsets[nMult] = {elem}
                    else:
                        cSubsets[nMult].add(elem)

            #print(cSubsets)
            char = "A0"
            lKeys = [chr(i) + "0" for i in range(ord("A"), ord("A") + len(cSubsets))]
            #print(lKeys)
            cSubsets = dict(zip(lKeys, list(cSubsets.values())))
            print(nSubsets)
            print(cSubsets)

        self.subsets = copy.deepcopy(cSubsets)



        return




        
    #afisam datele dupa citire
    def printData(self):

        print("Stari:")
        print(self.stari)
        print("Alfabet:")
        print(self.alfabet)
        print("Stare initiala:")
        print(self.stareInit)
        print("Stari finale:")
        print(self.stariFinale)
        print("A0:")
        print(self.subsets["A0"])
        print("B0:")
        print(self.subsets["B0"])
        print("Matrice: ")

        for i in self.matriceTranzitii:
            for j in i:
                print(j, end=' ')
            print()

        #print(self.lambdaInchidere)

            
if __name__ == "__main__":
    x = Automat()
    x.readAutomat("automat.txt")
    #x.printData()
    x.splitStates()