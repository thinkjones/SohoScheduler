    
/**
 * jQuery Soho Survey Form Builder Plugin
 * 
**/


jQuery(function($){

    // -------------------------------------------------------
	// Private Variables
	// -------------------------------------------------------

    //////////////////////////////////////////////////////
    // Init Values
    var defaults = {
        id: 0,
        save_url: false,
        load_url: false,
        load_data: false,
        formType: 'form',
        form_design_data: false,
        form_data: false,
        form_post_url: false,
        toolbox_control: 'ul',
        runtime_form_placeholder: '',
        menu_control_placeholder: '',
        save_handler: '',
        easysort_handler: '',
        testdrive_handler: '',
        setupscreen_mode:'design',
        controls: {
            'text':{'DisplayName':'Single Line Text','ControlType':'text','HtmlControl':'input','HtmlControlType':'text'},
            'textarea':{'DisplayName':'Paragraph Text','ControlType':'textarea','HtmlControl':'textarea','HtmlControlType':''},
            'narrative':{'DisplayName':'Help Text','ControlType':'narrative','HtmlControl':'div','HtmlControlType':''},
            'radio':{'DisplayName':'Multiple Choice','ControlType':'radio','HtmlControl':'div','HtmlControlType':''},
            'checkbox':{'DisplayName':'Checkboxes','ControlType':'checkbox','HtmlControl':'div','HtmlControlType':''},
            'select':{'DisplayName':'Dropdown List','ControlType':'select','HtmlControl':'div','HtmlControlType':''},
            /* 'rank':{'DisplayName':'Rating','ControlType':'rank','HtmlControl':'input','HtmlControlType':''}, */
            'date':{'DisplayName':'Date','ControlType':'date','HtmlControl':'input','HtmlControlType':'date'},
            'time':{'DisplayName':'Time','ControlType':'time','HtmlControl':'input','HtmlControlType':'time'}
         }

    };

    var formTypes = {
            'survey':{'type':'survey','TitleLabel':'Question Name:','HelpLabel':'Question','OptionLabel':'Multiple Choices','TitleWatermark':'-enter your question name here-','HelpWatermark':'-enter your question here-'},
            'form':{'type':'form','TitleLabel':'Label','HelpLabel':'Help Text','OptionLabel':'Multiple Choices','TitleWatermark':'-enter the field name-','HelpWatermark':'-enter some help text to assist your users when entering this form field-'}
        };

    var namingConventionTypes = {
        //Parent control that encapsulates all
        'P':['pa','pid'],               // THe main design container control for settings

        //Design time controls
        'D':['se','pid'],               // THe main design container control for settings
        'DL':['se','tb','lb','pid'],   // Design time input box for     - label of control
        'DH':['se','tb','ht','pid'],   // Design time input box for     - help text of control
        'DR':['se','ch','rq','pid'],   // Design time checkbox box      - required control
        'DRD':['se','dv','rq','pid'],  // Design time wrapper div       - required control
        'DCTL':['se','dvul','ct','pid'],  // Design time option container   - option controls select / radio / checkbox
        'DOP':['se','li','ls','pid','cid'],  // Design time option             - option controls select / radio / checkbox
        'DOPL':['se','tb','ls','pid','cid'],  // Design time option             - option controls select / radio / checkbox

        // Design time links and actions that don't appear in runtime controls
        'DC':['se','bt','ct','pid'],  // Design time option             - Delete whole control
        'DAO':['se','bt','ao','pid'],  // Design time option             - Add - option controls select / radio / checkbox
        'DRO':['se','bt','ao','pid','cid'],  // Design time option             - Remove - option controls select / radio / checkbox
        'DANC':['se','ln','an','pid'],  // Main Control Option - Used as an anchor to scroll to

         // Runtime controls
        'R':['rt','pid'],               // THe main runtimr container control for the runtime control
        'RL':['rt','tb','lb','pid'],    // Run time input box for  - label of control
        'RH':['rt','tb','ht','pid'],    // Run time input box for  - help text of control
        'RR':['rt','ch','rq','pid'],    // Run time checkbox box   - required control
        'RRD':['rt','dv','rq','pid'],   // Run time wrapper div    - required control
        'RHID':['rt','tb','hd','pid'],    // Run time input box for  - label of control
        'RW':['rt','dv','wr','pid'],    // Run time Wrapper around main control
        'RCTL':['rt','dvul','ct','pid'],  // Run time Main Control   -
        'ROP':['rt','li','ls','pid','cid'],     // Run time time option             - option controls select / radio / checkbox
        'ROPI':['rt','tb','ls','pid','cid'],    // Run time input box
        'ROPL':['rt','lb','ls','pid','cid'],     // Run time option label
        'RADD':['rt','bt','ad','pid']     // Run add new button
    };

    var elID = 0;
    var formid = 0;
    var last_id = 0;
    var hr_clearboth = '<hr class="clearboth" />';
    var opts = null;
    var formTypeAttributes = null;
    var CurrentScreenMode = null;
    

    // -------------------------------------------------------
	// Public Functions
	// -------------------------------------------------------
	$.fn.surveyFormBuilder = function(options) {

        //Merged passed and default options
        $.fn.surveyFormBuilderOptions(options);

        //Render form once to the first element returned by the this.each
        if(this.length > 0){
            var this_form = this[0];
            formid = options.formid;
            var newDesigner = RenderClass($(this_form),options);
            newDesigner.initialize();
        }
    };

    $.fn.surveyFormBuilderOptions =  function(options) {
        //Add any new controls
        if(options.controls){
            options.controls = $.extend(defaults.controls, options.controls);
        }

        opts = $.extend(defaults, options);

        
        formTypeAttributes = formTypes[opts.formType];
        CurrentScreenMode = opts.setupscreen_mode;
    };

    $.fn.surveyFormLoadDataByControl = function(calling_control, pkid, mnemonic) {
        
        // Calcualate parent control from child object
        var newRuntime = RenderClass();
        var controlHtmlID = newRuntime.GetControlParentWrapperID(calling_control,'control_mnemonic','R','id');
        var wrapperObject = $('#' + controlHtmlID);
        formid = $(wrapperObject).attr('form_id')
        var controlID = $(wrapperObject).attr('controlID');
        var field_name = $(wrapperObject).attr('field_name');

        //Get Parent Wrapper Object
        var form_control_data = {
            'control_id': controlID,
            'control_type':$(wrapperObject).attr('controltype'),
            'display_type':$(wrapperObject).attr('displaytype'),
            'value_string':mnemonic,
            'value_text':'',
            'value_int':pkid
        }


        newRuntime.loadControlWithData(field_name, form_control_data);
    };


    // -------------------------------------------------------
	// Render Class
	// -------------------------------------------------------
    function RenderClass(ul_obj, options){
        //Preapte and initialitzeve
        if(ul_obj){
            this.ul_obj = ul_obj;
        }
        if(options){
            this.opts = options;
        }


        //Main Rendering
        this.initialize = function(){
            //this.ul_obj = ul_obj;
            //this.opts = options;
            if(opts.setupscreen_mode=='runtime'){
                initializeRuntime();
             }else{
                initializeDesigner();
             }
        }

        //In runtime form design is passed when rendered
        this.initializeRuntime = function(){
            //Empty current object
            //$(ul_obj).html('');

            // Extract the form design data
            opts.form_design_data = opts.form_design_data; //['formdesign'];
            opts.form_data = opts.form_data;

            //Render Form Into Contorl
            var loopControlID = 0;  //assume it starts at zero and increments by one - doing it this way so the sort works correctly
            for(control in opts.form_design_data){
                // Get Control Item
                var controlItem = opts.form_design_data[loopControlID];
                loopControlID++;
                if(controlItem.id > elID){elID = controlItem.id;}

                //Get ControlID
                var controlID = controlItem.id;

                //Ensure the name is encoded correctly
                //controlItem.label =  controlItem.label.replace(/'/g,"&apos;");


                //Create runtime placeholder
                var fbRuntime = create_FB_Div().attr('id',GetObjectID('R',controlID)).addClass('fb-runtime');
                //Add Control Information
                fbRuntime.attr('controltype',controlItem.controlType)
                            .attr('displaytype',controlItem.displayType)
                            .attr('controlID',controlID)
                            .attr('control_mnemonic','R')
                            .attr('form_id',formid)
                            .attr('field_name',controlItem.label);
                var jLI =  $('<li></li>').addClass('fb-item').append(fbRuntime);
                $(ul_obj).append($(jLI));

                //Place Control in Placeholder
                renderRuntimeControlIntoPlaceholder(controlID,controlItem.controlType,false,controlItem);


                //Add RUntime
                if(controlItem.choices){
                    var newOptionID = 0;
                    if(controlItem.controlType!='radio'){
                        createRuntimeOption(controlID,"",controlItem.controlType,{'text':"--- Please Select ---",'selected':true},controlItem);
                    }
                    for(choice in controlItem.choices){
                        var optionAttrs = controlItem.choices[choice];
                        createRuntimeOption(controlID,newOptionID,controlItem.controlType,optionAttrs,controlItem);
                        newOptionID ++;
                    }
                }

                var rtContainer = GetObjectID('R',controlID);
                //$('#' + rtContainer).append("&nbsp;");


                
                elID++;
            }

            //Put Data Into Form
            loadFormWithData();


            $(ul_obj).show();
        }

        this.initializeDesigner = function(){
    
            //Empty current object
            $(ul_obj).html('');

            //Setup ul as Sortable
            $(ul_obj).sortable({
                    handle : '.movebutton',
                    axis : 'y',
                    placeholder: 'ui-state-highlight',
                    forcePlaceholderSize: true,
                    start: function (){$('.toggle-fb-holder').html('show options').addClass('toggle-fb-holder-closed');},
                    update : function () {
                    updateSort();
                  }
             });

            //Add Debug Window
            $(ul_obj).after('<div id="DebugWindow"></div>');

            // Save Form Handler
            $(opts.save_handler).click(function(){saveDesignForm(ul_obj);});

            //Easy sort handler
            $(opts.easysort_handler).click(function(){SetupScreen_EasySort(ul_obj);});

            //test Drive handler
            $(opts.testdrive_handler).click(function(){SetupScreen_TestDrive(ul_obj);});

            //Design Mode Handler
            $(opts.design_handler).click(function(){SetupScreen('design');});

            //Create the toolbox
            var objToolbox = createToolboxControl();

            // Add Toolbox To Screen
            if(opts.menu_control_placeholder){
                $(opts.menu_control_placeholder).find('.ToolbarContents').append($(objToolbox)).append(hr_clearboth);
            }else{
                var objTopToolbox = objToolbox.cloneNode(true);
                var objBotToolbox = objToolbox.cloneNode(true);
                $(objTopToolbox).attr('name','field_control_top');
                $(objBotToolbox).attr('name','field_control_bot');
                var objTopDiv = document.createElement('div');
                $(objTopDiv).append(objTopToolbox);
                var objBottomDiv = document.createElement('div');
                $(objBottomDiv).append(objBotToolbox);
                $(this).before($(objTopDiv).html() + hr_clearboth);
                $(this).after($(objBottomDiv).html() + hr_clearboth);
            }

            //Add function so when a toolbox item is clicked the object is added to form
            $('.field_control>li').click(function_add_control_to_form);

            // Load Data If Available
            if(opts.form_design_data){
                opts.form_design_data = opts.form_design_data['formdesign'];
                SetupFormFromDesignData(opts.form_design_data);
            }
        };

        this.SetupFormFromDesignData = function(formControlData){
            for(control in formControlData){
                var controlItem = formControlData[control];
                if(controlItem.id > elID){elID = controlItem.id;}
                AddFormElement(controlItem.id,controlItem.controlType,controlItem)
            }
            elID++;
            $('.fb-holder').slideUp();
            $('a.toggle-fb-holder').html('show options');
        }


        
        this.saveDesignForm = function(){
            // saves the serialized data to the server
            if(opts.save_url){

                //Show Ajax button
                $(opts.save_handler).fadeOut("fast",function(){
                    $(opts.save_handler).removeClass('savebutton')
                            .addClass('ajaxmsg processing')
                            .text('Saving')
                            .fadeIn();
                });

                //If new screen mode is easy sort then save new mode
                if(CurrentScreenMode=='easysort'){
                    //Save easy sort as we are moving to another screen.
                    SaveNewSortOrder();
                }

               var jsonDict = getfieldsJSON();
               var saveJsonDict = {'formdesign':jsonDict}
               postDict = {'action':'saveFormData','form_id':opts.id,'form_design':$.toJSON(saveJsonDict)};
               var strToJson = $.toJSON(postDict);
               var callbackFunc = function(data, textStatus){
                   opts.postsavefunction();
               };
               //$('#DebugWindow').html(strToJson);
               
                $.post(opts.save_url, postDict, callbackFunc , "json");
            }
            return false;
        }

         //Attach JSON Functions
         $('#lnkSaveddlAppointmentDateField').click(function(){
            var strURL  = '{%url designer.views.updatedsettings entity_id%}';
            var data = { action: 'defaultFieldUpdate', form_type: 1, 'default_field': $("#ddlAppointmentDateField").val()};
            $('#lnkSaveddlAppointmentDateField').toggle();
           // alert('hi');
            $.post(strURL, data, callbackFunc , "json");
            return false;
         });

        this.jsonLoadForm = function(){
            var jsonGetURL  = opts.load_url;
            var jsonGetData = opts.load_data;
            var jsonGetcallbackFunc = function(data, textStatus){
                opts.form_design_data = data;
                SetupFormFromDesignData(data);
            };
            $.post(jsonGetURL, jsonGetData, jsonGetcallbackFunc , "json");
        };

        this.createToolboxControl = function(){
            var objSelect = document.createElement(opts.toolbox_control);
            $(objSelect).attr('id','createEL').attr('class','field_control');
            var list_control = "";
            if (opts.toolbox_control == 'select')
                list_control = "option"
            if (opts.toolbox_control == 'ul')
                list_control = "li"

            ///////////////////////////////////////////////////////////////
            //Create toolbox items
            for (var listitem in options.controls){
                var objList = document.createElement(list_control);
                var listitemControlType = options.controls[listitem]['ControlType'];
                var listitemDisplayType = getDisplayType(listitemControlType);
                $(objList).attr('ControlType',listitemControlType).attr('DisplayType',listitemDisplayType).attr('class',listitemControlType).text(options.controls[listitem]['DisplayName']);  //.text(listitem['DisplayName']);
                $(objSelect).append(objList);
            }
            return objSelect;
        };

        this.function_add_control_to_form = function(){
            //Init
            $('.fb-holder').slideUp();
            $('.toggle-fb-holder').html('show options').addClass('toggle-fb-holder-closed');
            uid = getFBID();
            changesMade=true;

            //Create designer element and placeholder for runtime control
            ctrlType = $(this).attr('ControlType');
            ctrlAttrs = getDefaultFieldAttributesJSON(uid,ctrlType)
            AddFormElement(uid,ctrlType,ctrlAttrs);
            $(this).val('');

            //Todo scroll
            var scrollToAnchorID = GetJQObjectID('P',uid);
            $().scrollTo($(scrollToAnchorID), 800 );

            return false;
        };
        
        this.updateSort = function(loading){
            var sortOrder = ""
            if(loading!=true){
                changesMade=true;
            }
            jQuery.each($('#fb-eval ul li'),function()
            {
                if($(this).attr('id') !=''){

                    if(sortOrder.length > 0 ){
                        sortOrder+='&';
                    }
                    sortOrder+= $(this).attr('id');
                }
            });

            $("#fb-eval-sort").val(sortOrder);
        };

        getFBID= function(){
            last_id = elID;
            return elID++;
        };

        AddFormElement = function(id, ctrlType, controlAttributes){
            var fb_element ='';
            switch(ctrlType){
                case 'text':
                    fb_element = create_FB_Text(id, 'text',controlAttributes)
                    break;
                case 'narrative':
                    fb_element = create_FB_narrative(id, 'narrative',controlAttributes)
                    break;
                case 'textarea':
                    fb_element = create_FB_Text(id, 'textarea',controlAttributes)
                    break;
                case 'rank':
                    fb_element = create_FB_Rank(id, 'rank', controlAttributes)
                    break;
                case 'select':
                    fb_element = create_FB_Select(id, 'select', controlAttributes)
                    break;
                case 'checkbox':
                    fb_element = create_FB_Checkbox(id, 'checkbox', controlAttributes)
                    break;
                case 'radio':
                    fb_element = create_FB_Radio(id, 'radio', controlAttributes)
                    break;
                case 'date':
                    fb_element = create_FB_Date(id, 'date',controlAttributes)
                    break;
                case 'time':
                    fb_element = create_FB_Time(id, 'time',controlAttributes)
                    break;
                case 'customer':
                    fb_element = create_FB_AutoComplete(id, 'customer',controlAttributes)
                    break;
                case 'autocomplete':
                    fb_element = create_FB_AutoComplete(id, 'autocomplete',controlAttributes)
                    break;
                default:
                    return false;
            }
            //fb_element.find("#fb_q_" + id).html('&nbsp;(' + fb_element.find("#ctrlhelptext_" + id).val() + ')&nbsp;');

            // Create design elements and placeholder for runtime control
            $(ul_obj).append(fb_element);

            //Create runtime control and insert it into the placeholder
            renderRuntimeControlIntoPlaceholder(id,ctrlType,true);

            // Add any options into design and runtime control
            if(controlAttributes.choices){

                for(choice in controlAttributes.choices){
                    var newOptionID = AddOptionToDesignControlAndRuntimeControl(id,ctrlType,controlAttributes.choices[choice]);

                    //Add options to runtime control
                    update_runtime_input_from_design(id,newOptionID);
                }
            }



            $('.fb-header').hide();

            return true;
        };

        update_runtime_input_from_design = function(parentID, optionID){

            // Get Input Control
            var currentInputBoxID = $(GetJQObjectID('DOPL',parentID,optionID));
            var controlToUpdate = $('#' + currentInputBoxID.attr('controlToUpdate'));

            if (controlToUpdate){
                var newVal = currentInputBoxID.val();
                controlToUpdate.text(newVal);
            }

            return true;
        }
        
        renderRuntime= function(){
            if(opts.runtime_form_placeholder.length < 1)
                return false;

            var jsonDict = getfieldsJSON();
            var jsonText = "";
            $(opts.runtime_form_placeholder).empty();

            for(var control in jsonDict){
                jsonText = jsonText + control + '-';
                control_attrs = jsonDict[control];
                for(var control_attr in control_attrs){
                    jsonText = jsonText + '[' + control_attr + ':' +  control_attrs[control_attr] + '] ';
                    jsonText = jsonText + '<br />';
                }
            }

            //Check the dt entry is there
            var jqDL = $('dl#runtimeform');
            if(jqDL.length == 0){
                var htmlDL = document.createElement("dl");
                $(htmlDL).attr('id','runtimeform').attr('class','ctrl-runtime');
                jqDL = $(htmlDL);
            }

            for(var control in jsonDict){
                control_attrs = jsonDict[control];
                var htmlDT = document.createElement("dt");
                var htmlDD = document.createElement("dd");
                var htmlLabel = document.createElement("label");
                var htmlDIVControl = document.createElement("div");
                var htmlControl = document.createElement("input");
                $(htmlDT).text(control_attrs.label);
                $(htmlLabel).attr('class','help').text(control_attrs.help);
                $(htmlControl).attr('id','rt' + control_attrs.parentcontrol).attr('class','element text medium').attr('type','text').attr('value','')
                $(htmlDIVControl).append(htmlControl);
                $(htmlDD).append(htmlLabel).append(htmlDIVControl);
                $(jqDL).append(htmlDT).append(htmlDD);
            }


            //<dl class="table-display">
            //<dt>
            //<dd>
            $(opts.runtime_form_placeholder).append(jqDL);
        };

        create_FB_Div= function(){
            var jDIV =  $('<div></div>');
            return jDIV;
        };

        create_FB_Table= function(){
            return $('<table class="fb-table"></table>');
        };

        create_FB_TD= function(){
            return $('<td></td>');
        };

        create_FB_TR= function(){
            return $('<tr></tr>');
        };

        create_FB_UL= function(){
            return $('<ul></ul>');
        };

        create_FB_LI= function(){
            return $('<li></li>');
        };

        create_FB_A= function(){
            return $('<a></a>');
        };

        create_FB_Label= function(){
            return $('<label></label>');
        };

        create_FB_Option= function(text, value, selected){
            var jOPT =  $('<option></option>');
            jOPT.attr('text',text);
            jOPT.val(value);
            if(typeof(selected) != 'undefined'){ jOPT.attr('selected',true); }
            return jOPT;
        };

        create_FB_Select= function(name, id, options){
            var jSelect =  $('<select></select>');
            jSelect.attr('name',name);
            jSelect.attr('id',id);
            if(typeof(options) == 'object'){
                jQuery.each(options, function() {
                    jSelect.append(createOption(this.text,this.value,this.selected));
                });
            }
            return jSelect;
        };

        create_FB_Input= function(n, t, v){
            return $('<input type="' + t + '" />').attr({name:n, id:n}).val(v);
        };

        create_FB_TextArea= function(n, t, v){
            return $('<textarea type="' + t + '" ></textarea').attr({name:n, id:n}).val(v);
        };

        create_FB_Selectbox= function(n){
            return $('<select></select>').attr({name:n, id:n});
        };

        create_FB_DeleteLink = function (id){
            var jDelete = $('<a class="smallerbutton deletebutton right" title="Are you sure you want to delete this form section?" href="#" class="del-button delete-confirm">Delete</a>')
                .click( function() {
                var delete_id = $(this).attr("ctrlid");
                if(confirm( $(this).attr('title') )){
                    $(GetJQObjectID('P',delete_id)).animate({opacity: 'hide', height: 'hide', marginBottom: '0px'}, 'slow', function () {
                        $(this).remove();
                    });
                }
                return false;
            });
            jDelete.attr('ctrlid',id);
            jDelete.attr('id',GetObjectID('DC',id));

            return jDelete;
        };

        create_FB_ToggleLink= function(id){
            var fbToggleLink = $('<a href="#" class="toggle-fb-holder toggle-fb-holder-opened" id="fb_toggle_' + id + '">hide options</a>&nbsp;&nbsp;');
                fbToggleLink.click(function(){
                    var toggle_id = $(this).attr("id").replace(/fb_toggle_/, '');
                    if($(this).html() == 'hide options'){
                        $(this).html('show options').addClass('toggle-fb-holder-closed');
                    }else{
                        $(this).html('hide options').addClass('toggle-fb-holder-opened');
                    }
                    $('#fb_holder_' + toggle_id).slideToggle();
                    return false;
                });

            return fbToggleLink;
        };
        
        createComplexControls = function(id,control_attrs){
            // Some controls can't be made 'special' until after they have been added to the page.

            //At present only the timepickr is special
            if(control_attrs.displayType!='time'&&control_attrs.displayType!='date'&&control_attrs.displayType!='autocomplete')
                return

            var ctrlID = GetObjectID('RW',control_attrs.id);
            var ctrlJQ = $('#' + ctrlID);

            if(control_attrs.displayType=='time'){
                var anchorHandle = document.createElement('a');
                var anchorID = $(ctrlJQ).attr('id') + 'chooser';
                $(anchorHandle).attr('class','choose-time').text("&nbsp;").attr('href','#').attr('id',anchorID);
                $(anchorHandle).click(function(){$(ctrlJQ).focus();return false;})
                $(ctrlJQ).parent().append(anchorHandle);

                //$(ctrlID).timepickr({ convention: 12,dropslide:{top:'25'}});
                $(ctrlJQ).timepickr({ convention: 12});
            }

            if(control_attrs.displayType=='date'){
                var anchorHandle = document.createElement('a');
                var anchorID = $(ctrlJQ).attr('id') + 'chooser';
                $(anchorHandle).attr('class','choose-date').text("&nbsp;").attr('href','#').attr('id',anchorID);
                $(anchorHandle).click(function(){$(ctrlJQ).focus();return false;})
                $(ctrlJQ).parent().append(anchorHandle);
            }

            if(control_attrs.displayType=='autocomplete'){
                //Add AUto complete behiviour
                var ajaxURL = options.controls[control_attrs.controlType].AutoCompleteURL;  //  This is not retrieved from user settings because it is not offered as such yet.
                AddAutoCompleteBehaviour(id, ctrlID,ajaxURL,control_attrs.label,control_attrs);

                //Add add new me if required.
                //Get Passed in options
                var this_control_attrs = opts.controls[control_attrs.controlType];
                if(this_control_attrs.AutoCompleteAddNewObject){
                    var idAddNew = GetObjectID('RADD',control_attrs.id);
                    var anchorAddNew = $(this_control_attrs.AutoCompleteAddNewObject).clone();
                    $('#' + ctrlID).after(anchorAddNew);
                }
            }
        };

        AddAutoCompleteBehaviour = function (id, inputAutocompleteInputID, strURL, control_name,controlItem){
            //Init
            var jqIA  = $('#' + inputAutocompleteInputID);
            var inputHiddenID = GetObjectID('RHID',id);
            var inputHidden = $(create_FB_Input(id,'hidden',''));

            //Add hidden control attribtes
            $(inputHidden)
                .attr('id',inputHiddenID)
                .attr('name',control_name)
                .attr('value_field_name',controlItem.label)
                .css('display','none');

            // Add hidden control to page
            $(jqIA).after(inputHidden);

            // Set autosuggest options with all plugins activated
            var options = {
                script:strURL,
                varname:"q",
                json:true,						// Returned response type
                shownoresults:true,				// If disable, display nothing if no results
                noresults:"No Results",			// String displayed when no results
                maxresults:8,					// Max num results displayed
                cache:false,					// To enable cache
                minchars:2,						// Start AJAX request with at leat 2 chars
                timeout:100000,					// AutoHide in XX ms
                callback: function (obj) { 		// Callback after click or selection
                    // For example use :

                    // Build HTML
                    var html = "ID : " + obj.id + "<br>Main Text : " + obj.value  // + "<br>Info : " + obj.info;
                    $('#input_search_all_response').html(html).show() ;
                    $('#' + inputHiddenID).val(obj.id);

                    // => TO submit form (general use)
                    //$('#search_all_value').val(obj.id);
                    //$('#form_search_country').submit();
                }
            };
            // Init autosuggest
            var as_json = new bsn.AutoSuggest(inputAutocompleteInputID, options);

            // Display a little watermak
            //$("#" + inputAutocompleteInputID).Watermark("ex : Kermit, Mr Pink ...");

        };

        renderRuntimeControlIntoPlaceholder = function(id,controlType,bolCreateRuntimeInDesignMode,control_attrs){

            // Get Parent Object
            containerObj = "dl";
            var ctrlContainer = document.createElement(containerObj);
            $(ctrlContainer).attr('id','runtimecontrol_' + id).attr('class','ctrl-runtime');

            // Get Information on how to render control from settings elements
            if(bolCreateRuntimeInDesignMode){
                control_attrs = getfieldAttributesJSON(id);
            }

            //Control Label
            var htmlControlLabel = document.createElement("span");
            $(htmlControlLabel).attr('id', GetObjectID('RL',id)).text(control_attrs.label);

            //Required Label
            var htmlReq = document.createElement("span");
            $(htmlReq).addClass('required').attr('id',GetObjectID('RR',id)).text('* required');
            if(control_attrs.required==false){$(htmlReq).hide();}

            //Create Help Text
            var htmlHelpText = document.createElement("label");
            $(htmlHelpText).attr('class','help').text(control_attrs.help).attr('id', GetObjectID('RH',id));

            //Create Actual Control that this type is related to and wrapper for said control
            var htmlDIVControl = document.createElement("div");
            var htmlControl = create_FB_RuntimeControl(id,controlType,control_attrs);
            
            //Check whether this control has the name attribute or a hidden control stores the eventual value
            if(control_attrs.displayType != 'autocomplete'){
                //$(htmlControl).attr('name',control_attrs.label);
                field_name = generateFieldName(control_attrs.id)
                $(htmlControl).attr('name',field_name);

                $(htmlControl).attr('value_field_name',control_attrs.label);
            }

            $(htmlDIVControl).append(htmlControl);

            // Create clear booth
            var htmlHR = document.createElement("hr");
            $(htmlHR).attr('class','clearboth');

            //Create left hand side elements container and append elements
            var htmlDT = document.createElement("dt");
            $(htmlDT).append(htmlControlLabel).append(htmlReq);

            //Create right hand side container
            var htmlDD = document.createElement("dd");
            $(htmlDD).append(htmlHelpText).append(htmlDIVControl);

            //$(htmlControl).attr('id','rt' + control_attrs.pareadded ntcontrol).attr('class','element text medium').attr('type','text').attr('value','')
            $(ctrlContainer).append(htmlDT).append(htmlDD).append(htmlHR);

            //Place control in container created to insert runtime control
            var strRuntimeContainerID = GetJQObjectID('R',id);
            $(strRuntimeContainerID).append(ctrlContainer);

            //Some controls need to have functionality added after they have been added to the page
            createComplexControls(id,control_attrs);

            //Add listen events to populate runtime control
            if(bolCreateRuntimeInDesignMode){
                var fbCtrlName = $(GetJQObjectID('DL',id));
                $(fbCtrlName).keyup(onlistenforkeyup);
                var fbHelpText = $(GetJQObjectID('DH',id));
                $(fbHelpText).keyup(onlistenforkeyup);
                var strSelrequired = $(GetJQObjectID('DR',id));
                $(strSelrequired).change(requiredselected);
            }
        };

        generateFieldName = function(id){
            return 'fn' + id;
        };

        loadFormWithData = function(){
            //Loop through data returned
            for(dataKey in opts.form_data){
                // Get Control Item
                var dataDict = opts.form_data[dataKey];
                loadControlWithData(dataKey, dataDict);
            }
        };

        this.loadControlWithData = function(field_name, dataDict){
            var control_id = dataDict['control_id'];
            var control_type = dataDict['control_type'];
            var display_type = dataDict['display_type'];
            var dataString = dataDict['value_string'];
            var dataText = dataDict['value_text'];
            var dataInt = dataDict['value_int'];

            var inputID = GetJQObjectID('RW',control_id);
            var inputHiddenID = GetJQObjectID('RHID',control_id);

            if($(inputID).length > 0){
                var thisControl = $($(inputID)[0]);
                var thisControlHidden = $($(inputHiddenID)[0]);
                var bolEntered = false;

                if(control_type == 'customer'){
                    $(thisControl).val(dataString);
                    $(thisControlHidden).val(dataInt);
                    bolEntered=true;
                }

                if(display_type == 'textarea'){
                    $(thisControl).text(dataText);
                    bolEntered=true;
                }

                if(control_type == 'radio'||control_type == 'checkbox'){
                    var validIds = dataString.split('|');
                    var iIndex = 0
                    for(iIndex=0;iIndex<validIds.length;iIndex++){
                        var thisID = validIds[iIndex];
                        $(thisControl).find('li [value="' + thisID + '"]').attr("checked", "checked");
                    }
                    $(thisControlHidden).val(dataString);
                    bolEntered=true;
                }

                if(control_type == 'select'){
                    var selectID = GetJQObjectID('RCTL',control_id);
                    $('#' + selectID + ' option[value="' + dataString + '"]').attr('selected', 'selected');
                    bolEntered=true;
                }

                if(display_type == 'autocomplete'){
                    $(thisControl).text(dataString);
                    $(thisControlHidden).val(dataInt);
                }


                if(bolEntered==false){
                    $(thisControl).val(dataString);
                }

            }
        };

        create_FB_RuntimeControl= function(id,controlType,control_attrs){

            //Create control based on HtmlControl from settings
            var baseHtmlControl = opts.controls[controlType]['HtmlControl'];
            var baseHtmlControlType = opts.controls[controlType]['HtmlControlType'];
            var htmlControl = document.createElement(baseHtmlControl);
            $(htmlControl).attr('id',GetObjectID('RW',control_attrs.id));

             //Is required?
             if(control_attrs.required==1)
             {
                 $(htmlControl).addClass('validate[required]');
             }

            //Add additional parameters required.
            if(controlType=='text')
                $(htmlControl).addClass('element text medium').attr('type',baseHtmlControlType).attr('value','');
            if(controlType=='textarea')
                $(htmlControl).addClass('element text small');
            if(controlType=='checkbox')
                $(htmlControl).addClass('element text medium').attr('value','');
            if(controlType=='date')
                $(htmlControl).datepicker({changeMonth: true,changeYear: true}).addClass('short').addClass('floatleft');
            if(controlType=='time')
                $(htmlControl).addClass('short').addClass('floatleft');
            //if(controlType=='time')
             //   $(htmlControl).timepickr({ convention: 12 });


            return $(htmlControl)
        };

        getDisplayType = function(controlType){
            var listitemDisplayType = opts.controls[controlType]['DisplayType'];
             if(listitemDisplayType==null){listitemDisplayType=controlType;}
             return listitemDisplayType;
        }

        create_FB_Container= function(id,controlType){
            var cID = GetObjectID('P',id);  //'fb_item_' + id;

            //Create Anchor
            var anchor = create_FB_A();
            var anchorID = GetJQObjectID('DANC',id);
            anchor.attr('id',anchorID);

            //Get DisplayType
            var listitemDisplayType = getDisplayType(controlType);

            var fbRuntime = create_FB_Div().attr('id',GetObjectID('R',id)).addClass('fb-runtime');
            var jLI =  $('<li></li>')
                        .attr({id:cID})
                        .attr('controltype',controlType)
                        .attr('displaytype',listitemDisplayType)
                        .attr('uid',id)
                        .addClass('fb-item').addClass('fb-round-corners').addClass('fb-item-border')
                        .append(anchor)
                        .append(create_FB_Header(id,controlType))
                        .append(fbRuntime);
            return jLI;
        };

        create_FB_Header= function(id, controlType){
            var fbQType 		=  ""; //create_FB_Input('controltype_' + id, 'hidden', controlType);
            //fbQType.attr('class','hidden');
            var fbHeader =  create_FB_Div()
                                .attr('id','fb_header_' + id)
                                .addClass('fb-header')
                                .append('<strong id="fb_title_' + id + '" class"fb-title">&nbsp;[Control Label]&nbsp;</strong>')
                                .append('<strong id="fb_title_control_type_' + id + '" class"fb-title">&nbsp;(' + controlType +')&nbsp;</strong>')
                                .append(fbQType)
                                .append('<hr class="clearboth"');
            return fbHeader;
        };

        create_FB_Legend= function(id, legend){
            var fbLegend =  create_FB_Div()
                                .attr('id','fb_legend_' + id)
                                .addClass('fb-legend')
                                //.append($('<span class="fb-edit-bar"></span>')
                                .append('<a class="movebutton smallerbutton right">&nbsp;move</a>')
                                .append(create_FB_DeleteLink(id))
                                .append(create_FB_ToggleLink(id))
                                //.append('<span id="fb_q_'+id+'"></span')
                                .append('<hr class="clearboth"');
            return fbLegend;
        };

        create_FB_ElementsDiv = function(id, ctrlType,controlAttributes){
            var qName = '';
            var qLabel = '';
            var qIsRequired = false;
            var fbElements =  create_FB_Div().attr('id','fb_elements_' + id).addClass('fb-elements');
            var fbHelpText;
            var fbCtrlName 		=  create_FB_Input(GetObjectID('DL',id), 'text', '').addClass('fb-text-input-long fb-text-input');
            if(typeof(ctrlType) != 'undefined' && ctrlType == 'textarea'){
                fbHelpText 		=  create_FB_TextArea(GetObjectID('DH',id), 'text', '').addClass('fb-text-input-long fb-text-input');
            }else{
                fbHelpText 		=  create_FB_Input(GetObjectID('DH',id), 'text', '').addClass('fb-text-input-long fb-text-input');
            }

            if (formTypeAttributes['type'] == 'form'){
                fbCtrlName.addClass('fb-text-input');
            }else{
                fbHelpText.addClass('fb-text-input');
            }

            var fbRequiredInput =  create_FB_Input(GetObjectID('DR',id), 'checkbox', 1).addClass('required').addClass('checkbox');
            var fbRequiredLabel =  create_FB_Label().addClass('fb-required-label').attr('for',GetObjectID('DR',id)).text('Required');
            var fbRequired 		=  create_FB_Div().attr('id',GetObjectID('DRD',id)).addClass('fb-required').append(fbRequiredLabel);

            $(fbCtrlName).attr('controlToUpdate',GetObjectID('RL',id));
            $(fbHelpText).attr('controlToUpdate',GetObjectID('RH',id));
            $(fbRequiredInput).attr('controlToUpdate',GetObjectID('RR',id));

            if(typeof(controlAttributes) == 'object'){
                if (typeof(controlAttributes.label) != 'undefined') {
                    fbCtrlName.val(controlAttributes.label);
                }
                if (typeof(controlAttributes.help) != 'undefined') {
                    fbHelpText.val(controlAttributes.help);
                }
                if (typeof(controlAttributes.required) != 'undefined') {
                    if(controlAttributes.required == 'true' || controlAttributes.required == true){
                        fbRequiredInput.attr('checked',true);
                    }
                }
            }

            fbCtrlNameLabel = create_FB_Div().css('display','block').append('<label class="fb-label">' + formTypeAttributes['TitleLabel'] + '</label>');
            fbHelpTextLabel =create_FB_Div().css('display','block').append('<label class="fb-label">' + formTypeAttributes['HelpLabel'] + '</label>');

            var htmlDL = document.createElement('dl');
            $(htmlDL).attr('id','control_attributes_' + id).attr('class','ctrl-attrs');
            var jqDL = $(htmlDL);

            if(ctrlType!='narrative')
                var rowRequired = create_FB_Attribute_Row(fbRequired,fbRequiredInput);
            var rowCtrlName = create_FB_Attribute_Row(fbCtrlNameLabel,fbCtrlName);
            var rowCtrlHelp = create_FB_Attribute_Row(fbHelpTextLabel,fbHelpText);

            $(jqDL).append(rowRequired).append(rowCtrlName).append(rowCtrlHelp)

            //Create controls required to add item to select, radio or checkbox controls
            if(ctrlType=='radio'||ctrlType=='select'||ctrlType=='checkbox'){
                var fbOptionsLabel =create_FB_Div().css('display','block').append('<label class="fb-label">' + formTypeAttributes['OptionLabel'] + '</label>');
                var fbCtrlOptions = create_FB_MagicList(id, ctrlType,controlAttributes);
                var rowCtrlOptions = create_FB_Attribute_Row(fbOptionsLabel,fbCtrlOptions);
                $(jqDL).append(rowCtrlOptions);
            }

            $(jqDL).append('<hr class="clearboth" />');
            fbElements.append(jqDL);
            /*
             *fbElements.append(fbRequired.append(fbRequiredInput))
                      .append(fbCtrlName)
                      .append(fbHelpText);
                    */
            return fbElements;
        };

        onlistenforkeyup= function(e){
            var srcCtrl = $(this).attr('id');
            var destCtrl = $(this).attr('controltoupdate');
            var e_keyCode = e.keyCode;

            return listenforkeyup(srcCtrl, destCtrl,e_keyCode);
        }

        listenforkeyup = function(srcCtrl, destCtrl, e_keyCode){

            // Get Input Control
            var currentInputBoxID = srcCtrl;
            var controlToUpdate = destCtrl;
            
            if (controlToUpdate.length > 0){
                var newVal = $('#' + currentInputBoxID).val();
                var strControlToUpdate = '#' + controlToUpdate;
                $(strControlToUpdate).text(newVal);
            }

            return true;
        };
        
        onlistenforkeydown = function(e){
            var parentID = GetParentIDForControl(this);
            var optionID = $(this).attr('optionid');
            var e_keyCode = e.keyCode;
            return listenforkeydown(parentID, optionID,e_keyCode);
        }

        listenforkeydown = function(parentID, _optionID,e_keyCode){

             // Is an option control if not just return
            if(!_optionID)
                return true;

            //Is option control get paramters
            var optionID = parseInt(_optionID);
            var currentInputBoxID = GetObjectID('DOPL',parentID,optionID);
            var jqCurrentInputBox = $('#' + currentInputBoxID);

            //Get Useful controls
            var AddOptionLinkID = GetJQObjectID('DAO',parentID);
            var RemoveOptionLinkID = GetJQObjectID('DRO',parentID,optionID);

            //Get all options for this control
            var optionsHolder = GetJQObjectID('DCTL',parentID);
            var optionsInputs = optionsHolder + " input";
            var numberOfOptions = $(optionsInputs).length;

            //Find Current Option
            var iIndex = 0;
            var curIndex = -1;
            for(iIndex=0;iIndex<numberOfOptions;iIndex++){
                if($(optionsInputs)[iIndex].id==currentInputBoxID){
                    curIndex = iIndex;
                }
            }

            //Enter pressed then create new line
            if(e_keyCode == $.keyCode.ENTER){
                $(AddOptionLinkID).click();
            }

            //Backspace pressed on an empty control delete it
            if(e_keyCode == $.keyCode.BACKSPACE&&jqCurrentInputBox.val()==""){
                $(RemoveOptionLinkID).click();
                var moveToIndex = curIndex - 1;
                if(moveToIndex>=0){
                    $($(optionsInputs)[moveToIndex]).focus();
                }
            }

            if(e_keyCode == $.keyCode.UP){
                var moveToIndex = curIndex - 1;
                if(moveToIndex<numberOfOptions){
                    $($(optionsInputs)[moveToIndex]).focus();
                }
                if(jqCurrentInputBox.val().length == 0){
                    $(RemoveOptionLinkID).click();
                }
            }

            if(e_keyCode == $.keyCode.DOWN){
                if(curIndex==numberOfOptions-1){
                    if(jqCurrentInputBox.val().length > 0){
                        $(AddOptionLinkID).click();
                    }
                }else{
                    var moveToIndex = curIndex + 1;
                    if(moveToIndex<numberOfOptions){
                        $($(optionsInputs)[moveToIndex]).focus();
                    }
                }
            }

            return true;
        };

        GetParentIDForControl= function(childControl){
            return GetControlParentWrapper(childControl,'uid','','uid');
        };

        this.GetControlParentWrapperID = function(childControl,attribute_name, attribute_value, return_attribute_name){
            var retVal = "";
            var matchVal = "";
            //Starting at the child control go to each parent until i find the attribute uid, this then gives me the unique id for the control.
            var bolFin = false;
            var iCount = 0; //don't iterate more than 20 times
            var currentControl = childControl;
            while (bolFin == false){
                iCount++;
                if(iCount>20)
                    bolFin = true;

                if($(currentControl).attr('id')=="form-builder")
                    bolFin = true;

                if(bolFin==false){
                    var current_attribute_value = $(currentControl).attr(attribute_name);
                    var return_attribute_value = $(currentControl).attr(return_attribute_name);
                    
                    if(current_attribute_value==""||current_attribute_value==undefined){
                        currentControl = $(currentControl).parent();
                    }else{
                        // If attribute_value not specified then we can just finish if we have found any value
                        if(attribute_value == ''){
                            retVal = return_attribute_value;
                            bolFin = true;
                        }else{
                            //Can only finish if value also matches
                            if(current_attribute_value==attribute_value){
                                retVal = return_attribute_value;
                                bolFin = true;
                            }
                        }
                    }
                }
            }
            return retVal;
        };

        requiredselected= function(){
            var controlToUpdate = $(this).attr('controlToUpdate');
            var controlRequired = ($(this).attr("checked") ? $(this).val() : 0);
            if (controlToUpdate.length > 0){
                strControlToUpdate = '#' + controlToUpdate;
                if (controlRequired==1)
                    $(strControlToUpdate).show();
                else
                    $(strControlToUpdate).hide();
            }
        };


        create_FB_Attribute_Row = function(dt,dd){
            var divHolder = document.createElement("div");
            var htmlDT = document.createElement("dt");
            var htmlDD = document.createElement("dd");
            $(htmlDT).append(dt);
            $(htmlDD).append(dd);
            $(divHolder).append(htmlDT).append(htmlDD);
            return $(divHolder).children();
        };

        create_FB_Text_Base= function(id, ctrlType, controlAttributes){
            /*In the controlAttributes json
             * Need to pass Name, Label and isRequired
             */
            if(formTypeAttributes=='form'){
                if(ctrlType == 'text'){var _sQType = 'Single Line Response';}else{var _sQType = 'Multiple Line Response';}
            }else{
                if(ctrlType == 'text'){var _sQType = 'Text';}else{var _sQType = 'TextArea';}
            }
            if(ctrlType == 'date'){var _sQType = 'Date';}
            var fbContainer 	=  create_FB_Container(id,ctrlType);
            var fbQType 		=  ""; //create_FB_Input('controltype_' + id, 'hidden', ctrlType);
            var fbLegend 		=  create_FB_Legend(id,_sQType);
            var fbHolder 		=  create_FB_Div().attr('id','fb_holder_' + id).addClass('fb-holder');
            var fbElements 		=  create_FB_ElementsDiv(id,ctrlType,controlAttributes);
            fbContainer.append(fbQType).append(fbLegend).append(fbHolder.append(fbElements));
            return fbContainer;
        };

        create_FB_Text= function(id, ctrlType, controlAttributes){
            var tbText = create_FB_Text_Base(id,ctrlType,controlAttributes);
            return tbText;

        };

        create_FB_Date= function(id, ctrlType, controlAttributes){
            var tbDate = create_FB_Text_Base(id,ctrlType,controlAttributes);
            return tbDate;
        };

        create_FB_Time= function(id, ctrlType, controlAttributes){
            var tbTime = create_FB_Text_Base(id,ctrlType,controlAttributes);
            return tbTime;
        };

        create_FB_AutoComplete = function(id, ctrlType, controlAttributes){
            var tbAC = create_FB_Text_Base(id,ctrlType,controlAttributes);
            return tbAC;
        };

        create_FB_narrative= function(id, ctrlType,controlAttributes){
            /*In the controlAttributes json
             * Need to pass Name, Label and isRequired
             */
            if(ctrlType == 'text'){var _sQType = 'Single Line Response';}else{var _sQType = 'Multiple Line Response';}
            var fbQType 		=  ""; //create_FB_Input('controltype_' + id, 'hidden', ctrlType);
            var fbContainer 	=  create_FB_Container(id,ctrlType);
            var fbLegend 		=  create_FB_Legend(id,'Help Section');
            var fbHolder 		=  create_FB_Div().attr('id','fb_holder_' + id).addClass('fb-holder');
            var fbElements 		=  create_FB_ElementsDiv(id,ctrlType,controlAttributes);
            fbContainer.append(fbQType).append(fbLegend).append(fbHolder.append(fbElements));

            return fbContainer;
        };

        create_FB_Rank= function(id, ctrlType, controlAttributes){
            /*In the controlAttributes json
             * Need to pass Name, Label and isRequired
             */

            var fbQType 		=  ""; //create_FB_Input('controltype_' + id, 'hidden', ctrlType);
            var fbContainer 	=  create_FB_Container(id,ctrlType);
            var fbLegend 		=  create_FB_Legend(id,'Rank');
            var fbHolder 		=  create_FB_Div().attr('id','fb_holder_' + id).addClass('fb-holder');
            var fbElements 		=  create_FB_ElementsDiv(id,ctrlType,controlAttributes);
            var fbRank			=  create_FB_Div().attr('id','fb_rank_' + id).addClass('fb-rank');
            var fbRankOpts		=  create_FB_Div().attr('id','fb_rank_opts_' + id).addClass('fb-rank-opts');
            var sbRankFrom		=  create_FB_Selectbox('rank_from_' + id);
            var sbRankTo		=  create_FB_Selectbox('rank_to_' + id);
            var fbRankLabel		=  create_FB_Div().attr('id','fb_rank_label_' + id).addClass('fb-rank-label');
            var rankLabelTo		=  '';
            var rankLabelFrom	=  '';

            sbRankFrom.append(create_FB_Option('NA',-1));
            for (i=0;i<=2;i++)
            {
                sbRankFrom.append(create_FB_Option(i,i));
            }
            for (i=3;i<=10;i++)
            {
                sbRankTo.append(create_FB_Option(i,i));
            }
            if(typeof(controlAttributes) == 'object'){
                if (typeof(controlAttributes.RANKFROM) != 'undefined') {
                    sbRankFrom.val(controlAttributes.RANKFROM);
                }
                if (typeof(controlAttributes.RANKTO) != 'undefined') {
                    sbRankTo.val(controlAttributes.RANKTO);
                }
                if (typeof(controlAttributes.RANKLABELTO) != 'undefined') {
                    rankLabelTo = controlAttributes.RANKLABELTO;
                }
                if (typeof(controlAttributes.RANKLABELFROM) != 'undefined') {
                    rankLabelFrom = controlAttributes.RANKLABELFROM;
                }
            }
            var rankTabel 	= create_FB_Table();
            rankLabelFrom	= create_FB_TD().append(create_FB_Input('rank_label_from_' + id, 'text', rankLabelFrom));
            rankLabelFrom 	= create_FB_TR().append('<td>From</td').append(rankLabelFrom);
            rankLabelTo		= create_FB_TD().append(create_FB_Input('rank_label_to_' + id, 'text', rankLabelTo));
            rankLabelTo 	= create_FB_TR().append('<td>To</td').append(rankLabelTo);

            rankTabel.append(rankLabelFrom).append(rankLabelTo);
            var temp = fbRankOpts.append('<span>Rank</span>').append('&nbsp;From&nbsp;').append(sbRankFrom).append('&nbsp;To&nbsp;').append(sbRankTo)
            fbRank.append(temp);
            fbRank.append(
                        fbRankLabel.append('<p>Labels Optional</p>')
                                  .append(rankTabel)
                         );

            fbContainer.append(fbQType).append(fbLegend).append(fbHolder.append(fbElements.append(fbRank)));
            return fbContainer;
        };

        create_FB_Select= function(id, ctrlType, controlAttributes){
            /*In the controlAttributes json
             * Need to pass Name, Label and isRequired
             */
            if(ctrlType == 'text'){var _sQType = 'Single Line Response';}else{var _sQType = 'Choose from a list';}
            var fbQType 		=  ""; //create_FB_Input('controltype_' + id, 'hidden', ctrlType);
            var fbContainer 	=  create_FB_Container(id,ctrlType);
            var fbLegend 		=  create_FB_Legend(id,_sQType);
            var fbHolder 		=  create_FB_Div().attr('id','fb_holder_' + id).addClass('fb-holder');
            var fbElements 		=  create_FB_ElementsDiv(id,ctrlType,controlAttributes);
            fbContainer.append(fbQType).append(fbLegend).append(fbHolder.append(fbElements));  //.append(create_FB_MagicList(id, ctrlType,controlAttributes)));
            return fbContainer;
        };

        create_FB_Radio= function(id, ctrlType, controlAttributes){
            /*In the controlAttributes json
             * Need to pass Name, Label and isRequired
             */
            if(ctrlType == 'text'){var _sQType = 'Single Line Response';}else{var _sQType = 'Multiple choice';}
            var fbQType 		=  ""; //create_FB_Input('controltype_' + id, 'hidden', ctrlType);
            var fbContainer 	=  create_FB_Container(id,ctrlType);
            var fbLegend 		=  create_FB_Legend(id,_sQType);
            var fbHolder 		=  create_FB_Div().attr('id','fb_holder_' + id).addClass('fb-holder');
            var fbElements 		=  create_FB_ElementsDiv(id,ctrlType,controlAttributes);
            fbContainer.append(fbQType).append(fbLegend).append(fbHolder.append(fbElements));
            return fbContainer;
        };

        create_FB_Checkbox= function(id, ctrlType, controlAttributes){
            /*In the controlAttributes json
             * Need to pass Name, Label and isRequired
             */
            if(ctrlType == 'text'){var _sQType = 'Single Line Response';}else{var _sQType = 'Checkbox';}
            var fbQType 		=  ""; //create_FB_Input('controltype_' + id, 'hidden', ctrlType);
            var fbContainer 	=  create_FB_Container(id,ctrlType);
            var fbLegend 		=  create_FB_Legend(id,_sQType);
            var fbHolder 		=  create_FB_Div().attr('id','fb_holder_' + id).addClass('fb-holder');
            var fbElements 		=  create_FB_ElementsDiv(id,ctrlType,controlAttributes);
            fbContainer.append(fbQType).append(fbLegend).append(fbHolder.append(fbElements));
            return fbContainer;
        };


        create_FB_MagicList= function(id, ctrlType,controlAttributes){
            //Create main container
            var mlContainer = create_FB_Div().addClass('fb-options-holder');
            //Create listcontainer for options
            var mlList = create_FB_UL().addClass('fb-options-holder').attr('id',GetObjectID('DCTL',id));
            //Create the add option link container
            var mlAddOption = create_FB_Div().attr('id','fb_add_option_row_' + id ).addClass('add-option-holder');
            //Create the add option link
            var mlAddOptionLink = create_FB_MagicList_AddOptionButton(id);

            //Combine elements
            mlContainer.append(mlList);
            mlAddOption.append(mlAddOptionLink);
            mlContainer.append(mlAddOption);
            return mlContainer;
        };

        create_FB_MagicList_AddOptionButton= function(id){
            //attr('class','smallerbutton deletebutton')
            var mlAddOptionLink = create_FB_A();

            var AddOptionLinkID = GetObjectID('DAO',id);
            mlAddOptionLink.attr('href','#').attr('parentID',id).attr('id',AddOptionLinkID).text('Add Option').attr('class','smallerbutton addbutton');
            //var mlAddOptionLink2 = $('<a href="#" class="add-option" add_to_container="' + optionContainerID + '" id="fb_add_option_' + id + '">Add Option</a>')
            mlAddOptionLink.click(OnAddOptionClick);
            return mlAddOptionLink;
        };

        OnAddOptionClick = function(){
            var parentID = $(this).attr("parentID");
            var ctrlType = $(GetJQObjectID('P',parentID)).attr('controltype');
            AddOptionToDesignControlAndRuntimeControl(parentID,ctrlType);
            return false;
        }
        
        AddOptionToDesignControlAndRuntimeControl = function(parentID,ctrlType,choice){

            //Get Current and new ids
            var newOptionID = getFBID();

            //Get Option Container
            var ulID = GetObjectID('DCTL',parentID);

            //Create <li> row to insert into option controls
            var liID  = GetObjectID('DOP',parentID,newOptionID);
            var _blankLi = create_FB_LI().attr('id',liID);

            //Create Actual control that will sit in this list
            var inputID = GetObjectID('DOPL',parentID,newOptionID);
            var _inputBox = create_FB_Input(inputID,'text','').addClass('fb-text-option').attr('optionid',newOptionID);
            if(choice){
                $(_inputBox).val(choice.text);
            }

            //Add Control to update to input box so it updates the runtime control correctly.
            if (ctrlType=='select'){
                var rtLabelID = GetObjectID('ROP',parentID,newOptionID);
                //add this  as a parameter to the control to update and add the kup event
                $(_inputBox).attr('controltoupdate',rtLabelID).keyup(onlistenforkeyup).keydown(onlistenforkeydown);

            }else{
                var rtLabelID = GetObjectID('ROPL',parentID,newOptionID);
                //add this  as a parameter to the control to update and add the kup event
                $(_inputBox).attr('controltoupdate',rtLabelID).keyup(onlistenforkeyup).keydown(onlistenforkeydown);
            }

            //Add additional parameters important when saving
            //This is a new item add a pk  of 0 will indicate to database that it is a new item.
            $(_inputBox).attr('pk','0');
            
            //Add position index so rendered in order entered use length of current list to ensure added at end.
            var strOptionsSelector = '#' + GetObjectID('DCTL',newOptionID) + ' input';
            $(_inputBox).attr('pos',$(strOptionsSelector).length);


            //Create remove link for option
            var removeLinkID = GetObjectID('DRO',parentID,newOptionID);
            var _removeLink = $('<a href="#">remove</a>')
                    .attr('id',removeLinkID)
                    .attr('class','smallerbutton deletebutton')
                    .attr('optionid',newOptionID)
                    .attr('parentid',parentID)
                    .click(RemoveOptionLinkClick);

            //Now put the input box and remove link into the li
            $(_blankLi).append(_inputBox).append(_removeLink);

            //Add the li to the ul
            $('#' + ulID).append(_blankLi);

            //SEt Focus
            $(_inputBox).focus();

            //Now Create Runtime Version Of Control
            pseduoDict = {label:'new_option' + newOptionID};
            createRuntimeOption(parentID,newOptionID,ctrlType,null,pseduoDict);



            //TODO: checkboxes
            //if(ctrlType != 'checkboxes'){
            //    _blankLi.append(create_FB_Input('default_option_'+ _optID + '_' + _id,'checkbox',1).addClass('fb-radio-option').attr('name','group_' + optionContainerID));
            //}

            //$('#fb_add_option_row_' + _id).parent().prepend(_blankDiv);


            return newOptionID;
        };


        RemoveOptionLinkClick = function(){
            var optionID = $(this).attr("optionid");
            var parentID = $(this).attr("parentid");
            var runtimeCtrlToUpdate = GetJQObjectID('ROP',parentID,optionID);

            $(this).parent().remove();
            $(runtimeCtrlToUpdate).remove();
            return false;
        };

        createRuntimeOption = function(parentID,OptionID,ctrlType,optionAttrs,controlItem){
            var parentContainerID = GetObjectID('P',parentID);
            //var ctrlType = $('#' + parentContainerID).attr('controltype');

            if(ctrlType=='radio'||ctrlType=='checkbox')
                createRuntimeOptionList(parentID,OptionID,ctrlType,optionAttrs,controlItem);
            if(ctrlType=='select')
                createRuntimeOptionSelect(parentID,OptionID,ctrlType,optionAttrs,controlItem);
        };

        createRuntimeOptionList= function(parentID,OptionID,ctrlType,optionAttrs,controlItem){

            //Init
            var rtContainer = GetObjectID('R',parentID);
            var rtMainControlWrapperID = GetObjectID('RW',parentID);
            var controlName = $('#' + rtMainControlWrapperID).attr('name');
            var inputHiddenID = GetObjectID('RHID',parentID);

            // Check if parent control ul exists
            var ulID = GetObjectID('RCTL',parentID);
            if ($('#' + ulID).length == 0){
                rtUL = create_FB_UL().addClass('fb-options-holder').attr('id',ulID).attr('class','element text medium');
                $('#' + rtMainControlWrapperID).append(rtUL);

                
                var inputHidden = create_FB_Input(parentID,'hidden','');
                $(inputHidden)
                    .attr('id',inputHiddenID)
                    .attr('name',controlName)
                    .attr('value_field_name',controlItem.label)
                    .css('display','none');
                $('#' + rtMainControlWrapperID).append(inputHidden);
            }

            //Create <li> row to insert into option controls
            var liID  = GetObjectID('ROP',parentID,OptionID);
            var _blankLi = create_FB_LI().attr('id',liID);

            //Create Control To Render
            var inputID = GetObjectID('ROPI',parentID,OptionID);
            var _inputBox = create_FB_Input(inputID,ctrlType,'');
            
            if(controlItem.required){
                if(controlItem.required=="1"){
                    $(_inputBox).addClass('validate[required]');
                }
            }

            $(_inputBox).addClass('fb-text-option').attr('name','rtgroup_' + parentID);

            $(_inputBox).click(function(){
                var selectedVal = "";
                $(this).val();
                // Loop through parent container and find all that are checked
                $.each($('#' + ulID + ' input:checked'),function(){
                    if(selectedVal==""){
                        selectedVal = selectedVal + $(this).val();
                    }else{
                        selectedVal = selectedVal + '|' + $(this).val();
                    }
                });

                $('#' + inputHiddenID).val(selectedVal);
            });

             if(optionAttrs){
                $(_inputBox).val(optionAttrs['text']);
            }

            //Create label FOr Control
            var labelID = GetObjectID('ROPL',parentID,OptionID);
            var htmlLabel = document.createElement("label");
            $(htmlLabel).attr('id',labelID)
                        .attr('for',inputID);
            if(optionAttrs){
                $(htmlLabel).text(optionAttrs['text']);
            }

            //Build it all together
            _blankLi.append(_inputBox).append(htmlLabel);
            $('#' + ulID).append(_blankLi);
        };

        createRuntimeOptionSelect = function(parentID,OptionID,ctrlType,optionAttrs,controlItem){

            //Init
            var rtContainer = GetObjectID('R',parentID);
            var rtMainControlWrapperID = GetObjectID('RW',parentID);
            var controlName = $('#' + rtMainControlWrapperID).attr('name');

            // Check if parent control ul exists
            var selectID = GetObjectID('RCTL',parentID);
            if ($('#' + selectID).length == 0){
                var rtSelect = document.createElement('select');

                    if(controlItem.required){
                        if(controlItem.required=="1"){
                            $(rtSelect).addClass('validate[required]');
                        }
                    }

                $(rtSelect).attr('id',selectID)
                                    .attr('value_field_name',controlItem.label)
                                    .attr('name',controlName)
                $('#' + rtMainControlWrapperID).append(rtSelect);
            }

            //Create <li> row to insert into option controls
            var optionID  = GetObjectID('ROP',parentID,OptionID);
            var optionRow = create_FB_Option('','',false)
                            .addClass('fb-radio-option')
                            .attr('id',optionID);

             if(optionAttrs){
                 var optVal = optionAttrs['text'];
                $(optionRow).attr('value',optVal).html(optVal);
                if(optionAttrs['selected']){
                    $(optionRow).attr('value',"");
                }
            }

            //Build it all together
             $('#' + selectID).append(optionRow);
             $('#' + selectID + ' option[value=""]').attr('selected', 'selected');
         };

        getDefaultFieldAttributesJSON = function(uid,controlType) {
                strparentcontrol = 'fb_item_' + uid;
               var field = {
                   id:uid,
                   parentcontrol:strparentcontrol,
                   type:controlType,
                   required:false,
                   label:'New ' + options.controls[controlType].DisplayName,
                   help:'<help text>',
                   defaultoption:'',
                   choices:{}
               };

               return field;
        };

        getfieldsJSON= function(){

           var fields = {};
           var selectorLi = '#' + $(ul_obj).attr('id') + '>li';
           var liLength = $(selectorLi).length;
           for (var liIndex=0;liIndex<liLength;liIndex++){
               var liRow = $(ul_obj).children()[liIndex];

               //uid
               var uid = $(liRow).attr('uid');

               // Get Field Dictionary
               var field = getfieldAttributesJSON(uid,liIndex);

               //Add field to dictionary
               fields[liIndex] = field;
           }
            return fields;
        };

        /// This function gets all the attributes of any particular control and returns a dictionary
        getfieldAttributesJSON= function(liid,posIndex) {
            uid = liid;
            strli = GetJQObjectID('P',uid);
            var liRow = $(strli)[0];

             //uid
               var uid = $(liRow).attr('uid');

               //parentControl
               var controlID = $(liRow).attr('id');

               // Get Control Type
               var controlType = $(liRow).attr('controltype');

               // Get Control Type
               var displayType = $(liRow).attr('displaytype');

               // Get Required
               var controlRequired = ($(GetJQObjectID('DR',uid)).attr("checked") ? $(GetJQObjectID('DR',uid)).val() : 0)

               //  Get Label
               var controlLabel = $(GetJQObjectID('DL',uid)).val();

               //  Get Help Text
               var controlHelpText = $(GetJQObjectID('DH',uid)).val();

               //  Get Multi Select Options
               var ulOptionsHolderID = GetObjectID('DCTL',uid);
               //strOptionsSelector = '#' ulOptionsHolderID + ' div[id^=fb_option_row_] input[id^=option]';
               var strOptionsSelector = '#' + ulOptionsHolderID + ' input';
               var field_options = {};
               for(var i=0;i < $(strOptionsSelector).length;i++){
                   var thisControl = $(strOptionsSelector)[i];
                   var field_option = {
                                id:$(thisControl).attr('pk'),
                                text:$(thisControl).val(),
                                pos:$(thisControl).attr('pos')
                            };
                   field_options[i] = field_option;
               }

               //  Get Default Value
               var defaultOptionID = "";
               strDefaultOptionsSelector = '#fb_holder_' + uid + ' div[id^=fb_option_row_] input[id^=default_option]:checked';
               var defaultOptions = $(strDefaultOptionsSelector);
               if (defaultOptions.length > 0){
                   defaultOptionID = $($(strDefaultOptionsSelector)[0]).attr('id');
               }

               // Add Values to dictionary
               var field = {
                   id:uid,
                   pos:posIndex,
                   parentcontrol:controlID,
                   controlType:controlType,
                   displayType:displayType,
                   required:controlRequired,
                   label:controlLabel,
                   help:controlHelpText,
                   defaultoption:defaultOptionID,
                   choices:field_options
               };

               return field;
        };

        // Using an array of predefined control names this can look up an entry via an id
        GetObjectID = function (objectID, parentID, childID){
            var namingConventionInfo = namingConventionTypes[objectID];
            var strRet = "";

            //Loop through list object returned and create id
              for (i=0;i<namingConventionInfo.length;i++){
               var row = namingConventionInfo[i];
               switch(row)
                {
                case 'pid':
                   strRet = strRet + parentID + "_";
                  break;
                case 'cid':
                   strRet = strRet + childID + "_";
                  break;
                default:
                   strRet = strRet + row + "_";
                }
              }
              if (strRet.length > 0){
                var iLen = String(strRet).length;
                strRet = String(strRet).substring(0, iLen - 1);
              }

             //Prefix with unique id for this form
             return formid + '_' + strRet;
        };

        GetJQObjectID = function (objectID, parentID, childID){
            return '#' + GetObjectID (objectID, parentID, childID);
        };

        /* Setupscreen Options */
        SetupScreen = function(strScreenMode){

            //If new screen mode is not easy sort then save previous sorting
            if(CurrentScreenMode=='easysort'&&strScreenMode!='easysort'){
                //Save easy sort as we are moving to another screen.
                SaveNewSortOrder();
            }

            //Init
            var mainDesignID = $(ul_obj).attr('id');
            var designer = $('#' + mainDesignID);
            var wrapperES = mainDesignID + '_easysort_wrapper';
            var easysort = $('#' + wrapperES);
            var wrapperTD = mainDesignID + '_testdrive_wrapper';
            var testdrive = $('#' + wrapperTD);
            var currObject = null;
            var newMode = null;
            var showToolbox = false;

            // Hide all items
            designer.fadeOut(300);
            easysort.fadeOut(300);
            testdrive.fadeOut(300);
            $(opts.menu_control_placeholder).hide();

            if(CurrentScreenMode=='design')
                currObject = designer;
            if(CurrentScreenMode=='easysort')
                currObject = easysort;
            if(CurrentScreenMode=='testdrive')
                currObject = testdrive;

            // Get new mode
            if(strScreenMode=='design'){
                newMode = designer;
                showToolbox = true;
            }
            if(strScreenMode=='easysort')
                newMode = easysort;
            if(strScreenMode=='testdrive')
                newMode = testdrive;

            CurrentScreenMode = strScreenMode;

            //Perform Hide and Show
            $(currObject).fadeOut(300,function(){$(newMode).fadeIn(300);if(showToolbox)$(opts.menu_control_placeholder).show();});

        };
        
        /* Easy Sort Options */
        SetupScreen_EasySort= function(){

            //INit
            var mainDesignID = $(ul_obj).attr('id');
            var wrapperDIVID = mainDesignID + '_easysort_wrapper';
            var sortableULID = mainDesignID + '_easysort'


            //Does the wrapper div exist  if yes remove and start again
            var wDiv = $('#' + wrapperDIVID);
            if($(wDiv).length> 0)
            $(wDiv).remove();

            //Create new div
            wDiv = create_FB_Div().attr('id',wrapperDIVID);
            wDiv.hide();

            //Add ul to div
            var es = create_FB_UL();
            es.attr('id',sortableULID);
            es.addClass('easysort');
            wDiv.append(es);

            //Get Fields Json
            var jsonDict = getfieldsJSON();

            //Loop Through Dictioary and add <li> entries to easy sort
            for(var control in jsonDict){
                var li = create_FB_LI();
                var control_attrs = jsonDict[control];
                li.attr('id',control_attrs.id)
                    .text(control_attrs.label)
                    .addClass('fb-item-easysort')
                    .addClass('fb-round-corners')
                    .addClass(control_attrs['type']);
                es.append(li);
            }

            //Set as sortable
            $(es).sortable({
                axis : 'y',
                placeholder: 'fb-item-easysort-dropzone',
                forcePlaceholderSize: true,
                update : function () {updateSort();}
            });

            //Add finish sort buttons
            //cancelSort = $('<a class="cancelbutton smallerbutton floatleft">cancel</a>');
            //cancelSort.click(function(){ $(wDiv).fadeOut(700,function(){$(ul_obj).fadeIn(300);});$(opts.menu_control_placeholder).show(); })
            //cancelSort.click(function(){ SetupScreen('design');});


            //saveSort  = $('<a class="savebutton smallerbutton floatleft">save</a>');
            //saveSort.click(function(){ SaveNewSortOrder(); });

            //es.after(saveSort);
            //es.after(cancelSort);

            //Slide Design Out
            $(ul_obj).after(wDiv);
            SetupScreen('easysort');
            //$(ul_obj).fadeOut(700,function(){wDiv.fadeIn(300);});
            //$(opts.menu_control_placeholder).hide();
            //wDiv.fadeIn(300,);
        };

        SaveNewSortOrder= function(){
            // Get The New Sort Order
            var mainDesignID = $(ul_obj).attr('id');
            var sortableULID = mainDesignID + '_easysort'
            var newSortOrder = GetSortOrder('#' + sortableULID);
            var wrapperDIVID = mainDesignID + '_easysort_wrapper';

            //Create temp ul
            var mainDesignID = $(ul_obj).attr('id');
            var tempsortableULID = mainDesignID + '_easysort_temp'
            var tempSort = create_FB_UL();
            tempSort.attr('id',tempsortableULID);

            // Copy Current list items to a temp ul.
            $(tempSort).append($('#' + mainDesignID + '>li'))
            $(tempSort).hide();

            // Empty the live ul holder
            $(ul_obj).empty();

            // Copy temp elements to document in a hidden state
            $(ul_obj).after(tempSort)

            // Loop through new list and get li from temp ul to live appending in order
            for(var control in newSortOrder){
                var control_attrs = newSortOrder[control];
                var JQObjID   = GetJQObjectID('P',control_attrs.id);
                $(ul_obj).append($(JQObjID));
            }

            // Remove the temp ul
            $('#' + tempsortableULID).remove();

            //Show new sorted list
            //$('#' + wrapperDIVID).fadeOut(700,function(){$(ul_obj).fadeIn(300);$(opts.menu_control_placeholder).show();});
            //SetupScreen('design');
        };

        GetSortOrder= function(sort_ul){

           var fields = {};
           var selectorLi = '#' + $(sort_ul).attr('id') + '>li';
           var liLength = $(selectorLi).length;
           for (var liIndex=0;liIndex<liLength;liIndex++){
               var liRow = $(sort_ul).children()[liIndex];

               //uid
               var uid = $(liRow).attr('id');

               // Get Field Dictionary
               var field = {id:uid,pos:liIndex};

               //Add field to dictionary
               fields[liIndex] = field;
           }
            return fields;
       };

        /* Setup Screen Test Drive */
        SetupScreen_TestDrive= function(){

            //INit
            var mainDesignID = $(ul_obj).attr('id');
            var wrapperDIVID = mainDesignID + '_testdrive_wrapper';
            var sortableULID = mainDesignID + '_testdrive'


            //Does the wrapper div exist  if yes remove and start again
            var wDiv = $('#' + wrapperDIVID);
            if($(wDiv).length> 0)
                $(wDiv).remove();

            //Create new div
            wDiv = create_FB_Div().attr('id',wrapperDIVID);
            wDiv.hide();

            //Append runtime controls to new div
            wDiv.append($('#' + $(ul_obj).attr('id') + '>li').clone()
                    .removeClass('fb-round-corners')
                    .addClass('borderbottom'));

            //Add finish sort buttons
            //cancelTD = $('<a class="cancelbutton smallerbutton floatleft">Finish Testing</a>');
            //cancelTD.click(function(){ $(wDiv).fadeOut(700,function(){$(ul_obj).fadeIn(300);});$(opts.menu_control_placeholder).show(); })
            //cancelTD.click(function(){ SetupScreen('design');});
            //wDiv.append(cancelTD);

            //Add to main page
            $(ul_obj).after(wDiv);

            //Remove Design options
            $('#' + wrapperDIVID + ' div.fb-legend').remove();
            $('#' + wrapperDIVID + ' div.fb-holder').remove();
            $('#' + wrapperDIVID + ' div').removeClass('fb-runtime');
            $('#' + wrapperDIVID + ' li').removeClass('fb-item-border');

            SetupScreen('testdrive');
            //$(ul_obj).fadeOut(700,function(){wDiv.fadeIn(300);});
            //$(opts.menu_control_placeholder).hide();
            //wDiv.fadeIn(300);
        };

        return this;
    }
});





/* Magic List Json Load Code
 *                 if(typeof(controlAttributes) == 'object'){
                    if (typeof(controlAttributes.OPTIONS) != 'undefined' && typeof(controlAttributes.OPTIONS) == 'object') {
                        //Add all of the options here
                        jQuery.each(controlAttributes.OPTIONS,function(opt){
                            var _id = id;
                            var _optID = getFBID();
                            var _blankDiv = create_FB_Div();
                            var _removeLink = $('<a href="#">remove</a>').click(function(){$(this).parent().remove();});
                            var mlBlankRow =  create_FB_Div().attr('id','fb_option_row_' + _optID + '_' + _id );
                            var optVal = '';
                            var optDefault = false;
                            if(typeof(this.OPTION) != 'undefined'){
                                optVal = this.OPTION;
                            }
                            if(typeof(this.SELECTED) != 'undefined'){
                                optDefault = this.SELECTED;
                            }
                            _blankDiv.attr('id','fb_option_row_' + _optID + '_' + _id );

                            _blankDiv.append($('<span></span>').append(create_FB_Input('default_option_' + _optID + '_' + _id,'radio',1).attr('checked',optDefault).addClass('fb-radio-option')));
                            _blankDiv.append($('<span></span>').append(create_FB_Input('option_' + _optID + '_' + _id,'text',optVal).addClass('fb-text-option')));
                            _blankDiv.append(_removeLink);
                            mlContainer.append(_blankDiv);
                        });
                    }
                }
 */