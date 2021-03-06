##############################################################################
#
#
#
##############################################################################

{
    'name':'Website Directory',
    'category': 'Theme',
    'website': 'https://www.communities.pt',
    'summary': 'Website Directory',
    'version':'1.0',
    'description': """
    Website Directory
==========================
        """,
    'author':'Communities',
    'data': [
        'views/assets.xml',
        'views/directory_template.xml',
        'views/homepage_template.xml',
        'views/contact_template.xml',
        'views/aboutus_template.xml',
        'views/404_template.xml',
        'views/login_template.xml',
        'views/admin/admin_templates.xml',
        'views/admin/proposals_templates.xml',
        'views/admin/services_templates.xml',
        'views/admin/account_templates.xml',
    ],
    'depends': ['website', 'mail'],
    'installable': True,
    'auto_install': False,
    'application': True,
}

