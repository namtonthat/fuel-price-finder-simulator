from dataclasses import dataclass
import json
import getpass
import logging
import pexpect
import platform
import re
import requests
import subprocess


# Configure logging for console output
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Script started.")


def remove_ansi_codes(s):
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", s)


@dataclass
class FuelPrice:
    """Class to hold Fuel Price data"""

    state: str
    postcode: str
    price: float
    suburb: str
    name: str
    lat: float
    lng: float
    type: str

    @property
    def location(self):
        return f"{self.suburb}, {self.state} {self.postcode}, Australia"

    @property
    def gps(self):
        return (self.lat, self.lng)


def get_cheapest_fuel_location():
    url = "https://projectzerothree.info/api.php?format=json"
    page = requests.get(url)

    data = json.loads(page.text)
    best_prices = data.get("regions")[0].get("prices")

    selected_fuel_type = "U91"
    for fuel_type_best_price in best_prices:
        single_fuel_price = FuelPrice(**fuel_type_best_price)
        if selected_fuel_type == single_fuel_price.type:
            logging.info(f"Cheapest fuel price {single_fuel_price.location}")
            return single_fuel_price.gps


def start_tunnel_and_wait():
    logging.info("Starting the rsd connection command...")

    command = "sudo -E poetry run python3 -m pymobiledevice3 remote start-quic-tunnel"
    logging.info("About to run command: %s", command)

    try:
        # Start the command with pexpect
        child = pexpect.spawn(command, timeout=10)

        # Wait for the password prompt and send the password
        child.expect_exact("Password:")
        child.sendline(getpass.getpass("Enter sudo password: "))

        index = child.expect(["Use the follow connection option:", pexpect.TIMEOUT, pexpect.EOF])

        if index == 0:
            logging.info("Command output: %s", child.before.decode())

            output = child.before.decode()
            rsd_address_match = re.search(r"RSD Address: (\S+)", output)
            rsd_port_match = re.search(r"RSD Port: (\S+)", output)

            if rsd_address_match and rsd_port_match:
                rsd_address = remove_ansi_codes(rsd_address_match.group(1))
                rsd_port = remove_ansi_codes(rsd_port_match.group(1))
                logging.info("Extracted RSD Address: %s, RSD Port: %s", rsd_address, rsd_port)
                return child, (rsd_address, rsd_port)

            logging.error("Failed to extract RSD Address and Port")

    except pexpect.exceptions.ExceptionPexpect as e:
        logging.error("A pexpect exception occurred: %s", str(e))

    except Exception as e:
        logging.error("An unexpected exception occurred: %s", str(e))

    return child, (None, None)


def print_simulate_command(gps_coords, rsd_info):
    rsd_address, rsd_port = rsd_info
    simulate_command = [
        "pymobiledevice3",
        "developer",
        "dvt",
        "simulate-location",
        "set",
        "--rsd",
        rsd_address,
        str(rsd_port),  # Make sure the port is converted to string
        "--",
        str(gps_coords[0]),
        str(gps_coords[1]),
    ]

    current_dir = subprocess.run(["pwd"], capture_output=True, text=True).stdout.strip()
    logging.info("Current directory: %s", current_dir)

    cmd_str = " ".join(simulate_command)
    cd_str = f"cd {current_dir}"
    logging.info("Copy and execute the following command manually in another window:")
    full_cmd = "\n".join([cd_str, cmd_str])
    print(full_cmd)  # print the command to the terminal for user to copy
    return full_cmd


def copy_simulate_command(cmd: str):
    # If on a macOS, copy the cmd_str to the clipboard
    if platform.system() == "Darwin":  # macOS is identified as 'Darwin' with platform.system()
        process = subprocess.Popen("pbcopy", universal_newlines=True, stdin=subprocess.PIPE)
        process.communicate(cmd)
        logging.info("The command has been copied to your clipboard.")


def prompt_to_close_terminal():
    input("Open a new terminal window and paste the command. Press Enter to continue...")
    input("Once you have executed the command and are done, press Enter to close the tunnel and exit...")


def main():
    cheapest_fuel_location = get_cheapest_fuel_location()

    tunnel_process, rsd_info = start_tunnel_and_wait()

    if not rsd_info or not tunnel_process:
        logging.error("Failed to retrieve RSD info. Exiting.")
        return

    try:
        cmd = print_simulate_command(cheapest_fuel_location, rsd_info)

        # If on a macOS, copy the cmd_str to the clipboard
        copy_simulate_command(cmd)

        # Prompt the user to close the terminal
        prompt_to_close_terminal()
    finally:
        logging.info("Closing the tunnel...")
        tunnel_process.terminate(force=True)


if __name__ == "__main__":
    main()
