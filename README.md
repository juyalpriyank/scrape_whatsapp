# WhatsApp-Scraping
Python script to scrape all the chats from WhatsApp Web.

# Description
Asynchronous WhatsApp Scraper written in Python. I have tried to keep this script independent of the changing classnames of WhatsApp web. Simply prints the text from each chat to the console. 

# Requirements 
Script uses Python3.5+.
All the libraries that we are going to use are in the [requirement.txt](requirement.txt) file.
You can install it with PIP in the terminal with:
```
pip install -r requirements.txt
```

## Selenium
Selenium requires a driver to interface with the chosen browser. This script uses the Chrome driver. Please Download your driver from below link. NOTE:- The driver version should match your Chrome browser's version.

* [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)

>For more information you can go to the [Selenium Website](http://selenium-python.readthedocs.io/installation.html) at the installation section.

# Limitations
*  Doesn't prints the link of the pictures/videos.
*  Doesn't scrape the archived chats.
*  Marked replies to texts are not seperated as of now.

# Settings
**AT THIS MOMENT THE PROJECT ONLY WORKS WITH CHROME**.<br>
**THE SCRIPT IS RUN USING AN IDE LIKE IPYTHON**.<br>
**BELOW ARE THE STEP-BY-STEP GUIDANCE FOR THE SAME**.


# Step-1:
*  Clone the repo
*  Change the ["--driver_path"](https://github.com/juyalpriyank/scrape_whatsapp/blob/a57bae9299c1e355159e835ceefa5d5b1b988c97/script.py#L13) to absolute path of your chrome driver.
*  Open IPython and import the script.py(using the below command) which will launch the browser and redirect you to whatsapp web.
``` 
import script
```

# Step-2:
*  Scan the QR code and wait for the page to load.
*  Now import the start_scrape() function from script.py
``` 
from script import start_scrape
```

# Step-3:
*  Now call the function and you will see the script printing "processing..." until it completely scrolls the chat window. When the chat ends it will print all the text from the chat to console and move on to the next chat. 
 ```
await start_scrape()
 ``` 
