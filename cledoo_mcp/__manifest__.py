# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (c) 2026 Cledoo
{
    "name": "Cledoo: Odoo MCP Server - Free - Claude, GPT, Copilot",
    # Kept series-neutral on the dev branch: this source tree runs on both
    # Odoo 18 and 19, and a hard series prefix makes the *other* series
    # refuse to install ("incompatible version, setting installable=False"
    # -- verified live on 19 with an 18.0 prefix). The Apps Store release
    # branches MUST prefix it per series (18.0.1.2.0 on branch 18.0,
    # 19.0.1.2.0 on branch 19.0) so a wrong-series install fails cleanly.
    "version": "19.0.1.7.0",
    "summary": "MCP Server for Odoo: connect Claude, ChatGPT, Copilot and any "
               "AI agent. Free, native, secured by your own Odoo permissions.",
    "description": """
Give Claude direct access to your Odoo -- for free, and secured by your own
permissions.

Cledoo MCP turns your Odoo instance into a native MCP server. Install the
module, flip one switch in Settings, and Claude (claude.ai, Claude Desktop)
or any MCP client connects directly to /mcp -- with a standard Odoo API key,
or the built-in OAuth 2.1 flow with a branded consent screen (paste the URL,
approve, done). No external server, no new dependency, nothing leaving your
instance.

Every one of the 17 tools runs as the connected user, under their existing
Odoo ACLs, record rules and field rights -- exactly what they can do in the
UI. Token-efficient by design: a curated model catalog, compact metadata and
response guards so the AI spends its context on answers, not noise. Multi-
company aware, tested on Odoo 18 and 19.

Need to govern the AI itself -- a global read-only kill-switch, per-connection
scopes, audit trail, data privacy masking, per-user allow/deny policies,
human-confirmed writes, an outbound-comms guard? A separate module, Cledoo
MCP Pro, is available on the Odoo Apps Store.

Data privacy: the module collects NO data by default. It offers an
OPT-IN anonymous usage statistic (disabled by default): if -- and only
if -- you enable it in Settings, a weekly anonymous ping is sent to
PostHog (EU) containing version numbers and aggregate counters only
(never your data, model names, hostnames, users or company
information). The exact payload is documented in the README and the
toggle can be turned off again at any time. Privacy policy:
https://cledoo.com/privacy.

Not installable on Odoo Online (SaaS): custom modules require Odoo.sh or an
on-premise deployment.
""",
    "category": "AI",
    "author": "Cledoo",
    "maintainer": "Cledoo",
    "website": "https://cledoo.com",
    "license": "LGPL-3",
    "support": "support@cledoo.com",
    "live_test_url": "https://cledoo.com/preview",
    "price": 0.0,
    "currency": "EUR",
    "images": [
        "static/description/banner.gif",
        "static/description/banner.png",
        "static/description/screenshot_1_settings.png",
        "static/description/screenshot_2_connect_claude.png",
        "static/description/screenshot_5_oauth_consent.png",
        "static/description/screenshot_6_chatter_badge.png",
    ],
    "depends": ["base", "web", "base_setup", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "data/mcp_model_profiles.xml",
        "data/mcp_data.xml",
        "views/oauth_admin_views.xml",
        "views/mcp_session_views.xml",
        "views/model_profile_views.xml",
        "views/res_config_settings_views.xml",
        "views/oauth_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "cledoo_mcp/static/src/core/message_model_patch.js",
            "cledoo_mcp/static/src/core/message_patch.xml",
        ],
    },
    "application": True,
    "installable": True,
}
