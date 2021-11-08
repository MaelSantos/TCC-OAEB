if($(".dataframe") != undefined){
    tabela = $(".dataframe");
    tabela.addClass("table table-hover");
    tabela.css("width", "100%");
    $("tr").css("text-align", "");
}

$('#alerta').hide();
$('#alerta').hide();

function regraBases(){
    base1 = $( "#base1 option:selected" ).text();
    base2 = $( "#base2 option:selected" ).text();

    if(base1 == base2){
        $.alert("As bases de dados não podem ser iguais!");
        $("#buscar").attr("disabled", true);
        $('#alerta').show()
    } else{
        $("#buscar").attr("disabled", false);
        $('#alerta').hide()
    }
}

function exibirPopover(id){

    base1 = $( "#base1 option:selected" ).text();
    base2 = $( "#base2 option:selected" ).text();

    if(base1 == "")
        $(id).attr("data-bs-content", "Selecione uma base de dados.");
    else if(base2 == "")
        $(id).attr("data-bs-content", "Somente 1 base selecionada, não ocorrerá nenhum cruzamente, somente será retornado as informações do(a) "+base1+".");
    else {
        tipo = $("#tipoCruzamento").val();
        if(tipo == "intersecao")
            $(id).attr("data-bs-content", "O cruzamento retornará os dados das pessoas que estejam presentes em ambas as bases de dados. Presentes no(a) "+base1+" e no(a) "+base2+".");
        else if(tipo == "diferenca")
            $(id).attr("data-bs-content", "O cruzamente retornará os dados das pessoas que estejam presentes no(a) "+base1+", entretanto não são encontrados no(a) "+base2+".");
    }
}

function ocultarCampo(id){
    $(id).popover("hide");
}

function salvarPdf(){
    html = $("#tabelaDados").html();

    $.ajax({
        url: "/polls/cruzamento/salvar/pdf/",
        method: "POST",
        data: { "htmlstring": html},
        success: function(data) {
            console.log(data);
        },
        error: function( request, status, error ){
            console.log(error);
        }

    });
}

function regraPeriodo(id){
    radio = $(id).val();
    div = $('#divPeriodo');
    console.log(radio);

    if(radio == "informar_periodo"){
        div.show();
    }
    else{
        div.hide();
        $("#de").val("");
        $("#ate").val("");
    }

}

$(document).ready(function(){
    $('[data-bs-toggle="popover"]').popover();

    if($('input[name="tipo_periodo"]:checked') != undefined){
        $("#todo_periodo").attr('checked', true);
        $('#divPeriodo').hide();
    } else
        $('#divPeriodo').show();
});