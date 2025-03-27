const fs = require('fs');
const turf = require('@turf/turf');

// Load the precinct shapes file
console.log('Loading precinct shapes file...');
const shapesData = JSON.parse(fs.readFileSync('11-2024-precinct-shapes.json', 'utf8'));
console.log(`Loaded ${shapesData.features.length} precinct shapes`);

// Calculate the centroid for each precinct
const centroids = [];

// Process each precinct
shapesData.features.forEach(precinct => {
  const precinctId = precinct.properties.prec_2012;
  
  try {
    // Calculate centroid using turf.js
    const centroid = turf.centroid(precinct);
    const [longitude, latitude] = centroid.geometry.coordinates;
    
    // Only include valid centroids
    if (!isNaN(longitude) && !isNaN(latitude)) {
      centroids.push({
        id: precinctId,
        longitude,
        latitude,
        description: precinct.properties.Description,
        neighborhood: precinct.properties.find_neighborhood
      });
    } else {
      console.warn(`Warning: Invalid centroid for precinct ${precinctId}`);
    }
  } catch (error) {
    console.error(`Error calculating centroid for precinct ${precinctId}:`, error.message);
  }
});

console.log(`Calculated centroids for ${centroids.length} precincts`);

// Write the centroids to a new file
fs.writeFileSync('precinct-centroids.json', JSON.stringify({
  centroids: centroids
}, null, 2));

console.log('Wrote precinct centroids to precinct-centroids.json'); 