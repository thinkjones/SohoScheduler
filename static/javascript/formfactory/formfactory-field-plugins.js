var formFactoryFieldPlugins =
{
    textFieldBuilder: {
        name: 'text',
        create: function() {
            return '<input type="text" disabled="disabled" />';
        },
        initEdit: function() {
            return null;
        }
    },

    textareaFieldBuilder: {
        name: 'textarea',
        create: function(field) {
            field.cols = field.cols || 30;
            field.rows = field.rows || 5;
            return '<textarea disabled="disabled"  cols="' +
                    field.cols + '" rows="' + field.rows + '"></textarea>';
        },
        initEdit: function(field) {
            return '<label>cols</label><input type="text" id="textarea-cols" value="' + field.cols + '"/>' +
                     '<br />' +
                     '<label>rows</label><input type="text" id="textarea-rows" value="' + field.rows + '"/>';
        },
        onSave: function(editContainer, field, htmlField) {
            console.log('textarea.onSave');
            var cols = $(editContainer).find("#textarea-cols").val();
            var rows = $(editContainer).find("#textarea-rows").val();
            field.cols = cols;
            field.rows = rows;
            $(htmlField).find('textarea').attr('cols', cols).attr('rows', rows);
        }
    },

    checkboxFieldBuilder: {
        name: 'checkbox',
        create: function(field) {
            field.default_checked = field.default_checked || false;
            var ch = '';
            if (field.default_checked) {
                ch = 'checked="checked"';
            }
            return '<input type="checkbox" disabled="disabled"' + ch + ' />';
        },
        initEdit: function(field) {
            var ch = '';
            if (field.default_checked) {
                ch = 'checked="checked"';
            }

            return '<label>Is checked by default </label><input type="checkbox" id="default-checked" ' + ch + ' />';
        },
        onSave: function(editContainer, field, htmlField) {
            console.log('checkbox.onSave');
            var default_checked = $(editContainer).find("#default-checked").attr('checked');
            field.default_checked = default_checked;
            $(htmlField).find('input').attr('checked', default_checked);
        }
    },

    selectFieldBuilder: {
        name: 'select',
        create: function(field) {
            var options = '';
            if (typeof field.options == 'undefined' || field.options == null) {
                field.options = [
                { title: 'unnamed option 1' },
                { title: 'unnamed option 2' },
               ]
            }
            $.each(field.options, function() {
                var val = this.value || this.title;
                var selected = field.default_selected == val ? ' selected="selected"' : '';
                options += '<option value="' + val + '"' + selected + '>' + this.title + '</option>';
            });

            return '<select disabled="disabled"' + options + '</select>';
        },
        initEdit: function(field) {
            var edit_select;
            var found_default = false;
            var ch;
            var new_counter = 1;
            var onAddOption;
            var onDelOption;
            edit_select = '<table>' +
                '<tr><th>title</th><th>value</th><th>default<br />selected</th><th>actions</th></tr>';
            $.each(field.options, function() {
                var val = this.value || this.title;
                ch = field.default_selected == val ? ' checked="checked"' : '';
                if (ch.length > 0) {
                    found_default = true;
                }
                edit_select += '<tr class="select-option">' +
                    '<td><input type="text" value="' + this.title + '" class="select-title"/></td>' +
                    '<td><input type="text" value="' + val + '" class="select-value"/></td>' +
                    '<td><input type="radio" name="select-default" value="' + val + '"' + ch + '/></td>' +
                    '<td><div class="select-del-option">-</div>' +
                        '<div class="select-add-option">+</div></td>'
                '</tr>';
            });
            ch = found_default ? '' : ' checked="checked"';

            edit_select += '<tr>' +
                '<td colspan="2">check for none:</td>' +
                '<td colspan="2"><input type="radio" name="select-default" value="__none_default__"' + ch + '/></td>' +
                '</tr>';
            edit_select += '</table>';

            edit_select = $(edit_select);
            edit_select.find('.select-del-option').click(onDelOption = function() {
                $(this).parents('tr.select-option').remove();
            });

            edit_select.find('.select-add-option').click(onAddOption = function() {
                var row = $(this).parents('tr.select-option');
                var newrow = row.clone();
                newrow.insertAfter(row).find(':input').val('new option ' + new_counter++);
                newrow.find('.select-add-option').click(onAddOption);
                newrow.find('.select-del-option').click(onDelOption)
            });

            return edit_select;
        },

        onSave: function(editContainer, field, htmlField) {
            console.log('select.onSave');
            this._objFromEditor(editContainer, field);
            
            $(htmlField).find('select').replaceWith(this.create(field));
        },
        //create the js object from editor data
        _objFromEditor: function(editContainer, field) {
            var found_default = false;
            var options_rows = $(editContainer).find("tr.select-option");

            field.options = [];
            options_rows.each(function() {
                var _title = $(this).find('.select-title').val();
                var _value = $(this).find('.select-value').val();
                var option = { title: _title };
                if (_title.length == 0) {
                    return true;
                }

                if (_value.length) {
                    option.value = _value;
                } else {
                    option.value = _title;
                }

                if ($(this).find("input[name=select-default]:checked").length > 0) {
                    field.default_selected = option.value;
                    found_default = true;
                }

                field.options.push(option);
            });

            if (!found_default) {
                delete field.default_selected;
            }
        }
    }
};

//radio
//put here to inherit the select edit ;)
formFactoryFieldPlugins.radioFieldBuilder = {
    name: 'radio',
    create: function(field) {
        var options = '';
        if (typeof field.options == 'undefined' || field.options == null) {
            field.options = [
                { title: 'unnamed option 1' },
                { title: 'unnamed option 2' },
               ]
        }
        $.each(field.options, function() {
            var val = this.value || this.title;
            var selected = field.default_selected == val ? ' checked="checked"' : '';
            options += '<input name="' + field.name + '" disabled="disabled" type="radio" value="' + val + '"' + selected + '/><label>' + this.title + '</label>';
        });

        return '<span class="radio-container">' + options + '</span>';
    },
    initEdit: formFactoryFieldPlugins.selectFieldBuilder.initEdit,
    onSave: function(editContainer, field, htmlField) {
        console.log('radio.onSave');
        this._objFromEditor(editContainer, field);
        $(htmlField).find('.radio-container').replaceWith(this.create(field));
    },
    _objFromEditor: formFactoryFieldPlugins.selectFieldBuilder._objFromEditor
};


formFactoryFieldPlugins.datePickerFieldBuilder = {};
$.extend(formFactoryFieldPlugins.datePickerFieldBuilder, formFactoryFieldPlugins.textFieldBuilder);
formFactoryFieldPlugins.datePickerFieldBuilder.name = 'Date Picker';

formFactoryFieldPlugins.customerPickerFieldBuilder = {};
$.extend(formFactoryFieldPlugins.customerPickerFieldBuilder, formFactoryFieldPlugins.textFieldBuilder);
formFactoryFieldPlugins.customerPickerFieldBuilder.name = 'Customer Picker';



formFactoryFieldPlugins.emailFieldBuilder = {};
$.extend(formFactoryFieldPlugins.emailFieldBuilder, formFactoryFieldPlugins.textFieldBuilder);
formFactoryFieldPlugins.emailFieldBuilder.name = 'email';

formFactoryFieldPlugins.urlFieldBuilder = {};
$.extend(formFactoryFieldPlugins.urlFieldBuilder, formFactoryFieldPlugins.textFieldBuilder);
formFactoryFieldPlugins.urlFieldBuilder.name = 'Url';

formFactoryFieldPlugins.numberFieldBuilder = {};
$.extend(formFactoryFieldPlugins.numberFieldBuilder, formFactoryFieldPlugins.textFieldBuilder);
formFactoryFieldPlugins.numberFieldBuilder.name = 'Number';