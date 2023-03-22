console.log('hola0')
function ejemploLodash() {
  // Cargar la librería Lodash
  colsole.log('hola1')
  var response = UrlFetchApp.fetch('https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js');
  eval(response.getContentText());

  // Utilizar la librería Lodash
  var array = [1, 2, 3, 4, 5];
  var sum = _.sum(array);
  console.log('hola2');
  console.log('La suma del array es ' + sum);
}
