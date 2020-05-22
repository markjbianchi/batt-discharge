# Coin Cell Discharger #

This repo contains python modules and scripts for discharging coincell batteries in a controlled manner. The key device employed in doing this is the [LabJack U3](https://labjack.com/products/u3) data acquisition (dacq) module, along with some customer loading circuitry.

* `BattDischarge.py` - module used to interface with UC dacq.
* `discharger.py` - script that monitors and controls battery discharging; configurable sampling period which logs battery voltage and cumulative charge drain as CSV output.
* `example_cfg` - example config file used by `discharger.py` to specify various parameters for each _battery discharge channel_ (e.g., discharge load resistance, cutoff voltage or cumulative coulombs).
* `example_initial_drain` - optional input file to `discharger.py` which specifies previous charge drained from each _discharge channel_; useful for restarting a discharge session and accounting for previous discharge amounts.
* `filter_csv.py` - script for culling CSV log output.
* `plot_csv.py` - script to plot CSV log output.

