# gps_experimentation

This code listens to a USB GPS device, parses the data and saves it to a log file in a raw and simplified format.

This was tested to work with Raspberry Pi and a GlobalSat BU-353 USB GPS Receiver.

You can plot the simplified log file in an application like [gpsprune](http://activityworkshop.net/software/gpsprune/). To install that on the Pi, use:

    sudo apt-get install gpsprune
