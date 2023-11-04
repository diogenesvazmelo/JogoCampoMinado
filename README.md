# Jogo Campo Minado

## Como jogar?
Para jogar, basta realizar o download do executável "CampoMinado.exe" disponível na pasta "/dist".

## Demonstração
https://github.com/diogenesvazmelo/JogoCampoMinado/assets/24704387/56226150-0250-493d-939b-968113ba2888

## Símbolos
* (   .   ): Posição oculta no campo minado,
* (   *   ): Bomba,
* (   5   ): Quantidade de bombas ao redor da posição,
* (   L3   ): Linha 3 do campo minado,
* (   C2   ): Coluna 2 do campo minado.

## Instrução
Jogue tentando não explodir as bombas! Quanto mais posições revelar, maior o seu Score!

Para salvar seu Score, é necessária conexão com a internet.

## Comentários
Jogo desenvolvido em Python.

O ranking do histórico de pontuações (score) funciona como em fliperamas antigos, ou seja, seu nickname não é único. Portanto, seja criativo na escolha! 

Ainda sobre o ranking, vale observar que ele é salvo em um Json armazenado em um bucket no AWS S3. As chaves de acesso não foram disponibilizadas.

