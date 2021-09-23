@if ($tipo == 'sucesso')
    <div class="alert alert-success mt-3" role="alert">
        <i class="close icon"></i>
        <h5 class="alert-heading">Sucesso</h5>
        <p>{{ $corpo }}</p>
    </div>
@elseif($tipo == 'erro')
    <div class="alert alert-danger mt-3" role="alert">
        <i class="close icon"></i>
        <h5 class="alert-heading">Erro!</h5>
        <p>{{ $corpo }}</p>
    </div>
@endif

<script type="text/javascript" src="{{ asset('assets/js/mensagem.js') }}"></script>
