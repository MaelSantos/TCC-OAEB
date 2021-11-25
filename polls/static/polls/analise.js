
regraGraficos()

function regraGraficos(){

    tipo = $("#tipoGrafico").val();

    if(tipo == "total"){
        $("#divMunicipio").hide();
    }else{
        $("#divMunicipio").show();
    }

}

function carregarDados(){

    getResponse();
    $("#buscar").click();
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
