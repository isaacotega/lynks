$(document).ready(function() {
	
	function reportPost(postBox) {
	
		Android.reportPost($(postBox).attr("id"));
	
	}
	
	function likePost(postBox, clicked) {
	
		if(clicked == "false") {
			
			var iconHolder = $(postBox).find("#icnLike");
		
			$(iconHolder).html( icons["liked"] + '<label id="content">' + (Number($(iconHolder).children("#content").html()) + 1) + '</label>').attr("clicked", "true");
		
		}
		
		if(clicked == "true") {
			
			var iconHolder = $(postBox).find("#icnLike");
		
			$(iconHolder).html( icons["like"] + '<label id="content">' + (Number($(iconHolder).children("#content").html()) - 1) + '</label>').attr("clicked", "false");
		
		}
		
		requestAction($(postBox).attr("id"), "like");
	
	}

	function dislikePost(postBox, clicked) {
	
		var iconHolder = $(postBox).find("#icnDislike");
		
		if(clicked == "false") {
			
			$(iconHolder).html( icons["disliked"] + '<label id="content">' + (Number($(iconHolder).children("#content").html()) + 1) + '</label>').attr("clicked", "true");
		
		}
		
		if(clicked == "true") {
			
			$(iconHolder).html( icons["dislike"] + '<label id="content">' + (Number($(iconHolder).children("#content").html()) - 1) + '</label>').attr("clicked", "false");
		
		}
	
		requestAction($(postBox).attr("id"), "dislike");
	
	}
	
	function requestAction(postId, action) {
	
		$.ajax({
			type: "POST",
			url: "../ajax-handlers/post-actions",
			dataType: "JSON",
			data: {
				usercode: usercode,
				postId: postId,
				action: action
			},
			success: function(response) {
			
		//		alert( JSON.stringify(response) );
			
			}
		});
	
	}

	function loadPosts() {

		$.ajax({
			type: "POST",
			url: "../ajax-handlers/posts",
			dataType: "JSON",
			data: {
				usercode: usercode
			},
			success: function(response) {
			
				$("#dotsLoader").show();
	
				$("#lynksSplash").hide();
	
				var postsData = response;
			
				for(var i = 0; i < postsData.length; i++) {
			
					var newBox = $(postBox);
			
					$(newBox).attr({
						id: postsData[i]["postId"]
					});
				
					$(newBox).children("#head").children("#title").html(postsData[i]["title"]);
				
					$(newBox).children("#body").children("#descriptionHolder").children("#description").html(postsData[i]["body"]);
				
					$(newBox).children("#body").children("#linkHolder").children("#link").attr("href", "../redirector?url=" + postsData[i]["link"]).html(postsData[i]["link"]);
				
					$(newBox).children("#foot").children("#iconHolder").find("#icnLike").html( (postsData[i]["user"]["liked"] ? icons["liked"] : icons["like"] ) + '<label id="content">' + postsData[i]["statistics"]["likes"] + '</label>').attr("clicked",  (postsData[i]["user"]["liked"] ? "true" : "false") ).click(function() {
					
						likePost($(this).parents(".box"), $(this).attr("clicked") );
				
					});
				 
					$(newBox).children("#foot").children("#iconHolder").find("#icnDislike").html( (postsData[i]["user"]["disliked"] ? icons["disliked"] : icons["dislike"] ) + '<label id="content">' + postsData[i]["statistics"]["dislikes"] + '</label>').attr("clicked",  (postsData[i]["user"]["disliked"] ? "true" : "false") ).click(function() {
					
						dislikePost($(this).parents(".box"), $(this).attr("clicked") );
				
					});
				 
					$(newBox).children("#foot").children("#iconHolder").find("#icnViews").html( icons["views"] + '<label id="content">' + postsData[i]["statistics"]["views"] + '</label>');
				 
					$(newBox).children("#foot").children("#iconHolder").find("#icnReport").html( (postsData[i]["user"]["reported"] ? icons["reported"] : icons["report"] ) + '<label id="content">' + postsData[i]["statistics"]["reports"] + '</label>').click(function() {
					
						reportPost($(this).parents(".box"));
				
					});
				 
				 
					$("#container").append( newBox );
			
				}
			
			},
			error: function(response) {
		
				alert( response.statusText )
			
			}
		});
	
	}
	
	var icons = {
		like: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M21.406 9.558c-1.21-.051-2.87-.278-3.977-.744.809-3.283 1.253-8.814-2.196-8.814-1.861 0-2.351 1.668-2.833 3.329-1.548 5.336-3.946 6.816-6.4 7.401v-.73h-6v12h6v-.904c2.378.228 4.119.864 6.169 1.746 1.257.541 3.053 1.158 5.336 1.158 2.538 0 4.295-.997 5.009-3.686.5-1.877 1.486-7.25 1.486-8.25 0-1.648-1.168-2.446-2.594-2.506zm-17.406 10.442h-2v-8h2v8zm15.896-5.583s.201.01 1.069-.027c1.082-.046 1.051 1.469.004 1.563l-1.761.099c-.734.094-.656 1.203.141 1.172 0 0 .686-.017 1.143-.041 1.068-.056 1.016 1.429.04 1.551-.424.053-1.745.115-1.745.115-.811.072-.706 1.235.109 1.141l.771-.031c.822-.074 1.003.825-.292 1.661-1.567.881-4.685.131-6.416-.614-2.239-.965-4.438-1.934-6.959-2.006v-6c3.264-.749 6.328-2.254 8.321-9.113.898-3.092 1.679-1.931 1.679.574 0 2.071-.49 3.786-.921 5.533 1.061.543 3.371 1.402 6.12 1.556 1.055.059 1.024 1.455-.051 1.584l-1.394.167s-.608 1.111.142 1.116z"/></svg>',
		
		liked: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M5 22h-5v-12h5v12zm17.615-8.412c-.857-.115-.578-.734.031-.922.521-.16 1.354-.5 1.354-1.51 0-.672-.5-1.562-2.271-1.49-1.228.05-3.666-.198-4.979-.885.906-3.656.688-8.781-1.688-8.781-1.594 0-1.896 1.807-2.375 3.469-1.221 4.242-3.312 6.017-5.687 6.885v10.878c4.382.701 6.345 2.768 10.505 2.768 3.198 0 4.852-1.735 4.852-2.666 0-.335-.272-.573-.96-.626-.811-.062-.734-.812.031-.953 1.268-.234 1.826-.914 1.826-1.543 0-.529-.396-1.022-1.098-1.181-.837-.189-.664-.757.031-.812 1.133-.09 1.688-.764 1.688-1.41 0-.565-.424-1.109-1.26-1.221z"/></svg>',
		
		dislike: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="transform: rotate(-180deg)"><path d="M21.406 9.558c-1.21-.051-2.87-.278-3.977-.744.809-3.283 1.253-8.814-2.196-8.814-1.861 0-2.351 1.668-2.833 3.329-1.548 5.336-3.946 6.816-6.4 7.401v-.73h-6v12h6v-.904c2.378.228 4.119.864 6.169 1.746 1.257.541 3.053 1.158 5.336 1.158 2.538 0 4.295-.997 5.009-3.686.5-1.877 1.486-7.25 1.486-8.25 0-1.648-1.168-2.446-2.594-2.506zm-17.406 10.442h-2v-8h2v8zm15.896-5.583s.201.01 1.069-.027c1.082-.046 1.051 1.469.004 1.563l-1.761.099c-.734.094-.656 1.203.141 1.172 0 0 .686-.017 1.143-.041 1.068-.056 1.016 1.429.04 1.551-.424.053-1.745.115-1.745.115-.811.072-.706 1.235.109 1.141l.771-.031c.822-.074 1.003.825-.292 1.661-1.567.881-4.685.131-6.416-.614-2.239-.965-4.438-1.934-6.959-2.006v-6c3.264-.749 6.328-2.254 8.321-9.113.898-3.092 1.679-1.931 1.679.574 0 2.071-.49 3.786-.921 5.533 1.061.543 3.371 1.402 6.12 1.556 1.055.059 1.024 1.455-.051 1.584l-1.394.167s-.608 1.111.142 1.116z"/></svg>',
		
		disliked: '',
		
		views: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12.015 7c4.751 0 8.063 3.012 9.504 4.636-1.401 1.837-4.713 5.364-9.504 5.364-4.42 0-7.93-3.536-9.478-5.407 1.493-1.647 4.817-4.593 9.478-4.593zm0-2c-7.569 0-12.015 6.551-12.015 6.551s4.835 7.449 12.015 7.449c7.733 0 11.985-7.449 11.985-7.449s-4.291-6.551-11.985-6.551zm-.015 3c-2.21 0-4 1.791-4 4s1.79 4 4 4c2.209 0 4-1.791 4-4s-1.791-4-4-4zm-.004 3.999c-.564.564-1.479.564-2.044 0s-.565-1.48 0-2.044c.564-.564 1.479-.564 2.044 0s.565 1.479 0 2.044z"/></svg>',
		
		report: '',
	
		reported: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M15.526 11.409c-1.052.842-7.941 6.358-9.536 7.636l-2.697-2.697 7.668-9.504 4.565 4.565zm5.309-9.867c-2.055-2.055-5.388-2.055-7.443 0-1.355 1.356-1.47 2.842-1.536 3.369l5.61 5.61c.484-.054 2.002-.169 3.369-1.536 2.056-2.055 2.056-5.388 0-7.443zm-9.834 17.94c-2.292 0-3.339 1.427-4.816 2.355-1.046.656-2.036.323-2.512-.266-.173-.211-.667-.971.174-1.842l-.125-.125-1.126-1.091c-1.372 1.416-1.129 3.108-.279 4.157.975 1.204 2.936 1.812 4.795.645 1.585-.995 2.287-2.088 3.889-2.088 1.036 0 1.98.464 3.485 2.773l1.461-.952c-1.393-2.14-2.768-3.566-4.946-3.566z"/></svg>'
	
	}
	
	loadPosts();
	
	$(window).on('scroll', function(e){
		
		if( (window.innerHeight + window.scrollY) >= document.body.scrollHeight ) {

			loadPosts();

		}

	});

});			