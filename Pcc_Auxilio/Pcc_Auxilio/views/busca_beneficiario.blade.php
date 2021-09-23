@extends('templates.menu', ['busca' => 'active'])

@section('titulo', 'Beneficíarios')

@section('content')

    <form method="POST" class="ui large form" action="{{ route('busca.beneficiarios') }}">
        @csrf
        <div class="form-group mb-3">
            <label for=" nomeBeneficiario">Nome do Beneficíario:</label>
            <input type="text" class="form-control" id="nomeBeneficiario" name="nomeBeneficiario"
                value="{{ @$nome }}" required>
        </div>
        <button type="submit" class="btn btn-primary">Buscar<i class="ui search icon"></i></button>
    </form>

@endsection("content")

@section('optional')
    @isset($beneficiarios)
        <table class="table table-striped">
            <tr>
                <th>Nome</th>
                <th>CPF</th>
                <th>NIS</th>
                <th>Responsavel</th>
                <th>CPF Responsavel</th>
                <th>NIS Responsavel</th>
                <th>Enquadramento</th>
            </tr>

            @foreach ($beneficiarios as $b)
                <tr>
                    <td>{{ $b['nome_beneficiario'] }}</td>
                    <td>{{ $b['cpf_beneficiario'] }}</td>
                    <td>{{ $b['nis'] <= 0 ? '-' : $b['nis'] }}</td>
                    <td>{{ $b['resposnsavel'] }}</td>
                    <td>{{ $b['cpf_responsavel'] <= 0 ? '-' : $b['cpf_responsavel'] }}</td>
                    <td>{{ $b['nis_responsavel'] <= 0 ? '-' : $b['nis_responsavel'] }}</td>
                    <td>{{ $b['enquadramento'] }}</td>
                </tr>
            @endforeach

        </table>
    @endisset
@endsection('optional')
