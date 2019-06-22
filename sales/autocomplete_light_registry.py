import autocomplete_light
from inventory.models import Products

autocomplete_light.register(Products,
    # Just like in ModelAdmin.search_fields
    search_fields=['^Name'],
    attrs={
        'placeholder': 'Search Item',
        # This will set the yourlabs.Autocomplete.minimumCharacters
        # options, the naming conversion is handled by jQuery
        'data-autocomplete-minimum-characters': 1,
    },
    widget_attrs={
        'data-widget-maximum-values': 4,
        # Enable modern-style widget !
        'class': 'modern-style',
    },
)