/*
  --------------------------------------------------------------------------------------
  Função para obter a lista de bois existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getListBois = async () => {
  let url = 'http://127.0.0.1:5000/bois';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.bois.forEach(item => insertListBoi(item.brinco, item.raca, item.comentario))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getListBois()

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista de Pesos existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getListPesos = async () => {
  let url = 'http://127.0.0.1:5000/pesos';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.pesos.forEach(item => insertListPeso(item.id, item.brinco, item.peso, item.data_pesagem))
    })      
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getListPesos()

/*
  --------------------------------------------------------------------------------------
  Função para colocar um boi na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postBoi = async (inputBrinco, inputRaca, inputComentario) => {
  const formData = new FormData();
  formData.append('brinco', inputBrinco);
  formData.append('raca', inputRaca);
  formData.append('comentario', inputComentario);

  let url = 'http://127.0.0.1:5000/boi';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para alterar um boi na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const updateBoi = async (inputBrinco, inputRaca, inputComentario) => {
  const formData = new FormData();
  formData.append('brinco', inputBrinco);
  formData.append('raca', inputRaca);
  formData.append('comentario', inputComentario);

  let url = 'http://127.0.0.1:5000/boi?brinco='+inputBrinco;
  fetch(url, {
    method: 'put',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para colocar uma Peso na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postPeso = async (inputBrinco, inputValor, inputData) => {
  const formData = new FormData();
  formData.append('brinco_referencia', inputBrinco);
  formData.append('valor', inputValor);
  formData.append('data_pesagem', inputData);
  

  let url = 'http://127.0.0.1:5000/peso';
  fetch(url, {
    method: 'post',
    body: formData
  })
  .then((response) => {
	if (response.status == 200)	{  
	var tableHeaderRowCount = 1;
	var table = document.getElementById('myTablePeso');
	var rowCount = table.rows.length;
		for (var i = tableHeaderRowCount; i < rowCount; i++) {
			table.deleteRow(tableHeaderRowCount);
		}
		getListPesos()
		//insertListPeso(" ",inputBrinco, inputValor, inputData);
	    alert("Item adicionado!")
	} else {
		alert("Insira um brinco ja cadastrado");
	}
    response.json()})
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada boi da lista
  --------------------------------------------------------------------------------------
*/
const insertButtonBoi = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "closeBoi";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada peso da lista
  --------------------------------------------------------------------------------------
*/
const insertButtonPeso = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "closePeso";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um boi da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeBoi = () => {
  let close = document.getElementsByClassName("closeBoi");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteBoi(nomeItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um boi ou Peso da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removePeso = () => {
  let close = document.getElementsByClassName("closePeso");
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deletePeso(nomeItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um boi da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteBoi = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/boi?brinco=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para alterar um boi da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const alteraBoi = () => {
  let inputBrinco = document.getElementById("newBrinco").value;
  let inputRaca = document.getElementById("newRaca").value;
  let inputComentario = document.getElementById("newComentario").value;
  if (inputBrinco === '' || isNaN(inputBrinco)) {
    alert("Escreva um brinco cadastrado!");
  } else {
    updateBoi(inputBrinco, inputRaca, inputComentario)
    updateListBoi(inputBrinco, inputRaca, inputComentario)
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um peso da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deletePeso = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/peso?id=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo boi com brinco, raça e comentario 
  --------------------------------------------------------------------------------------
*/
const newBoi = () => {
  let inputBrinco = document.getElementById("newBrinco").value;
  let inputRaca = document.getElementById("newRaca").value;
  let inputComentario = document.getElementById("newComentario").value;

  if (inputBrinco === '') {
    alert("Escreva o brinco de um boi!");
  } else {
    insertListBoi(inputBrinco, inputRaca, inputComentario)
    postBoi(inputBrinco, inputRaca, inputComentario)
    alert("Item adicionado!")
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo peso com brinco, valor(peso) e data 
  --------------------------------------------------------------------------------------
*/
const newPeso = () => {
  let inputBrinco = document.getElementById("newBrincoRef").value;
  let inputValor = document.getElementById("newValor").value;
  let inputData = document.getElementById("newData").value;
  if (inputBrinco === '' || isNaN(inputBrinco)) {
    alert("Escreva um brinco cadastrado!");
  } else {
    postPeso(inputBrinco, inputValor, inputData)
  }
}
/*
  --------------------------------------------------------------------------------------
  Função para inserir boi na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertListBoi = (nmbBrinco, raca, comentario) => {
  var item = [nmbBrinco, raca, comentario]
  var table = document.getElementById('myTableBoi');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButtonBoi(row.insertCell(-1))
  document.getElementById("newBrinco").value = "";
  document.getElementById("newRaca").value = "";
  document.getElementById("newComentario").value = "";

  removeBoi()
}

/*
  --------------------------------------------------------------------------------------
  Função para inserir peso na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertListPeso = (nmbId, nmbBrinco, valor, data_pesagem) => {
  var item = [nmbId, nmbBrinco, valor, data_pesagem]
  var table = document.getElementById('myTablePeso');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButtonPeso(row.insertCell(-1))
  document.getElementById("newBrincoRef").value = "";
  document.getElementById("newValor").value = "";
  document.getElementById("newData").value = "";

  removePeso()
}

/*
  --------------------------------------------------------------------------------------
  Função para inserir boi na lista apresentada
  --------------------------------------------------------------------------------------
*/
const updateListBoi = (nmbBrinco, raca, comentario) => {
  var item = [nmbBrinco, raca, comentario]
  var table = document.getElementById('myTableBoi');
  for (var i = 0; i < table.rows.length; i++) {
    var row = table.rows[i]
    var boiID = row.cells[0].innerHTML ;
    if (boiID == item[0]){
        row.cells[1].textContent = item[1];
        row.cells[2].textContent = item[2];
        alert("alterando boi");
        break;
      }
    if (i == (table.rows.length -1))
    alert("brinco não cadastrado");
  }
  document.getElementById("newBrinco").value = "";
  document.getElementById("newRaca").value = "";
  document.getElementById("newComentario").value = "";

  removeBoi()
}

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'https://ai-weather-by-meteosource.p.rapidapi.com/current?lat=-22.303074&lon=-49.065628&timezone=auto&language=en&units=auto';
    const options = {
      method: 'GET',
      headers: {
      'X-RapidAPI-Key': '037f4adf44mshc47d844cfe6718fp170108jsnfbac8ee43379',
      'X-RapidAPI-Host': 'ai-weather-by-meteosource.p.rapidapi.com'
      }
    };
  fetch(url, options)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      document.getElementById("temperature").textContent = data.current.temperature;
      document.getElementById("clima").textContent = data.current.summary;
      document.getElementById("humid").textContent = data.current.humidity;
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/

