
$("#buscar").hide()

if($("#lista") != undefined){
    $("#lista").show()
    $("#lista").addClass("table table-hover")
    $("#lista").css("width", "100%")
}

function verificarCampos(){
    nome = $("#nomeBeneficiario").val().trim()
    nis = $("#nis").val().trim()

    if(nis == "" && nome == "")
        $.alert("Campos vazios")
    else
        $("#buscar").click()
}

function exibirCidades(){

    tipoBusca = $("#tipoBusca").val()

    if(tipoBusca == "prefeitura")
        $("#divCidades").show()
    else
        $("#divCidades").hide()

}


