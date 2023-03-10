
# Installation Guide

This guide outlines the steps required to install and run the econdash program on your local machine.

## Prerequisites

Before proceeding with the installation, make sure that you have the following prerequisites installed on your machine:

- Python 3.10+ installed
- pip package manager installed
- Git installed

## :one: Clone the repository

To begin, clone the econdash repository onto your local machine by opening a terminal window and running the following command:

``` bash
git clone https://github.com/m-amin-alavian/econdash.git
```

## :two: Install dependencies

After successfully cloning the repository, navigate to the cloned repository's directory on your local machine and install the necessary Python dependencies using pip:

``` bash
cd econdash
pip install -r requirements.txt
```

## :three: Run the program

Once the dependencies have been successfully installed, you can run the program by typing the following command:

``` bash
streamlit run econdash/main.py
```

This will launch the econdash program in your default web browser.
