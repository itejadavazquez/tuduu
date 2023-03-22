// console.log("Hola");

function ejemploLodash() {
  // Cargar la librería Lodash
  var response = UrlFetchApp.fetch('https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js');
  eval(response.getContentText());

  // Utilizar la librería Lodash
  var array = [1, 2, 3, 4, 5];
  var sum = _.sum(array);
  Logger.log('La suma del array es ' + sum);
}

