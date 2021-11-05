if($(".dataframe") != undefined){
    tabela = $(".dataframe");
    tabela.addClass("table table-hover");
    tabela.css("width", "100%");
    $("tr").css("text-align", "");
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
        $('#campoTipo').hide()
    }else{
        $("#buscar").attr("disabled", false);
        $('#alerta').hide()
    }
}

function exibirPopover(id){
    bases = $('[data-id="bases"]').attr("title").replace("Nothing selected", "").split(",");
    if(bases[0] == "")
        $(id).attr("data-bs-content", "Selecione uma base de dados");
    else if(bases.length == 1)
        $(id).attr("data-bs-content", "Somente 1 base selecionada, não ocorrerá nenhum cruzamente, somente será retornado as informações do(a) "+bases[0]);
    else if(bases.length == 2){
        tipo = $("#tipoCruzamento").val();
        if(tipo == "intersecao")
            $(id).attr("data-bs-content", "O cruzamento retornará os dados das pessoas que estejam presentes em ambas as bases de dados. Presentes no(a) "+bases[0]+" e no(a)"+bases[1]);
        else if(tipo == "diferenca")
            $(id).attr("data-bs-content", "O cruzamente retornará os dados das pessoas que estejam presentes no(a) "+bases[0]+", entretanto não são encontrados no(a)"+bases[1]);
    }
}

function ocultarCampo(id){
    $(id).popover("hide");
}

$(document).ready(function(){
    $('[data-bs-toggle="popover"]').popover();
});