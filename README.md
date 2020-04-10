# cyberglove
Interface the CyberGlove Systems CyberGlove II data glove in Python.

The interface is implemented using a serial communication.

Here is a minimal working example:

```python
from cyberglove import CyberGlove

cg = CyberGlove(n_df=18, s_port='COM6', baud_rate=115200, samples_per_read=1)
cg.start()
cg.read()
cg.stop()
```

Some more examples are provided in [examples](examples).

## Dependencies
* Python >= 3.6 (other versions have not been tested and may or may not work)
* [pyserial](https://pythonhosted.org/pyserial/) 

## Notes
* To calibrate the glove you will need to install the CyberGlove Systems VirtualHand Software.
