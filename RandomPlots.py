'''
RandomPlots.py v.1.0
Python version 3.6 (works at least with Python 3.4)
Author: Arto Vesterbacka

Description:
Generates user specified number of csv-files containing randomly picked plants for sampling.
Contains a basic, terminal based user interface.

ToDo:
1. Checking for duplicate selections in one plot/treatment, redrawing when duplicate is found. DONE!
2. Randomly selecting beans in plots with beans. DONE!
3. Comment everything
4. Make code look pretty
5. Make options easily changable. DONE! Partly

Long term:
1. GUI?
2. Output as map image?
'''
from random import randrange as rnd
import random
import csv

'''
dArray

Description:
Initializes the array for checking if a plant has already been selected.

toDo:
1. needs to account for different configurations. Currently does only 12x12 and 18x18 (for beans) DONE!
2. Might not need the if-else
'''

def dArray(Rows, Cols,isBean=False):
    if(isBean == True):
        beanArray = [[]]
        for i in range(Rows[1]+1):
            for a in range(Rows[1]+1):
                beanArray[i].append([])
                beanArray[i][a] = False
            beanArray.append([])
        return beanArray
    else:
        dupArray = [[]]
        for i in range(Rows[1]+1):
            for a in range(Cols[1]+1):
                dupArray[i].append([])
                dupArray[i][a] = False
            dupArray.append([])
        return dupArray

'''
toDict(plants, row, column, i)

Desription:
Places the selected plant into a dictionary.

toDo:

'''
def toDict(plants, row, column, i):
    plants['plant' + str(i+1)] = str(i+1)
    plants['plant' + str(i+1)] = {}
    plants['plant' + str(i+1)]['row'] = row
    plants['plant' + str(i+1)]['column'] = column
    return plants

'''
selectPlantsIn(plot, numPlants)

Description:
Randomly selects specified number of plants from the inside of the plot/treatment

toDo:
1. needs to account for different number of plots/treatments per replicate. Currently does only 5 with a specified
   configuration. DONE!?
2. needs to account for different number of plants for each row and column. Currently does only 12x12 configuration. DONE!
'''
def selectPlantsIn(plot, numPlants, innerRows, innerCols, beanPlots, beanCols):
    duplicateArray = dArray(innerRows, innerCols)
    plants = {}
    if plot not in beanPlots:
        for i in range(numPlants):
            first = True
            duplicate = True
            while(first == True or duplicate == True):
                row  = rnd(innerRows[0], innerRows[1])
                column = rnd(innerCols[0], innerCols[1])
                if(duplicateArray[row-1][column-1] == False):
                    plants.update(toDict(plants, row, column, i))
                    duplicateArray[row-1][column-1] = True
                    duplicate = False
                first = False
        return plants
    elif plot in beanPlots:
        for i in range(numPlants):
            first = True
            duplicate = True
            while(first == True or duplicate == True):
                cols = [x for x in range(innerCols[0], innerCols[1]) if x not in beanCols]
                row = rnd(innerRows[0], innerRows[1])
                column = random.choice(cols)
                if(duplicateArray[row-1][column-1] == False):
                    plants.update(toDict(plants, row, column, i))
                    duplicateArray[row-1][column-1] = True
                    duplicate = False
                first = False
        return plants

'''
selectPlantsOut(plot, numPlants)

Description:
Randomly selects plants from the outside circle of a plot/treatment.

toDo:
1. needs to account for different number of plots/treatments per replicate/block. Currently does only 5 with the specified
   configuration. DONE!
2. needs to account for different number of plants per row and column. Currently does only 12x12. DONE!
'''
def selectPlantsOut(plot, numPlants, outerPlants, plotsWithBroc, plotsWithBrocBar):
    plants = {}
    place = list(range(1, outerPlants))
    if plot not in plotsWithBroc and plot not in plotsWithBrocBar:
        for i in range(numPlants): #tämän koodia voi ehkä vielä parantaa siirtämällä tämä looppi omaan funktioon
            num = random.choice(place)
            plants['cabbage_' + str(i+1)] = num
            place.remove(num)
        return plants
    elif plot in plotsWithBroc:
        for i in range(numPlants):
            num = random.choice(place)
            plants['broccoli_' + str(i+1)] = num
            place.remove(num)
        return plants
    elif plot in plotsWithBrocBar:
        place_broc = list(range(1, int(outerPlants/2), 2))
        place_bar = list(range(2, int(outerPlants/2), 2))
        for i in range(numPlants):
            num = random.choice(place_broc)
            plants['broccoli_' + str(i+1)] = num
            place_broc.remove(num)
        for i in range(numPlants):
            num = random.choice(place_bar)
            plants['barbarea_' + str(i+1)] = num
            place_bar.remove(num)
        return plants

'''
selectBeans(plot

Description:
Randomly selects 4 beans from plots with beans.

toDo:
1. needs to count for changes in configuration and number of beans to be sampled. Currently does only 4 beans from 2 rows
   of beans. DONE!
'''
def selectBeans(plot, numberBeans, beanRows, beanCols):
    duplicates = dArray(beanRows, beanCols, True)
    plants = {}
    for i in range(numberBeans): #Selection of the beans
        first = True
        duplicate = True
        while(first == True or duplicate == True):
            cols = [beanCols[0], beanCols[1]]
            row = rnd(beanRows[0], beanRows[1])
            column = random.choice(cols)
            if(duplicates[row-1][column-1] == False):
                plants.update(toDict(plants, row, column, i))
                duplicates[row-1][column-1] = True
                duplicate = False
            first = False
    return plants
'''
writeCsv(plantsIn, plantsOut, ite)

Description:
Writes one CSV-file for each replicate/block.

toDo:
1. make the CSV-files a bit prettier.
2. Possibly make one CSV-file with all the replicates.
'''

def writeCsv(plantsIn, plantsOut, plantsBeans, ite):
    with open('replicate_' + str(ite) + '.csv', 'w', newline='') as csvfile:
        plotwriter = csv.writer(csvfile, delimiter = ";")
        plotwriter.writerow(["Replicate " + str(ite)])
        for plot in plantsIn:
            plotwriter.writerow([plot, "Inside"])
            plotwriter.writerow(['Plant', 'Row', 'Column'])
            for plant in plantsIn[plot]:
                row = str(plantsIn[plot][plant]['row'])
                column = str(plantsIn[plot][plant]['column'])
                plotwriter.writerow(['Cabbage' , row, column])
        for plot in plantsBeans:
            plotwriter.writerow([plot, "beans"])
            plotwriter.writerow(['Plant', 'Row', 'Column'])
            for plant in plantsBeans[plot]:
                row = str(plantsBeans[plot][plant]['row'])
                column = str(plantsBeans[plot][plant]['column'])
                plotwriter.writerow(['Bean', row, column])
        for plot in plantsOut:
            plotwriter.writerow([plot, "Outside"])
            for plant in plantsOut[plot]:
                plotwriter.writerow([plant, plantsOut[plot][plant]])


'''
RandomPlots

Description:
A random number generator to randomly pick plants from plots/treatments to be sampled.

toDo:
1. Make this a stand-alone application.
'''


'''
Variables

Change these to accomodate your field study parameters

toDo:
1. add variables for configuring the size of the plots (# of rows and columns). Change some variables to automatically calculate
   the number of plants.
'''
defaultPlants = 5          #number of plants to be selected randomly from each plot/treatment
defaultPlots = 5           #number of plots/treatments in each replicate/block. Currently changing this will break the program!
defaultReplicates = 5      #number of replicates/blocks
innerPlantRows = [2, 11]   #Indexes for the inner plants, rows
innerPlantCols = [2, 11]   #Indexes for the inner plants, columns
outerPlants = 44           #Number of outer plants
numberBeans = 4            #Number of beans to be selected
beanCols = [4, 9]          #rows of beans
beanRows = [2, 17]         #columns of beans
beanPlots = [4, 5]         #indexes of the plots where beans
plotsWithBroc = [2, 4]     #indexes of the plots where only broc
plotsWithBrocBar = [3, 5]  #indexes of the plots where broc and bar

ans = input("Do you wish to generate " + str(defaultReplicates) + " replicates? (y/n): ")
#ans = "y" #testiä varten, muuta, kun valmis!!!!
if ans == "y":
    for i in range(defaultReplicates):
        ite = i+1
        plantsIn = {}
        plantsOut = {}
        plantsBeans = {}
        for n in range(defaultPlots):
            plantsIn['plot' + str(n+1)] = n+1
            plantsIn['plot' + str(n+1)] = selectPlantsIn(n+1, defaultPlants, innerPlantRows, innerPlantCols,
                beanPlots, beanCols)
            plantsOut['plot' + str(n+1)] = n+1
            plantsOut['plot' + str(n+1)] = selectPlantsOut(n+1, defaultPlants, outerPlants, plotsWithBroc, plotsWithBrocBar)
            if n+1 in beanPlots:
                plantsBeans['plot' + str(n+1)] = selectBeans(n+1, numberBeans, beanRows, beanCols)
        writeCsv(plantsIn, plantsOut, plantsBeans, ite)
elif ans == "n":
    rep = int(input("How many replicates do you wish to generate? "))
    if rep == 1:
        num = int(input("Which replicate do you wish to generate? "))
        plantsIn = {}
        plantsOut = {}
        plantsBeans = {}
        for n in range(defaultPlots):
            plantsIn['plot' + str(n+1)] = n+1
            plantsIn['plot' + str(n+1)] = selectPlantsIn(n+1, defaultPlants, innerPlantRows, innerPlantCols,
                beanPlots, beanCols)
            plantsOut['plot' + str(n+1)] = n+1
            plantsOut['plot' + str(n+1)] = selectPlantsOut(n+1, defaultPlants, outerPlants, plotsWithBroc, plotsWithBrocBar)
            if n+1 in beanPlots:
                plantsBeans['plot' + str(n+1)] = selectBeans(n+1, numberBeans, beanRows, beanCols)
        writeCsv(plantsIn, plantsOut, plantsBeans, num)
    elif rep > 1:
        for i in range(int(rep)):
            ite = i+1
            plantsIn = {}
            plantsOut = {}
            plantsBeans = {}
            for n in range(defaultPlots):
                plantsIn['plot' + str(n+1)] = n+1
                plantsIn['plot' + str(n+1)] = selectPlantsIn(n+1, defaultPlants, innerPlantRows, innerPlantCols,
                    beanPlots, beanCols)
                plantsOut['plot' + str(n+1)] = n+1
                plantsOut['plot' + str(n+1)] = selectPlantsOut(n+1, defaultPlants, outerPlants,
                    plotsWithBroc, plotsWithBrocBar)
                if n+1 in beanPlots:
                    plantsBeans['plot' + str(n+1)] = selectBeans(n+1, numberBeans, beanRows, beanCols)
            writeCsv(plantsIn, plantsOut, plantsBeans, ite)
else:
    print("Goodbye!")