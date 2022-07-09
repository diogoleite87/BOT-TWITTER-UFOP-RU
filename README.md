# BOT Cardapio dos Restaurantes Universitarios da UFOP

> Bot construído utilizando API do Twitter, Web Scraping e Python!

<h4>A ideia do BOT é diariamente fazer posts referente ao cardapio dos RUs na UFOP, um dos desafios foi criar condições para que ele faça os posts corretamente, visto que o site do cardapio nem sempre é atualizado ou mesmo feito em um horario especifico. Isso foi necessario porque a forma de obter esse cardapio é feito por Web Scraping, ou seja, extraindo direto do HTML do site.</h4>

<h4>Bot hosteado pela Heroku, ativado diaramente as 11:00AM, se o cardapio ja estiver atualizado na primeira verificação sera feito o post, caso contrario, é feito uma verificação a cada 30 minutos no período de 11:00AM as 18:00PM</h4>

<h4>Para visualizar o perfil do Bot, copie ou clique no link: <a href="https://twitter.com/BotUfopRU">twitter.com/BotUfopRU</a></h4>

<h2>Features:</h2>

<ul>
    <li>Web Scraping, cardapio atualizado direto do site da UFOP;</li>
    <li>Funções para não fazer posts desnecessarios em caso de cardapio desatualizado e etc;</li>
    <li>Tentativas de 30 em 30 minutos, das 11:00 às 18:00.</li>
</ul>

<h2>Exemplo de post:</h2>

<div align="center">
    <img alt="Readme" title="Readme" src="./img/post.png" width="70%"/>
</div>