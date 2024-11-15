from datetime import datetime

# Intercommerce Login Credentials (intercommerce.com.ph)
intercommerce_username = 'username'
intercommerce_password = 'password'
intercommerce_credentials = dict({
    'username': intercommerce_username,
    'password': intercommerce_password
})

# VBS Login Credentials (vbs.1-stop.biz)
vbs_username = 'username'
vbs_password = 'password'
vbs_credentials = dict({
    'username': vbs_username,
    'password': vbs_password
})

# Dates for the VBS system.
# The format is 'mm-dd-yy'.
vbs_start_date = '00-00-00'
vbs_end_date = '00-00-00'

vbs_start_date = datetime.strptime(vbs_start_date, '%m-%d-%y').date()
vbs_end_date = datetime.strptime(vbs_end_date, '%m-%d-%y').date()

# URLS for the intercommerce system.
# We place these in secrets because the URL contain sensitive information.
intercommerce_urls = dict({

})