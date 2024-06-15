"""
img-to-ascii.py

Images to ASCII.

Author: Álvaro Cordero
    
"""
from os import path
### Functions

# Get the path and check if there are any related files whit it, if so display them
def relatedFiles(userPath: str):
    ''' Print the name of the related to the user's image, if there are any '''
    from difflib import SequenceMatcher  
    from os import listdir
    MIN_SIMILARITY = 5
    
    # Get the name of the file
    userImage = userPath.split("/")[-1]
    # Get the path of the file
    userPath = path.dirname(userPath) + "/"
    
 
    # List of only files
    listFiles = [i for i in listdir(userPath) if path.isfile(userPath + i) and 
                 (i.endswith(".png") or i.endswith(".jpg")) ]

    # Files related to userImage
    relatedFiles = [file for file in listFiles if (int(SequenceMatcher(
                    None, file, userImage).ratio() * 10) >= MIN_SIMILARITY)]


    # Check the number of related files
    if (len(relatedFiles) != 0):
        # If there are one or more results show the related files and path relevant
        print("Did you mean any of these options \u001B[1;34m",relatedFiles,
              "\u001B[0m in path \u001B[1;34m'",userPath,"'\u001B[0m ?", sep="")
    else:
        # If there are no results show a message and path
        print("There are NO related files to name \u001B[1;34m'",userImage,
              "'\u001B[0m in path \u001B[1;34m'",userPath,"'\u001B[0m", sep="")




# Check if the path introduced it's correct
def pathVerificator(userPath: str):
    ''' Change the file name if the file begins and ends with '
    It usually happens when you drop the file to python and not to cmd. '''
    realPathImage: str = userPath
    
    
    # Get the path if it is like "'C:/Users/example'" and it change to "C:/Users/example"
    if (userPath.startswith("'") and userPath.endswith("'")):
        realPathImage = ''.join([userPath[i] for i in range(1, len(userPath)-1)])
        
        
    # If the path doesn't exists 
    if (not path.exists(realPathImage)):
        # But the parent path exists 
        if (path.exists( path.dirname(realPathImage) )):
            # Show the related files if there are any
            relatedFiles(realPathImage)
            
        raise Exception("File doesn't exist")
    
    return realPathImage




# imageToASCII
def imageToASCII(imagePath):
    ''' Giving the path of the image it retruns the ascii art '''
    from PIL import Image
    
    #gscale used by https://www.geeksforgeeks.org/converting-image-ascii-image-python/ 
    gscale = "$#*/\|0{:.-_+~<>;:,.   "
    ascii_Art = ''
    
    print("--  Processing the image  --")
    
    
    # stored image in grayscale as "image"
    with Image.open(imagePath).convert("L") as image:
        
        # Get the width and height of the image
        width, height = image.size[0], image.size[1]
        ratio = height/width
        
        
        # The image could be very taller, so we reduce it down to 125 and 
        # we have to keep the aspect ratio. And then we reduce the heigh 0.5 
        # cause characters are taller than wide
        width = 100
        height = int(width * ratio * 0.5)
        image = image.resize((width, height))
        pixels = image.getdata()


        # Each pixel is exchanged for a character based on the gscale                        
        text_ascii = [gscale[i//len(gscale)] for i in pixels]

        
        # The image must be separated into differents rows
        for pixelNum in range(0, len(text_ascii)):
            ascii_Art += text_ascii[pixelNum]
            if (pixelNum%width == (width-1) ):
                ascii_Art += "\n"
                
                
        # The art ASCII is finally done and we can show and store it
        print(ascii_Art)        
        
        
    return ascii_Art




# Set the name and the content of a file
def outputFile(name: str, text: str):
    from os import path
    
    # We join the name given and the specifier from ascii-art
    fileName= getFilename(name) + "-ascii-art.txt"
    
    with open(fileName, "w") as newFile:
        newFile.write(text)
        print("ASCII art stored in \u001B[1;34m'", path.abspath(newFile.name),
              "'\u001B[0m", sep="")
        newFile.close()




# Get the filename without the extension
def getFilename(path: str):
    # Get the name of the file
    path.split("/")[-1]
    # Get the name without the extension
    return path.split(".")[0]




# Current main function
def main():
    correctPath = True
    print("- Welcome :) !!")    
    userPath = input("- Drop the image here --> ")
    
    
    try:
        userPath = pathVerificator(userPath)
    except Exception as e:
        print("\u001B[1;31m[!]",e,"[!]\u001B[0m  ")
        correctPath = False
    
    
    if (correctPath):
        asciiArt = imageToASCII(userPath)
        
        outputFile(userPath.split("/")[-1], asciiArt)
    
    print("- See you :D !!")




# =============================================================================
# Doesn't execute the main function when imported
if __name__ == "__main__":
    main()


