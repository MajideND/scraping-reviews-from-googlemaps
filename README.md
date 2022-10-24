# Google Maps Reviews Scraper   
A python script to scrape reviews from google maps.
## Requirements
1. Python 3
2. PIP (package manager)
3. Chrome/Firefox driver
4. Install requirement.txt file using PIP. 
   
   `pip install -r requirements.txt `

Question: Where to download web browser driver?

Answer: Follow links in `Driver/driver_links.txt`.

## How to use?
1. Put URL of your location reviews and driver path in `env.py`
   
   Example:
   ```
   URL = "https://www.google.com/maps/place/Google+UK/@51.5332608,-0.1304879,17z/data=!4m7!3m6!1s0x48761b3c54efa6e1:0xc7053ab04745950d!8m2!3d51.5332609!4d-0.1260032!9m1!1b1"
   DriverLocation = "./Driver/chromedriver.exe"
   ```
 
2. Run the `app.py` file.

   ```
   python ./app.py
   ```
   
## Options

### Show browser during an scraping

Comment the headless tag from selenuim.

```
# options.add_argument("--headless")  # show browser or not
```

### Change output filename

You can change it in `def write_to_xlsx`

```
df.to_excel('what_you_like.xlsx')
```

### Scroll slower (problem with Google or network limits)

Go to `def scrolling`, change sleeping time

```
time.sleep(your_new_time_in_seconds)
```

## License

This source is licenced under MIT Licence, for more information read `LICENSE` file.
