/*
 * @author stuartb
 * @date 2008.10.08
 * @description Wizard forms made easy.
 */
jQuery(function($){
    // -------------------------------------------------------
	// Private Variables
	// -------------------------------------------------------
    var settings = null;
    var wizardLinks = null;
    var wizardPages = null;

    
    // -------------------------------------------------------
	// Public Functions
	// -------------------------------------------------------
    $.fn.wizard = function(options)
    {
         settings = $.extend({
             onShow: function(element,link) { return true; },
             onValidation: false,
             onBeforeNext:false,
             onBeforePrev:false,
             setupprevnext: true,
             addprevnext: true,
             submitpage: null,
             wizardstagelinks: false,
             wizardpages: false,
             wizardcontrols: "",
             currentpage: 0
          }, options);

       $.wizard = {
            manualPrev : function(){
                var wizardpage = $($(wizardPages)[settings.currentpage]);
                $(wizardLinks).removeClass("active");
                var wizardlink  = $($(wizardLinks)[settings.currentpage]);
                $(wizardlink).addClass("active");
                $.wizard.setupButtons(settings.currentpage);
            },
            manualNext : function(){
                settings.currentpage = settings.currentpage + 1;
                var wizardpage = $($(wizardPages)[settings.currentpage]);
                var wizardlink  = $($(wizardLinks)[settings.currentpage]);
                $(wizardLinks).removeClass("active");
                $(wizardlink).addClass("active");
                $(wizardPages).hide();
                $(wizardpage).fadeIn();
                settings.onShow(wizardpage);
                $.wizard.setupButtons(settings.currentpage);
            },
            pageInfo : function(currentPage){
                var eventObj = {
                    currentPage: null,
                    prevButton:  null,
                    nextButton:  null,
                    wizardlink: null
                };

                var wizardpage = $($(wizardPages)[currentPage]);
                var wizardlink  = $($(wizardLinks)[currentPage]);
                eventObj.currentPage = currentPage;
                eventObj.prevButton = $('.wizardprev');
                eventObj.nextButton = $('.wizardnext');
                eventObj.wizardLink = wizardlink;
                return eventObj;
            },
            setupButtons : function(currentPage){
                var numberofPages = $('.wizardpage').length;
                $('a.wizardprev').show(); // hide prev button on first page
                $('a.wizardnext').show(); // hide prev button on first page

                if(currentPage==0){
                    $('a.wizardprev').hide(); // hide prev button on first page
                }

                if(currentPage==numberofPages-1){
                    $('a.wizardnext').text('Finish'); // hide prev button on first page
                    $('a.wizardprev').hide(); // hide prev button on first page
                }
            }
        }

        //Render
        return this.each(function() {

            //Get Wizardstage links
            wizardLinks = $(this).find(settings.wizardstagelinks);

            //Get Wizardstage pages
            wizardPages = $(this).find(settings.wizardpages);

            // Hide all wizard stages and show first page
            $(wizardPages).hide();
            $($(wizardPages)[settings.currentpage]).show();

            // set first link to active
            $($(wizardLinks)[settings.currentpage]).addClass("active");

            //Launch show event for first page
            settings.onShow($(wizardLinks)[settings.currentpage]);

            //
            $.wizard.setupButtons(settings.currentpage);

            // Wire progress thingy
            //$(wizardLinks).each(function (i) {
            //    $(this).click(function(){
            //        var target = $(this).attr("href");
            //        $(this).parent().parent().children(".wizardpage").hide();
            //        $(target).fadeIn('slow');
            //        settings.onShow($(target), this);
            //        $(this).parent().children('a').removeClass('active', 'slow');
            //        $(this).addClass('active', 'slow');
            //        return false;
            //    });
            //});


            // Prevent form submission on a wizard page...
            $(wizardPages).each(function(i){
                // unless there is a submit button on this page
                if((settings.submitpage == null && $(this).find('input[type="submit"]').length < 1) ||
                   (settings.submitpage != null && !$(this).is(settings.submitpage)))
                {
                    $(this).find('input,select').keypress(function(event){
                        return event.keyCode != 13;
                    });
                }
            });

            if(settings.setupprevnext)
            {
                var jqWizardcontrols = null;

                // Add prev/next step buttons if requested or use ones already there
                if(settings.addprevnext){
                    $(wizardPages)
                    .append('<div class="row wizardcontrols"></div>')
                    .children(".wizardcontrols")
                    .append('<input type="button" class="wizardprev" value="< Back" /><input type="button" class="wizardnext" value="Next >" />');

                    jqWizardcontrols = $(wizardPages).children(".wizardcontrols");                    
                }else{
                    jqWizardcontrols = $(settings.wizardcontrols);
                }

                //Setup Wizard Prev Next Buttons


                // Wire prev/next step buttons
                $(jqWizardcontrols)
                .find('.wizardprev').click(function(){
                    //Process Before Previous
                    if(settings.onBeforePrev){
                        settings.onBeforePrev(settings.currentpage);
                    }

                    var wizardlink  = $($(wizardLinks)[settings.currentpage]);
                    $(wizardlink).removeClass("active");
                    settings.currentpage = settings.currentpage - 1

                    var wizardpage = $($(wizardPages)[settings.currentpage]);  //$(this).parent().parent(); // wizardcontrols div, wizardpage div
                    var wizardlink  = $($(wizardLinks)[settings.currentpage]);
                    $(wizardlink).addClass("active");

                    $(wizardPages).hide();
                    $(wizardpage).fadeIn();
                    settings.onShow(wizardpage);

                    // Can continue if you get here
                    $.wizard.manualPrev();

                });

                $(jqWizardcontrols)
                .find('.wizardnext').click(function(){

                    //Check for validation
                    var bolCanContinue = false;
                    if(settings.onValidation){
                        bolCanContinue = settings.onValidation($.wizard.pageInfo(settings.currentpage));
                    }
                    if(bolCanContinue==false){return;}

                    //Can go to next page?
                    if(settings.onBeforeNext){
                        var curPageInfo = $.wizard.pageInfo(settings.currentpage);
                        var nextPageInfo = $.wizard.pageInfo(settings.currentpage + 1);
                        bolCanContinue = settings.onBeforeNext(curPageInfo,nextPageInfo);
                    }
                    if(bolCanContinue==false){return;}

                    // Can continue if you get here
                    $.wizard.manualNext();
                });
            }


 
        });
    };
});
