$(document).ready(function(){
    $("#btn-pesquisar").click(function(){
        $("#form-pesquisa").submit();
    });
    resultados = $("#resultados");
    var html_resultados = resultados.html();
    if(html_resultados){
        var urls = $(".url", resultados);
        urls.each(function(){
            var url = $(this).html();
            var url_md5 = $(this).attr("id");
            executa_scrapy_na_url(url, url_md5);
        });
    }
});

function executa_scrapy_na_url(url, url_md5)
{
    $.get("/google_academico_acha_autores/get_page/" + url, function(resultado_html){
        var resultado_id = "#propriedades_" + url_md5;
        resultado_id = $.trim(resultado_id);
        $(resultado_id).html(resultado_html);
    });
}
