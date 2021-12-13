$(document).ready(function() {
  
  contents = document.getElementsByClassName('comment-content');
  for (let item of contents) {
  oldHTML = item.innerHTML;
  var newHtml = oldHTML.replace(new RegExp(/(^|[^@\w])@(\w{1,15})\b/g), '$1<span href="{{}}" style="color:green">@$2</span>'); 
  item.innerHTML = newHtml
}
$('.post-comment-list').on('click','.comment-reply', function(){
  $('.subcomment-input-form').css('display', 'none')
  $(this).closest('.post-comment').children('.subcomment-input-form').css('display','block')
  $(this).closest('.post-comment').children('.subcomment-input-form').find('.subcomment-input').val('')
  $(this).closest('.post-comment').children('.subcomment-input-form')[0].scrollIntoView(
    {block:'center'}
  )
})

})
