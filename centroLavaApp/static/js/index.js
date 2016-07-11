$( document ).ready(function() {
/*     generateButtonTags(); */
});

function generateButtonTags(){
	var list = ["Financial Challenge", "Poor English", "Government Regulations", "Training & Workshop", "Tax", "Credit Health", "Legal Issues", "Technical Support", "Loan", "Social Media and Website", "Sales", "Bookkeeping & Accounting"]
	var $tagsGroup = $('<div class="form-group"></div>');
	var buttonTags = [];
	$.each(list, function(index, value){
		$tagsGroup.append($('<a class="btn btn-primary tag" href="#" role="button">{0}</a>'.format(value)));
	})
	$tagsGroup.insertBefore( ".submitButton" );
}

$('form').on('click', '.tag', function(){
	$(this).toggleClass("btn-success");
})

$("#initForm").submit(function(){
	var tageSelected = $('.tag.btn-success');
	$.each(tageSelected, function(i, v){
		var tagName = $(this).text()
    var input = $("<input>").attr({"type":"hidden","name":"selected[]"}).val(tagName); 
    $('#initForm').append(input);  
  });
  console.log(tageSelected.length);
/*   return false; */
});