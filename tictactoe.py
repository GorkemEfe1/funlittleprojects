import random
arr = [{0,3,6} , {0,1,2} , {0,4,8} , {1,4,7} , {2,4,6} , {2,5,8} , {3,4,5} , {6,7,8}] 
s = []
winX = []
winO = []
inputHandling = ["0","1","2","3","4","5","6","7","8"]
for i in range(9):
    s.append("#")
print(s[0]+s[1]+s[2] + "\n" + s[3]+s[4]+s[5] +"\n" + s[6]+s[7]+s[8])

def userAction(user):
    while (True):
        print("User " + str(user) + " Choose a number between 0 and 8:")
        index = input() 
        if (index in inputHandling):
            if (s[int(index)] == "X" or s[int(index)] == "O" ):
                print("try again")     
            else:
                if (user == 1):
                    string_val = "X"
                    s[int(index)] = string_val
                    winX.append(int(index)) # Number entered
                    break
                if (user == 2):
                    string_val = "O"
                    s[int(index)] = string_val
                    winO.append(int(index)) # Number entered
                    break
        else:
                print("try again")
    return winX, winO
def wincheck(i, arr, winX, winO):
    if (i >= 2):
        for j in range(len(arr)):
            if (arr[j].issubset(set(winX))):
                print("X wins")
                return True
            elif (arr[j].issubset(set(winO))):
                print("O wins")
                return True
def tictactoe(s, arr, winX, winO):
    for i in range(5):
        userAction(1)
        print(s[0]+s[1]+s[2] + "\n" + s[3]+s[4]+s[5] +"\n" + s[6]+s[7]+s[8])
        done = wincheck(i, arr, winX, winO)
        if done:
            return True
        if "#" not in s:
            print("Draw")
            return True
        userAction(2)
        print(s[0]+s[1]+s[2] + "\n" + s[3]+s[4]+s[5] +"\n" + s[6]+s[7]+s[8])
        done = wincheck(i, arr, winX, winO)
        if done:
            return True                    
tictactoe(s, arr, winX, winO) 

# Random ai
# Will act as user 2 and will put an O in a random location
# First we need to generate a random number between 0 and 8
# or make an array including all numbers between 0 and 8 then cross of or simply remove the ones that have been used either by the player or the ai
