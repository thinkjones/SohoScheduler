var varUseAjax = true;

var placeholder_entityid = '999999999999';

var debug_ajax = false;

var global_ajax_options = {
              type: "POST"
            };

function selectAjaxURL(strURL,callbackfunction) {
    if(varUseAjax){
        selectAjaxURLPart(strURL, "divMainContent",callbackfunction);
    }else{
            top.location.href = strURL;
    }
}

function selectAjaxURLPart(strURL, strDIV, callbackfunction) {
    if(debug_ajax)
        $("#debug_info").append(strURL + ' ' + strDIV + ' ' + callbackfunction + '<br />');

    if(varUseAjax){
        ShowAjaxMessage('selectAjaxURLPart');
        strDIV = '#' + strDIV;

        $(strDIV).load(strURL,global_ajax_options,function(){
            HideAjaxMessage('selectAjaxURLPart - postback');
           if(callbackfunction){
               callbackfunction();
           }
        });
    }else{
            top.location.href = strURL;
    }
}

function sohoJsonLoad(strURL, strDIV, callbackfunction,data) {
    if(debug_ajax)
        $("#debug_info").append(strURL + ' ' + strDIV + ' ' + callbackfunction + '<br />');

    if(varUseAjax){
        ShowAjaxMessage('selectAjaxURLPart');
        strDIV = '#' + strDIV;

        $(strDIV).load(strURL,data,function(){
            HideAjaxMessage('selectAjaxURLPart - postback');
           if(callbackfunction){
               callbackfunction();
           }
        });
    }else{
            top.location.href = strURL;
    }
}

function RedirectWithPostback(strURL){
    top.location.href = strURL;
}

function ShowAjaxMessage(source){
    // Try a new moethod of inserting the javascript into the top of the body.
    var html_loading_message = '<div id="global_ajax_message"><img src="/static/images/ajax-loader4.gif" alt="..." />&nbsp;Loading...</div>'
    $("body").prepend(html_loading_message);
    $("#global_ajax_message").fadeIn("slow");
    if(debug_ajax){
        if(!source)
            source = '';
        $("#debug_info").append('ShowAjaxMessage:' + source + '<br />');
    }
}
function HideAjaxMessage(source){
    $("#global_ajax_message").remove();
    if(debug_ajax){
        if(!source)
            source = '';
        $("#debug_info").append('HideAjaxMessage:' + source + '<br />');
    }
}

function SelectSubMenuTab(tabURLS, tabIndexSelected, divToUpdate){
    // Select Sub Tab
    $('#nav2>ul>li').removeClass('selected');
    $('#nav2>ul>li').eq(tabIndexSelected).addClass('selected');
    if(divToUpdate.length > 0){
        selectAjaxURLPart(tabURLS[tabIndexSelected], divToUpdate);
    }
}

function SetupTabNavigation(tabURLS, divToUpdate){
    //Setup Tabs
    $('#nav2>ul>li a').each(function(idx, item){
        $(this).click(function(){
                SelectSubMenuTab(tabURLS, idx, divToUpdate);
        });
    });
}

function SetupFormForAjax(jqsSubmitButtons, ajaxFormOptions, jqsFormID){
    // 1.  Setup Form Action Buttons to initiate form submission
    $(jqsSubmitButtons).each(function(idx, item){
        $(this).click(function(){
            $(jqsFormID).submit();
            return false;
	});
    });

    //2. Set Form to be an ajax submssion
    if(varUseAjax){
        $(jqsFormID).ajaxForm(ajaxFormOptions);
    }else{
        $(jqsFormID).attr("action",ajaxFormOptions['url']);
    }
    
    $(jqsFormID).submit(function() {
        if(varUseAjax)
            return false;
        else
            return true;
    });
}

function HideModal(strRefreshType,params)
{
    $.nyroModalRemove();
    if (strRefreshType){
        if (strRefreshType == 'ConfigurationSaved'){
            if(RefreshConfiguration)
                RefreshConfiguration();
        }
        if (strRefreshType == 'GotoNewEntityDashBoard'){
            location.href = params;
        }
        if (strRefreshType == 'RuntimeFormDataHasPosted'){
            if(RefreshAfterRuntime)
                RefreshAfterRuntime();
        }
        if (strRefreshType == 'TemplatePublished'){
            if(RefreshAfterTemplatePublish)
                RefreshAfterTemplatePublish();
        }
    }
}

function ReplaceButtonWithSavingGif(buttonToReplace, strLoadingText){
    //Assumes Jquery is installed
    $(buttonToReplace).hide();
    var phDiv = document.createElement('div');
    $(phDiv).append('<span id="ajaxmsg' + $(buttonToReplace).attr('id') +  '" class="ajaxmsg">' + strLoadingText + '</span>');
    $(buttonToReplace).after($(phDiv).html());
}
function ReplaceSavingGifWithButton(buttonToReplace){
    //Assumes Jquery is installed
    $('#ajaxmsg' + $(buttonToReplace).attr('id')).remove();
    $(buttonToReplace).show();
}

function ShowLoadingMessage(elementToAppendTo, strLoadingText){
    //Assumes Jquery is installed
    var phDiv = document.createElement('div');
    $(phDiv).append('<span class="ajaxmsg">'  + strLoadingText + '</span>');
    $(elementToAppendTo).html($(phDiv).html());
}

function ShowDoingMsg(idObjToHide, idObjToShow, idObjParentContainer){
    //$(JQParentContainerID).find("#lnkSaveFormJSON").fadeOut("fast",function(){$(JQParentContainerID).find("#divSaveFormJSON").show();});
    $(idObjParentContainer).find(idObjToHide).fadeOut("fast",function(){$(JQParentContainerID).find(ObjToShow).show();});
}

 function hideLoadingMessages(){
        $('.ajaxmsg').hide();
 }

function FadeOutAndRemove(selector){
    $(selector).fadeOut("slow",function(){$(selector).remove();});
}

function json_post(strURL, data, callbackFunc , call_type){
    //Ignore call_Type
    ShowAjaxMessage('json_post: :' + strURL);
    call_type = "json";

    $.post(strURL, data, function(data, textStatus){
        HideAjaxMessage('json_post - postback:' + strURL);
        callbackFunc(data, textStatus);
    }, call_type);
}

function ShowNotification(message_text,message_type){
    if(message_text!=''){
       var not_options = {timeout:3000};
        switch(message_type)
        {
        case 'success':
            $.n.success(message_text, not_options);
          break;
        case 'warning':
            $.n.warning(message_text, not_options);
          break;
        case 'error':
            $.n.error(message_text, not_options);
          break;
        default:
            $.n(message_text,not_options);
        }
    }
}