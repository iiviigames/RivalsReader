#   FILE:       rivals_reader.py
#   AUTHOR:     iivii   |   @odd_codes
#   EMAIL:      iiviigames@pm.me
#   WEBSITE:    https://odd.codes
#   GITHUB:     https://github.com/iiviigames/RivalsReader
#   DATE:       07/30/2020
#   INFO:       This script is meant to help with quickly identifying characters
#               and other resources in the %APPDATA%\..\Local\RivalsOfAether
#               folder. It produces a list matching each ID number with the
#               character/resource's name.
#   ============================================================================
'''
Rivals Reader is a helper to more easily visualize and get information about the
workshop content you are currently subscribed to, and have stored on your PC.

NOTE:   Leave the initialize() function intact to help ensure functionality!

USAGE:

    EXAMPLE 1 - Print the ID's of the items in the Rivals Workshop folder:
    --------------------------------------------------------------------------
    #   Print the contents of the Rivals Workshop folder
    workshop = list_workshop_items()
    list_print(workshopfolders)


    EXAMPLE 2 - Print the names of all items as listed in their config.ini:
    --------------------------------------------------------------------------
    #   Obtain the folder list
    workshop = list_workshop_items()
    #   Loop through the config files in each folder, seeking their 'name' key.
    namelist = iterate_folders(workshop,'name')
    #   Print the list of names obtained in console.
    list_print(namelist)

    
    EXAMPLE 3 - Log all the name keys obtained from the config to a .txt file:
    --------------------------------------------------------------------------
    #   Obtain the folder list
    workshop = list_workshop_items()
    #   Loop through the config files in each folder, seeking their 'name' key.
    namelist = iterate_folders(workshop,'name')
    #   Write the the names to a file.
    #   write_to_file(namelist, 'roa_names.txt',"C:/Users/{YourName}/Desktop")



    EXAMPLE 4 - Obtain multiple keys' data at once, and pretty print as a table:
    --------------------------------------------------------------------------
    #   Define a list containing the keys you want information for
    query = ['url','name', 'type']
    
    #   Define a Table
    table = Table(show_header=True,header_style="bold magenta")

    #   Define the Table's Columns
    table.add_column("Asset ID", style="dim", width = 12)
    table.add_column("Asset Name",width=24)
    table.add_column("Asset Type",justify="left",width=16)

    #   Obtain the folder list
    workshop = list_workshop_items()
    #   Loop through the data for each key listed
    keydata = get_key_data(workshop,query)
    #   Parse the retrieved data for terminal output
    rowcontent = parse_key_data(keydata)
    #   Populate the table with the data obtained
    populate_rows(rowcontent)
    
    #   Print the Table in the Terminal
    console.print(table)

'''

#                                                                        IMPORTS
#   ============================================================================

#   Requirements
from rich.console import Console
from rich.table import Column, Table
import psutil

#   Builtins
import os,sys,platform
from datetime import datetime

#   Library Shorthands
plat = platform.uname()

#   Rich Terminal
# Console
console = Console()

# Table
table = Table(show_header=True,header_style="bold magenta")

# Columns
table.add_column("Asset ID", style="dim", width = 12)
table.add_column("Asset Name",width=24)
table.add_column("Asset Type",justify="left",width=16)

# Example Row
# table.add_row("[green]"+str(1865940669)+"[/green]", "Sandbert", "[yellow]Character[/yellow]")
    

#                                                                        GLOBALS
#   ============================================================================

# System Variables
#   Valid Operating System Names
VALIDOS = {
    "Windows": "%APPDATA%//..//Local//RivalsofAether//workshop"
}
#   Operating System Simple Name
SYSOS = plat.system

#   Rivals Stuff
#   ----------------------------------------------------------------------------

# App Number
STEAMID = "383980"
# Config file
CFG = 'config.ini'

# Rivals of Aether folders
STEAMCOMMON = "C:/Program Files (x86)/Steam/steamapps/workshop/content"+STEAMID
STEAMCUSTOM = "E:/SteamLibrary/steamapps/workshop/content/383980"
CHARFOLDER  = "%APPDATA%/../Local/RivalsofAether//workshop"
STAGEFOLDER = "%APPDATA%/../Local/RivalsofAether//stages"
# Valid workshop folder
VALIDATED = ''

# Initializing Folder Check Macros
SteamCheck = 999


# Rivals of Aether config.ini data
ROACHAR = {'character': 0}
['character','buddy','stage'] # char=0,bud=1,stg=2


#                                                                      FUNCTIONS
#   ============================================================================

#   Returns a validation operation
def validate(path,ftype='any',ext=None):
    """
Runs 1 of 3 functions to determine if the [name] item exists on the system.

[path] should be a file or directoy.
[ftype] can be 'file','dir', 'end', or 'any' Defaults to 'any'
[ext] is only used with the 'end' operation, and checks the end of [path]
    against the [ext] argument
    
Here are the operations that can be performed:

    file=======> Checks if the path is specifically a file.
    directory==> Checks if the path is specfically a directory.
    exists=====> Checks if the path exists at all without consideration of type.
    
    """
    #   Return values
    ret = ''
    pend = ''
    
    #   Format the ftype argument
    ftype = ftype.lower()
    ftype = ftype[0]

    #   Ending path operation
    if ftype == 'e':
        if ext is None:
            return
        elif type(ext) == 'int':
            #   If ext isn't negative, make it so
            if ext > 0:
                ext = ext * -1
            pend = path[ext:]
            return pend == STEAMID

            
    
    #   Perform the proper operation and store it
    if ftype == 'f':
        ret = os.path.isfile(path)
    elif ftype == 'd':
        ret = os.path.isdir(path)
    elif ftype == 'a':
        ret = os.path.exists(path)
    else:
        ret = os.path.exists(path)

    return ret


#   Initializer function
def initialize(dbg=False):
    """
Performs the special setup function SteamCheck, which validates and ensures the
user is in a valid Rivals of Aether workshop content folder.
    """
    #   Boolean storing the results of the initialization check
    steamvalid = special_operation(SteamCheck)
    #   Move to the validated folder
    folder_switch(VALIDATED)

    #   Logs some information to console.
    if dbg:
        print("System OS:    " +SYSOS)
        print("Steam Folder: " + str(steamvalid))
        print("Valid Path:   " + str(VALIDATED)+'\n')

    return
    

#   Performs predefined initializing functions
def special_operation(special=None):
    """
Performs predefined initializing functions.

[special] is a defined operation that performs some set of instructions.

IMPLEMENTED:
    SteamCheck:    Checks for the STEAMCOMMON and STEAMCUSTOM folders
    """ 
    
    ret = ''
    custombool = False
    global VALIDATED
    
    #   Steam Common Check
    if special == SteamCheck1:
        #   Check the common folder
        ret = validate(STEAMCOMMON)
        if ret:
            #   Found the common workshop location, return
            print('Found Steam Common Folder!')
            VALIDATED = STEAMCOMMON
            return ret
        
        else:
            #   Check if the STEAMCUSTOM folder has been defined
            if STEAMCUSTOM != "":
                #   Seek that folder
                ret = validate(STEAMCUSTOM)
                #   If a valid custom folder is predefined, return
                if not ret:
                    print('Invalid cutom folder defined.')
                    yn = input('Would you like to enter a custom destination now? [y/n]\n::: ')
                    if not 'y' in yn.lower():
                        print('Exiting...')
                        raise(sys.exit())
                    else:
                        custombool = True
                else:
                    VALIDATED = STEAMCUSTOM
                    return ret
            #   Ask user for input if no custom was set or they responded 'y'
            if STEAMCUSTOM == '' or custombool:
                print("\nUnable to locate the normal Steam folder")
                print("A custom Steam folder hasn't been provided\n")
                response = input("Enter the location of the ROA content\n::: ")
                # Make sure the parent folder ends in STEAMID
                if len(response) < 6:
                    return false
                else:
                    #idstring = response[-6:]
                    #if idstring != STEAMID:
                    if not validate(response,'end',6):
                        print('\nInvalid folder entered!')
                        print('Folder should end in the ROA app ID!')
                        print('Exiting...')
                        raise(sys.exit())
                    else:
                        #   Check if the folder exists
                        ret = validate(response)
                        #   Show that the folder ends with the right string
                        if ret:
                            print('Valid folder with correct Steam App ID located!')
                            VALIDATED = reponse
                        else:
                            print('Invalid folder. Incorrect Steam App ID.\nExiting...')
                            raise(sys.exit())
                        #   If it's not found exit
                        return ret
                    
    else:
        return 'ass'


#   Navigates to different folders
def folder_switch(folder):
    """
Moves from the current directory into [folder] to perform new operations
    """
    os.chdir(folder)


#   Performs the listing operating dependent on the operating system
def list_workshop_items():
    """
Returns a list of folder names from the Steam folder containing Rivals content.
    """
    # Ensure we are in the valid path
    if os.curdir == VALIDATED:
        print('Must be in the validated path!')
        return
    workshoplist = os.listdir(os.curdir)
    return workshoplist


#   Iterates through list of folders and gets the desired data from config.ini
def iterate_folders(workshop,operation='name'):
    """
Iterates through all folders in the ROA workshop folder.
[workshop] indicates the list of folders obtained previously
[operation] should be the KEY you are looking for at the start of each line

EXAMPLES:
    names = iterate_folders(workshoplist, 'name')

VALID KEYS:
    CHARACTERS:
        name, description, author, type, url, info1, info2, info3,
        finished, version, minor version, major version, plural
    STAGES:
        ...
    BUDDIES:
        ...
    """
    #   Key Name and Length of String
    key = operation
    klen = len(key)
    
    #   Return item
    final = []
    
    #   Loop through each folder
    for folder in range(len(workshop)):
        #   Getting key and content
        current = workshop[folder]
        lc = 0
        #   Debugs
        #print('-'*80)
        #print('\nFolder #: ' + current)
        
        #   Move to current folder
        folder_switch(current)
        #   Open the config.ini item
        conf = open(CFG, 'r')
        #   Loop through lines
        while True:
            #   Line counter
            lc +=1
            #   Read next line
            line = conf.readline()
            
            #   Blank line check
            if not line:
                break
            
            #   Name indexes
            n1,n2,name= 0,None,''
            #   Find the index of first '=' sign
            e = line.find('=')
            #   Set the second name index
            n2 = e
            #   Assign the name of the data
            name = line[n1:n2]
            #print(name)
            #   Check if name matches the string "name"
            if name == key:
                #   Data indexes
                d1,d2,data = None,None,''
                #   Find first '"' char,add 1 to get first data index
                d1 = line.find('"')+1
                #   Find last '"' char, sub 1 to get last data index
                d2 = line.rindex('"')

                #   Store the relevant data in content variable
                content = line[d1:d2]

                #   If the key is 'type', add the abbreviation for the type
                if key == 'type':
                    if content == '0':
                        content += ' (Character)'
                    elif content == '1':
                        content += '(Buddy)'
                    elif content == '2':
                        content += '(Stage)'
                    else:
                        content = content
                        
                #   Found match debug
                #print('MATCH: ' + content)
                
                #   Append the content to the final_list                
                final.append(content)
            else:
                continue
                
        #   Close the file
        conf.close()
        #   Move back a directory
        folder_switch(VALIDATED)

    #   Return the final content
    return final


#   Takes a list of key names to call the iterate_folders() function on
def get_key_data(folder, keys):
    """
Performs a query in the config.ini files for each key given.

[folder] is the workshop folder containing all the character/stage folders
[keys] should be a list of strings containing valid key names.

VALID KEYS:
    CHARACTERS:
        name, description, author, type, url, info1, info2, info3,
        finished, version, minor version, major version, plural
    STAGES:
        ...
    BUDDIES:
    """
    keydata = dict()
    for i in range(len(keys)):
        key = keys[i]
        data = iterate_folders(folder, key)
        keydata[key] = data

    return keydata


#   Writes a file containing a list
def write_to_file(items,fname,path=os.getcwd()):
    """
Creates a new file in a given path containing a list of data retrieved from
the config.txt files!
    """
    #   Moved dirs boolean
    moved = False
    #   Validate path
    if not validate(path, 'dir'):
        print('Invalid path given.')
        return
    
    #   Store current dir
    cwd = os.getcwd()
    
    #   Move to desired dir
    if cwd != path:
        moved = True
        folder_switch(path)

    #   Create the file in directory
    outfile = open(fname,'w')
    
    #   Write each line to the file
    for line in items:
        #   Create the line and break
        outfile.write(line)
        outfile.write('\n')

    #   Close the file.
    outfile.close()
    #   Notify user of file and location
    console.print('New file ' + fname + ' created in:\t ' + path + ' !')
    #   If directory changed, switch back to original
    if moved:
        folder_switch(cwd)
    #   Done!
    return


            
#   Logs the contents of a folder
def list_print(fold):
    """
Debugging function to log the content of a list on new lines within the console.
    """
    for i in range(len(fold)):
        console.print(fold[i])


#   Logs a dictionaries contents
def dict_print(data):
    """
Uses rich console to print out the keys retrieved from Rivals Workshop Data.
    """
    for key in data.keys():
        console.print(data[key])


#   Performs individual operations on lists within a dict
def parse_key_data(data):
    """
Converts the dict returned by retrieve_data_keys() into individual lists
which can then be added into the output table with the function populate_rows()
    """
    final=[]
    rows=[]
    #   Add a list for each key entry
    for key in data.keys():
        final.append([])

    # Total loops
    lc = -1
    
    #   Loop through each key entry list
    for key in data.keys():
        lc += 1
        lst = data[key]
        name = key

        #  Add rows until their number is equal to list size
        while len(lst) > len(rows):
            #   Checks if rows needs more entries
            if len(rows) < len(lst):
                rows.append([])
            else:
                break
            

            
        #   Loop through the current list's data
        for i in range(len(lst)):
            #   Create/get the next row in the rows list
            entry = lst[i]
            rows[i].append(entry)

    #   Return the row data
    return rows


#   Adds rows for parsed data
def populate_rows(rows):
    """
Needs to be customized based on the number of columns defined at the top
of the code. If you want more, they must be coded in by hand, as I'm not
rewriting this to work with dicts, but you can!!!

FULL EXAMPLE:
    workshop = list_workshop_items()
    querykeys = ['name', 'author', 'url']
    keydata = get_key_data(workshop, querykeys)
    rowcontent = parse_key_data(keydata)
    console.print(table)

    """
    #   Add each list to the table
    #   NOTE: ONLY WORKS WITH 3 ENTRIES EXACTLY
    for i in range(len(rows)):
        row = rows[i]
        #console.print(row)
        #console.print(len(row))
        if len(row) == 3:
            a = "[red]"+str(row[0])+"[/red]"
            b = "[green]"+str(row[1])+"[/green]"
            c = "[yellow]"+str(row[2])+"[/yellow]"
            table.add_row(a,b,c)
        
        

#                                                                           MAIN
#   ============================================================================

#   Currently reproduces the content of EXAMPLE 4
if __name__ == "__main__":


    #   Print the contents of the folder
    workshop = list_workshop_items()
    #   list_print(workshopfolders)

    #   Get data for each key listed
    query = ['url','name', 'type']
    keydata = get_key_data(workshop,query)

    #   Parse the retrieved data for terminal output
    rowcontent = parse_key_data(keydata)

    #   Populate the table with the data obtained
    populate_rows(rowcontent)
    
    #   Table Print
    console.print(table)


    #   Print the keydata
    #   dict_print(keydata)
    
    #   Loop through the names of config files
    #   namelist = iterate_folders(workshop,'name')
    
    #   Print the list of names obtained
    #   list_print(namelist)
    #   print('\n')

    #   Write the the names to a file.
    #   write_to_file(namelist, 'roa_names.txt')

    #   Exit
    raise(sys.exit())


#   ===========================================================================
#                                   NOT BEING USED
#   ===========================================================================

#   Adds rows to the console table
"""
def add_rows(keys,data):
    '''
Adds rows to the console table
    '''
    rows = []
    #   Create a template for each item
    template = dict()
    for i in range(len(keys)):
        key = keys[i]
        template[key] = None

    #   Data size and create a row for each
    size = len(data[1])
    for i in range(size):
        rows.append([])
  
    #   Loop through data and add to a row
    for i in range(len(data)):
        #   Get inner data list
        current = data[i]
        #   Set matching key name
        key = keys[i]
        #   Loop through the inner list (ie; names, authors)
        for j in range(len(current)):
            #   Get the row from the rows dict
            row = rows[j]
            #   Store the current data list's content in that key
            row[key] = current[j]

    #   All rows populated, so go through the row list and add each item toa row
    #   Loop through keylist and add the row
"""    
        
