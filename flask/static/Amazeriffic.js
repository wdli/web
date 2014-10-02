var main = function() {
    "use strict";
    
    var addCommentFromInput = function() {

        var $new_comment;

        if ($(".comments-input input").val() != "") {
           $new_comment = $("<p>").text($(".comments-input input").val());
           $new_comment.hide();
           $(".comments").append($new_comment);
           $new_comment.fadeIn();
           $(".comments-input input").val("");
         }
    } 


    $(".comments-input button").on("click", function(event) {
	console.log("Hello David's console");
        addCommentFromInput();
    })

    $(".comments-input input").on("keypress", function(event) {
         if (event.keyCode === 13) {
             addCommentFromInput();
         }
     })
};


$(document).ready(main);
