function FormFactory(options) {
    var ff = this;
    var editingLi;
  this.fields = [];
  this.registeredFields = {};
  this.options = options;
  this.options.newFieldTemplate = ''+
  '<li>'+
  '    <span title="Drag to move" class="btn move icon">move</span>'+
  '    <span title="Click to edit" class="btn edit icon">edit</span>'+
  '    <span title="Click to remove" class="btn del icon">delete</span>' +
  '    <label class="name">new text field:</label>' +
  '    <span class="required">*</span>'+
  '    <span class="description">Lorem ipsum dolor sit amet.</span>'+
  '</li>';
  
  //make list sortable
  $(options.fieldsContainerSelector).sortable(
    {
        axis: 'y',
        handle: '.btn.move',
        tolerance: 'pointer',
        opacity: 0.9,
        stop: function(e, ui) {
            var direction = 'up'; //we assume up direction
            var field = ff.fields[ui.item.get(0).ff_data.fieldRef]; ;

            if (ui.item.prev().length > 0) {
                var prev_order = ff.fields[ui.item.prev().get(0).ff_data.fieldRef].order;
                console.log(prev_order);
                console.log(field.order);
                console.log(ff.fields);
                if (prev_order > field.order) {
                    direction = 'down';
                }
            }
console.log(direction);
            if (direction == 'down') {
                var next_order_index = ff.fields.length;
                if (ui.item.next().length > 0) { //have next
                    next_order_index = ff.fields[ui.item.next().get(0).ff_data.fieldRef].order;
                }
                var prev_DOMFields = ui.item.prevAll();
                var index = next_order_index - 1;

                field.order = index; //set my new order index
                prev_DOMFields.each(function() {
                    index -= 1;
                    ff.fields[this.ff_data.fieldRef].order = index;
                });
            } else {
                var prev_order_index = -1;
                if (ui.item.prev().length > 0) {
                    prev_order_index = ff.fields[ui.item.prev().get(0).ff_data.fieldRef].order;
                }
                var next_DOMFields = ui.item.nextAll();
                var index = prev_order_index + 1;

                field.order = index; //set my new order index
                next_DOMFields.each(function() {
                    index += 1;
                    ff.fields[this.ff_data.fieldRef].order = index;
                });
            }
        }
    });


  this._createFieldHandler = function(e) {
      var name = e.data; //name of the field type to create
      var newName = ff.newName(name);
      var fieldRef = ff.fields.push(
        {
            type: name,
            fromdb: false,
            deleted: false,
            name: newName,
            description: '',
            required: false,
            order: ff.fields.length
        }) - 1;
      ff.createField(fieldRef);
      console.log('created');
  }

  this._deleteFieldHandler = function(e) {
      var confirm_detele = false;
      var doDelete = function() {
          var fieldElement = e.data;
          //remove from dom
          $(fieldElement).fadeOut(1200, function() {
              $(fieldElement).remove();
          });

          var field = ff.fields[fieldElement.ff_data.fieldRef];

          //mark as deleted
          field.deleted = true;
          //end editing of this field with no saving
          if (fieldElement.ff_data.is_editing) {
              ff.endEdit(fieldElement, false);
          }
      }
      
      $('<p>Are you sure?</p>').dialog({
          modal: true,
          buttons: { "Yes": function() { $(this).dialog("close"); doDelete(); },
              "No": function() { $(this).dialog("close"); $(e.data).removeClass('toRemove') }
          },
          resizable: false,
          draggable: false
      });
      
      $(e.data).addClass('toRemove');

  }

  this._editFieldHandler = function(e) {
      var fieldElement = e.data.el;
      var editContainer = $(ff.options.fieldEditContainerSelector);
      var specificDataDOM;
      var editingField = ff.fields[fieldElement.ff_data.fieldRef];

      if (editContainer.get(0).ff_data) {
          $(editContainer.get(0).ff_data).removeClass('editing').get(0).ff_data.is_editing = false;
      }

      ///editingLi = fieldElement;
      fieldElement.ff_data.is_editing = true;
      $(fieldElement).addClass('editing');


      editContainer.get(0).ff_data = fieldElement; //reference to the editing element

      //for specific data
      specificDataDOM = ff.registeredFields[e.data.name].initEdit(editingField);
      if (specificDataDOM == null) {
          //make specific data hidden
          editContainer.find('.specific').css('display', 'none');
      } else {
          editContainer.find('.specific').css('display', 'block').html('').append(specificDataDOM);
      }

      //general stuff
      editContainer.find('#field-name').val(editingField.name);
      editContainer.find('#field-desc').val(editingField.description);
      editContainer.find('#field-required').attr('checked', editingField.required);

      editContainer.css('visibility', 'visible');
  }

  this._saveEditHandler = function(e) {
      var editContainer = e.data;
      var editingDomEl = editContainer.ff_data;
      if (typeof editingDomEl == 'undefined' ||
          editingDomEl == null
      ) { return; }

      
      ff.endEdit(editingDomEl, true);
      editContainer.ff_data = null;
  }

  this._cancelEditHandler = function(e) {
      var editContainer = e.data;
      var editingDomEl = editContainer.ff_data;
      if (typeof editingDomEl == 'undefined' ||
          editingDomEl == null
      ) { return; }
      
      
      ff.endEdit(editingDomEl, false);
  }

  //some inits to the editContainer
  var editContainer = $(ff.options.fieldEditContainerSelector);
  editContainer.find('#edit-save').bind('click', editContainer.get(0), this._saveEditHandler);
  editContainer.find('#edit-cancel').bind('click', editContainer.get(0), this._cancelEditHandler);
}

//use to register a new form field type
FormFactory.prototype.register = function(fieldBuilder) {
    this.registeredFields[fieldBuilder.name] = fieldBuilder;
    this._createToolbarButton(fieldBuilder.name);
}

//private
FormFactory.prototype._createToolbarButton = function(name) {
    var img = 'btn-' + name + '.png';
    var alt = 'Add new ' + name + ' field';
    var title = alt;
    var toolbarButton = $('<li></li>').append(
                              $('<img/>').attr('src', img).attr('alt', alt).attr('title', title)
        ).addClass('create-' + name).bind('click', name, this._createFieldHandler);

    $(this.options.toolbarSelector).append(toolbarButton);

}

//end edit
FormFactory.prototype.endEdit = function(el, save) {
    var editContainer = $(this.options.fieldEditContainerSelector);
    $(el).removeClass('editing');
    if (save) {
        //do save actions
        var editingField = this.fields[el.ff_data.fieldRef];
        //general stuff
        editingField.name = editContainer.find('#field-name').val();
        editingField.description = editContainer.find('#field-desc').val();
        editingField.required = editContainer.find('#field-required').attr('checked');

        this.bindFieldToHtml(el);
        //call the custom fieldBuilder method
        if (this.registeredFields[editingField.type].onSave) {
            this.registeredFields[editingField.type].onSave(editContainer, editingField, el);
        }
    }
    editContainer.css('visibility', 'hidden');
}

//aux function to generate new name for a field
FormFactory.prototype.newName = function(fieldType) {
    var fieldsContainer = $(this.fieldsContainerSelector);
    var currentIndex = 1;
    var newName = fieldType + currentIndex;

    while ($('#' + newName).length != 0) {
        currentIndex = currentIndex + 1;
        newName = fieldType + currentIndex;
    }
    return newName;
}

//aux function to bind field object to html
//el - the html element
FormFactory.prototype.bindFieldToHtml = function(el) {
    var editingField = this.fields[$(el).get(0).ff_data.fieldRef];
    //general stuff
    $(el).find('label.name').text(editingField.name);
    $(el).find('.description').text(editingField.description);
    $(el).find('.required').removeClass('isrequired notrequired')
                .addClass(editingField.required ? 'isrequired' : 'notrequired');
}

//create fields from array
FormFactory.prototype.fromArray = function(afields) {
    var ff = this;
    var field = {};
    var index = 0;
    $.each(afields, function() {
        field = this;
        field.fromdb = true;
        field.deleted = false;
        field.order = index;
        ff.createField(ff.fields.push(field) - 1);
        index = index + 1;
    });
}

FormFactory.prototype.createField = function(fieldRef) {
    var field = this.fields[fieldRef];
    var name = field.type;
    var newCustomField = this.registeredFields[name].create(field);
    var newField = $(this.options.newFieldTemplate);
    var newName = this.newName(name);

    newField.children('.required').after(newCustomField);
    newField.get(0).ff_data = { fieldRef: fieldRef }

    //attach events to delete and edit buttons
    newField.children('.btn.del').bind('click', newField.get(0), this._deleteFieldHandler) //add reference to parent field
    newField.children('.btn.edit').bind('click', { el: newField.get(0), name: name }, this._editFieldHandler);

    newField.attr('id', newName);
    this.bindFieldToHtml(newField);

    $(this.options.fieldsContainerSelector).append(newField);
}

FormFactory.prototype.FieldsOrdered = function() {
   var fields_copy = clone(this.fields);
   return fields_copy.sort(function(f1, f2) {
                  return f1.order - f2.order;
               }); 
}

FormFactory.prototype.FieldsJSON = function() {
   var fields_ordered = this.FieldsOrdered();
   $.each(fields_ordered, function(i, val) {
      delete fields_ordered[i].order;
   });
   return $.toJSON(fields_ordered);
}


function clone(obj){

    if(obj == null || typeof(obj) != 'object')

        return obj;



    var temp = new obj.constructor(); // changed (twice)

    for(var key in obj)

        temp[key] = clone(obj[key]);



    return temp;

}

