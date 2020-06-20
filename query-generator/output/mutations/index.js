const fs = require('fs');
const path = require('path');

module.exports.createHuman = fs.readFileSync(path.join(__dirname, 'createHuman.gql'), 'utf8');
module.exports.createWizard = fs.readFileSync(path.join(__dirname, 'createWizard.gql'), 'utf8');
module.exports.createMuggle = fs.readFileSync(path.join(__dirname, 'createMuggle.gql'), 'utf8');
