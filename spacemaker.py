# The goal is to make a web app that can take a string input and output a correctly spaced string

# 1st iteration 
# Take a string output each character with a space between

print("Enter a sentence:")
spaced_text = input()
# arr = []
# for i in range(len(spaced_text)):
#         arr.append(spaced_text[i])
# print(" ".join(arr))

# 2nd iteration
# So the world longest word in english is 45 characters
# I made an educated guess that the longest average word that is commonly used is around 13 characters so I will divide by that 
# Take a string input insert a space into the spesified location and output the final string
arr = []
for i in range(len(spaced_text)):
        arr.append(spaced_text[i])
for i in range(len(arr)):
        if (i % 13 == 0):
                arr.insert(i," ")
print("".join(arr))