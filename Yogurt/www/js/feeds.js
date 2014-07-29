define(function() {
    return {
	upcoming:function () {
	    $.get ("http://teamliquid.net", function (data) {
		console.log ("loly")
	    });
	}
    }
}());
