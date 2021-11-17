
regraGraficos()

function regraGraficos(){

    tipo = $("#tipoGrafico").val();

    if(tipo == "total"){
        $("#divMunicipio").hide();
        $("#divPeriodo").hide();
    }else{
        $("#divMunicipio").show();
        $("#divPeriodo").show();
    }

}