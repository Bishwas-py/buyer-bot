
from typing import Any, Dict

JAZZMIN_SETTINGS: Dict[str, Any] = {
    "site_title": "Bestbuy Automation",
    "site_header": "Bestbuy Bot",
    "site_logo": "default/favicon.png",
    "site_icon": "default/favicon.png",
     "topmenu_links": [
        {"name": "Home", "url": "/", "permissions": ["auth.view_user"], "new_window": True},
    ],
    "custom_links": {
        "app": [
            {
                "name": "Bot Center", 
                "url": "dashboard", 
                "icon": "fas fa-spider",
                "permissions": ["app.custom_links"]
            },
        ]
    },
    "order_with_respect_to": ["dashboard", "production"],
    "icons": {
        "auth": "fas fa-users-cog",
        "app.Items": "fas fa-list-alt",
        "app.Settings": "fas fa-cog",
        "dashboard.Supplier": "fas fa-user-plus",
        "production.Chamber": "fas fa-industry",
        "auth.user":  "fas fa-user",
        "auth.group":  "fas fa-user-friends",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-book",
    "default_icon_children": "fas fa-circle",

    # Activate Bootstrap modal
    "related_modal_active": False,
    
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    }
}