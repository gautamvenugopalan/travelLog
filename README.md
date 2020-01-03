# travelLog
Python code for plotting geodesics approximating flight paths.

## Files
 - `airports.csv` : List of coordinates and IATA codes (plus much more) of airports around the world
 - `travels_2019.py` : Python script that generates a map with geodesic paths and calculates total distance

## Usage
In `travels_2019.py`, edit the list of destinations and the individual journey (source, destination) pairs. For example:
```python
airports = ['FLL', 'LAX','SIN']

trips = [('FLL','LAX'), ('LAX','SIN')]
```
Then run from the shell
`python travels_2019.py`

This will generate a file called `map.pdf` with the flight paths overlaid.
