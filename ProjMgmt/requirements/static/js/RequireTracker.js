function showDialog(actionUrl){
    $.ajax({
        url: actionUrl,
        success: function(result) {
            $("#dialogModal").html(result);
            $("#dialogModal").modal({
                backdrop: false,
                show: true
            })
        },
        async:false
    }); 
}

// close Story Dialog and erase the content
function closeDialog(){
    $("#dialogModal").modal('hide');
    $("#dialogModal").html('');
}

function getStoryPointHtml(point) {
	var pointhtml = '';
	if (point <= 0) {
		pointhtml = '<i class="fa fa-star-o fw"></i><i class="fa fa-star-o fw"></i><i class="fa fa-star-o fw"></i><i class="fa fa-star-o fw"></i><i class="fa fa-star-o fw"></i>';
	} else {
		for (var i = 0; i < point; i++) {
			pointhtml += '<i class="fa fa-star fw"></i>'
		}
		for (var i = 5; i > point; i--) {
			pointhtml += '<i class="fa fa-star-o fw"></i>'
		}
	}
	return pointhtml;
}


function loadUsersInProject(projectID) {
	var taskUrl = "/req/usersinproject/" + projectID;
	var jquerySearchID = "#userlist_" + projectID;
	$.ajax({
		url: taskUrl,
		success: function(result) {
			$(jquerySearchID).html(result);
		},
		async: true
	});
}

function loadTasks(storyID) {
	var taskUrl = "/req/tasks/" + storyID;
	var jquerySearchID = "#task_" + storyID;
	$.ajax({
		url: taskUrl,
		success: function(result) {
			$(jquerySearchID).html(result);
		},
		async: true
	});
}

function loadComments(storyID) {
	var commentUrl = "/req/comments/" + storyID;
	var jquerySearchID = "#comment_" + storyID;
	$.ajax({
		url: commentUrl,
		success: function(result) {
			$(jquerySearchID).html(result);
		},
		async: true
	});
}
