# GestioIP Script
## Overview
The GestioIP script is a Python tool designed to interact with the GestioIP API for managing IP addresses and networks. It provides functionalities to retrieve network information, get details about a specific host, change
the site associated with a network, and list networks based on a site.

## Prerequisites
Before using the script, make sure you have the following prerequisites installed:

- Python

- Required Python packages: ipaddress, platform, os, requests, time, dotenv, prettytable

You can install the required packages using:

pip install ipaddress requests prettytable python-dotenv

## Configuration
Create a .env file in the script directory with the following content:

KEY=your_api_key_here

Replace your_api_key_here with your actual API key for GestioIP.

## Usage
Run the script by executing:

python gestioip_script.py

The script presents a Quick Menu with options to input an IP address, access the Full Menu, or exit.

The Full Menu provides additional functionalities, including getting network information, changing network site of a single network or a whole site, and listing networks of a site.
