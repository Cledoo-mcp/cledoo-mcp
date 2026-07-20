# Cledoo MCP — talk to your Odoo from Claude, ChatGPT, Copilot or Le Chat

[![License: LGPL-3](https://img.shields.io/badge/license-LGPL--3.0-blue.svg)](LICENSE)
[![Odoo 18](https://img.shields.io/badge/Odoo-18.0-875A7B.svg)](https://github.com/vincent2021/cledoo-mcp-release/tree/18.0)
[![Odoo 19](https://img.shields.io/badge/Odoo-19.0-875A7B.svg)](https://github.com/vincent2021/cledoo-mcp-release/tree/19.0)
[![MCP](https://img.shields.io/badge/protocol-MCP-black.svg)](https://modelcontextprotocol.io)

Turn your Odoo instance into a native **MCP (Model Context Protocol)** server.
Install one module, flip one switch, and your AI assistant — **Claude,
ChatGPT, GitHub Copilot, Mistral's Le Chat, Cursor, or any MCP client** —
connects directly to `/mcp` on your own server:

> *"Which invoices are overdue for the Paris subsidiary?"*
> *"Summarize the last 3 exchanges with Acme and log them on the deal."*
> *"Which manufacturing orders risk missing their delivery this week?"*

Every call runs as a **real Odoo user, under their existing ACLs, record rules
and field rights** — exactly what they can see and do in the Odoo UI, nothing
more. No external server, no SaaS relay, no new permission system to
misconfigure: your Odoo permissions are the only rule, and your data never
leaves your instance.

**Free and open source (LGPL-3), on the Odoo Apps Store.**

## Highlights

- **One-click connection from AI chat apps** — built-in **OAuth 2.1** with a
  branded consent screen: paste your MCP URL into claude.ai, ChatGPT or Le
  Chat, log into Odoo, approve.
  Revoke any connected agent from Settings at any time. Plain Odoo API keys
  work side by side for header-capable clients.
- **17 MCP tools** — `whoami`, `list_models`, `get_model_fields`,
  `search_records`, `get_record`, `count_records`, `describe_access`,
  `aggregate_records` (GROUP BY stats), `get_messages` / `post_message`
  (chatter), `export_records` (CSV/XLSX), `print_report` (any Odoo report as
  PDF/HTML), `read_resource` (attachments), `list_modules`, `create_record`,
  `update_record`, `delete_record`.
- **Token-efficient by design** — a curated, admin-editable model catalog (not
  a 500-model dump), compact field metadata, no inline binary blobs,
  pagination probes and a 100 kB response guard. The AI spends its context on
  answers, not noise.
- **MCP chatter badge** — messages written through MCP get a small "MCP" badge
  with the AI client's name, so humans always know who wrote what.
- **Built for operations** — a `/mcp/health` endpoint that self-diagnoses the
  most common deployment issues, per-connection rate limiting, per-agent
  activity counters. Multi-company aware. Tested on Odoo 18 and 19.
- **Zero dependencies** — stdlib-only Python, no extra process to host.

## Quickstart

1. Drop `cledoo_mcp/` on your addons path and install it from Apps
   (use the branch matching your Odoo series: [`18.0`](../../tree/18.0) or
   [`19.0`](../../tree/19.0)). Detailed steps in
   [Installation](#installation) below.
2. **Settings > General Settings > MCP Server** → enable. The endpoint URL is
   shown once enabled. (Restart a long-running Odoo process so it serves the
   new route.)
3. Connect a client:
   - **OAuth-capable AI clients** (claude.ai, Claude Desktop, ChatGPT, Le
     Chat…): add a custom connector with `https://<your-odoo>/mcp` — OAuth
     flow, no key to copy.
   - **Any header-capable client**: create an Odoo API key (Preferences >
     Account Security) and send `Authorization: Bearer <key>`.

Test from a shell:

```bash
curl -s -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -X POST https://your-odoo/mcp \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

**Requirement:** works only where custom addons can be installed —
**On-Premise or Odoo.sh**. It will never work on Odoo Online (SaaS).

## Installation

Download the module from the Odoo Apps Store (a zip archive) or clone this
repository, then:

1. Unzip the archive — you get a `cledoo_mcp/` folder.
2. Copy that folder into an addons directory of your server: any path listed
   in `addons_path` in your `odoo.conf` (on the official Docker image,
   `/mnt/extra-addons` mounted as a volume works out of the box).
3. Restart the Odoo service.
4. Enable developer mode, then go to **Apps → Update Apps List**.
5. Search for *Cledoo MCP* and click **Install**.

Do **not** use the **Apps → Import Module** upload screen: that importer only
handles data-only modules and cannot load this module's Python code — always
go through the addons path as described above.

On **Odoo.sh**: no zip to upload — commit the `cledoo_mcp/` folder to the
GitHub repository linked to your project; the next build installs it.

### Installation (français)

Téléchargez le module depuis l'Odoo Apps Store (une archive zip) ou clonez ce
dépôt, puis :

1. Dézippez l'archive — vous obtenez un dossier `cledoo_mcp/`.
2. Copiez ce dossier dans un répertoire d'addons de votre serveur : n'importe
   quel chemin listé dans `addons_path` de votre `odoo.conf` (sur l'image
   Docker officielle, `/mnt/extra-addons` monté en volume fonctionne
   directement).
3. Redémarrez le service Odoo.
4. Activez le mode développeur, puis **Apps → Mettre à jour la liste des
   applications**.
5. Cherchez *Cledoo MCP* et cliquez sur **Installer**.

N'utilisez **pas** l'écran **Apps → Importer un module** : cet importeur ne
gère que les modules de données et ne peut pas charger le code Python de ce
module — passez toujours par l'addons path comme décrit ci-dessus.

Sur **Odoo.sh** : pas de zip à téléverser — commitez le dossier `cledoo_mcp/`
dans le dépôt GitHub lié à votre projet ; le build suivant l'installe.

## Security model

This module deliberately adds **no** policy engine of its own:

- Every caller is authenticated as a real Odoo user (API key or OAuth token).
- Every ORM call runs under that user's ACLs, record rules and field rights.
- Write tools (`create_record`, `update_record`, `delete_record`,
  `post_message`) run plain `create`/`write`/`unlink` as that user — the
  backstop is that user's Odoo rights. Give the AI a dedicated user with
  tight ACLs to restrict what it can touch.

If you need governance over the AI itself — a global read-only kill-switch,
per-connection read-only/model scopes, exportable audit trail, data privacy
masking even in exports, per-user allow/deny policies with a dry-run simulator,
human-confirmed writes, an outbound-comms guard — that is
[**Cledoo MCP Pro**](https://cledoo.com) (proprietary, one-time purchase).

## Privacy

The module collects **no data by default**. It offers one **opt-in** anonymous
usage statistic, disabled by default: if — and only if — an administrator
enables it in Settings, a weekly anonymous ping (version numbers and aggregate
counters, never your data, model names or hostnames) is sent to PostHog (EU).
The exact payload is documented in the module README and at
<https://cledoo.com/privacy>.

## Repository layout

Odoo-ecosystem convention: **one branch per Odoo series** — no `main`.
Install from the branch matching your Odoo version:
[`18.0`](../../tree/18.0) · [`19.0`](../../tree/19.0)

## Contributing

Issues and pull requests are welcome — against the branch of the Odoo series
you're running. Please keep the test suite green (`--test-tags /cledoo_mcp`,
290+ tests) and follow the existing code style.

## License

[LGPL-3.0-or-later](LICENSE) — the same license as Odoo Community.
Copyright (c) 2026 [Cledoo](https://cledoo.com) · support@cledoo.com
