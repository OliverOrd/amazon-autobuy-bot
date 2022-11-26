# Amazon In Stock Alerts
I modified [Currys-PC-Order-Bot](https://github.com/OliverOrd/currys-pc-order-bot) created by [abayomi185](https://github.com/abayomi185) to automatically purchase items on Amazon instead of Currys. 
<br/>
<br/>
The program will send you a discord alert when a desired product is in stock on Amazon. The bot will also attempt to purchase the product for you if the price isn't too high.
<br>
> Use this software at YOUR OWN RISK. This software offers no guarantee. I do not assume any risk you might incure from using this software.

<br/>

### Getting Started

To use the bot, confirm that you have chrome and python-pip. It would be ideal to install virtualenv or similar too.

Install the python dependencies using:
```pip install -r requirements.txt```

<br/>
Next, you will need to get chrome drivers. Confirm your version of Chrome or Chromium (Other chromium based browsers should work too) using the command or gui method.

For Chrome
```google-chrome --version```

You can then get the Chrome driver corresponding to your chrome version and Operating System from here: [https://chromedriver.chromium.org]()

The Chrome driver should be named ```chromedriver``` and placed in the project root folder.

<br/>

### You are almost ready to get your item from Amazon.

Rename the file ```secrets-template.yaml``` to ```secrets.yaml``` and fill in your personal details.

**Discord Notifications** can be enabled in ```conf.yaml``` and filling the *discord-webhook-url* in ```secrets.yaml```. The user-id would mention you when stock is available and/or item(s) has been purchased (This config is optional).

### Launching the bot

Enter the "name", "max_price" and "asin" values for the products that you want to buy in the '''conf.yaml''' file to setup a bot instance per product.

Then run the command:
```python amazon.py```

Good luck!


