$('#join-group-button').on('click', function() {

    let csrf_join_group = $('#join-group-button > input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        url: window.location.pathname + 'join-channel/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: csrf_join_group,
        },
        success: function(response) {
            $('#join-group-button').remove()
        }
})
})


$('#insert-photo-button').on('click', function() {
    document.getElementById('id_image').click()
})

var $imageInput = $('#id_image')
$('#id_image').on('change',function() {
    document.getElementById('image-preview').style.display = 'block';
    const [file3] = $imageInput.prop('files')
    if (file3) {
        var newImageUrl = URL.createObjectURL(file3)
        $('#image-preview').prop('src',newImageUrl)
    }
})

$('#discard-image-button').on('click', function() {
    $('#id_image').val('')
    $('#image-preview').prop('src','')
})

$('#discard-button').on('click', function() {
    $('#id_title').val('')
    $('#id_content').val('')
    $('#id_image').val('')
    $('#image-preview').prop('src','')
})