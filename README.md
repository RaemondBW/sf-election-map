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

## Deploying to Vercel

This project is ready to deploy on Vercel. Follow these steps:

1. Install the Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy to Vercel:
```bash
vercel
```

3. Or connect your GitHub repository to Vercel for automatic deployments.

## Data Sources

- San Francisco Department of Elections
- Precinct shapes and voting data from November 2024 general election

## Technologies Used

- D3.js for data visualization
- Node.js for local development server
- Vercel for deployment

## Implementation Details

This visualization is built using:

- D3.js for data visualization
- GeoJSON for geographic data
- Node.js for the optional server component

Based on Mike Bostock's bubble map tutorial: https://bost.ocks.org/mike/bubble-map/ 