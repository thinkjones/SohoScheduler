/* Copyright (c) 2008 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
  * Add support for Array.some() on older browsers.
  */
if (!Array.prototype.some)
{
 Array.prototype.some = function(fun)
 {
   var len = this.length;
   if (typeof fun != "function")
     throw new TypeError();

   var thisp = arguments[1];
   for (var i = 0; i < len; i++)
   {
     if (i in this &&
         fun.call(thisp, this[i], i, this))
       return true;
   }

   return false;
 };
}

var Picker = {
  AUTH_SCOPE: 'http://www.google.com/m8/feeds/',
  CONTACTS_URL: 'http://www.google.com/m8/feeds/contacts/default/full',
  GROUPS_URL: 'http://www.google.com/m8/feeds/groups/default/full',
  
  GROUPS_PANE_ID: 'picker_groups_pane',
  CONTACTS_PANE_ID: 'picker_contacts_pane',
  INFO_PANEL_ID: 'picker_info_pane',
  INFO_CONTAINER_ID: 'picker_info_container',
  
  GROUPS_LIST_ID: 'picker_groups',
  CONTACT_LIST_ID: 'picker_contacts',
  CONTACTS_TOADD_LIST_ID: 'picker_contacts_to_add',
  
  GROUP_SELECTED_CLASS: 'picker_selected',
  GROUP_END_SPECIAL_CLASS: 'picker_endspecial',
  CONTACT_SELECTED_CLASS: 'picker_selected',
  
  CONTACT_INFO_BLOCK_CLASS: 'picker_info_block',
  CONTACT_INFO_TITLE_CLASS: 'picker_info_title',
  CONTACT_INFO_META_CLASS: 'picker_info_meta',
  GOOGLE_MAPS_QUERY_URL: 'http://maps.google.com/?q=',
  
  serviceName: 0,
  contactsService: 0,
  container: 0,
  groupSelector: 0,
  userAddCallback: 0,
  userRemoveCallback: 0,
  errorCallback: 0,
  selectedGroup: 0,
  selectedUser: 0,
  selectedUsers: [],
  
  /* Callback functions */
  
  /**
   * Callback function invoked by the Google Contacts library after 
   * calling populateGroups(). Generates the DOM entries that comprise the 
   * list of group entries. Do not call directly.
   * 
   * @param feedRoot The list of groups as returned by the Contacts 
   *        service.
   */
  processGroupFeed: function(feedRoot) {
    // Convert result set to an array of entries
    var entries = feedRoot.feed.entry;
    
    var newGroupList = document.createElement('ul');
    newGroupList.id = Picker.GROUPS_LIST_ID;    
    
    // Write out new list of groups
    for (var i = 0; i < entries.length; i++) {
      var entry = entries[i];
      var newGroup = document.createElement('li');
      newGroup.id = 'picker-group-' + i;
      
      // Create a hyperlink to represent the group
      var newGroupSelector = document.createElement('a');
      newGroupSelector.setAttribute('href', 
          'javascript:Picker.displayContactGroup(\'' 
          + entry.getId().getValue() + '\', \'' + newGroup.id + '\')');
      var name = entry.getTitle().getText();
      
      // Finalize group and add to groups pane
      newGroupSelector.appendChild(document.createTextNode(name));
      newGroup.appendChild(newGroupSelector);
      newGroupList.appendChild(newGroup);
    }
    
    // Replace the old group list with the newly generated one
    var groupsPane = document.getElementById(Picker.GROUPS_PANE_ID);
    var oldGroupsList = document.getElementById(Picker.GROUPS_LIST_ID);
    groupsPane.replaceChild(newGroupList, oldGroupsList);
    
    // Update the list of contacts
    //Picker.displayContactGroup(Picker.CONTACTS_URL, allContactsGroup.id);


    //Add Contacts List Header
    var jLIHeader =  $('<li>Contact Groups</li>').addClass('picker_header');
    $('#' + Picker.GROUPS_LIST_ID).prepend($(jLIHeader));

    //Render Final Column
    Picker.renderContactsToAddPanel();
  },
  
  /**
   * Callback function invoked by the Google Contacts library after calling
   * populateContatcts(). Generates the DOM entries that comprise the list 
   * of contact entries. Do not call directly.
   * 
   * @param feedRoot The list of contact entries as returned by the 
   *        Contacts service.
   */
  processContactFeed: function(feedRoot) {
    // Convert result set to an array of entries
    var entries = feedRoot.feed.entry;
    
    var newContactList = document.createElement('ul');
    newContactList.id = Picker.CONTACT_LIST_ID;

    var addAllDone = false;

    // Write out new list of groups
    for (var i = 0; i < entries.length; i++) {
        //if(addAllDone==false){
         //   newContactList.appendChild("<li>Add All</li>");
          //  addAllDone = true;
        //}
      var entry = entries[i];
      var id = entry.getId().getValue()
      var newContact = document.createElement('li');
      newContact.id = 'picker_contact_' + i;

      // List the contact's name next to the checkbox
      var name = 0;
      if (entry.getTitle() && entry.getTitle().getText()) {
        name = entry.getTitle().getText();
      } else if (entry.getEmailAddresses()) {
        name = entry.getEmailAddresses()[0].getAddress();
      } else {
        // This should never actually be reached, since users are currently
        // required to have either a name or an email address
        name = 'Untitled Contact';
      }

      //Create check box in this style
      //<label for="checkbox2">This is the Label</label>
	  //<input name="checkbox2" id="checkbox2" type="checkbox" value="true" class="crirHiddenJS" />

      //Create Label
      var objLabel = document.createElement('label');
      var chkID = 'chk' + i;
      $(objLabel).attr('for',chkID).text(name);

      //Create input box
      var objInput = document.createElement('input');
      $(objInput).attr('name',chkID).attr('id',chkID).attr('type','checkbox').val(false).addClass('crirHiddenJS').attr('atomid',id).attr('contactname',name);
      $(objInput).click(function(){
            Picker.syncContactsToAdd();
      });

      //Append info to the li
      $(newContact).append(objLabel).prepend(objInput);

      //Append this to the li
      $(newContactList).append(newContact);

    }

    // Replace the old contact list with the newly generated one
    var contactsPane = document.getElementById(Picker.CONTACTS_PANE_ID);
    var oldContactList = document.getElementById(Picker.CONTACT_LIST_ID);
    contactsPane.replaceChild(newContactList, oldContactList);

    //Create Options All
    var objAll = document.createElement('a');
    $(objAll).text('All').attr('href','#');
    $(objAll).click(function(){
        $('#' + Picker.CONTACT_LIST_ID).find('input').attr('checked',true).append(' ');
        Picker.syncContactsToAdd();
    });

    //Create Options None
    var objNone = document.createElement('a');
    $(objNone).text('None').attr('href','#');
    $(objNone).click(function(){
        $('#' + Picker.CONTACT_LIST_ID).find('input').attr('checked',false).append(' ');
        Picker.syncContactsToAdd();
    });

    //Add Contacts List Menu
    var jLIMenu =  $('<li></li>').append('Select: ').append(objAll).append(' ').append(objNone).addClass('picker_menu');
    $('#' + Picker.CONTACT_LIST_ID).prepend($(jLIMenu));

    //Add Contacts List Header
    var jLIHeader =  $('<li>Contacts</li>').addClass('picker_header');
    $('#' + Picker.CONTACT_LIST_ID).prepend($(jLIHeader));

  },
    
  /**
   * Callback method invoked when a user has been added by selecting the
   * user's checkbox. Used by updateStatus(), do not call directly.
   * 
   * @param entryRoot The root node for the entry that should be added 
   *        as returned by the Contacts service.
   */
  callUserAddCallback: function(entryRoot) {
    var entry = entryRoot.entry;
    var id = entry.getId().getValue();
    
    // Check to see if the contact has already been added. If not, add
    // the contact to the list of added IDs.
    var match = Picker.selectedUsers.some(function(selectedUserId) {
      return (selectedUserId == id);
    });
    
    if (!match) {
      Picker.selectedUsers.push(id);
    } else {
      Picker.error('Attempt to add a contact which has already been added.');
    }
    
    // Invoke callback
    if (Picker.userAddCallback != 0 && typeof(Picker.userAddCallback) != 
        'undefined') {
      Picker.userAddCallback(entry);
    } else {
      Picker.error('User callback function undefined: userAddCallback');
    }
  },
  
  /**
   * Callback method invoked when a user has been removed by deselecting 
   * the user's checkbox. Used by updateStatus(), do not call directly.
   * 
   * @param entryRoot The root node for the entry that should be removed 
   *        as returned by the Contacts service.
   */
  callUserRemoveCallback: function(entryRoot) {
    var entry = entryRoot.entry;
    var id = entry.getId().getValue();
    
    // Check to see if the contact has already been added. If so, remove
    // the contact to the list of added IDs.
    var match = false;
    for (var i = 0; i < Picker.selectedUsers.length; i++) {
      if (Picker.selectedUsers[i] == id) {
        match = true;
        break;
      }
    }
    
    if (match) {
      Picker.selectedUsers.splice(i, 1);
    } else {
      Picker.error('Attempt to remove a contact which has not been added.');
    }
    
    // Invoke callback
    if (Picker.userRemoveCallback != 0 && typeof(Picker.userRemoveCallback) 
        != 'undefined') {
      Picker.userRemoveCallback(entry);
    } else {
      Picker.error('User callback function undefined: userRemoveCallback');
    }
  },
  
  /* Class methods */
  
  /**
   * Create an authenticated session with the Google Contacts server. 
   * Requires that setServiceName() has been called previously.
   */
  login: function() {
    if (this.serviceName != 0 && typeof(this.serviceName) != 'undefined') {
      // Obtain a login token
      google.accounts.user.login(this.AUTH_SCOPE);
      // Create a new persistant service object
      this.contactsService = new google.gdata.contacts.ContactsService(
        this.serviceName);
    } else {
      this.error('Service name undefined, call setServiceName()');
    }
  },
  
  /**
   * Destroy the current Google Contacts session, including cached 
   * authentication tokens.
   */
    logout: function() {
      google.accounts.user.logout();
      this.container.innerHTML = '<h3 align=\'center\'>Please Sign In To' +
        ' Use This Feature</h3><p align=\'center\'><input type=\'button\'' + 
        ' value=\'Sign In\' onclick=\'Picker.login()\' /></p>';
    },
  
  /**
   * Display an error message. Custom behavior can be defined by using
   * setErrorCallback() to register a callback function.
   * 
   * @param errorMessage The error string to display.
   */
  error: function(errorMessage) {
    if (this.errorCallback != 0 && typeof(this.errorCallback) 
        != 'undefined') {
      this.errorCallback(errorMessage);
    } else {
      alert(errorMessage);
    }
  },
  
  /**
   * Set the service name which will be provided to the Google Contacts
   * servers during login. This name should uniquely identify yourself,
   * your application's name, and your application's version. For example:
   * "Google-PickerSample-1-0" would represent Google Picker Sample v1.0.
   * 
   * @param serviceName A string indicating your service's name.
   */
  setServiceName: function(serviceName) {
    this.serviceName = serviceName;
  },
  
  /**
   * Set a callback function which will be invoked when a error is 
   * thrown. If not set or set to 0, then alert() will be used as a 
   * default error handler. This function should accept a single 
   * parameter: A string representing the error message.
   * 
   * @param callback The callback function to use, or 0 if alert() should
   *        be used instead.
   */
  setErrorCallback: function(callback) {
    this.errorCallback = callback;
  },
  
  /**
   * Set a callback function which will be invoked when a new user is
   * selected. This function should accept a single parameter: a 
   * ContactEntry representing the newly selected contact.
   */
  setUserAddCallback: function(callback) {
    this.userAddCallback = callback;
  },
  
  /**
   * Set a callback function which will be invoked when a user is
   * deselected. This function should accept a single parameter: a 
   * ContactEntry representing the newly deselected contact.
   */
  setUserRemoveCallback: function(callback) {
    this.userRemoveCallback = callback;
  },

  renderContactsToAddPanel: function(){
    //Init
    var jContactsPanel = $('#' + Picker.INFO_PANEL_ID);

    // Add UL
    var newContactsToAddList = document.createElement('ul');
    newContactsToAddList.id = Picker.CONTACTS_TOADD_LIST_ID;

    //Add Header
    var jLIHeader =  $('<li>Contacts To Import</li>').addClass('picker_header');
    $(newContactsToAddList).append(jLIHeader);

    //Add Ul To panel
    $(jContactsPanel).append(newContactsToAddList);

 },

  syncContactsToAdd: function(){

      // Loop thorugh contacts and syn with contacts to add.
      var julSource = $('#' + Picker.CONTACT_LIST_ID);
      var julDest = $('#' + Picker.CONTACTS_TOADD_LIST_ID);

      //Loop through source
      var sourceInputs = $(julSource).find('input');
      for(var i=0;i<sourceInputs.length;i++){
          //Is checked?
          var thisInput = $(sourceInputs[i]);
          var thisInputIsChecked = $(thisInput).attr('checked');
          var atomId = $(thisInput).attr('atomid');
          var thisContactName = $(thisInput).attr('contactname');

          var destEntry = $(julDest).find('li[atomid="' + atomId + '"]');
          if(thisInputIsChecked==true){
              //Make sure it is in RHS
              if($(destEntry).length==0){
                  //Needs to be added
                  Picker.addContactDetails(thisContactName,atomId);
              }
          }else{
              //Remove From RHS irrespective of whether it is there or not.
              $(destEntry).remove();
          }
      }

      Picker.setupImportContactsHeader();
  },

  setupImportContactsHeader: function(){

    var julHeader = $('#' + Picker.CONTACTS_TOADD_LIST_ID);
    var itemsSelected = $(julHeader).find('.picker_info_title');

    // if not items remove header and return
    if($(itemsSelected).length == 0){
        //Remove header if exists
        $(julHeader).find('.picker_menu').remove();
        return;
    }
    
    //Create Options None
    var objNone = document.createElement('a');
    $(objNone).text('Remove All').attr('href','#');
    $(objNone).click(function(){
        //Remove all items from checked menu
        $(julHeader).find('.picker_info_title').remove();
        $(julHeader).find('.picker_menu').remove();

        //Uncheck any checked items
        $('#' + Picker.CONTACT_LIST_ID).find('input[type=checkbox]').attr('checked', false);
    });

    //Add Contacts List Menu
    if($(julHeader).find('.picker_menu').length == 0){
        var jLIMenu =  $('<li></li>').append('Select: ').append(' ').append(objNone).addClass('picker_menu');
        $(julHeader).find('.picker_header').after($(jLIMenu));
    }

  },

  addContactDetails: function(contactName, atomId) {

    //Init
    var jCTA = $('#' + Picker.CONTACTS_TOADD_LIST_ID);

    // Get Contact name
    //var contactName = $(this).text();

    //Check whether contact already exists
    if(jCTA.find('li[atomId="' + atomId + '"]').length > 0 ){
        return;
    }


    //Add New Contact Entry
    var jLIHeader =  $('<li></li>')
                .addClass('picker_info_title')
                .attr('atomid',atomId)
                .text(contactName);

    //Add Entry to list
    $(jCTA).append(jLIHeader);
    //alert(atomId + ' ' + elementId);
  },
  
  /**
   * Display details for a given contact.
   * 
   * @param groupId The Atom ID of the group which should be retrieved.
   * @param elementId The DOM element ID which should be marked as 
   *        selected.
   */
  showContactDetails: function(atomId, elementId) {
    // Retrieve details for contact
    this.contactsService.getContactEntry(
      atomId,
      this.processContactDetails, 
      this.error);
    
    // De-select the old contact, if any
    if (this.selectedContact != 0 && typeof(this.selectedContact) != 
        'undefined') {
      this.selectedContact.className = '';
    }

    // Mark the new contact as selected
    var element = document.getElementById(elementId);
    element.className = this.CONTACT_SELECTED_CLASS;
    this.selectedContact = element;
  },

  /**
   * Update whether a given entry is selected or not. Automatically 
   * invoked whenver a contact's checkbox is toggled.
   *
   * @param selectorId The ID of the DOM node whose status has been 
   *        changed. Ordinarily the ID of the checkbox invoking this
   *        method.
   */
  updateStatus: function(selectorId) {
    // Get the ID of the contact selected, as well as the state of the
    // checkbox
    var selector = document.getElementById(selectorId);
    var contactID = selector.value;
    var contactState = selector.checked;
    
    // Retrieve user information and dispatch to user callback
    if (contactState == true) {
      // Adding new user
      this.contactsService.getContactEntry(
        contactID,
        this.callUserAddCallback, 
        this.error);
    } else {
      // Removing existing user
      this.contactsService.getContactEntry(
        contactID,
        this.callUserRemoveCallback, 
        this.error);
    }
  },
  
  /**
   * Retrieve the list of user's groups and populate the group list. */
  populateGroups: function() {
    // Compose a new query requesting all groups
    var query = new google.gdata.contacts.ContactQuery(this.GROUPS_URL);
    query.setParam('max-results', 1000);
    
    // Submit query for asynchronous execution. After execution, 
    // processGroupFeed() will be called on success, error() on 
    // failure.
    this.contactsService.getContactGroupFeed(
        query, this.processGroupFeed, this.error);
  },
  
  /**
   * Retrieve the group ID associated with a DOM group selector, mark it 
   * as selected, then retrieve the list of contact entries for the current
   * group and populate the contact list. 
   * 
   * @param groupId The Atom ID of the group which should be retrieved.
   * @param elementId The DOM element ID which should be marked as 
   *        selected.
   */
  displayContactGroup: function(groupId, elementId) {
    // Locate the given DOM element
    var selector = document.getElementById(elementId);

    // De-select the old group
    if (this.selectedGroup != 0 && 
          typeof(this.selectedGroup) != 'undefined') {
      if (this.selectedGroup.className == 
          this.GROUP_SELECTED_CLASS + ' ' + this.GROUP_END_SPECIAL_CLASS) {
        this.selectedGroup.className = this.GROUP_END_SPECIAL_CLASS;
      } else {
        this.selectedGroup.className = '';
      }
    }
    
    // Select the new group
    if (selector.className == this.GROUP_END_SPECIAL_CLASS 
        || selector.className == this.GROUP_SELECTED_CLASS + ' ' 
        + this.GROUP_END_SPECIAL_CLASS) {
      selector.className = 
         this.GROUP_SELECTED_CLASS + ' ' + this.GROUP_END_SPECIAL_CLASS;
    } else {
      selector.className = this.GROUP_SELECTED_CLASS;
    }
    this.selectedGroup = selector;
    
    // Compose a new query requesting all contacts for the given group
    var query = new google.gdata.contacts.ContactQuery(this.CONTACTS_URL);
    query.setParam('max-results', 1000);
    if (groupId != Picker.CONTACTS_URL)
      query.setParam('group', groupId);
    
    // Submit query for asynchronous execution. After execution, 
    // processGroupFeed() will be called on success, error() on 
    // failure.
    this.contactsService.getContactFeed(query, this.processContactFeed, 
        this.error);
  },
  
  /**
   * Create the initial layout for this class and insert it into a div
   * with the given name.
   * 
   * @param containerId The name of the div which will hold the contact
   *        picker.
   */
  render: function(containerId) {
    // Import the stylesheet for this script
    var stylesheet = document.createElement('style');
    stylesheet.setAttribute('type', 'text/css');
    var rulesDef = '\
      #' + containerId + ' {\
        font: 100% Arial, sans-serif;\
        background-color: #fff;\
        border: 2px solid #c3d9ff;\
        -moz-border-radius: 3px;\
        -webkit-border-radius: 3px;\
        position: relative;\
        top: 0.5em;\
      }\
      \
      #' + containerId + ' div {\
        height: 100%;\
        float: left;\
        margin: 0;\
        padding: 0;\
      }\
      \
      #' + containerId + ' div#picker_header_pane {\
        height: 32px;\
        background-color: #e0ecff;\
        vertical-align: middle;\
        width: 100%;\
      }\
      \
      #' + containerId + ' div#picker_groups_container {\
        width: 25%;\
        height: 250px;\
        position: relative;\
        border-right: 2px solid #c3d9ff;\
      }\
      \
      #' + containerId + ' div#picker_contacts_container {\
        width: 30%;\
        height: 250px;\
        position: relative;\
        border-right: 2px solid #c3d9ff;\
      }\
      \
      #' + containerId + ' div#picker_info_container {\
        width: 44%;\
        height: 250px;\
        position: relative;\
      }\
      \
      #' + containerId + ' div.picker_column {\
        width: 100%;\
      }\
      \
      #' + containerId + ' div#picker_groups_pane {\
        position: static;\
        overflow: auto;\
      }\
      \
      #' + containerId + ' div#picker_groups_pane li {\
        overflow: hidden;\
      }\
      \
      #' + containerId + ' div#picker_groups_pane li a {\
        width: 9999%;\
      }\
      \
      #' + containerId + ' div#picker_contacts_pane {\
        position: static;\
        overflow: auto;\
      }\
      \
      #' + containerId + ' div#picker_contacts_pane li {\
        overflow: hidden;\
      }\
      \
      #' + containerId + ' div#picker_contacts_pane li a {\
        width: 9999%;\
      }\
      \
      #' + containerId + ' div#picker_info_pane {\
        width: 100%;\
        position: relative;\
        overflow: auto;\
      }\
      \
      #' + containerId + ' div#picker_footer_pane {\
        height: 32px;\
        background-color: #e0ecff;\
        vertical-align: middle;\
        width: 100%;\
        clear: both;\
        float: none;\
      }\
      \
      #' + containerId + ' #picker_title {\
        font-weight: bold;\
        margin: 0;\
        padding: 0.4em;\
        height: 100%;\
        vertical-align: middle;\
        font-size: 125%;\
      }\
      \
      #' + containerId + ' ul {\
        list-style-type: none;\
        padding: 0;\
        margin: 0;\
      }\
      \
      #' + containerId + ' li {\
        margin: 0;\
        padding: 2px 5px;\
        height: 1.3em;\
        line-height: 1.3em;\
      }\
      \
      #' + containerId + ' li input {\
        margin: 0 3px;\
      }\
      \
      #' + containerId + ' li.picker_endspecial {\
        border-bottom: 1px solid #c3d9ff;\
      }\
      \
      #' + containerId + ' li a {\
        display: block;\
        color: #000;\
        text-decoration: none;\
      }\
      \
      #' + containerId + ' li.picker_selected, #' 
          + containerId + ' li.picker_selected:hover,  #'
            + containerId + ' li.picker_header {\
        background-color: #c3d9ff;\
        color: #0000cc;\
        font-weight: bold;\
      }\
      \
      #' + containerId + ' li.picker_selected a, #' + containerId 
          + ' li.picker_selected:hover a {\
        color: #0000cc;\
      }\
      \
      #' + containerId + ' li:hover {\
        background-color:  #ffffcc;\
      }\
      \
      #' + containerId + ' .' + Picker.CONTACT_INFO_BLOCK_CLASS + ' {\
        float: none;\
        width: 95%;\
        position: static;\
        padding: 0.5em;\
        height: auto;\
      }\
      \
      #' + containerId + ' #picker_info_pane p {\
        margin: 0;\
        padding: 0;\
      }\
      \
      #' + containerId + ' .' + Picker.CONTACT_INFO_TITLE_CLASS + ' {\
        font-weight: bold;\
        font-size: 1.1em;\
      }\
      \
      #' + containerId + ' .' + Picker.CONTACT_INFO_META_CLASS + ' {\
        color: #777;\
      }\
      \
      #' + containerId + ' #picker_logout {\
        padding: 0.6em;\
        margin: 0 1em;\
        line-height: 32px;\
      }\
      \
      #' + containerId + ' #picker_logout a {\
        text-decoration: none;\
      }';
    rulesDef = "";
    if (stylesheet.styleSheet) {
      // IE-specific hack
      stylesheet.styleSheet.cssText = rulesDef;
    } else {
      // Everything else
      var rulesNode = document.createTextNode(rulesDef);
      stylesheet.appendChild(rulesNode);
    }
    document.getElementsByTagName('head')[0].appendChild(stylesheet);
    
    this.container = document.getElementById(containerId);
    
    // Make sure that the client library is initialized
    google.gdata.client.init(this.error);
    
    // Execute only if the current session is valid.
    if (google.accounts.user.checkLogin(this.AUTH_SCOPE)) {
      // Even though we're supposedly authenticated, let's be certain...
      this.login();
      
      // Render the basic UI framework
      this.container.innerHTML = '\
        <div id=\'picker_header_pane\'>\
          <p id=\'picker_title\'>Friend Picker Sample for Google Contacts\
              Data API</p>\
        </div>\
        <div id=\'picker_groups_container\'>\
        <div id=\'picker_groups_pane\' class=\'picker_column\'>\
             <ul id=\'picker_groups\'></ul>\
        </div>\
        </div>\
        <div id=\'picker_contacts_container\'>\
        <div id=\'picker_contacts_pane\' class=\'picker_column\'>\
          <ul id=\'picker_contacts\'></ul>\
        </div>\
        </div>\
        <div id=\'picker_info_container\'>\
          <div id=\'picker_info_pane\' class=\'picker_column\'></div>\
        </div>\
        <div id=\'picker_footer_pane\'><p align=\'right\' \
            id=\'picker_logout\'><a href=\'javascript:Picker.logout()\'>\
            &raquo; Logout</a></p>\
        </div>';
      
      // Begin loading data
      var groups = this.populateGroups();
    } else {
      // Display a login button
      this.container.innerHTML = 
        '<h3 align=\'center\'>Please Sign In To Use This Feature</h3>\
          <p align=\'center\'><input type=\'button\' value=\'Sign In\'\
          onclick=\'Picker.login()\' /></p>';
    }
  }
}

