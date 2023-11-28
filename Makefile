default:
	@echo "Please use 'make install' to install the workflow"

install:
	@echo "Installing workflow..."
	@sh ./install.sh
	@echo "Done!"

run:
	@echo "Running workflow..."
	@sh ./run.sh
	@echo "Done!"
