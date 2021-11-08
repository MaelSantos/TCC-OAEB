
$("#buscar").hide();
exibirCidades();

if($("#lista") != undefined){
    $("#lista").show();
    $("#lista").addClass("table table-hover");
    $("#lista").css("width", "100%");
}

function verificarCampos(){
    $("#buscar").click();
}

function exibirCidades(){

    tipoBusca = $("#tipoBusca").val()

    if(tipoBusca == "prefeitura"){
        $("#divCidades").show();
        $("#divMes").show();
        $("#divPeriodo").hide();
    }
    else{
        $("#divCidades").hide();
        $("#divMes").hide();
        $("#divPeriodo").show();
    }

}


