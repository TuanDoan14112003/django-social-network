function connect() {
  if (location.protocol == "http:") {
    scheme = "ws://"

  } else if (location.protocol == "https:") {
    scheme = "wss://"
  }
  var likeCommentNotificationSocket = new WebSocket(
    scheme
    + window.location.host
    + '/ws/like-comment-notification/'
);

likeCommentNotificationSocket.onopen = function (e) {
  // fetchNotifications();
  console.log('open')
};

likeCommentNotificationSocket.onclose = function(e) {
  console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
  setTimeout(function() {
    connect();
  }, 1000);
};

likeCommentNotificationSocket.onmessage = function (event) {
  let data = JSON.parse(event.data);
  if (data['command'] === 'notifications') {
  } else if (data['command'] === 'new_like_comment_notification') {
    createLikeCommentNotification(JSON.parse(data['notification']))
    if (!$('#mobile-notification-icon').attr("class").split(/\s+/).includes('unread')) {
      $('#mobile-notification-icon').addClass('unread')
    }
}};

createLikeCommentNotification = function(notificationData) {

  let notificationHtml =   `                <!-- DROPDOWN BOX LIST ITEM -->
  <div class="dropdown-box-list-item unread">
    <!-- USER STATUS -->
    <div class="user-status notification">
      <!-- USER STATUS AVATAR -->
      <a class="user-status-avatar" href="${notificationData.actor.profile.my_absolute_url}">
        <!-- USER AVATAR -->
        <div class="user-avatar small no-outline">
          <!-- USER AVATAR CONTENT -->
          <div class="user-avatar-content">
            <!-- HEXAGON -->
            <img style="width:40px;height:40px;object-fit:cover;border-radius:50%" src="${notificationData.actor.profile.avatar}"></img>
            <!-- /HEXAGON -->
          </div>
          <!-- /USER AVATAR CONTENT -->
      
        </div>
        <!-- /USER AVATAR -->
      </a>
      <!-- /USER STATUS AVATAR -->
  
      <!-- USER STATUS TITLE -->
      <p class="user-status-title"><a class="bold" href="${notificationData.actor.profile.my_absolute_url}">${notificationData["actor"]["username"]}</a> <a class="highlighted" style="font-family:Robot, sans-serif;font-weight:500" href="${notificationData["my_absolute_url"]}">${notificationData["verb"]}</a></p>
      <!-- /USER STATUS TITLE -->
  
      <!-- USER STATUS TIMESTAMP -->
      <p class="user-status-timestamp">Just now</p>
      <!-- /USER STATUS TIMESTAMP -->
  
      <!-- USER STATUS ICON -->
      <div class="user-status-icon">
        <!-- ICON COMMENT -->
        <svg class="icon-comment">
          <use xlink:href="#svg-comment"></use>
        </svg>
        <!-- /ICON COMMENT -->
      </div>
      <!-- /USER STATUS ICON -->
    </div>
    <!-- /USER STATUS -->
  </div>
  <!-- /DROPDOWN BOX LIST ITEM -->`;
  $('#notification-list').find('.simplebar-content').prepend(notificationHtml);
  if (!$('#notification-icon').attr("class").split(/\s+/).includes('unread')) {
    $('#notification-icon').addClass('unread')
  }
}
}

$('#notification-icon').on('click',function() {
  var csrf_notification = $("#notification-icon > input[name=csrfmiddlewaretoken]:first").val();
  $.ajax({
    url: '/read-all-notification/',
    type: 'POST',
    data: {
      csrfmiddlewaretoken:csrf_notification
    },
    success: function (data) {
      $('#notification-icon').removeClass('unread')
    }
  })
})

$('#mobile-notification-icon').on('click',function(e) {
  var csrf_notification = $("#mobile-notification-icon > input[name=csrfmiddlewaretoken]:first").val();
  var notification_url = $(this).attr('data-next-url')
  $.ajax({
    url: '/read-all-notification/',
    type: 'POST',
    data: {
      csrfmiddlewaretoken:csrf_notification
    },
    success: function (data) {
      window.location.replace(notification_url)

    }
  })
})

connect()