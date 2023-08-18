const input = document.getElementById("input-field")
const button = document.getElementById("submit-button")

let dataBase = true
let string = ""
let data = ""
let jsonObject = {} 
let result_cep = document.getElementById("result_cep")

button.addEventListener("click", function(){
  const cep = input.value
  const proxy = "https://cors-anywhere.herokuapp.com/"
 
  fetch(proxy + `https://0wr6ic76da.execute-api.us-east-1.amazonaws.com/cep/consultacep?cep=${cep}`)
    .then(response => response.text())
    .then(data =>{ 
      
      //Checagem se os dados estão no banco
      if (data.substring(0,1) === "b"){
        dataBase = true
        string = data.slice(1)
      } else {
        dataBase = false
        string = data
      }
       
      //Transformação da string em JSON
      data = string.replace(/'/g, "\"")
      jsonObject = JSON.parse(data)
            
      //Retorno para o HTML  
      if (dataBase == true){
        result_cep.textContent = `O CEP se encontra no banco de dados. Ele pertence à ${jsonObject["logradouro"]}, cidade de ${jsonObject["cidade"]}, estado ${jsonObject["estado"]}.`
      }else{
        result_cep.textContent = `O CEP não se encontra no banco de dados. Ele pertence à ${jsonObject["logradouro"]}, cidade de ${jsonObject["cidade"]}, estado ${jsonObject["estado"]}.`
      }
       }
      ) 

  }
  )

