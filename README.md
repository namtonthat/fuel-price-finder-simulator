## Purpose
A simple python script that scrapes `https://projectzerothree.info/prices.php` to find the cheapest fuel price within Australia.


### Requirements
- :beer:  [`brew`](https://brew.sh/)
- :snake:  [`pyenv`](https://github.com/pyenv/pyenv)
- :book:  [`poetry`](https://github.com/python-poetry/poetry)

#### Installing Packages
`make install` - sets up environment and install required packages

#### Run script
`make run`
- runs the `run.sh` script -> required for iOS 17 and above to simulate a location
- to use an alternative fuel type, use the arg `fuel_type=<e10|u91|u95|u98|diesel|lpg>`


The `run.sh` script does two things:
1. Creates a tunnel - requires iPhone to be unlocked and a trusted device.
  a) Finds the lowest price for given `fuel_type` (`U91` by default)
  b) Creates the GPS location (lat / long) for this
2. Populates the command required and copies to clipboard

**Manual step**
- After the command has been copied, you'll need to open a new window and paste this into the Terminal.
- This will mimic the location whilst active
- Whilst active, lock in the fuel price within the 7-11 app
- Hit `RETURN` to stop the location

