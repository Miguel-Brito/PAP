##############################################################################
#
#
#
##############################################################################

{
    'name': "website_directory",
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
    'depends': ['base','mail', 'website', 'website_crm', 'mass_mailing'],

    # always loaded
    'data': [
        
    ],
    # only loaded in demonstration mode
    'demo': [],
    'images': [],
    'installable': True,
}
