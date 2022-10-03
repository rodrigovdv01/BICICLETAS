function show_data(user) {
    document.getElementById("todos").innerHTML = '';
    fetch('/show-data/' + user, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(response) {
        return response.json();
    }).then(function(responseJSON) {
        const img = document.createElement('img');
        const li1 = document.createElement('li');
        const li2 = document.createElement('li');
        const li3 = document.createElement('li');
        const li4 = document.createElement('li');
        const li5 = document.createElement('li');
        const li6 = document.createElement('li');
        const li7 = document.createElement('li');
        const li8 = document.createElement('li');

        li1.innerHTML = "Publicado por: " + responseJSON['user'];
        li2.innerHTML = "Marca " + responseJSON['Marca'];
        li3.innerHTML = "Modelo: " + responseJSON['Modelo'];
        li4.innerHTML = "Tamaño de aro: " + responseJSON['Aro'];
        li5.innerHTML = "Color: " + responseJSON['Color'];
        li6.innerHTML = "Tipo: " + responseJSON['Tipo'];
        li7.innerHTML = "Nivel: " + responseJSON['Nivel'];
        li8.innerHTML = "Precio: S/." + responseJSON['Precio'];
        img.src = responseJSON['Imagen'];
        img.style.width = '300px';


        document.getElementById("todos").appendChild(img);
        document.getElementById("todos").appendChild(li1);
        document.getElementById("todos").appendChild(li2);
        document.getElementById("todos").appendChild(li3);
        document.getElementById("todos").appendChild(li4);
        document.getElementById("todos").appendChild(li5);
        document.getElementById("todos").appendChild(li6);
        document.getElementById("todos").appendChild(li7);
        document.getElementById("todos").appendChild(li8);

        document.getElementById('show-info').className = '';
    })
}

function ocultar() {
    document.getElementById('show-info').className = 'hidden';
}

function update_data(user) {
    fetch('/actualizar/' + user, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(response) {
        return response.json();
    }).then(function(responseJSON) {})
}

function delete_data(id) {
    fetch('/delete/' + id, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(response) {
        return response.json();
    }).then(function(responseJson) {
        location.reload();
    })
}