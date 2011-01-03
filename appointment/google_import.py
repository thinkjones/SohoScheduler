import gdata.spreadsheet.service
import gdata.spreadsheet.text_db
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import appointment.helpers

try: 
	from xml.etree import ElementTree
except ImportError:  
	from elementtree import ElementTree


def importdata(request, company_id):
	#1. init
	company = svrCompany.GetCompany(company_id)
	scope = 'http://spreadsheets.google.com/feeds/'
	googleauthenticated = False
	sfeed = None
	wfeed = None
	drToken = None
	spreadsheets = None
	stage = "1"
	worksheets = None
	worksheet_data = None
	spreadsheet_selected = None
	spreadsheet_selected_key = None
	worksheet_selected = None
	worksheet_selected_key = None
	gd_client = None
	authSubHref = None

	# If token passed from google process that
	if request.GET:
		authsub_token = request.GET['token']
		authsub_token_scope = scope
		gd_client = gdata.spreadsheet.service.SpreadsheetsService()
		gd_client.auth_token = authsub_token
		gd_client.UpgradeToSessionToken()
		authsub_token = gd_client.auth_token.split('=')[1]
		drToken = appointment.helpers.ServerStoredToken().SaveToken(users.get_current_user(),authsub_token, authsub_token_scope)
		return http.HttpResponseRedirect(reverse('schedule.views.importdata', args=[company_id]))
	else:
		drToken = appointment.helpers.ServerStoredToken().GetTokensByOwner(users.get_current_user())

	#Do we have a token therefore authentication stage has passed.
	if drToken:
		stage = "2"
		googleauthenticated = True

	#Test for post processeing
	if drToken:
		if request.POST:
			if request.POST['stage'] == "2":
				spreadsheet_selected = request.POST['ddlSpreadsheet']
				spreadsheet_selected_key = spreadsheet_selected.rsplit('/', 1)[1]
				stage = "3"
			if request.POST['stage'] == "3":
				spreadsheet_selected_key = request.POST['spreadsheet_selected_key']
				worksheet_selected = request.POST['ddlWorksheet']
				worksheet_selected_key = worksheet_selected.rsplit('/', 1)[1]
				stage = "4"

	#Stage = 1 - Authentication Required
	if stage == "1":
		authSubHref = GetAuthSubUrl(request, scope)

	#Stage = 2 - Get list of spreadsheets for this user
	if stage == "2":
		gd_client = gdata.spreadsheet.service.SpreadsheetsService()
		gd_client.auth_token = drToken.session_token
		sfeed = gd_client.GetSpreadsheetsFeed()
		spreadsheets = sfeed.entry

	#Stage = 3 - Get list of worksheets for this spreadsheet
	if stage == "3":
		gd_client = gdata.spreadsheet.service.SpreadsheetsService()
		gd_client.auth_token = drToken.session_token
		wfeed = gd_client.GetWorksheetsFeed(spreadsheet_selected_key)
		worksheets = wfeed.entry

	#stage 4 - Import data from worksheet
	if stage == "41":
		gd_client = gdata.spreadsheet.service.SpreadsheetsService()
		gd_client.auth_token = drToken.session_token
		worksheet_data = ListGetAction(gd_client, spreadsheet_selected_key,  worksheet_selected_key, company_id)

	if stage == "4":
		gd_client = gdata.spreadsheet.service.SpreadsheetsService()
		gd_client.auth_token = drToken.session_token
		query = gdata.spreadsheet.service.CellQuery()
		query['min-col'] = '1'
		query['max-col'] = '12'
		query['min-row'] = '1'
		query['max-row'] = '50'
		feed = gd_client.GetCellsFeed(spreadsheet_selected_key, worksheet_selected_key, query=query)
		#worksheet_data = ParseFeed(gd_client.GetCellsFeed(spreadsheet_selected_key, worksheet_selected_key, query=query))
		ImportCellFeed(feed, company_id)        

	# Generate the AuthSub URL and write a page that includes the link
	sohoResponse = SohoResponse(request, 'schedule/import')
	sohoResponse.company = company
	sohoResponse.tabSchedule = True
	sohoResponse.signed_up = True
	sohoResponse.company_id = company_id
	sohoResponse.authSubHref = authSubHref
	sohoResponse.spreadsheets = spreadsheets
	sohoResponse.worksheets = worksheets 
	sohoResponse.googleauthenticated = googleauthenticated
	sohoResponse.spreadsheet_selected = spreadsheet_selected
	sohoResponse.spreadsheet_selected_key = spreadsheet_selected_key
	sohoResponse.worksheet_selected = worksheet_selected
	sohoResponse.worksheet_data = worksheet_data

	sohoResponse.stage = stage
	sohoResponse.stage2 = stage

	return sohoResponse.respond()

def ParseFeed(feed):
	strRet = ""
	for i, entry in enumerate(feed.entry):
		if isinstance(feed, gdata.spreadsheet.SpreadsheetsCellsFeed):
			strRet = strRet , 'A %s %s %s<br />' % (entry.cell.row, entry.cell.col, entry.content.text)
		elif isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
			strRet = strRet, '<br/>B %s %s %s<br />' % (i, entry.title.text, entry.content.text)
			# Print this row's value for each column (the custom dictionary is
			# built from the gsx: elements in the entry.) See the description of
			# gsx elements in the protocol guide.
			strRet = strRet , 'Contents:'
			for key in entry.custom:
				strRet = strRet , 'C  %s: %s' % (key, entry.custom[key].text)
		else:
			strRet = strRet , 'D %s %s<br />' % (i, entry.title.text)
	return strRet

def ImportCellFeed(CellsFeed, company_id):
	q = db.GqlQuery("SELECT * FROM Schedule")
	results = q.fetch(500)
	for result in results:
		result.delete()

	company = svrCompany.GetCompany(company_id)
	strRet = ""
	currentRow = 0
	currentCol = 0
	addSchedule = None
	bolCanSave = False
	for i, entry in enumerate(CellsFeed.entry):
		if currentRow < 50 or 1==1:
			newCurrentRow = int(entry.cell.row)
			currentCol = int(entry.cell.col)

			#Determine if new row - if is then save and create new object
			if currentRow != newCurrentRow:
				#Save Previous Row
				if bolCanSave and currentRow > 2:
					if len(strImportError) > 0:
						addSchedule.booking_notes = strImportError
					addSchedule.company_reference = company
					addSchedule.put()

				#Create new row information
				currentRow = newCurrentRow
				addSchedule = Schedule()
				bolCanSave = True
				strImportError = ""

			#loop through row parameters and import.
			if currentCol == 1:
				dte = None
				try:
					dte = datetime.datetime.strptime(entry.content.text, "%d/%m/%Y")
				except ValueError:
					continue

				if isinstance(dte, datetime.datetime):
					addSchedule.booking_date = dte.date()
				else:
					bolCanSave = False

			if currentRow > 2:   
				if currentCol == 2:
					addSchedule.booking_time = entry.content.text.decode("utf-8")
				if currentCol == 3:
					customer_reference = svrCustomer.GetorCreate(company,entry.content.text.decode("utf-8"))
					addSchedule.customer_reference = customer_reference
				if currentCol == 4:
					addSchedule.booking_from = entry.content.text.decode("utf-8")
				if currentCol == 5:
					addSchedule.booking_to = entry.content.text.decode("utf-8")
				if currentCol == 6:
					try:
						addSchedule.number_of_passengers = int(entry.content.text.decode("utf-8"))
					except ValueError:
						#strImportError = strImportError.join("%s %s" % "PAX:", entry.content.text)
						continue

				if currentCol == 7:
					driver_car_reference = svrResourceCode.GetorCreate(company,entry.content.text.decode("utf-8"))
					addSchedule.driver_car = driver_car_reference
				if currentCol == 9 or currentCol == 10 or currentCol == 11:
					strPT = None
					if currentCol == 9:
						strPT = "Account"
					if currentCol == 10:
						strPT = "Cash or Cheque"
					if currentCol == 11:
						strPT = "Credit Card"

					payment_type_reference = svrPaymentType.GetorCreate(company,strPT)
					addSchedule.payment_type_reference = payment_type_reference
					strAmount = u"%s" % entry.content.text.decode("utf-8")
					if len(strAmount) > 0:
						firstChar = strAmount[0]
						if firstChar.isdigit() == False:
							strAmount = strAmount.replace(firstChar, '')

					#strAmount = unicode(entry.content.text)
					strErrorMessage = "%s Amt: %s" % (strPT, strAmount)
					try:
						addSchedule.amount = float(strAmount)
					except:
						strImportError = strImportError.join(strErrorMessage)
						continue

def ListGetAction(gd_client, key, wksht_id, company_id):
	# Get the list feed
	feed = gd_client.GetCellsFeed(key, wksht_id)
	feed2 = None
	ParseFeed(gd_client.GetCellsFeed(key, wksht_id))
	ImportCellFeed(feed, company_id)
	return feed2

def ProcessSpreadsheetData(gd_client, sheet_key, worksheet_selected):
	db = gd_client.GetDatabases(name=sheet_key)
	genee= geoff
	return len(db)

def ProcessSpreadsheetData1(gd_client, sheet_key, worksheet_selected):
	feed = gd_client.GetListFeed(sheet_key, worksheet_selected)
	return ParseFeed(feed)

def GetAuthSubUrl(request, scope):
	next = ('http://%s%s' % (request.META["HTTP_HOST"], request.META["PATH_INFO"]))
	secure = False
	session = True
	gd_client = gdata.spreadsheet.service.SpreadsheetsService()
	return gd_client.GenerateAuthSubURL(next, scope, secure, session);

