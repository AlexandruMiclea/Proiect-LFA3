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
            
            stariBune = [self.stareInit]
            cStariBune = list()
            while stariBune != cStariBune:
                for el in stariBune:
                    for i in range(len(self.alfabet)):
                        if self.matriceTranzitii[self.stari.index(el)][i] != "":
                            if self.matriceTranzitii[self.stari.index(el)][i] not in stariBune:
                                stariBune.append(self.matriceTranzitii[self.stari.index(el)][i])
                cStariBune = stariBune

            cMatriceTranzitii = [["" for x in range(len(self.alfabet))] for i in range(len(stariBune))]
            for i in range(len(stariBune)):
                cMatriceTranzitii[i] = copy.deepcopy(self.matriceTranzitii[self.stari.index(stariBune[i])])
            self.matriceTranzitii = copy.deepcopy(cMatriceTranzitii)
            self.stari = copy.deepcopy(stariBune)


        return
            

    
    def firstSubset(self):
        self.subsets["A0"] = {x for x in self.stari}
        self.subsets["B0"] = {x for x in self.stariFinale}
        #print(self.subsets["A0"])
        for x in self.stariFinale:
            self.subsets["A0"].remove(x)

    def splitStates(self):

        self.firstSubset()
        
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
            

        self.subsets = copy.deepcopy(cSubsets)

        cStari = [x for x in self.subsets.keys()]
        
        cStareInit = ""
        for mult in self.subsets.keys():
            if self.stareInit in self.subsets[mult]:
                cStareInit = mult
        
        cMatriceTranzitii = [["" for x in range(len(self.alfabet))] for i in range(len(cStari))] 

        for stare in cStari:
            nod = list(self.subsets[stare])[0]
            for i in range(len(self.matriceTranzitii[self.stari.index(nod)])):
                for mult in self.subsets.keys():
                    if self.matriceTranzitii[self.stari.index(nod)][i] in self.subsets[mult]:
                        cMatriceTranzitii[cStari.index(stare)][i] = mult

        cStariFinale = list()

        for elem in self.stariFinale:
            for mult in self.subsets.keys():
                if elem in self.subsets[mult]:
                    if mult not in cStariFinale:
                        cStariFinale.append(mult)
        self.stari = copy.deepcopy(cStari)
        self.stariFinale = copy.deepcopy(cStariFinale)
        self.matriceTranzitii = copy.deepcopy(cMatriceTranzitii)
        self.stareInit = copy.deepcopy(cStareInit)

        return
    
    #afisam datele dupa citire
    def printData(self, fisier=""):

        print("Stari:")
        print(*self.stari)
        print("Alfabet:")
        print("".join(x for x in self.alfabet))
        print("Tranzitii: ")
        for i in range(len(self.stari)):
             for j in range(len(self.alfabet)):
                 if self.matriceTranzitii[i][j] != "":
                     print(self.stari[i] + " " + self.alfabet[j] + " " + self.matriceTranzitii[i][j])
        print("Stare initiala:")
        print(self.stareInit)
        print("Stari finale:")
        print("".join(x for x in self.stariFinale))

        if (fisier != ""):
            with open(fisier, "w") as output:
                output.write(" ".join(self.stari) + "\n")
                output.write("".join(self.alfabet) + "\n")

                for i in range(len(self.stari)):
                    for j in range(len(self.alfabet)):
                        if self.matriceTranzitii[i][j] != "":
                            output.write("".join(self.stari[i]) + " ")
                            output.write(self.alfabet[j] + " ")
                            output.write("".join(self.matriceTranzitii[i][j]) + '\n')
                output.write("".join(self.stareInit) + '\n')
                for i in range(len(self.stariFinale)):
                    output.write("".join(self.stariFinale) + " ")


        #print(self.lambdaInchidere)

            
if __name__ == "__main__":
    x = Automat()
    x.readAutomat("automat.txt")
    #x.printData()
    x.splitStates()
    x.printData("minDFA.txt")