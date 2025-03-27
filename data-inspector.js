const fs = require('fs');

// Read a small portion of the JSON files to inspect their structure
fs.readFile('11-2024-precinct-shapes.json', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading precinct shapes:', err);
    return;
  }
  
  try {
    const shapesData = JSON.parse(data);
    console.log('PRECINCT SHAPES STRUCTURE:');
    console.log('Type:', shapesData.type);
    console.log('Number of features:', shapesData.features ? shapesData.features.length : 'N/A');
    if (shapesData.features && shapesData.features.length > 0) {
      console.log('Sample feature properties:', shapesData.features[0].properties);
      console.log('Sample precinct ID:', shapesData.features[0].properties.prec_2012 || 'N/A');
    }
    console.log('\n');
  } catch (parseErr) {
    console.error('Error parsing precinct shapes JSON:', parseErr);
  }
});

fs.readFile('11-2024-precinct-vote.json', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading precinct votes:', err);
    return;
  }
  
  try {
    const voteData = JSON.parse(data);
    console.log('PRECINCT VOTES STRUCTURE:');
    
    // Check if it's an array or object
    if (Array.isArray(voteData)) {
      console.log('Vote data is an array with length:', voteData.length);
      if (voteData.length > 0) {
        console.log('First item structure:', Object.keys(voteData[0]));
        console.log('Sample first item:', voteData[0]);
      }
    } else {
      console.log('Vote data is an object with keys:', Object.keys(voteData).length);
      // Sample a few keys to understand structure
      const sampleKeys = Object.keys(voteData).slice(0, 5);
      console.log('Sample keys:', sampleKeys);
      
      if (sampleKeys.length > 0) {
        const sampleKey = sampleKeys[0];
        console.log('Sample data for key', sampleKey, ':', voteData[sampleKey]);
      }
    }
  } catch (parseErr) {
    console.error('Error parsing precinct votes JSON:', parseErr);
  }
});

fs.readFile('11-2024-meta.json', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading meta data:', err);
    return;
  }
  
  try {
    const metaData = JSON.parse(data);
    console.log('\nMETA DATA STRUCTURE:');
    console.log('Keys:', Object.keys(metaData));
    
    if (metaData.contests) {
      console.log('Number of contests:', metaData.contests.length);
      console.log('First few contests:');
      metaData.contests.slice(0, 5).forEach(contest => {
        console.log(`  - ID: ${contest.Id}, Description: ${contest.Description}`);
      });
    }
    
    if (metaData.candidates) {
      console.log('Number of candidates:', metaData.candidates.length);
      console.log('Sample candidate structure:', metaData.candidates[0]);
    }
  } catch (parseErr) {
    console.error('Error parsing meta JSON:', parseErr);
  }
}); 