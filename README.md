# tap-impact

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from the following [Impact Radius API](https://developer.impact.com/default) catalogs:
  - [Advertiser API](https://developer.impact.com/default/documentation/Rest-Adv-v8)
  - [Agency API](https://developer.impact.com/default/documentation/Agencies)
  - [Partner API](https://developer.impact.com/default/documentation/Rest-Mp-v11)

- Extracts the following resources:
  - [API Submissions](https://developer.impact.com/default/documentation/Rest-Adv-v8#operations-API_Submissions-GetAPISubmissions)
  - [Campaigns](https://developer.impact.com/default#operations-Campaigns-GetCampaigns)
    - [Actions](https://developer.impact.com/default#operations-Actions-GetActions)
    - [Action Inquiries](https://developer.impact.com/default#operations-Action_Inquiries-GetActionInquiries)
    - [Action Updates](https://developer.impact.com/default#operations-Action_Updates-ListActionUpdates)
    - [Clicks](https://developer.impact.com/default#operations-Clicks-GetClicks)
    - [Contacts](https://developer.impact.com/default#operations-Contacts-GetContacts)
    - [Notes](https://developer.impact.com/default#operations-Notes-GetNotes)
    - [Media Partner Groups](https://developer.impact.com/default#operations-Partner_Groups-GetMediaPartnerGroups)
  - [Ads](https://developer.impact.com/default#operations-Ads-ListAds)
  - [Catalogs](https://developer.impact.com/default#operations-Catalogs-ListCatalogs)
    - [Catalog Items](https://developer.impact.com/default#operations-Catalog_Items-ListCatalogItems)
  - [Company Information](https://developer.impact.com/default#operations-Company_Information-GetCompanyInfo)
  - [Deals](https://developer.impact.com/default#operations-Deals-GetDeals)
  - [Exception Lists](https://developer.impact.com/default#operations-Exception_Lists-GetExceptionLists)
    - [Exception List Items](https://developer.impact.com/default#operations-Exception_Lists-GetExceptionListItems)
  - [FTP File Submissions](https://developer.impact.com/default#operations-FTP_File_Submissions-GetFTPFileSubmissions)
  - [Invoices](https://developer.impact.com/default#operations-Invoices-GetInvoices)
  - [Media Partners](https://developer.impact.com/default#operations-Partners-GetMediaPartners)
  - [Phone Numbers](https://developer.impact.com/default#operations-Phone_Numbers-GetPhoneNumbers)
  - [Promo Codes](https://developer.impact.com/default#operations-Promo_Codes-GetPromoCodes)
  - [Reports](https://developer.impact.com/default#operations-Reports-ListReports)
    - [Report Metadata](https://developer.impact.com/default/documentation/Rest-Adv-v8#operations-Reports-GetReportMetadata)
  - [Tracking Value Requests](https://developer.impact.com/default#operations-Tracking_Value_Requests-GetTrackingValueRequests)
  - [Unique URLs](https://developer.impact.com/default#operations-Unique_Urls-GetUniqueUrls)

- Outputs the schema for each resource
- Incrementally pulls data based on the input state


## Streams
[actions](https://developer.impact.com/default#operations-Actions-GetActions)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/Actions
- Primary key fields: id
- Foreign key fields: ad_id, caller_id, campaign_id, customer_id, media_partner_id, shared_id
- Replication strategy: INCREMENTAL (Query filtered)
  - Filter: CampaignId (parent)
  - Filter: StartDate (event_date)
  - Bookmark: event_date
- Transformations: camelCase to snake_case
- Parent: campaigns

[action_inquiries](https://developer.impact.com/default#operations-Action_Inquiries-GetActionInquiries)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/ActionInquiries
- Primary key fields: id
- Foreign key fields: action_id, campaign_id, media_partner_id, order_id
- Replication strategy: INCREMENTAL (Query filtered)
  - Filter: CampaignId (parent)
  - Filter: StartDate (creation_date)
  - Bookmark: creation_date
- Transformations: camelCase to snake_case
- Parent: campaigns

[action_updates](https://developer.impact.com/default#operations-Action_Updates-ListActionUpdates)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/ActionUpdates
- Primary key fields: id
- Foreign key fields: action_id, ad_id, caller_id, campaign_id, customer_id, media_partner_id, shared_id
- Replication strategy: INCREMENTAL (Query filtered)
  - Filter: CampaignId (parent)
  - Filter: StartDate (update_date)
  - Bookmark: update_date
- Transformations: camelCase to snake_case
- Parent: campaigns

[ads](https://developer.impact.com/default#operations-Ads-ListAds)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/Ads
- Primary key fields: id
- Foreign key fields: campaign_id, deal_id
- Replication strategy: FULL_TABLE
- Transformations: camelCase to snake_case

[api_submissions](https://developer.impact.com/default/documentation/Rest-Adv-v8#operations-API_Submissions-GetAPISubmissions)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/APISubmissions
- Primary key fields: batch_id
- Foreign key fields: account_id, campaign_id, media_partner_id, order_id
- Replication strategy: INCREMENTAL (query all, filter_results)
  - Bookmark: submission_date (date-time)
- Transformations: camelCase to snake_case

[campaigns](https://developer.impact.com/default#operations-Campaigns-GetCampaigns)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/Campaigns
- Primary key fields: id
- Foreign key fields: none
- Replication strategy: FULL_TABLE
- Transformations: camelCase to snake_case
- Children: actions, action_inquiries, action_updates, clicks, contacts, notes, media_partner_groups

[catalogs](https://developer.impact.com/default#operations-Catalogs-ListCatalogs)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/Catalogs
- Primary key fields: id
- Foreign key fields: campaign_id, advertiser_id
- Replication strategy: FULL_TABLE
- Transformations: camelCase to snake_case
- Children: catalog_items

[catalog_items](https://developer.impact.com/default#operations-Catalogs-ListCatalogs)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/Catalogs/{catalog_id}/Items
- Primary key fields: catalog_item_id
- Foreign key fields: catalog_id
- Replication strategy: FULL_TABLE (ALL for parent Catalog)
- Transformations: camelCase to snake_case, add catalog_id (parent id)
- Parent: catalogs

[clicks](https://developer.impact.com/default#operations-Clicks-GetClicks)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/Campaigns/{campaign_id}/Clicks
- Primary key fields: id
- Foreign key fields: ad_id, campaign_id, media_id, shared_id
- Replication strategy: INCREMENTAL (Query filtered by Date for parent CampaignId)
  - Filter: CampaignId (parent)
  - Filter: Date (event_date)
  - Bookmark: event_date
- Transformations: camelCase to snake_case
- Parent: campaigns

[contacts](https://developer.impact.com/default#operations-Contacts-GetContacts)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/Campaigns/{campaign_id}/Contacts
- Primary key fields: id
- Foreign key fields: campaign_id, accounts > id
- Replication strategy: FULL_TABLE (ALL for parent Campaign)
- Transformations: camelCase to snake_case, add campaign_id (parent id)
- Parent: campaigns

[deals](https://developer.impact.com/default#operations-Deals-GetDeals)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/Deals
- Primary key fields: id
- Foreign key fields: campaign_id
- Replication strategy: FULL_TABLE
- Transformations: camelCase to snake_case

[exception_lists](https://developer.impact.com/default#operations-Exception_Lists-GetExceptionLists)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/ExceptionLists
- Primary key fields: id
- Foreign key fields: campaign_id
- Replication strategy: FULL_TABLE
- Transformations: camelCase to snake_case
- Children: exception_list_items

[exception_list_items](https://developer.impact.com/default#operations-Exception_Lists-GetExceptionListItems)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/ExceptionLists/{list_id}/Items
- Primary key fields: id
- Foreign key fields: list_id
- Replication strategy: FULL_TABLE (ALL for parent Exception List)
- Transformations: camelCase to snake_case
- Parent: exception_lists

[ftp_file_submissions](https://developer.impact.com/default#operations-FTP_File_Submissions-GetFTPFileSubmissions)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/FTPFileSubmissions
- Primary key fields: batch_id
- Foreign key fields: account_id
- Replication strategy: INCREMENTAL (query all, filter_results)
  - Bookmark: submission_date (date-time)
  - Sort: SubmissionDate ASC
- Transformations: camelCase to snake_case
- Children: exception_list_items

[invoices w/ line_items](https://developer.impact.com/default#operations-Invoices-GetInvoices)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/Invoices
- Primary key fields: id
- Foreign key fields: campaign_id, media_id
- Replication strategy: INCREMENTAL (Query filtered)
  - Filter: StartDate (created_date)
  - Bookmark: created_date (date-time)
- Transformations: camelCase to snake_case

[media_partners](https://developer.impact.com/default#operations-Partners-GetMediaPartners)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/MediaPartners
- Primary key fields: id
- Foreign key fields: campaign_id
- Replication strategy: FULL_TABLE
- Transformations: camelCase to snake_case

[media_partner_groups](https://developer.impact.com/default#operations-Partner_Groups-GetMediaPartnerGroups)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/Campaigns/{campaign_id}/MediaPartnerGroups
- Primary key fields: id
- Foreign key fields: campaign_id, media_partners > id
- Replication strategy: FULL_TABLE (ALL for parent Campaign)
- Transformations: camelCase to snake_case, add campaign_id (parent id)
- Parent: campaigns

[notes](https://developer.impact.com/default#operations-Notes-GetNotes)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/Campaigns/{campaign_id}/Notes
- Primary key fields: id
- Foreign key fields: campaign_id, media_id
- Replication strategy: INCREMENTAL (query all for parent campaign_id, filter_results)
  - Bookmark: modification_date (date-time)
  - Sort: ModificationDate ASC
- Transformations: camelCase to snake_case, add campaign_id (parent id)
- Parent: campaigns

[phone_numbers](https://developer.impact.com/default#operations-Phone_Numbers-GetPhoneNumbers)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/PhoneNumbers
- Primary key fields: id
- Foreign key fields: none
- Replication strategy: FULL_TABLE
- Transformations: camelCase to snake_case

[promo_codes](https://developer.impact.com/default#operations-Promo_Codes-GetPromoCodes)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/PromoCodes
- Primary key fields: id
- Foreign key fields: campaign_id
- Replication strategy: FULL_TABLE
- Transformations: camelCase to snake_case

[reports](https://developer.impact.com/default#operations-Reports-ListReports)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/Reports
- Primary key fields: id
- Foreign key fields: none
- Replication strategy: FULL_TABLE
- Transformations: camelCase to snake_case
- Children: report_metadata

[report_metadata](https://developer.impact.com/default/documentation/Rest-Adv-v8#operations-Reports-GetReportMetadata)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/Reports/{report_id}/MetaData
- Primary key fields: id
- Foreign key fields: id (reports)
- Replication strategy: FULL_TABLE (ALL for parent report id)
- Transformations: camelCase to snake_case
- Parent: reports

[tracking_value_requests](https://developer.impact.com/default#operations-Tracking_Value_Requests-GetTrackingValueRequests)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/TrackingValueRequests
- Primary key fields: id
- Foreign key fields: campaign_id, deal_id, media_partner_id, phone_numbers > id, promo_codes > id, unique_urls > id
- Replication strategy: FULL_TABLE
- Transformations: camelCase to snake_case

[unique_urls](https://developer.impact.com/default#operations-Unique_Urls-GetUniqueUrls)
- Endpoint: https://api.impact.com/{api_catalog}/{account_sid}/UniqueUrls
- Primary key fields: id
- Foreign key fields: campaign_id, media_partner_id
- Replication strategy: FULL_TABLE
- Transformations: camelCase to snake_case

## Quick Start

1. Install

    Clone this repository, and then install using setup.py. We recommend using a virtualenv:

    ```bash
    > virtualenv -p python3 venv
    > source venv/bin/activate
    > python setup.py install
    OR
    > cd .../tap-impact
    > pip install .
    ```
2. Dependent libraries
    The following dependent libraries were installed.
    ```bash
    > pip install singer-python
    > pip install singer-tools
    > pip install target-stitch
    > pip install target-json
    
    ```
    - [singer-tools](https://github.com/singer-io/singer-tools)
    - [target-stitch](https://github.com/singer-io/target-stitch)

3. Create your tap's `config.json` file. The `api_catalog` is one of the following: Advertisers, Agencies, Partners. The `account_sid` and `auth_token` may be found in your user settings when API access is enabled.
    ```json
    {
        "account_sid": "YOUR_API_ACCOUNT_SID",
        "auth_token": "YOUR_API_AUTH_TOKEN",
        "api_catalog": "YOUR_API_CATALOG",
        "start_date": "2019-01-01T00:00:00Z",
        "user_agent": "tap-impact <api_user_email@your_company.com>"
    }
    ```
    
    Optionally, also create a `state.json` file. `currently_syncing` is an optional attribute used for identifying the last object to be synced in case the job is interrupted mid-stream. The next run would begin where the last job left off.

    ```json
    {
        "currently_syncing": "ftp_file_submissions",
        "bookmarks": {
            "actions": "2019-09-21T01:05:17.000000Z",
            "action_inquiries": "2019-09-14T14:34:03.000000Z",
            "action_updates": "2019-09-21T02:27:16.000000Z",
            "clicks": "2019-09-21T00:54:26.000000Z",
            "api_submissions": "2019-09-21T00:47:35.000000Z",
            "ftp_submissions": "2019-09-20T00:42:39.000000Z",
            "invoices": "2019-09-03T10:02:01.000000Z"
        }
    }
    ```

4. Run the Tap in Discovery Mode
    This creates a catalog.json for selecting objects/fields to integrate:
    ```bash
    tap-impact --config config.json --discover > catalog.json
    ```
   See the Singer docs on discovery mode
   [here](https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#discovery-mode).

5. Run the Tap in Sync Mode (with catalog) and [write out to state file](https://github.com/singer-io/getting-started/blob/master/docs/RUNNING_AND_DEVELOPING.md#running-a-singer-tap-with-a-singer-target)

    For Sync mode:
    ```bash
    > tap-impact --config tap_config.json --catalog catalog.json > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```
    To load to json files to verify outputs:
    ```bash
    > tap-impact --config tap_config.json --catalog catalog.json | target-json > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```
    To pseudo-load to [Stitch Import API](https://github.com/singer-io/target-stitch) with dry run:
    ```bash
    > tap-impact --config tap_config.json --catalog catalog.json | target-stitch --config target_config.json --dry-run > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```

6. Test the Tap
    
    While developing the impact tap, the following utilities were run in accordance with Singer.io best practices:
    Pylint to improve [code quality](https://github.com/singer-io/getting-started/blob/master/docs/BEST_PRACTICES.md#code-quality):
    ```bash
    > pylint tap_impact -d missing-docstring -d logging-format-interpolation -d too-many-locals -d too-many-arguments
    ```
    Pylint test resulted in the following score:
    ```bash
    Your code has been rated at 9.79/10
    ```

    To [check the tap](https://github.com/singer-io/singer-tools#singer-check-tap) and verify working:
    ```bash
    > tap-impact --config tap_config.json --catalog catalog.json | singer-check-tap > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```
    Check tap resulted in the following:
    ```bash
    Checking stdin for valid Singer-formatted data
    The output is valid.
    It contained 80959 messages for 24 streams.

        135 schema messages
    80766 record messages
        58 state messages

    Details by stream:
    +-------------------------+---------+---------+
    | stream                  | records | schemas |
    +-------------------------+---------+---------+
    | tracking_value_requests | 0       | 1       |
    | ftp_file_submissions    | 0       | 1       |
    | api_submissions         | 345     | 1       |
    | unique_urls             | 0       | 1       |
    | invoices                | 34      | 1       |
    | ads                     | 54      | 1       |
    | phone_numbers           | 603     | 1       |
    | deals                   | 1       | 1       |
    | campaigns               | 1       | 1       |
    | notes                   | 0       | 1       |
    | media_partner_groups    | 10      | 1       |
    | action_updates          | 1389    | 1       |
    | actions                 | 1075    | 1       |
    | action_inquiries        | 1       | 1       |
    | clicks                  | 76213   | 1       |
    | contacts                | 383     | 1       |
    | exception_lists         | 0       | 1       |
    | promo_codes             | 20      | 1       |
    | media_partners          | 230     | 1       |
    | catalogs                | 1       | 1       |
    | catalog_items           | 181     | 1       |
    | reports                 | 112     | 1       |
    | report_metadata         | 112     | 1       |
    | company_information     | 1       | 1       |
    +-------------------------+---------+---------+

    ```
---

Copyright &copy; 2019 Stitch
