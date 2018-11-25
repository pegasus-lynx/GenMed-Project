
function addField() {
    $('#addrow').css('visibility','visible');
    $('#add').css('visibility','visible');
    $('#addBtn').css({'visibility':'hidden', 'display':'none'});
    $('#cancelBtn').css({'display':'inline', 'visibility':'visible'})
    $('#subBtn').css({'display':'inline', 'visibility':'visible'})
}

function addName() {
    console.log($('#add'))
    $('#add').submit();
}

function cancelAdd() {
    $('#addBtn').css({'visibility':'visible', 'display':'inline'});
    $('#cancelBtn').css({'display':'none', 'visibility':'hidden'})
    $('#subBtn').css({'display':'none', 'visibility':'hidden'})
    $('#addrow').css('visibility','collapse');
    $('#add').css('visibility','hidden');
}