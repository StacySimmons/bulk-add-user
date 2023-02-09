# bulk-add-user
A script to provision New Relic users in batch in the new user model
# Instructions
1. Update the license.py file with your own User API key and Auth Domain ID
2. Update the license.py file with the name of your user data file in TSV format
3. Format of TSV should be:

| Name     	| Email                	| User Type      	|
|----------	|----------------------	|----------------	|
| John Doe 	| john.doe@myemail.com 	| FULL_USER_TIER 	|

4. Valid values for user type are: FULL_USER_TIER, CORE_USER_TIER, BASIC_USER_TIER
