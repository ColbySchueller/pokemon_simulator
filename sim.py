import random
import os
import time

#Terminal colors
class bcolors:
    HEADER = '\033[0;36m'
    OKBLUE = '\033[0;30m'
    OKCYAN = '\033[96m'
    OKGREEN = '\33[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    TRAINER = '\033[0;34m' #CUSTOM
    ENDING = '\033[0m' #CUSTOM
    WILD = '\033[0;96m' #CUSTOM
    ENDING = '\033[0m' #CUSTOM
    WARNHIGHLIGHT = '\033[0;41m' #CUSTOM

class strcolors:
    player = bcolors.HEADER + "[TRAINER]:" +  bcolors.ENDC
    battle = bcolors.WARNING + "[BATTLE]:" +  bcolors.ENDC
    trainer = bcolors.WARNING + "[BATTLE]" +  bcolors.ENDC + bcolors.HEADER + "[TRAINER]:" +  bcolors.ENDING
    wildpokemon = bcolors.WARNING + "[BATTLE]" +  bcolors.ENDC + bcolors.WILD + "[POKEMON]:" +  bcolors.ENDING
    info = bcolors.OKBLUE + "[INFO]:" +  bcolors.ENDC
    world = bcolors.WARNHIGHLIGHT + "Starting Simulation" +  bcolors.ENDC








#Trainer Class
class trainer:
    type = "Trainer" #class variable

    def __init__(self) -> None:
        self.name = "Jason"
        self.bag = []
        self.pokidex = []
    def addPokemon(self, pokemon):
        if len(self.bag) < 6:
            self.bag.append(pokemon)
            self.uiUpdate()
    def uiUpdate(self):
        bOutputStr = ""
        print(strcolors.info+ " You have {} pokemon in your bag!".format(len(self.bag)))
        for pokemon in self.bag:
            bOutputStr += "\n\t{} | {} | lvl {} | health {}".format(pokemon.name, pokemon.species,pokemon.lvl, pokemon.health, pokemon.exp)

        print(strcolors.info + " Pokemon: {}".format(bOutputStr))

#Pikachu Class
class pikachu:  

    type = "electric"

    def __init__(self) -> None:
        self.species = "Pikachu"
        self.name = ""
        self.health = 100
        self.lvl = 3
        self.exp = 0
        self.skills = {"SCRATCH": 10, "THUNDER JOLT": 20}
        self.isAlive = 1
        self.expIfDefeated = random.random() * 10
        self.levelDif = 3.0
        self.difficulty = int(random.random())
        self.owner = ""
    
    def levelUp(self):
        self.lvl += 1
        print(strcolors.info + " {} gained a level and is now level {}".format(self.name, self.lvl))
        self.levelDif *= 2

    
    def setName(self, name):
        self.name = name
        print(strcolors.info + " {} is now called {}".format(self.species,name))
    
    def addSkill(self, skills):
        for skill in skills.keys():
            self.skills[skill] = skills[skill]
    
    def useRandomSkill(self):
        randomSkill = random.choice(list(self.skills))
        print(strcolors.wildpokemon + " {} used {}.".format(self.species, randomSkill))
        return (randomSkill, self.skills[randomSkill]) #returns skill being used
    
    def useSkill(self, name):
        print(strcolors.battle + " {} used {}.".format(self.species, name))
        return (name, self.skills[name.upper()]) #returns skill being used
    
    def modifyHealth(self, attack):
        if self.health - attack < 0:
            self.isAlive = 0
            self.health = 0
            print(strcolors.battle + " {} was defeated.".format(self.species))
        else:
            self.health -= attack
    
    def addExp(self,exp):
        print(strcolors.info + " Your {} gained {} experience!".format(self.species, exp))
        self.exp += exp
        if(self.exp / self.levelDif > 1):
            for x in range(0, int(self.exp / self.levelDif)):
                self.levelUp()
            self.exp = self.exp % self.levelDif
    def catch(self, owner):
        print(strcolors.info + " {} threw a pokeball at the wild {}".format(owner, self.species))
        time.sleep(2)
        catchRate = int(random.random())
        if (catchRate == self.difficulty):
            self.owner = owner
            return True
        else:
            return False

#Walking in grass simulator
def walking():
    global isInBattle

    randomNum = random.random()
    encounterChance = abs(randomNum - 0.5)
    if encounterChance < 0.05:
        isInBattle = True
    else:
        isInBattle = False

#Battle simulation
def battle(wildPokemon, trainer):
    global isInBattle
    #os.system('cls')

    #Battle Starting
    print(strcolors.battle + " A wild {} has appeared!".format(wildPokemon.species))
    print(strcolors.battle + " You are starting a battle! Get ready!")

    #Players Turn First
    turnFlag = True

    #Battle until either pokemon has 0 health
    while(wildPokemon.health > 0 and trainer.bag[0].health > 0):

        #Trainers Turn
        if (turnFlag and wildPokemon.health > 0 and trainer.bag[0].health > 0):
            choice = battleOptions("default", wildPokemon, trainer) #Trainer Turn
            battleOptions(choice, wildPokemon, trainer)
        
        #Run away from battle
        if (isInBattle == False):
            break

        #Switch Turns
        turnFlag = False
        print(battleMenu["spacer"])
        time.sleep(1)

        #Wild Pokemon Turn
        if (turnFlag == False and wildPokemon.health > 0 and trainer.bag[0].health > 0):
           wildPokemonOptions("attack", wildPokemon, trainer)
        time.sleep(1)
        
        turnFlag = True

    #If wild pokemon's was defeated, add exp to trainers pokemon
    if(wildPokemon.health == 0):
        trainer.bag[0].addExp(wildPokemon.expIfDefeated)
        
        #exit out of battle
        isInBattle = False
    
    print(battleMenu["spacer"])


#Wild Pokemon Behaviour 
def wildPokemonOptions(option, wildPokemon, trainer):
    match option.lower():
        case "attack":
            print(strcolors.wildpokemon + " It is wild {}'s turn".format(wildPokemon.species))

            #Wild Pokemon uses random skill in its skill list
            wpk = wildPokemon.useRandomSkill()
            print(strcolors.wildpokemon + " It wasn't very effective.")

            #Modify trainers health for current pokemon
            trainer.bag[0].modifyHealth(wpk[1])
            print(strcolors.wildpokemon + " Your {} health decreased by {}.".format(trainer.bag[0].species, wpk[1]))

#Trainer Battle Behaviour
def battleOptions(option, wildPokemon, trainer):
    global isInBattle

    #Set Pokemon Battling 
    currentPokemon = trainer.bag[0]

    #Battle Option for Trainer
    match option.lower():
        
        case "default": #First option to appear

            print(battleMenu["spacer"])
            time.sleep(1)
            print(strcolors.trainer + " It's your turn!")
            print(strcolors.trainer + " What will {} do?".format(currentPokemon.species))
            choice = input(battleMenu["menu"])
            return choice
        case "fight": #Return skill list for current pokemon

            #Get Skills from Pokemon
            skills = list(currentPokemon.skills.keys())

            #Pick a skill to use
            choice = input("\n" +strcolors.trainer + " Which ability would you like to use?\n\n\t\t------------------------------\n\t\t|    {}  \t{}  |\n\t\t|    {}\t{}  |\n\t\t------------------------------\n".
                           format(skills[0],skills[1],
                                  skills[2],skills[3] ))
            
            #Use the skill
            wpk = currentPokemon.useSkill(choice)

            #Attack Descriptor
            print(strcolors.trainer + " It wasn't very effective.")

            #Update wild pokemons health after attack
            wildPokemon.modifyHealth(wpk[1])

            #Update UI
            print(strcolors.trainer + " {} health decreased by {}.".format(wildPokemon.species, wpk[1]))

            return choice
        case "bag":
            #Open bag
            choice = input(strcolors.trainer + battleMenu["bag"])

            match choice.lower():
                case "use pokeball":
                    #Call obj.catch() function to catch the pokemon
                    wpk = wildPokemon.catch(trainer.name)

                    #If obj.catch() returns True, the pokemon is caught
                    if(wpk):

                        #Update UI
                        print(strcolors.trainer + " You caught the wild {}!".format(wildPokemon.species)) 
                        time.sleep(1) #Wait
                        print(battleMenu["spacer"]) #Spacer

                        #Name the pokemon after its been caught
                        newName = input(strcolors.trainer + " What would you like to call your {}\n".format(wildPokemon.species))
                        wildPokemon.setName(newName)

                        #Add the pokemon to the trainers bag
                        trainer.addPokemon(wildPokemon)

                        #Update battle flag to False
                        isInBattle = False
                    else:
                        print(strcolors.trainer + " The wild {} escaped!".format(wildPokemon.species)) #Notification

            return choice
        case "pokemon":
            #change pokemon
            return 
        case "run":
            #run
            print(strcolors.trainer + " You ran away...")
            isInBattle = False
            return -1
        case _:
            return -1
        

if __name__ == "__main__":
    print(strcolors.world)
    #Global Variables
    global exitFlag
    exitFlag = True 
    global isInBattle
    isInBattle = False
    contextMenu = {
        "walking": [strcolors.player +  bcolors.ENDC + "walking.", 
                    strcolors.player +  bcolors.ENDC + "walking..", 
                    strcolors.player +  bcolors.ENDC + "walking...", 
                    strcolors.player +  bcolors.ENDC + "walking...."]
    }
    battleMenu = {
        "menu": "\t\t---------------------\n\t\t|    FIGHT  \tBAG  |\n\t\t|    POKEMON\tRUN  |\n\t\t---------------------\n",
        "bag": "\n\t\t---------------------\n\t\t|     USE POKEBALL\tEXIT  |\n\t\t---------------------\n",
        "spacer": "\n----------------\n----------------\n"
        }

    #Creating my trainer
    myTrainer = trainer()

    #Creating my pikachu
    myPikachu = pikachu()

    #Giving my pikachu a name/skills and adding it to my bag
    myPikachu.setName("Pikachus")
    myPikachu.addSkill({"LIGHTNING ROD": 80, "STAB": 40})
    myTrainer.addPokemon(myPikachu)

    
    #Start Simulation
    while(exitFlag):
        print(strcolors.player + "You begin to walk in grass....")

        #Walking in Grass
        ct = 0
        while(isInBattle == False):
            
            print(contextMenu["walking"][ct])
            walking() #Determines if you encounter a pokemon
            ct += 1
            if ct > 3:
                ct = 0
            time.sleep(0.5)
        
        #Start Battle with a Pikachu
        battle(pikachu(), myTrainer)
        time.sleep(5)























        

    
        
            

