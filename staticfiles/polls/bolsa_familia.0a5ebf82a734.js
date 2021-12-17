
$("#buscar").hide()

function verificarCampos(){
    nome = $("#nomeBeneficiario").val().trim()
    nis = $("#nis").val().trim()

    if(nis == "" && nome == "")
        $.alert("Campos vazios")
    else
        $("#buscar").click()
}