if($(".dataframe") != undefined){
    tabela = $(".dataframe")
    tabela.addClass("table table-hover")
    tabela.css("width", "100%")
}

$('#bases').selectpicker();
$('#bases').css("width", "100%")
$('#alerta').hide()

function regraBases(campo){

    bases = $(campo).val();
    $("#basesSelecionadas").val(bases.join());
    if(bases.length > 2){
        $.alert("Escolha no máximos duas bases de dados");
        $("#buscar").attr("disabled", true);
        $('#alerta').show()
    }else{
        $("#buscar").attr("disabled", false);
        $('#alerta').hide()
    }

}