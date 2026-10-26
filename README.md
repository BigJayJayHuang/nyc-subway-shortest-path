# NYC Subway Shortest-Path Finder (Dijkstra's Algorithm)

A Python implementation of Dijkstra's shortest-path algorithm that finds the fastest route between two NYC subway stations.

## Project overview

The subway system is modeled as a weighted graph. Each station is a node, and each segment between two stations is an edge. The edge weight is the average travel time between the two stations plus the average wait time for that line, so a single number represents the total time cost of each hop.

Given a starting station and a destination station, the program returns the stations on the fastest route, the total estimated time in minutes, and the subway line used for each hop.

## Methodology

The script:

1. Reads the subway segment data from `final_subway_segments.csv`.
2. Builds a graph as a dictionary of lists, where each station maps to its neighboring stations.
3. Adds the average wait time to the average travel time to create one edge weight.
4. Merges stations that share a name into a single node and keeps one edge per station pair.
5. Runs Dijkstra's algorithm with a `heapq` priority queue, always expanding the station with the lowest total time so far.
6. Returns the path, total time, and subway lines once the destination is reached, or reports that no path exists.

A priority queue is a data structure that always returns the item with the smallest value first. Using one means the algorithm does not have to scan every unvisited station each time it picks the next one, which improves pathfinding performance on a graph of this size.

## Data

`final_subway_segments.csv` has one row per subway segment with these columns:

| Column | Description |
|---|---|
| `route_short_name` | Subway line (for example `1`, `6`, `A`) |
| `from_station` | Starting station of the segment |
| `to_station` | Ending station of the segment |
| `average_travel_time_minutes` | Average ride time for the segment |
| `average_wait_time_minutes` | Average wait time for that line |

The file contains 2,088 segments across 27 routes. After merging duplicate segments, the graph has 378 stations with outgoing connections and 1,049 edges.

## Example

Running the script from `96 St` to `Castle Hill Av` returns a 7-station route that uses the 1, 4, 6, and 6X lines, with an estimated total time of about 31.6 minutes including wait times.

## Repository contents

```text
nyc-subway-shortest-path/
├── README.md
├── Dijkstra_Alg_NYC_Subways.py
└── final_subway_segments.csv
```

## Setup and usage

This project uses only the Python standard library and requires Python 3.8 or newer.

```bash
python Dijkstra_Alg_NYC_Subways.py
```

To try a different route, change `starting_station` and `destination_station` at the bottom of the script. Station names must match the names in the CSV exactly.

## Limitations and future improvements

- Stations with the same name in different boroughs (for example 79th St) are merged into one node, so the model cannot tell them apart.
- Only one edge is kept per station pair, so alternative lines between the same two stations are not compared.
- Transfers between lines are not given their own time cost.
- Wait times are averages and do not reflect time of day or service changes.
- Future improvements could include separate nodes for each line at a station, transfer penalties, time-of-day wait times, and a simple command-line or web interface for choosing stations.
