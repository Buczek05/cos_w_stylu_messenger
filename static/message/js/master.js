function pressed(e) {
    if (e.which === 13 && !e.shiftKey) {
        send()
        e.preventDefault()
    }
}
function to_down() {
    document.documentElement.style.scrollBehavior = 'auto';
    window.scrollTo(0, document.body.scrollHeight)
}

document.onload = to_down()
document.onload = checkPreviousMessage()

function send() {
    event.preventDefault();
    url = 'http://192.168.0.179:8000/send_js/' + $('#user_pk').html()
    $.ajax({
        url: url,
        data: $('#post_message').serialize(),
        type: 'POST',
        processData: false,
    });
    $('.text_message').val('')
    setTimeout(new_message, 50)
}

async function delay(time) {
    await new Promise(resolve => setTimeout(resolve, time));
  }

function new_message(){
    url = 'http://192.168.0.179:8000/check_js/' + $('#user_pk').html()
    $.get(url).then(function (html) {
        if($(html).find('.message').length > 1){
            for(const x of Array($(html).find('.message').length).keys()){
                pk = $(html).find('#pk').eq(x).html()
                l = $(html).find('#l').eq(x).html()
                r = $(html).find('#r').eq(x).html()
                add_new_message(pk,l,r)
                to_down()
            }
        } else if($(html).find('.message').length === 1) {
            pk = $(html).find('#pk').html()
            l = $(html).find('#l').html()
            r = $(html).find('#r').html()
            add_new_message(pk,l,r)
            to_down()
        }
    })
}
var interval = setInterval(new_message, 5000)

function add_new_message(pk, l,r){
    table = document.getElementById('message_table')
    if($('.mess_pk').last().text() < pk){
        newRow = table.insertRow(table.rows.length)
        add_row(newRow, pk, l, r)
    }

}

function add_row(newRow, pk, l, r){
    var cel0 = newRow.insertCell(0)
    var cel1 = newRow.insertCell(1)
    var cel2 = newRow.insertCell(2)
    cel0.innerHTML  = pk
    if(l===''){
        cel2_span = document.createElement('span')
        cel2_span.innerHTML  = r
        cel2_span.classList.add('text_border_r')
        cel2.appendChild(cel2_span)
    }
    else{
        cel1_span = document.createElement('span')
        cel1_span.innerHTML  = l
        cel1_span.classList.add('text_border_l')
        cel1.appendChild(cel1_span)
    }
    
    cel0.classList.add('visually-hidden')
    cel0.classList.add('mess_pk')
    cel1.classList.add('to_left')
    cel2.classList.add('to_right')
}

function checkPreviousMessage(){
    url = 'http://192.168.0.179:8000/add_previous_js/' + $('#user_pk').html() + '/' + $('.mess_pk').eq(0).html()
    $.get(url).then(function (html) {
        if($(html).find('.message').length < 30){
            $('#previous').text('')
        }
    })
}
function addPrevious(){
    var table = document.getElementById('message_table')
    scl_height = document.body.scrollHeight
    url = 'http://192.168.0.179:8000/add_previous_js/' + $('#user_pk').html() + '/' + $('.mess_pk').eq(0).html()
    $.get(url).then(function (html) {
        if($(html).find('.message').length > 1){
            for(const x of Array($(html).find('.message').length).keys()){
                pk = $(html).find('#pk').eq(x).html()
                l = $(html).find('#l').eq(x).html()
                r = $(html).find('#r').eq(x).html()
                table = document.getElementById('message_table')
                newRow = table.insertRow(0)
                add_row(newRow, pk, l, r)
            }
            window.scrollTo(0,40 * $(html).find('.message').length)
        }
        else if ($(html).find('.message').length === 1){
            pk = $(html).find('#pk').html()
            l = $(html).find('#l').html()
            r = $(html).find('#r').html()
            table = document.getElementById('message_table')
            newRow = table.insertRow(0)
            add_row(newRow, pk, l, r)
        }
        if($(html).find('.message').length < 30){
            $('#previous').text('')
        }
    })
}