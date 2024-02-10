## Purpose
A simple python script that scrapes `https://projectzerothree.info/prices.php` to find the cheapest fuel price within Australia.
#### Requirements
- :beer:  [`brew`](https://brew.sh/)
- :snake:  [`pyenv`](https://github.com/pyenv/pyenv)
- :book:  [`poetry`](https://github.com/python-poetry/poetry)

Ensure you have the above installed before proceeding.

#### Makefile 
A Makefile has been created to simplify the process of setting up the environment and running the script.

- Run `make` to see the available commands

#### Installing Packages
`make install` - sets up environment and install required packages

#### Run script
`make run`
- runs the `fuel-prices.py` script -> required for iOS 17 and above to simulate a location
- to use an alternative fuel type, use the arg `fuel_type=<e10|u91|u95|u98|diesel|lpg>` i.e.
```
# defaults to u91
make run 
# sets the fuel type to u95
make run fuel_type=u95
```


#### Procedure
1. Creates a tunnel - requires iPhone to be unlocked and a trusted device.
  - Finds location the best price for given `fuel_type` (`U91` by default)
  - Returns the GPS location (lat / long) which is used to simulate the location

2. Populates the command required and copies to clipboard

3.  **Manual step**
  - After the command has been copied, you'll need to open a new window and paste this into the Terminal.
  - This will mimic the location whilst active
  - Whilst active, lock in the fuel price within the 7-11 app. Sometimes, 7-11 app will return an error. Quit the app and retry.
  - *Hit `CTRL+C` to stop the location simulation* or else you'll be stuck there until you open the simulation and cancel it again.
