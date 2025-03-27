# San Francisco Election Results Bubble Map

An interactive visualization of San Francisco election results by precinct, displayed as a bubble map. The size of each bubble represents the number of votes in that precinct for a given contest.

## Features

- Interactive map of SF precincts
- Dropdown selection for different contests (President, Mayor, Propositions, etc.)
- Bubbles sized proportionally to vote count
- Color-coded by supervisorial district
- Hover tooltips showing detailed vote counts by candidate

## Data Sources

- Precinct shapes (GeoJSON): `11-2024-precinct-shapes.json`
- Vote data by precinct: `11-2024-precinct-vote.json`
- Metadata for contests and candidates: `11-2024-meta.json`

## Running the Visualization

### Option 1: Simple HTTP Server

Run the included Node.js server:

```bash
node server.js
```

Then open your browser to http://localhost:3000

### Option 2: Any Web Server

You can also use any HTTP server (Python's http.server, PHP's built-in server, etc.) to serve the files.

For example, with Python:

```bash
python -m http.server
```

## Implementation Details

This visualization is built using:

- D3.js for data visualization
- GeoJSON for geographic data
- Node.js for the optional server component

Based on Mike Bostock's bubble map tutorial: https://bost.ocks.org/mike/bubble-map/ 