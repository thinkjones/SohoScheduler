// When the document is ready set up our sortable with it's inherant function(s) 
//from http://www.wil-linssen.com/extending-the-jquery-sortable-with-ajax-mysql/

jQuery(document).ready(function() { 
  jQuery("#formcontainer").sortable({ axis: 'y', containment: 'parent', handle:'.move' }); 
}); 