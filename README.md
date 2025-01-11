# raspi-rack-frontpanel

## Overview

This repository contains a python program for handling the frontpanel i use on my [pi5 server rack](TODO: link thingiverse).

The frontpanel contains a 0.91inch I2C oled screen, a button and 2 LEDs.
- The display is serving as a system monitor by showing information about system load, network status, etc.
- The button is used to power on/off the Pi
- The first LED is not programmable and is just directly hooked up to the 3.3V line of the PI
- The 2nd LED is connect to GPIOx and is performing a heartbeat, to show that this service (and therefore the Pi) is running

## Prerequisites

- Raspberry Pi 5
- 0.91inch I2C OLED screen
- At least 1 LED for the activity indication
- 1 push button for powering on/off

## Usage

TODO: add instructions

## Development

TODO: add instuctions