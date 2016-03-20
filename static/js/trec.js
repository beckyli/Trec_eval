$('body').on('click', '.order-but', function(event){

    var order_by, direction, researchers, tracks, results_for, researcher_or_task;
    var researchers  = new Array();
    var headers = new Array();
    var tracks = new Array();
    var tasks = new Array();

    $(".order-but").each(function(){
       headers.push([$(this).text().replace(/\s/g, ''), $(this).attr('data-order-by')]);
    });

     $("td").each(function(){

        if($(this).attr('data-username')!= undefined)
        {
            researchers.push($(this).attr('data-username'));
        }
       if($(this).attr('data-track-slug')!= undefined)
       {
            tracks.push($(this).attr('data-track-slug'));
       }
       if($(this).attr('data-task-id')!= undefined)
       {
            tasks.push($(this).attr('data-task-id'));
       }
       if($(this).attr('data-researcher-or-task') != undefined)
       {
            researcher_or_task = $(this).attr('data-researcher-or-task');
       }
    });

    direction = $(this).attr("data-direction");
    order_by = $(this).attr("data-order-by");
    results_for = $('#results-for').text().substring(24)

    data = {
        'researchers': $.unique(researchers),
        'tracks': $.unique(tracks),
        'tasks': $.unique(tasks),
        'order_by': order_by,
        'direction': direction,
        'headers': headers,
        'results_for': results_for,
        'researcher_or_task': researcher_or_task,
    }

    $('.data_row').each(function(){
        $(this).html(null)
    });

    $('#loading_image').css('display', 'block');
    $.ajax({
            type: 'get',
            url: '/ajax_get_res/',
            data: {'data': JSON.stringify(data)},
            success: function(data, text){

            $('#results_table').html(data);
            $('#loading_image').css('display', 'none');
        },
        error: function(request, status, error){
           $('#results_table').html('<h1 class="text-danger">Oops there\'s been an error, sorry about that.</h1>');
           $('#loading_image').css('display', 'none');
        }
        });
})