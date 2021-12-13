$(document).ready(function() {
  var previousResults = '';
$('#search-main').bind("enterKey", function (e) {
    query = $('#search-main').val()
    window.location.replace(window.location.origin + '/search?q=' + query)
});


$('#search-main').keyup(function (e) {
    query = $('#search-main').val()
    if (e.keyCode == 13 && $('#search-main').val() !== '') {
        $(this).trigger("enterKey");
    }
    if (query.length >= 3) {
        $.ajax({
            url: '/channel-autocomplete/?q=' + query,
            type: "GET",
            data: {},
            success: function (data) {
              var channel_ids = []
              for (channel of data["results"]) {
                channel_ids.push(channel.id)
              }
              stringifyChannelIds = JSON.stringify(channel_ids)
                if (stringifyChannelIds != previousResults) {
                previousResults = stringifyChannelIds
                $('#channel-list-container').empty()
                for (result of data["results"]) {
                    let searchResultItemHtml = `          <!-- DROPDOWN BOX LIST ITEM -->
                    <a class="dropdown-box-list-item" href="/channel/${result.id}">
                      <!-- USER STATUS -->
                      <div class="user-status notification">
                        <!-- USER STATUS AVATAR -->
                        <div class="user-status-avatar">
                          <!-- USER AVATAR -->
                          <div class="user-avatar small no-border">
                            <!-- USER AVATAR CONTENT -->
                            <div class="user-avatar-content">
                              <!-- HEXAGON -->
                              <img width="45" height="45" style="object-fit:cover;border-radius:50%" src="${result.channel_avatar}">
                              <!-- /HEXAGON -->
                            </div>
                            <!-- /USER AVATAR CONTENT -->
                          </div>
                          <!-- /USER AVATAR -->
                        </div>
                        <!-- /USER STATUS AVATAR -->
                    
                        <!-- USER STATUS TITLE -->
                        <p class="user-status-title"><span class="bold">${result.name}</span></p>
                        <!-- /USER STATUS TITLE -->
                    
                        <!-- USER STATUS TEXT -->
                        <p class="user-status-text">${result.member_count} members</p>
                        <!-- /USER STATUS TEXT -->
                    
                        <!-- USER STATUS ICON -->
                        <div class="user-status-icon">
                          <!-- ICON GROUP -->
                          <svg class="icon-group">
                            <use xlink:href="#svg-group"></use>
                          </svg>
                          <!-- /ICON GROUP -->
                        </div>
                        <!-- /USER STATUS ICON -->
                      </div>
                      <!-- /USER STATUS -->
                    </a>
                    <!-- /DROPDOWN BOX LIST ITEM -->`   
                $('#channel-list-container').prepend(searchResultItemHtml);
                
                }}
            }
        })
    }
});
})
