Rivals of Aether Workshop Reader and Helper
==========================================

**Rivals Reader** is a Python script I wrote to day that helps you obtain data about the [Steam Workshop](https://steamcommunity.com/app/383980/workshop/) content you currently have downloaded on your PC.

![](img/rivals_reader_table_example.gif)

If you are a creator of content, then you likely enjoy poking around through other users Characters and Stages to have a look under the hood.
If you decide you want to edit this content on the fly, then you also have to create copies of everything in your `%APPDATA%` folder, as this is where the game is checking for local content. _(See the [official documentation](https://rivalsofaether.com/introduction/) for more detailed info on this and everything else!)_


It can do many things, pretty print data to console, get a single list of key's from the `config.ini` files, get numerous key's data at once, create files containing that data for ease of use (that's what I made this for this morning), and some other cool stuff. 

I may write or add more info about this program, as well as expand its functionality a bit later on. I started this around 12pm, and its 7pm now, so I'm happy with what it can do for the moment! 

I hope it helps somebody! 


## How to Use

1) Ensure [Python 3](https://python.org) is installed.
2) Clone the git, or download it as a zip.
   - _OPTIONAL_: Put a copy of `rivals_reader.py` in your User `site-packages` folder. This allows you to call it from anywhere.
   - Usually located in: `%APPDATA%Python/Python38/site-packages`
3) Move to the folder you cloned or extracted, and open a terminal window there. (<kbd>Right Click</kbd>+<kbd>Open Terminal Window</kbd>)
4) Run this command:
  - `pip3 install -r requirements.txt`
  - This will have pip (_The Python Package Manager_) install the extra packages the script needs to run.
5) That's all! Edit the script to your heart's content, and hopefully it is of use to you.

## Usage Notes

The script will search for the most common Steam location by default, which is stored in the Global Variable `STEAMCOMMON`. You can, however, premptively set your own Steam folder if you have more than one by changing the `STEAMCUSTOM` variable to wherever your folder is.

If you decide not to do this, however, I added some rudimentary interactivity for the terminal so you can type it in on the fly.

All functions have some basic information on how they are used, with arguments described, and lots of comments throughout the code.

Usage Examples
--------------

These are also included in the `.py` file in the git.

### Example 1

_Printing the Rivals Workshop Folder as a list in console._
```python
    #   Print the contents of the Rivals Workshop folder
    workshop = list_workshop_items()
    list_print(workshopfolders)
```

### Example 2

_Printing the Names of Items from Rivals Workshop Folder, retrieved from their config file._
```python
    #   Obtain the folder list
    workshop = list_workshop_items()
    #   Loop through the config files in each folder, seeking their 'name' key.
    namelist = iterate_folders(workshop,'name')
    #   Print the list of names obtained in console.
    list_print(namelist)
```

### EXAMPLE 3

_Log all the name keys obtained from the config to a .txt file._
```python
    #   Obtain the folder list
    workshop = list_workshop_items()
    #   Loop through the config files in each folder, seeking their 'name' key.
    namelist = iterate_folders(workshop,'name')
    #   Write the the names to a file.
    write_to_file(namelist, 'roa_names.txt',"C:/Users/{YourName}/Desktop")
```

###EXAMPLE 4
_Obtain multiple keys' data at once, and pretty print as a table._
```python
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
```

---

**Enjoy!**
_-iivii-_
