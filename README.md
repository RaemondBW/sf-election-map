# SF Election Results Map

An interactive visualization of San Francisco election results by precinct, displayed as a bubble map. The size of each bubble represents the number of votes in that precinct for a given contest, while the color represents the winner or vote distribution.

## Features

- Interactive selection of different election contests
- Bubble size represents total votes in each precinct
- Color indicates winning candidate (for multi-candidate races) or vote distribution (for yes/no measures)
- For yes/no measures: red-white-green gradient shows percentage split (red=100% NO, white=50/50, green=100% YES)
- Detailed tooltips with precinct information, neighborhood, and vote breakdown
- Responsive design with intuitive controls

## Development

To run this project locally:

```bash
# Install dependencies
npm install

# Start the development server
npm run dev
```

The server will start at http://localhost:3000

## Hosting

The site is plain static files in `public/`, published with GitHub Pages by
`.github/workflows/pages.yml` on every push to `main`. Because the
`raemondbw.github.com` user site uses the `raemond.com` domain, this repo is served at
https://raemond.com/sf-election-map/.

One-time setup: in the repo's Settings → Pages, set **Source** to **GitHub Actions**.

## Updating the 2026 results

SF Elections posts new preliminary results most afternoons until the election is
certified (by Dec 3, 2026). Each report with a Statement of the Vote can be
converted into the map's data files:

```bash
# Newest report folder is listed at https://www.sfelections.org/results/20261103w/detail.html
URL=https://www.sfelections.org/results/20261103/data/20261108/sov.xlsx
curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130.0 Safari/537.36" -o /tmp/sov.xlsx "$URL"   # the site refuses requests without a browser user-agent
pip install openpyxl
python3 tools/sov_to_json.py /tmp/sov.xlsx 11-2026 "$URL"
```

The script refuses to write anything unless each contest's precinct totals add up
to the countywide totals. Commit and push the two updated `public/11-2026-*.json`
files to publish.

## Data Sources

- San Francisco Department of Elections
- Precinct shapes and voting data from the November 2024 and November 2026 general elections
- 2026 results are preliminary until certification; ranked-choice contests show first-choice votes

## Technologies Used

- D3.js for data visualization
- Node.js for local development server
- GitHub Pages for hosting

## Implementation Details

This visualization is built using:

- D3.js for data visualization
- GeoJSON for geographic data
- Node.js for the optional server component

Based on Mike Bostock's bubble map tutorial: https://bost.ocks.org/mike/bubble-map/ 