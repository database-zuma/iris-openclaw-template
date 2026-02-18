# Phantom MCP Server

**Researched:** 2026-02-18  
**Source:** https://github.com/dbernheisel/phantom_mcp  
**Stars:** ~31 ⭐  
**Language:** Elixir  
**Version:** 0.3.2 (on Hex.pm)  
**License:** Not specified in README  

---

## What It Is

Phantom MCP is an **Elixir library** (not a standalone server) for building MCP (Model Context Protocol) servers. It provides a complete implementation of the [MCP server specification](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports) using Elixir's **Plug** interface — meaning it integrates natively with Phoenix and plain Plug.Router apps.

> Think of it like a "framework plug-in" — you add it to your existing Elixir web app and it turns part of your app into a fully-spec-compliant MCP server.

---

## What It Does

Phantom handles the full MCP server lifecycle on your behalf:

### Supported MCP Methods
- `initialize` — auto-detects capabilities from your router config
- `tools/list`, `tools/call` — define & expose tools to LLM clients
- `prompts/list`, `prompts/get` — serve prompts with arguments & completion
- `resources/list`, `resources/read` — expose resources (text, blobs) via URI templates
- `resources/subscribe` / `resources/unsubscribe` — real-time resource change notifications
- `completion/complete` — autocomplete for prompt/resource arguments
- `logging/setLevel` — client-side log level control
- `notifications/*` — resource, prompt, and tool change notifications
- `ping` → pong

### Not Yet Supported
- `roots/list` — server requesting client file list
- `sampling/createMessage` — human-in-the-loop agentic sampling
- `elicitation/create` — server requesting input from client

---

## Core Concepts

### 1. Tools
Define tools with input/output schemas — these are exposed to the LLM for calling:
```elixir
tool :create_question, MyApp.MCP,
  input_schema: %{
    required: ~w[description label study_id],
    properties: %{
      study_id: %{type: "integer", description: "..."},
      label: %{type: "string", description: "..."}
    }
  }
```
Handlers can be **synchronous** (`{:reply, result, session}`) or **asynchronous** (return `{:noreply, session}` and call `Session.respond/2` later from a Task).

### 2. Prompts
Define prompts with optional arguments and completion functions:
```elixir
prompt :suggest_questions,
  completion_function: :study_complete,
  arguments: [%{name: "study_id", required: true}]
```

### 3. Resources
Define resources with URI templates:
```elixir
resource "https://example.com/studies/:study_id/md", :study,
  completion_function: :study_complete,
  mime_type: "text/markdown"
```

---

## Setup

### 1. Add dependency (mix.exs)
```elixir
{:phantom_mcp, "~> 0.3.2"}
```

### 2. Configure MIME types (config/config.exs)
```elixir
config :mime, :types, %{"text/event-stream" => ["sse"]}
```

### 3. Mount in Phoenix Router
```elixir
scope "/mcp" do
  pipe_through :mcp

  forward "/", Phantom.Plug,
    validate_origin: Mix.env() == :prod,
    router: MyApp.MCPRouter
end
```

### 4. Define your MCP Router
```elixir
defmodule MyApp.MCP.Router do
  use Phantom.Router,
    name: "MyApp",
    vsn: "1.0",
    instructions: "What this MCP server does..."
end
```

### 5. For Distributed / Persistent Streams (Optional)
Add to supervision tree:
```elixir
{Phoenix.PubSub, name: MyApp.PubSub},
{Phantom.Tracker, [name: Phantom.Tracker, pubsub_server: MyApp.PubSub]}
```

---

## Transport: Streamable HTTP (Modern MCP)

Phantom uses the **newer Streamable HTTP** transport, not the legacy SSE-only approach:
- `POST` requests → open SSE stream, close when done
- `GET` requests → persistent SSE channel for notifications/logs
- Session resumption via `mcp-session-id` header

> For local testing, use [`mcp-remote`](https://github.com/geelen/mcp-remote) (not `mcp-proxy`, which is SSE-only).

---

## Authentication & Authorization

Phantom **does not handle auth itself** — you implement it via the `connect/2` callback:

```elixir
def connect(session, %{headers: auth_info}) do
  with {:ok, user} <- MyApp.authenticate(auth_info) do
    {:ok, session |> assign(user: user) |> limit_for_plan(user.plan)}
  else
    :not_found -> {:unauthorized, %{method: "Bearer", resource_metadata: "..."}}
    :not_allowed -> {:forbidden, "Please upgrade plan"}
  end
end
```

You can **whitelist tools/resources per session** based on auth:
```elixir
session
|> Phantom.Session.allowed_tools(~w[create_question])
|> Phantom.Session.allowed_resource_templates(~w[study])
```

Recommended OAuth libraries: Oidcc, Boruta, ExOauth2Provider.

---

## Use Cases

- **Add MCP to an existing Phoenix app** — expose your app's data/actions to Claude, Cursor, Copilot, etc.
- **Multi-tenant MCP** — per-user tool/resource permissions via `connect/2`
- **Research/data platforms** — expose structured data as MCP resources with paginated lists
- **Async heavy operations** — non-blocking async handlers via Elixir Tasks
- **Distributed MCP** — cluster-aware via Phoenix.PubSub + Phoenix.Tracker

---

## Pros

| Pro | Detail |
|-----|--------|
| ✅ Full MCP spec (2025) | Implements the modern Streamable HTTP spec |
| ✅ Elixir/Phoenix native | First-class Plug integration, no awkward wrappers |
| ✅ Async-first | Handlers can be sync or async; Elixir OTP concurrency |
| ✅ Per-session auth & permissions | Fine-grained tool/resource whitelisting |
| ✅ Real-time notifications | PubSub-based resource change events |
| ✅ Distributed | Works across Elixir clusters via Phoenix.Tracker |
| ✅ Available on Hex.pm | Documented, versioned, published |

---

## Cons

| Con | Detail |
|-----|--------|
| ❌ Elixir-only | Not useful if you're not running an Elixir app |
| ❌ Small community | ~31 stars, niche ecosystem |
| ❌ No built-in auth | Must wire up OAuth2 yourself |
| ❌ Missing sampling/elicitation | Newer MCP methods not yet supported |
| ❌ No `last-event-id` resume | Broken SSE connections can't resume missed events yet |
| ❌ Batched requests not optimized | Will be deprecated by MCP spec anyway |

---

## Summary

Phantom MCP is a **mature, well-designed Elixir library** for embedding an MCP server into Phoenix/Plug applications. It's the right tool if you're already in the Elixir ecosystem and want to expose your app's data/tools to LLM clients. Not relevant outside of Elixir.

**Rating: 7/10** — solid implementation, limited by niche language choice.
