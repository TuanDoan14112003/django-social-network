function vote(voteButton) {
    var $voteType = $(voteButton).attr('data-vote-type');
    var $voteDiv = $(voteButton).parent().parent()
    var $objectid = $($voteDiv).attr('data-what-id');
    var $objectType = $($voteDiv).attr('data-what-type');
    var csrf_middleware = $($voteDiv).children('input[name=csrfmiddlewaretoken]').val()
    var $score = $voteDiv.find('p.vote-score')
    var $upVoteArrow = $voteDiv.find('.upvote')
    var $downVoteArrow = $voteDiv.find('.downvote')
    var $VoteDifferentValue;
    var scoreInt = parseInt($score.text());
    var new_value;
    

    if (($voteType) === 'upvote') {
        vote_value = 1;
    } else if (($voteType) === 'downvote') {
        vote_value = -1;
    } else {
        return;
    }


    if (vote_value == -1) {
        if ($downVoteArrow.hasClass("downvoted")) { // Canceled downvote
            $downVoteArrow.removeClass("downvoted")
            $VoteDifferentValue = +1
        } else {                                // new downvote
            $downVoteArrow.addClass("downvoted")
            $VoteDifferentValue = -1
        }

        if ($upVoteArrow.hasClass("upvoted")) { // remove upvote, if any.
            $upVoteArrow.removeClass("upvoted")
            $VoteDifferentValue = -2
        }
        
    } else if (vote_value == 1) {               // remove downvote
        if ($upVoteArrow.hasClass("upvoted")) { // if canceling upvote
            $upVoteArrow.removeClass("upvoted")
            $VoteDifferentValue = -1
        } else {                                // adding new upvote
            $upVoteArrow.addClass("upvoted")
            $VoteDifferentValue = +1
        }
        if ($downVoteArrow.hasClass("downvoted")) {
            $downVoteArrow.removeClass("downvoted")
            $VoteDifferentValue = +2
        }
        
    }
    new_value = scoreInt + $VoteDifferentValue
    $score.text(new_value);
    $.ajax({
        type: 'POST',
        url: '/vote/',
        data: {
            what: $objectType,
            what_id: $objectid,
            vote_value: vote_value,
            csrfmiddlewaretoken: csrf_middleware
        }, success: function (response) {
            if (response.error == null) {
                console.log('error')
            }
        }
    })
}