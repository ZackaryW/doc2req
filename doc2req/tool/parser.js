let inputPath = process.argv[2]
let targetPath = process.argv[3]

path = require('path')
apidoc = require('apidoc')
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

if (typeof doc == 'boolean') {
  console.log('Error: no valid apiDoc content!')
  process.exit(1)
}
console.log(doc.data) // the parsed api documentation object
