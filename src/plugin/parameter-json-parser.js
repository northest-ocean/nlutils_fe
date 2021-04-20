


function parserParamJSONFile(filePath) {
    var request = new XMLHttpRequest();
    console.log(filePath);
    request.open("GET", filePath);
    request.onreadystatechange = function() {
      if (request.readyState === 4 && request.status === 200) {
          console.log("this.responseText: " + request.responseText);
      } else {
          console.log("I was not ready");
      }
    };
    request.send(null);
}

function parserParamJSONFolder(folderPath) {
    console.log(folderPath);
}

export {
    parserParamJSONFile,
    parserParamJSONFolder
};