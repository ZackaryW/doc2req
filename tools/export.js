global.path = require('path')
global.apidoc = require('apidoc')
// use commandline args  

if (!inputPath) {
  inputPath = path.resolve(__dirname)
}
if (!targetPath) {
  targetPath = path.resolve(__dirname, 'output')
}

const doc = apidoc.createDoc({
  src: inputPath, // the input path of your app
  dest: targetPath, // the output path for the documentation
  // if you don't want to generate the output files:
  dryRun: true,
  // if you don't want to see any log output:
  silent: true,
})

console.log('apidoc was called with options:', doc.options)
if (typeof doc == 'boolean') {
  console.log('Error: no valid apiDoc content!')
  process.exit(1)
}
// Documentation was generated!
//console.log(doc.data) // the parsed api documentation object
//console.log(doc.project) // the project information
// write data to json file
fs = require('fs')
//create folder
if (!fs.existsSync(targetPath)) {
  fs.mkdirSync(targetPath)
}
fs.writeFile(
  path.resolve(targetPath, 'api.json'),
  doc.data,
  function (err) {
    if (err) throw err
    console.log('Saved!')
  }
)

