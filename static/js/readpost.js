

// var waypoints = $('.post-item').waypoint({
//     handler: function(direction) {
//         csrf_read_post = $(this.element).find('input[name=csrfmiddlewaretoken]').val()
//         var post_id = $(this.element).find('.reaction-options-dropdown-trigger').attr('data-what-id')
//         $.ajax({
//             type: 'POST',
//             url: '/read-post/',
//             data: {
//                 csrfmiddlewaretoken:csrf_read_post,
//                 post_id: post_id
//             },
//             error: function(response){
//                 alert('something went wrong')
//             }
//         })
//     }
// })