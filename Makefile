fuel_type := u91

default:
	@echo "Please use 'make install' to install the workflow"

install:
	@echo "Installing workflow..."
	@sh ./install.sh
	@echo "Done!"

run:
	@echo "Running workflow..."
	@poetry run python fuel-prices.py --fuel-type $(fuel_type)
	@echo "Done!"
