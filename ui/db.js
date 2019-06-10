let rest_uri = 'http://localhost:5000'

var fetchData = (keyword, source, callback) => {
    let url = `${rest_uri}/${keyword}/${source}`;
    var request = new XMLHttpRequest();
    request.open('GET', url, true ); // true for async
    request.onreadystatechange = () => {
        if (request.readyState == 4 && request.status == 200) {
            let response = request.responseText;
            let json = JSON.parse(response);
            callback(json);
        }
    };
    request.send();
};
