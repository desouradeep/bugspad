def get_products():     #will be replaced to use bugspad apis once they are ready
    return {
        1: {'id':1, 'product': 'Fedora', 'description': 'Bugs related to the components of the Fedora distribution. If you are reporting a bug against a stable release or a branched pre-release version please select that version number. The currently maintained released versions are Fedora 18 and Fedora 19. The branched pre-released version is Fedora 20. If you have a bug to report against the daily development tree (rawhide) please choose \'rawhide\' as the version.'},
        2: {'id':2, 'product': 'Fedora Documentation', 'description':'Fedora Documentation'},
        3: {'id':3, 'product': 'Fedora EPEL', 'description': 'For bugs relating to EPEL (Extra Packages for Enterprise Linux) run by Fedora Project'},
        4: {'id':4, 'product': 'Fedora Localization', 'description': 'Localization (Translations into other Languages)'},
        5: {'id':5, 'product': 'Fedora Management Console', 'description': 'For bugs related to the Fedora Management Console Software Development Kit'}
    }