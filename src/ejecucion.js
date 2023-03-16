const { spawn } = require('child_process');
const pyScript = spawn('python', ['automatizacion.py']);

pyScript.stdout.on('data', (data) => {
  console.log(`Resultado: ${data}`);
});

pyScript.stderr.on('data', (data) => {
  console.error(`Error: ${data}`);
});

pyScript.on('close', (code) => {
  console.log(`Proceso de Python cerrado con el código ${code}`);
});
