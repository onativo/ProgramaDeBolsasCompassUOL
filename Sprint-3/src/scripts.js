//pega o elemento pelo id e fica "esperando" um clique para ativar a função validate
document.getElementById("botao_submit").addEventListener("click", validate)

//capturar o email digitado e retornar na var email
const email = document.getElementById("email").value

//capturar o nome digitado e retornar na var nome
const name = document.getElementById("name").value

//capturar o nome digitado e retornar na var telefone
const telefone = document.getElementById("number").value


//**1 - Verificar se o endereço de e-mail é válido usando uma expressão regular.**
  //essa classe verifica se o uer digitou um email padrão
class CheckEmail{
  static isEmail(email){
    let emailRegex = new RegExp (/^[a-zA-Z0-9._-]+@[a-zA-Z0-9_-]+\.(com|br|edu|org|net)$/)
    return (emailRegex.test(email))
  }
}

// Classe para fazer a verificação se o nome contém apenas letras maisculas e minusculas
class NameValidator {
  static validar(name) {
    const regex = /^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ'\s]+$/ 
    return (regex.test(name))
  }
}

// Valida se o número de telefone está no formato (NN)NNNN-NNNN
class Telefone {
  static validarTelefone(number) {
    const regex = (/^\(\d{2}\)\d{4}-\d{4}$/)
    return (regex.test(number))
  }
}


//essa é a função principal que valida o nome, email e telefone
  //retorna o valor digitado quando correto ou uma mensagem de erro quando incorreto
function validate(event){
  let $result = $("#result")
  let $result_name = $("#result_name")
  let $result_number = $("#result_number")
  let $result_2 = $("#result_2")
  let email = $("#email").val()
  let name = $("#name").val()
  let number = $("#number").val()
  email = email.toLowerCase()
  $result.text("")
  $result_2.text("")
  $result_name.text("")
  $result_number.text("")

  //if isEmail == true & nameDomain == true retorna o email com msg de sucesso
  if(CheckEmail.isEmail(email)){
    $result.text("O email " + email + " é válido :D")
    $result.css("color", "green")
  }
  //se o email é inválido, retorna o email com uma mensagem de erro
  else{
    $result.text("O email " + email + " é inválido :/")
    $result.css("color", "red")
    $result_2.text("Aceitos: .com, .br, .edu, .net e .org")
    $result_2.css("color", "red")
  }

//VALIDAÇÃO DO NOME
  //se o nome não é (!) valido retorna erro + nome digitado
if(!NameValidator.validar(name)){
    $result_name.text("O nome foi digitado incorretamente: " + name)
    $result_name.css("color", "red")
}
//se o nome é valido retorna sucesso + o nome
else{
    $result_name.text("O nome foi digitado corretamente: " + name)
    $result_name.css("color", "green")
}

//VALIDAÇÃO DO TELEFONE
  //se o telefone não (!) é valido retorna erro + telefone digitado
if(!Telefone.validarTelefone(number)){
  $result_number.text("O numero foi digitado incorretamente: " + number + " o formato correto é (xx)xxxx-xxxx")
  $result_number.css("color", "red")
}
  //se o telefone é valido retorna sucesso + o telefone
else{
  $result_number.text("O numero foi digitado corretamente: " + number)
  $result_number.css("color", "green")
}

//prevent default para a página não atualizar e perder os dados já digitados nos inputs
  event.preventDefault()
}



