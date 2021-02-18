# January 2021 Higher Ed Migration

## Migrate Data

The following list is based on documentation sent by Phase2.

- The data set to be migrated is currently a copy of the Higher Ed data google sheet in the Phase2 google drive. Once the actual data has been cleaned by New America editors, the original google sheet should be linked to the code base. An easy to follow tutorial on how to do this can be found here: https://www.youtube.com/watch?v=T1vqS1NL89E​.
- The authentication object created by the above process should replace the one found in [Google Sheet credentials](./google_sheet_creds.json)
- From within the vagrant container login to heroku with `heroku login -i`
- To initiate the migration run `heroku run python ./manage.py migrate_higher_ed`
  - Currently on development (not on local) elasticsearch is throwing an error when saving files associated with surveys. We are currently working to fix this error but it has caused no discernable issues with the migration or the file content.
  - The Surveys Homepage will now be a child of the Education program, but not show up in any menus
- Once the migration has run, navigate within the Wagtail admin to NewAmerica -> Education Policy -> HigherEd Public Opinion.
  - With the exception of `partner_logo` all fields on the SurveyHomePage should be populated by the migration.

## Editing post-migration

- Add `partner_logo` and make any other changes.

- After changes, wait 3 hours or run `heroku run python ./manage.py clear_cache`. 
  - Because of the amount of survey data and number of cross entity/m2m relationships, and in accordance with best practice, the survey data is cached on a three hour cycle, and any changes will either take three hours to show up, or the cache must be cleared and the page reloaded in the browser.

- In order to see the page in the Projects & Initiatives list, make a Project in the Education program that is a redirect to the surveys homepage.
  - Title and name it "HigherEd Public Opinion Hub"
  - Make the slug `highered-public-opinion-hub-project`
  - Make sure "Show in Menus" is checked

## After everything is done

- Delete the following files:
  - [Google Sheet credentials](./google_sheet_creds.json)
  - [migrate_higher_ed.py](./home/management/commands/migrate_higher_ed.py)
- Remove from [requirements.txt](./requirements.txt)
  - `gspread`
  - `oauth2client`
  - `google-api-python-client`