# streams: API URL endpoints to be called
# properties:
#   <root node>: Plural stream name for the endpoint
#   path: API endpoint relative path, when added to the base URL, creates the full path
#   key_properties: Primary key from the Parent stored when store_ids is true.
#   replication_method:
#   replication_keys: bookmark_field(s), typically a date-time, used for filtering the results
#        and setting the state
#   params: Query, sort, and other endpoint specific parameters
#   data_key: JSON element containing the records for the endpoint
#   bookmark_query_field: From date-time field used for filtering the query
#   bookmark_type: Data type for bookmark, integer or datetime
#   children: A collection of child endpoints (where the endpoint path includes the parent id)
#   parent: On each of the children, the singular stream name for parent element
STREAMS = {
    'ads': {
        'path': 'Ads',
        'data_key': 'Ads',
        'key_properties': ['id'],
        'replication_method': 'FULL_TABLE'
    },
    'api_submissions': {
        'path': 'APISubmissions',
        'data_key': 'APISubmission',
        'params': {
            'SortBy': 'SubmissionDate',
            'SortOrder': 'ASC'
        },
        'key_properties': ['batch_id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['submission_date'],
        'bookmark_type': 'datetime'
    },
    'campaigns': {
        'path': 'Campaigns',
        'data_key': 'Campaigns',
        'key_properties': ['id'],
        'replication_method': 'FULL_TABLE',
        'children': {
            'actions': {
                'path': 'Actions',
                'data_key': 'Actions',
                'params': {
                    'CampaignId': '<parent_id>'
                },
                'key_properties': ['id'],
                'replication_method': 'FULL_TABLE'
            },
            'action_inquiries': {
                'path': 'ActionInquiries',
                'data_key': 'ActionInqueries',
                'params': {
                    'CampaignId': '<parent_id>'
                },
                'key_properties': ['id'],
                'replication_method': 'FULL_TABLE'
            },
            'action_updates': {
                'path': 'ActionUpdates',
                'data_key': 'ActionUpdates',
                'params': {
                    'CampaignId': '<parent_id>'
                },
                'key_properties': ['id'],
                'replication_method': 'FULL_TABLE'
            },
            'clicks': {
                'path': 'Campaigns/{}/Clicks',
                'data_key': 'Clicks',
                'key_properties': ['id'],
                'replication_method': 'FULL_TABLE'
            },
            'contacts': {
                'path': 'Campaigns/{}/Contacts',
                'data_key': 'Contacts',
                'key_properties': ['id'],
                'replication_method': 'FULL_TABLE',
                'parent': 'campaign'
            },
            'media_partner_groups': {
                'path': 'Campaigns/{}/MediaPartnerGroups',
                'data_key': 'Groups',
                'key_properties': ['id'],
                'replication_method': 'FULL_TABLE',
                'parent': 'campaign'
            },
            'notes': {
                'path': 'Campaigns/{}/Notes',
                'data_key': 'Notes',
                'key_properties': ['id'],
                'params': {
                    'SortBy': 'SubmissionDate',
                    'SortOrder': 'ASC'
                },
                'key_properties': ['batch_id'],
                'replication_method': 'INCREMENTAL',
                'replication_keys': ['modification_date'],
                'bookmark_type': 'datetime',
                'parent': 'campaign'
            }
        }
    },
    'catalogs': {
        'path': 'Catalogs',
        'data_key': 'Catalogs',
        'params': {
            'SortBy': 'DateLastUpdated',
            'SortOrder': 'ASC'
        },
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['date_last_updated'],
        'bookmark_type': 'datetime',
        'children': {
            'catalog_items': {
                'path': 'Catalogs/{}/Items',
                'data_key': 'Items',
                'key_properties': ['catalog_item_id'],
                'replication_method': 'FULL_TABLE',
                'parent': 'catalog'
            }
        }
    },
    'company_information': {
        'path': 'CompanyInformation',
        'data_key': 'CompanyInformation',
        'key_properties': ['company_name'],
        'replication_method': 'FULL_TABLE'
    },
    'deals': {
        'path': 'Deals',
        'data_key': 'Deals',
        'key_properties': ['id'],
        'replication_method': 'FULL_TABLE',
    },
    'exception_lists': {
        'path': 'ExceptionLists',
        'data_key': 'ExceptionLists',
        'params': {
            'SortBy': 'CreatedDate',
            'SortOrder': 'ASC'
        },
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['created_date'],
        'bookmark_type': 'datetime',
        'children': {
            'exception_list_items': {
                'path': 'ExceptionLists/{}/Items',
                'data_key': 'ExceptionListItems',
                'key_properties': ['id'],
                'replication_method': 'FULL_TABLE'
            }
        }
    },
    'ftp_file_submissions': {
        'path': 'FTPFileSubmissions',
        'data_key': 'FTPFileSubmissions',
        'params': {
            'SortBy': 'SubmissionDate',
            'SortOrder': 'ASC'
        },
        'key_properties': ['batch_id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['submission_date'],
        'bookmark_type': 'datetime'
    },
    'invoices': {
        'path': 'Invoices',
        'data_key': 'Invoices',
        'params': {
            'SortBy': 'CreatedDate',
            'SortOrder': 'ASC'
        },
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['created_date'],
        'bookmark_type': 'datetime'
    },
    'media_partners': {
        'path': 'MediaPartners',
        'data_key': 'MediaPartners',
        'params': {
            'SortBy': 'CreatedDate',
            'SortOrder': 'ASC'
        },
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['created_date'],
        'bookmark_type': 'datetime'
    },
    'phone_numbers': {
        'path': 'PhoneNumbers',
        'data_key': 'PhoneNumbers',
        'params': {
            'SortBy': 'DateCreated',
            'SortOrder': 'ASC'
        },
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['date_created'],
        'bookmark_type': 'datetime'
    },
    'promo_codes': {
        'path': 'PromoCodes',
        'data_key': 'PromoCodes',
        'params': {
            'SortBy': 'DateCreated',
            'SortOrder': 'ASC'
        },
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['date_created'],
        'bookmark_type': 'datetime'
    },
    'reports': {
        'path': 'Reports',
        'data_key': 'Reports',
        'key_properties': ['id'],
        'replication_method': 'FULL_TABLE',
    },
    'tracking_value_requests': {
        'path': 'TrackingValueRequests',
        'data_key': 'TrackingValueRequests',
        'params': {
            'SortBy': 'DatePlaced',
            'SortOrder': 'ASC'
        },
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['date_placed'],
        'bookmark_type': 'datetime'
    },
    'unique_urls': {
        'path': 'UniqueUrls',
        'data_key': 'UniqueUrls',
        'params': {
            'SortBy': 'DateCreated',
            'SortOrder': 'ASC'
        },
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['date_created'],
        'bookmark_type': 'datetime'
    }
}
