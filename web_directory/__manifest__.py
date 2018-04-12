##############################################################################
#
#
#
##############################################################################

{
    'name': "web_directory",
    'summary': """
        """,

    'description': """
        
    """,

    'author': 'Miguel Brito',
    'company': 'Communities - Comunicações, Lda',
    'website': "https://www.communities.pt/",
    'category': 'Themes',
    'version': '10.0.0.1',

    # any module necessary for this one to work correctly
    'depends': [],

    # always loaded
    'data': [
        'views/res_partner_views.xml',
        'views/menus_views.xml',
        'views/res_partner_interest_category_views.xml',
        'views/res_partner_interest_views.xml',
        'views/budget_views.xml',
        'views/sequence_data.xml',
        'views/work_type_views.xml'

    ],
    # only loaded in demonstration mode
    'demo': [],
    'images': [],
    'installable': True,
}
