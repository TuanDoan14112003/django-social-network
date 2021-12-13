var csrf_submit_form = $('#save-changes-form > input[name=csrfmiddlewaretoken]').val()
var previousDescription = $("#id_description").val()
$('#save-changes-button').on('click', function() {
    messageHtml = `<p id="success-message" class="widget-box-title" style="color:green">Saving..., please do not close this tab</p>`
    $('#profile-widget-box').prepend(messageHtml)
    description_val = String($("#id_description").val())
    if (previousDescription != description_val || $('#id_channel_avatar').prop('files').length > 0 || $('#id_channel_cover').prop('files').length > 0) {
        var formData = new FormData();
        formData.append("description",description_val)
        formData.append("csrfmiddlewaretoken",csrf_submit_form)
        if ($('#id_channel_avatar').prop('files').length >0) {
            formData.append("channel_avatar",$('#id_channel_avatar')[0].files[0])
        }
        if ($('#id_channel_cover').prop('files').length >0) {
            formData.append("channel_cover",$('#id_channel_cover')[0].files[0])
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            processData: false,
            contentType: false,
            mimeType: 'multipart/form-data',
            data: formData,
            success: function(data) {
                $('#success-message').remove()
                messageHtml = `<p id="success-message" class="widget-box-title" style="color:green">Your channel has been saved!</p>`
                $('#profile-widget-box').prepend(messageHtml)
                $('#success-message').show(3).delay(8000).hide(1);
                previousDescription = $("#id_description").val();
            },
            error: function(data) {
                messageHtml = `<p id="success-message" class="widget-box-title" style="color:red">Failed to connect to the server</p>`
                $('#profile-widget-box').prepend(messageHtml)
                $('#success-message').show(3).delay(8000).hide(1);
            }
        })
    }
})

$('#discard-all-button').on('click',function() {
    $("#id_description").val(previousDescription)
})

var $avatarInput = $('#id_channel_avatar')
$('#id_channel_avatar').on('change',function() {
    const [file] = $avatarInput.prop('files')
    if (file) {
        var newImageUrl = URL.createObjectURL(file)
        $('#avatar-preview').prop('src',newImageUrl)
    }
})

$('#avatar-upload-box').click(function(){ 
    document.getElementById('id_channel_avatar').click()
});


var $coverInput = $('#id_channel_cover')
$('#id_channel_cover').on('change',function() {
    const [file2] = $coverInput.prop('files')
    if (file2) {

        var newCoverImageUrl = URL.createObjectURL(file2)
        $('#cover-preview').prop('src',newCoverImageUrl)
        $('#cover-preview-figure').prop('style',`background: url("${newCoverImageUrl}") center center / cover no-repeat;`)
    }
})

$('#cover-upload-box').click(function(){ 
    document.getElementById('id_channel_cover').click()
});
