# Student Sorter Script to Divide Students Into Weighted Groups
# Code by Carlos Ortiz
#------------------------------------------------------------
# Description:
'''
The purpose of this code is to parse an excel document full of student names and their respective average quiz scores,
to then generate a set of groupings of students. Groupings are generated randomly, and the final grouping is decided by 
finding the random generated group's average quiz values subtracted from the class's average, then taking the standard
deviation. The set of groupings with the lowest standard deviation is considered to be the best fit because the average
diverges least from the class average from previous iterations.
To manipulate the behavior of this program, fields to change are designated by "### Change as Needed!!!"
These fields include the filename to open (filename, line 27), the name column name (nameColName, line 33)
average column name (avgColName, line 34) in the excel document, the number of people to attempt to put
in each group (pplPerGroup, line 48), and the number of iterations to cycle through (iterCount, line 72).
I recommend running the simulation for at least 100 iterations, but it runs pretty quickly for up to about
10000 iterations, at which point it starts to take a little while with diminishing returns.
For status readouts, you can uncomment lines 134 and 137, which show when the set is replaced.
'''

from pandas import read_excel
from math import ceil
from random import shuffle
from numpy import std
from numpy import array_split

# String to represent filename of interest
filename = 'Data_SAR.xlsx'   ### Change as Needed!!!

# Import dataframe from excel file of interest
df = read_excel(filename)

# Interchange with columns of interest: nameColName = name column name ||| avgColName = average column name
nameColName = 'Name:'   ### Change as Needed!!!
avgColName = 'AVG'      ### Change as Needed!!!  

# Generate lists of the names and averages from the above handles
nameList = [ii for ii in df[nameColName]]
avgList = [ii for ii in df[avgColName]]

# Generate tuples with the names and associated scores
NameAndScore = []
for ii in range(len(nameList)):
    PeopleScoreTuple = (nameList[ii], avgList[ii])
    NameAndScore.append(PeopleScoreTuple)

# Get class size and list properties to find the number of groups needed
totalPpl = len(nameList)
pplPerGroup = 5   ### Change as Needed!!!
numGroups = ceil(totalPpl / pplPerGroup)

# Define a function to pull the average value from any list (will use this a lot)
def GetAvgFromList(List):
    '''
    Returns the average value from a list of numerical values.\n
    Input: [List]\n
    Output: average (float)\n
    '''
    # Add all numbers in the list
    SumList = 0
    for items in List:
        SumList+=items
    # Get a divisor, the length of the list
    num = len(List)
    # Find the average
    average = SumList/num
    return average

#Find average quiz value from the whole class to later compare
classAvg = GetAvgFromList(avgList)

# Determine the number of iterations to run
iterCount = 1000    ### Change as Needed!!!

# Initialize values for iteration
counter = 0
BestGroups = None

# Iteration Cycle:
while counter < iterCount:

    # Randomly arrange list to send through the cycle to generate new combinations of groups
    shuffle(NameAndScore)

    # Split data into groups
    splitGroups = array_split(NameAndScore, numGroups)

    # Make list to store sets of groups: 
    # Sets holds the groups, and 
    # GroupAvgSubtList will hold the group's averages subtracted from the class average to take a standard deviation.
    Sets = []
    GroupAvgSubtList = []

    # Iterate through each individual group out of the split arrays
    for individualGroup in splitGroups:

        # Make list to store each member's ratings from each group to find the group average
        groupRatings = []

        # Iterate through each member of each group to scrub and pull the rating for average
        for members in individualGroup:

            # convert to string to manupulate, then scrub
            members = str(members).split(' ')
            rating = members[1].strip("'")
            # convert to float and finish scrubbing for a numerical result
            rating = float(rating.strip("']"))

            # add each rating to list to find an average value per group of people
            groupRatings.append(rating)

        # Calculate the average quiz value for the group of people
        groupAvg = GetAvgFromList(groupRatings)
        # Convert array to list to store
        individualGroup = individualGroup.tolist()

        # Subtract the average rating from each group from the class average to see how far off it is.
        GroupAvgSubtList.append((groupAvg - classAvg))

        # Create a set of all of the groups
        Sets.append(individualGroup)

    # Standard deviation of subtracted averages from the class avg
    SetStDev = std(GroupAvgSubtList)
    
    # If there is nothing in the best group section, fill it with the first iteration
    if BestGroups is None:
        BestGroups = Sets
        BestStd = SetStDev

    # If the difference in the average class rating and the group rating is less than that of the current best, replace the current best value
    if SetStDev < BestStd: 
        BestGroups = Sets
        BestStd = SetStDev
        #print("Best Group Replaced...")
    else:
        # ...Otherwise, the best group stays the same
        #print("Still the Best Group...")
        pass
    
    #Iterate counter forward
    counter += 1

    if counter == iterCount:
        # Once finished cycling, print out end message! (unnecessary for function, but pretty if you uncomment status messages lines 134 & 137)
        print("\nDone iterating!\n")

# Display end results:
print("The best groups, with a set standard deviation of " + str(BestStd) +" are:\n")
# Pull only name data from (name, value) pairs
for NamesAndValues in BestGroups:
    FinalAvgList = []
    for pieces in NamesAndValues:
        # Display the names in the groups
        print(pieces[0])
        # Append the values per name to get an average
        FinalAvgList.append(float(pieces[1]))
    FinalAvg = GetAvgFromList(FinalAvgList)
    print("\nThis group's average score:", FinalAvg)
    print("--------------------------------------")
    print('\n')

