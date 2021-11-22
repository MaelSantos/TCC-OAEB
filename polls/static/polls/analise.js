
regraGraficos()

function regraGraficos(){

    tipo = $("#tipoGrafico").val();

    if(tipo == "total"){
        $("#divMunicipio").hide();
    }else{
        $("#divMunicipio").show();
    }

}