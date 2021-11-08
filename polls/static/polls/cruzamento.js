if($(".dataframe") != undefined){
    tabela = $(".dataframe");
    tabela.addClass("table table-hover");
    tabela.css("width", "100%");
    $("tr").css("text-align", "");
}

$('#bases').selectpicker();
$('#bases').css("width", "100%")
$('#alerta').hide()

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

$(document).ready(function(){
    $('[data-bs-toggle="popover"]').popover();
});