const fs = require('fs');
const path = require('path');

module.exports.hero = fs.readFileSync(path.join(__dirname, 'hero.gql'), 'utf8');
module.exports.human = fs.readFileSync(path.join(__dirname, 'human.gql'), 'utf8');
module.exports.droid = fs.readFileSync(path.join(__dirname, 'droid.gql'), 'utf8');
module.exports.wizard = fs.readFileSync(path.join(__dirname, 'wizard.gql'), 'utf8');
module.exports.muggle = fs.readFileSync(path.join(__dirname, 'muggle.gql'), 'utf8');
module.exports.char = fs.readFileSync(path.join(__dirname, 'char.gql'), 'utf8');
