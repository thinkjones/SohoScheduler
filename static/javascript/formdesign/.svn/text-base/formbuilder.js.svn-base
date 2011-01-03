function formbuilder() {
	var fb = this;
	var deleteButton = '<button type="button" class="fieldDelete" title="Delete field">delete</button>';
	this.required_prefix = 'req_';
	var required = jQuery('<span class="required">required:<input type="checkbox" /></span>');
	var txt_click_edit = 'Click to edit';
	var description = jQuery('<div class="description small">Field description: <span class="editable">'+txt_click_edit+'</span><input type="text" style="display:none"/></div>');	
	var moveHandler = jQuery('<div class="move">move</div>');
   	
   this.unamed = {};
	//assign event handlers
	jQuery("#form-fields *[rel]").bind('click', function() {
		var me = jQuery(this);
		var type = me.attr('rel');
		
		fb.createFormElement(type);
	});
	
	//add required bools
	jQuery('#formcontainer li').each( function() {
      var name = $(this).find('.fieldValue').attr('name');
      var req = required.clone();
      req.find('input').attr('checked', fields[name].required )
                       .attr('name', fb.required_prefix + name);
      req.appendTo(this);
      
      var desc = description.clone();
      desc.find('span.editable').text( fields[name].description || txt_click_edit );
      desc.find('input').val( fields[name].description || txt_click_edit );
      desc.appendTo(this);

      moveHandler.clone().appendTo(this);
   });

	//add delete buttons to existing fields
	jQuery("#formcontainer li").append(deleteButton);
	
	//remove descriptions
	jQuery("#formcontainer .field-description").remove();
	
	//save form handler
	jQuery("#save_form *[type='submit']").bind('click', function() {
	   var fieldsJSON =  fb.fieldsJSON();
      var form_clone = jQuery('#formcontainer').clone();
      
      //make description ready for publishing      
		form_clone.find('.description').each(function() {
		    var me = $(this);  
		    me.siblings('label').after('<span class="field-description">'+ me.find('input').val() +'</span>');
      });
      
      //remove the delete, required, description, move buttons
		form_clone.find(".fieldDelete, .required, .move, .description").remove();


		//make it xhtml ;) stupid innerHTML
      var x = new RegExp('(<input[^>]*type="[a-z]*"[^>]*)(>)','gi');
      var y = new RegExp('(<img[^>]*)(>)','gi');

		jQuery('#form_html').val( form_clone.html().replace(x, "$1/$2").replace(y, "$1/$2") );
		jQuery('#fieldsJSON').val( jQuery.toJSON(fieldsJSON) ); //prototype function

	});

	this.createFormElement = function( type ) {
		var fnc_name = 'create'+type;
		if ( ! fb[fnc_name] ) {
			return false;
		}
		
		if ( !this.unamed[type] ) { this.unamed[type] = 1; }
		var new_name = type + this.unamed[type]++;
		
		var html = fb[fnc_name]( new_name );
		var req = required.clone();
      req.find('input').attr('name', fb.required_prefix + new_name);
		var desc = description.clone();
		if ( fields[name]  ) {
         desc.find('span.editable').text( fields[name].description );  
      }
          
      var x = jQuery('<li>' + html + '</li>');
		x.append(req);
		x.append(desc);
		moveHandler.clone().appendTo(x);
		x.append(deleteButton);
		
		jQuery('#formcontainer').append(x);
		
		fb.makeFormEditable();
	}
	
	this.makeFormEditable = function() {
		//delete buttons
		var del_buttons = jQuery('.fieldDelete');
		del_buttons.unbind('click.formbuilder');
		del_buttons.bind('click.formbuilder', function() {
			jQuery(this).parent('li').remove();
		});
			
		//inline edit for name
		function makeLabelsEditable() {
			var iedits = jQuery('#formcontainer').find('.inlineEdit');
			if ( iedits.length == 0 ) { return; }
			jQuery('#formcontainer').find('.inlineEdit').editable( { onSubmit: function(content){
				if ( !this.hasClass('noname') ) {//we may have inline edits that do not affect the name attr
				     if (  content.current ) {
					    var fv = jQuery(this).parent().find('.fieldValue');
					    fv.attr('name', content.current);
					    
					    var req = jQuery(this).parent().find('input[name^='+fb.required_prefix+']');
					    req.attr('name', fb.required_prefix + content.current);
					 } else {
                  this.text(content.previous);
                }
				}
				
				//edit radio input value
				if ( this.hasClass('radioValue')  ) {
					jQuery(this).prev('input[type="radio"]').val(content.current);
				}
			} });
		};

		makeLabelsEditable();
		
		//make descriptions editable
		var desc_edits = jQuery('#formcontainer .description .editable');
		if (desc_edits.length) {
   		desc_edits.editable( { type:'textarea', onSubmit: function(content){
   			     if (  content.current ) {
   				    var desc_value = jQuery(this).next('input');
   				    desc_value.val(content.current);
   				 } else {
                  this.text(content.previous);
                }
   		 }});
		 }

		
		//datepickers
		jQuery('#formcontainer .datepicker').datepicker({
			showOn: "both", 
			buttonImage: "/static/javascript/jquery/img/calendar.gif", 
			buttonImageOnly: true
		});
		
		//edit selects
		var select_fields = jQuery('#formcontainer select');
		select_fields.unbind('click.formbuilder');
		select_fields.bind('click.formbuilder', function() {
			var select = jQuery(this);
			
			fb.buildOptionsEditor( select.children('option'), select, function(value) {
				return '<option value="'+ value +'">'+ value +'</option>';
			});
	
			return false;
		});
	
		//edit radios
		var radio_fields = jQuery('#formcontainer input[type="radio"]');
		radio_fields.die('click.formbuilder');
		radio_fields.live('click.formbuilder', function() {
			var radio_clicked = jQuery(this);
			var radio_container = radio_clicked.parent('.radio');
			var radios = radio_container.find('input[type="radio"]');
	
				fb.buildOptionsEditor( radios, radio_container, function(value) {
					return fb.radioOptionHtml( value, radio_clicked.attr('name') );
					}, function() { fb.makeFormEditable(); } );
	
			return false;
		});
	};
	this.makeFormEditable();
	
	
	jQuery(".fieldDelete,.del_opt").live('mouseover', function() {
		var me = jQuery(this);
      me.parent().css('background-color','#ffeff0');		
	});

	jQuery(".fieldDelete,.del_opt").live('mouseout', function() {
		var me = jQuery(this);
      me.parent().css('background-color','transparent');		
	});


};


//functions for creating different types of forms 
formbuilder.prototype.createText = function( name ) {
	var text_input = 
	'<label class="inlineEdit">' + name + ':</label>'
	+ '<input type="text" class="fieldValue text" name="' + name + '" />';
	
	return text_input;	
}

//create a radio group with default options
formbuilder.prototype.createRadio = function( name ) {
	var radio_input =
		  '<label class="inlineEdit">' + name + ':</label>'
		+ '<div class="radio">'
		+ this.radioOptionHtml( 'value1', name )
		+ this.radioOptionHtml( 'value2', name )
		+ '</div>' ;
	
	return radio_input;
}

formbuilder.prototype.radioOptionHtml = function( value, name ) {
	var radio_option = 
		'<input type="radio" class="fieldValue radio" name="' + name + '"  value="' + value + '"  />'
 	  + '<label class="inlineEdit radioValue noname">'+value+'</label>';
 	 
  return radio_option;
}



formbuilder.prototype.createSelect = function( name , multiline ) {
	var multiline = multiline ? ' multiple="multiple"': '';
	var field_type = multiline ? 'mselect': 'select';
	var select_input = 
	      '<label class="inlineEdit">' + name + ':</label>'
		+ '<select class="fieldValue ' + field_type + '" name="' + name + '" '+ multiline +'  >'
		+ '<option value="option1">option1</option>'
		+ '<option value="option2">option2</option>'
		+ '</select>';
	return select_input;
}

formbuilder.prototype.createSelectMultiline = function( name ) {
	return fb.createSelect( name, true); 
} 

formbuilder.prototype.createTextArea = function( name ) {
	var text_input = 
	'<label class="inlineEdit">' + name + ':</label>'
	+ '<textarea class="fieldValue textarea" name="' + name + '"></textarea>';
	
	return text_input;	
}

formbuilder.prototype.createDatePicker = function( name ) {
	var date_input = 
	'<label class="inlineEdit">' + name + ':</label>'
	+ '<input type="text" class="fieldValue datepicker" name="' + name + '" />';

	return date_input;
}

formbuilder.prototype.createCustomerPicker = function( name ) {
	var customer_input = 
	'<label class="inlineEdit">' + name + ':</label>'
	+ '<select class="fieldValue customer_select" name="' + name + '" >'
	+ '<option>this will be filled with customers</option>'
	+ '</select>';

	return customer_input;	
}

formbuilder.prototype.createNumber = function( name ) {
	var number_input = 
	'<label class="inlineEdit">' + name + ':</label>'
	+ '<input type="text" class="fieldValue number" name="' + name + '" />';

	return number_input;	
}

formbuilder.prototype.createEmail = function( name ) {
	var email_input = 
	'<label class="inlineEdit">' + name + ':</label>'
	+ '<input type="text" class="fieldValue email" name="' + name + '" />';

	return email_input;	
}

formbuilder.prototype.createURL = function( name ) {
	var url_input = 
	'<label class="inlineEdit">' + name + ':</label>'
	+ '<input type="text" class="fieldValue url" name="' + name + '" />';

	return url_input;	
}


/** aux functions **/

formbuilder.prototype.optionEdit = function( value ) {
	var option = 
		'<input type="text" name="" value="'+value+'" />'
	  + '<button type="button" class="del_opt" title="Remove option">delete option</button>';

	return option;
}


formbuilder.prototype.buildOptionsEditor = function( options, edited_element, onSaveHandler, onSave ) {
	var options_edit= '';
	var fb = this;
	options.each( function() {
		options_edit += '<li>'+ fb.optionEdit( jQuery(this).val() ) +'</li>';
	});
	options_edit = '<div class="select_edit">'
			    + '<ul>' + options_edit + '</ul>' 
				+ '<button type="button" class="add_opt" title="Add new option">Add option</button>'
				+ '<button type="button" class="save_edit" title="Save options">Save these options</button>'
				+ '<button type="button" class="cancel_edit" title="Cancel edit operation">Cancel</button>'
				+ '</div>';
	//make it an object			
	options_edit = jQuery(options_edit);
	
	fb.optionsEditorAttachHandlers( options_edit, edited_element, onSaveHandler, onSave );
	
	edited_element.toggle();
	edited_element.after(options_edit);
}

formbuilder.prototype.optionsEditorAttachHandlers = function( options_edit, edited_element, optionRebuilder, onSave ) {
	var options_unamed_counter = 1;	
	//attach event handlers to del options buttons			
	function attach_del_click_handlers() {
		options_edit.find('.del_opt').bind('click', function() {
			jQuery(this).parent().remove();
		});
	};
	attach_del_click_handlers();
		
	//attach handler to allow adding new options
	options_edit.children('.add_opt').bind('click', function() {
		var options_container = jQuery(this).parent('.select_edit').children('ul');
		options_container.append( 
		  	'<li>' + fb.optionEdit( 'option'+options_unamed_counter++ ) + '</li>' );	
		attach_del_click_handlers();
	});
	
	//attach handler to the save button
	options_edit.children('.save_edit').bind('click', function() {
		var parent = jQuery(this).parent('.select_edit');
		var new_options = '';
		
		//get the values and create the new options
		parent.find('input').each( function() {
			new_options += optionRebuilder( jQuery(this).val() );
		});
		
		//exit the edit mode
		//remove the edit stuff
		parent.remove();
		//set new options and make it visible again
		edited_element.html(new_options);
		edited_element.toggle();

		if ( onSave ) {
			onSave();
		}
	});
	
	//attache handler to the cancel button
	options_edit.children('.cancel_edit').bind('click', function() {
		jQuery(this).parent('div').remove();
		edited_element.toggle();
	});	
}

formbuilder.prototype.fieldsJSON = function() {
      var fields = {};
	   var processed_field_names = [];
	   var fb = this;
		jQuery('#formcontainer :input.fieldValue').each(function() {
		    var me = jQuery(this);
		    var field = {};
		    var get_input_type = function( jqo ) {
            var types = ['url', 'email', 'number', 'textarea', "text", 'radio', 'select', 'mselect', 'customer_select', 'datepicker'];
            var my_type = 'text';
            var found = 0;
            jQuery.each(types, function() {
               if ( jqo.hasClass(this) ) {
                  my_type = this;
                  found = 1; 
                  return false;
               }
            });

            //legacy code (try to guess if type not set)
            if ( !found ) {
               //try guess
               //radio
               if (  jqo.attr('type') == 'radio' ) {
                  my_type = 'radio';
               } else if ( jqo.attr('tagName').toLowerCase() == 'select' ) { //select
                  my_type = 'select';
                  if ( jqo.attr('multiple') ) {
                     my_type = 'mselect';
                  }
               } 
            }

            return my_type.toString();
          }
          //if it has a name and hasn't been added (this is for radio buttons) then added it
		    if ( me.attr('name') && -1 == jQuery.inArray( me.attr('name'), processed_field_names) ) {
		      processed_field_names.push( me.attr('name') );
            field.name = me.attr('name');
            field.type = get_input_type(me);
            field.required = me.parent().find('input[name=' + fb.required_prefix + field.name + ']').is(":checked");
            field.description = me.parent().find('.description input').val();
            
            //(m)select
            if (  field.type == 'select' ||  field.type == 'mselect' ) {
               field.options = [];
               me.find('option').each(function() {
                 field.options.push( jQuery(this).val() );
               });
            }

            //radio
            if (  field.type == 'radio' ) {
               field.options = [];
               field.options.push( me.val() ) //add myself
               me.siblings(':radio').each(function() {
                 field.options.push( jQuery(this).val() );
               });
            }          
            fields[ field['name'] ] = field;        
         }
      });

   return fields;
}

var _formbuilder;
jQuery(function(){ _formbuilder = new formbuilder();});
