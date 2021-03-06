if($(".dataframe") != undefined){
    tabela = $(".dataframe");
    tabela.addClass("table table-hover");
    tabela.css("width", "100%");
    $("tr").css("text-align", "");
}

$('#alerta').hide();
$('#progresso').hide();

function regraBases(){
    base1 = $( "#base1 option:selected" ).text();
    base2 = $( "#base2 option:selected" ).text();

    if(base1 == base2){
        $.alert("As bases de dados não podem ser iguais!");
        $("#buscar").attr("disabled", true);
        $('#alerta').show();
    } else{
        $("#buscar").attr("disabled", false);
        $('#alerta').hide();
    }

    if(base1 == "Órgãos de Classe" || base2 == "Órgãos de Classe")
        $('#divOrgaos').show();
    else
        $('#divOrgaos').hide();
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

function regraPeriodo(id){
    radio = $(id).val();
    div = $('#divPeriodo');

    if(radio == "informar_periodo"){
        div.show();
    }
    else{
        div.hide();
        $("#de").val("");
        $("#ate").val("");
    }
}

function carregarDados(){

    orgao = $("#orgaos").val();
    nome = $("#nomeBeneficiario").val().trim();
    if(orgao != "medicina")
        if(nome.length < 3){
            $.alert("Para realizar um cruzamento com essa opção de orgão deve-se informar obrigatoriamente um nome com no mínimo 3 caracteres.");
            return;
        }

    getResponse();
    $('#progresso').show();
    $(".dataframe").hide();
    $("#salvarpdf").hide();
    $("#buscar").click();
}

function salvarPdf(){
    html = $("#tabelaDados").html();
    $("#htmlstring").val(html);
    $("#salvar").click();
}

function getResponse() {
    $('#loadingModal_content').html('Carregando...');
    $('#loadingModal').modal('show');
}

function displayMsgCarregamento() {
    const arrayMensagens = ['Aguarde', 'Estamos Preparando Resultados','Carregando', 'Extraindo Dados', 'Gerando Tabelas',
    'Estamos Quase Prontos', 'Em Andamento', 'Coletando Informações'];
    const msgModalCarregamento = arrayMensagens[Math.floor(Math.random() * arrayMensagens.length)];

   document.getElementById('loadingModal_content').textContent = msgModalCarregamento+"...";
}

const criarCarregamento = setInterval(displayMsgCarregamento, 10*1000);

$(document).ready(function(){
    $('[data-bs-toggle="popover"]').popover();

    console.log($('#informar_periodo').is(':checked'))
    if($('#informar_periodo').is(':checked')){
        $('#divPeriodo').show();
    }else{
        $('#divPeriodo').hide();
    }

    if($("#base1 option:selected").text() == "Órgãos de Classe" || $("#base3 option:selected").text() == "Órgãos de Classe")
        $('#divOrgaos').show();
    else
        $('#divOrgaos').hide();
});