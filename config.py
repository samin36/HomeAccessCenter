import json

login_info = {
    'url': "https://hacprd.fultonschools.org/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f",
    'username': '2000004079',
    'password': '04272005'
}

appState = {
    "recentDestinations": [{
        "id": "Save as PDF",
        "origin": "local"
    }],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    "isHeaderFooterEnabled": False
}

chrome_profile = {
    "printing.print_preview_sticky_settings.appState": json.dumps(appState)
}
