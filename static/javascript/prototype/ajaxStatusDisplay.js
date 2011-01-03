var ajaxStatus = Class.create();
ajaxStatus.prototype = {
	ajaxStatusDisplayUserMessageElementID: 'ajaxStatusDisplay_userMessage',
	ajaxStatusContainerID: 'ajaxStatusContainer',
	ajaxStatusContainerCssClass: 'ajaxStatusDisplay_userStyle',
	userDefinedAjaxStatusContainerCssClass: false,
	ajaxStatusMessageContainerID: 'ajaxStatusMessageContainer',
	ajaxStatusMessageContainerCssClass: 'ajaxStatusDisplay_userMessageStyle',
	userDefinedAjaxStatusMessageContainerCssClass: false,
	useUserCssStylesContainerID: 'ajaxStatusDisplay_useUserCssStyles',
	statusMessage: 'Loading...',
	useUserCssStyles: false,
	/*
	Function:	initialize
	Description: Creates the hidden status display elements and configures
	the default status message and css styles
	*/
	initialize: function() {
		// Create the ajax status container
		Element.insert(
			$$('body')[0],
			{'bottom':
				new Element('div', {
					id: this.ajaxStatusContainerID,
					style: 'display: none'
				})
			}
		);
 
		// Create the ajax status message container
		Element.insert(
			$(this.ajaxStatusContainerID),
			{'bottom':
				new Element('div', {
					id: this.ajaxStatusMessageContainerID
				})
			}
		);
 
		// Setup the css styles
		this.setCssStyles();
 
		// Setup the status message text
		this.setStatusMessage('');
 
		// Register the global Ajax responders
		// to show hide the status container
		Ajax.Responders.register({
			onCreate: this.toggle.bindAsEventListener(this),
			onComplete: this.toggle.bindAsEventListener(this)
		});
	},
	setCssStyles: function() {
		// If the user has defined styles
		if (document.styleSheets.length > 0) {
			var theRules = new Array();
 
			// If this is Firefox or other W3C complient browser
			if (document.styleSheets[0].cssRules) {
				theRules = document.styleSheets[0].cssRules;
			}
			// If this is IE
			else if (document.styleSheets[0].rules) {
				theRules = document.styleSheets[0].rules;
			}
 
			// Loop over the css rules
			for (i = 0; i < theRules.length; i++) {
				// If the current rule matches the name of the ajax status container css class
				if (theRules[i].selectorText == '.' + this.ajaxStatusContainerCssClass) {
					this.userDefinedAjaxStatusContainerCssClass = true;
				}
				// If the current rule matches the name of the ajax status message container css class
				else if (theRules[i].selectorText == '.' + this.ajaxStatusMessageContainerCssClass) {
					this.userDefinedAjaxStatusMessageContainerCssClass = true;
				}
			}
		}
 
		// If the user definfed css styles with the specific name
		// for the ajax status container
		if (this.userDefinedAjaxStatusContainerCssClass) {
			// Set css class name for the container
			$(this.ajaxStatusContainerID).addClassName(this.ajaxStatusContainerCssClass);
		}
		else {
			// The user has not defined the custom css style class
			// so apply default style
			$(this.ajaxStatusContainerID).setStyle({
				position: 'absolute',
				left: '45%',
				top: '2px',
				height: '10px'
			});
		}
 
		// If the user definfed css styles with the specific name
		// for the ajax status message container
		if (this.userDefinedAjaxStatusMessageContainerCssClass) {
			$(this.ajaxStatusMessageContainerID).addClassName(this.ajaxStatusMessageContainerCssClass);
		}
		else {
			// The user has not defined the custom css style class
			// so apply default style
			$(this.ajaxStatusMessageContainerID).setStyle({
				background: '#FFF1A8 none repeat scroll 0%',
				color: '#000',
				padding: '0pt 5px',
				fontFamily: 'Arial, Helvetica, sans-serif',
				fontSize: '14px',
				fontWeight: 'bold',
				textAlign: 'center',
				width: '100%'
			});
		}
	},
	setStatusMessage: function(statusMessage) {
		if (!statusMessage.empty()) {
			this.statusMessage = statusMessage;
		}
		else {
			// If there is an element on the page with a user defined status message
			if ($(this.ajaxStatusDisplayUserMessageElementID)) {
				// If the user's status message is inside a input element
				if ($(this.ajaxStatusDisplayUserMessageElementID).readAttribute('value') != null) {
					// Use the value of the input element
					// for the display as the status
					this.statusMessage = $F(this.ajaxStatusDisplayUserMessageElementID);
				}
				else {
					// Use the value of the element for the display as the status
					this.statusMessage = $(this.ajaxStatusDisplayUserMessageElementID).innerHTML;
				}
 
				// Hide the user's status message container
				$(this.ajaxStatusDisplayUserMessageElementID).hide();
			}
		}
 
		$(this.ajaxStatusMessageContainerID).update(this.statusMessage);
	},
	toggle: function() {
		$(this.ajaxStatusContainerID).toggle();
	}
};
 
document.observe("dom:loaded", function() {
	// Create an instance of the object defined above
	ajaxStatusDisplay = new ajaxStatus();
});