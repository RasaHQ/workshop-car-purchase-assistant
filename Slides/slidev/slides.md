---
theme: default
background: '#0a0a0a'
class: text-center
highlighter: shiki
lineNumbers: false
drawings:
  persist: false
transition: slide-left
title: A2A & MCP Workshop
defaults:
  layout: default
---

# A2A & MCP Workshop

<div class="mt-6 text-gray-400 text-lg">Agent-to-Agent & Model Context Protocol</div>

<div class="mt-10 grid grid-cols-2 gap-3 max-w-2xl mx-auto text-left">
  <div v-for="item in [
    'Core concepts',
    'MCP React agents',
    'Connecting via A2A',
    'File structure',
    'Orchestration',
    'What\'s in the future',
    'Troubleshooting quiz',
    'Debugging walkthrough',
  ]" class="bg-[#141414] border border-[#222] rounded-lg px-4 py-2.5 text-sm text-gray-300 flex items-center gap-3">
    <span class="text-green-400 font-extrabold shrink-0">›</span>
    <span>{{ item }}</span>
  </div>
</div>

<style>
  h1 { color: #fff; font-size: 2.5rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---
layout: center
class: text-center
---

<div class="text-green-400 text-xs font-extrabold tracking-widest mb-4">SECTION 1</div>

# Core Concepts

<div class="mt-4 text-gray-500 text-lg">How LLMs process information and use tools</div>

<style>
  h1 { color: #fff; font-size: 3rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---

# Interacting with LLMs

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-6">The foundation of everything that follows</div>

<div class="grid grid-cols-2 gap-6 max-w-3xl">
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-blue-400 rounded-xl p-5">
    <div class="text-blue-400 text-xs font-extrabold tracking-widest mb-3">FUNDAMENTAL TRUTH</div>
    <div class="text-2xl font-bold text-white mb-3">LLMs output just text tokens</div>
    <div class="text-gray-400 text-sm leading-relaxed">
      At their core, language models produce one token at a time — nothing more, nothing less.
    </div>
  </div>

  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-green-400 rounded-xl p-5">
    <div class="text-green-400 text-xs font-extrabold tracking-widest mb-3">BUT PROVIDERS ADD STRUCTURE</div>
    <div class="text-gray-300 text-sm leading-relaxed">
      LLM Providers expose APIs that allow you to ensure text responses from the model adhere to a <span class="text-green-400 font-bold">JSON schema you define</span>.
    </div>
    <div class="mt-4 font-mono text-xs text-gray-500 bg-[#0d0d0d] rounded p-3">
      response_format: &#123; type: "json_schema", schema: ... &#125;
    </div>
  </div>
</div>

<div class="mt-6 bg-[#141414] border-l-3 border-yellow-400 rounded-r-lg px-5 py-3 text-gray-400 text-sm max-w-3xl">
  This is why <span class="text-yellow-400 font-bold">tool calling / function calling</span> is possible at all —
  and it's the fundament that enables MCP servers.
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---
clicks: 4
---

# Anatomy of an LLM Response

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">A single response can contain many types of output</div>

<div v-if="$clicks === 0" class="flex gap-6 items-start">
  <div class="relative group shrink-0">
    <img src="/anatomy-llm-response.png" class="rounded-xl border border-[#222] h-64 object-contain object-top cursor-pointer" />
    <div class="absolute inset-0 flex items-end justify-end p-2 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
      <span class="bg-black/80 text-gray-400 text-xs px-2 py-1 rounded font-mono">→ click to zoom</span>
    </div>
  </div>

  <div class="flex flex-col gap-3 flex-1">
    <div v-for="[icon, color, label, desc] in [
      ['🧠', 'text-purple-400', 'Reasoning tokens', 'Internal chain-of-thought before answering'],
      ['🔍', 'text-blue-400', 'Web / tool calls', 'Multiple tools invoked in parallel or sequence'],
      ['⚙️', 'text-green-400', 'Code execution', 'Code interpreter, function calls, API requests'],
      ['🖼️', 'text-orange-400', 'Generated images', 'Image output from multimodal models'],
      ['💬', 'text-gray-300', 'Text output', 'Streamed incrementally as separate events'],
    ]" class="bg-[#141414] border border-[#222] rounded-lg px-4 py-2.5 flex items-start gap-3 text-sm">
      <span>{{ icon }}</span>
      <div>
        <span :class="color" class="font-bold">{{ label }}</span>
        <span class="text-gray-500 ml-2">{{ desc }}</span>
      </div>
    </div>
  </div>
</div>

<transition name="fade">
  <div v-if="$clicks >= 1" class="absolute inset-0 overflow-hidden bg-[#0a0a0a] z-10">
    <img
      src="/anatomy-llm-response.png"
      class="w-full h-full object-contain origin-center transition-transform duration-500 ease-in-out"
      :style="{
        transform: $clicks === 1
          ? 'scale(2) translateY(25%)'
          : $clicks === 2
            ? 'scale(2) translateY(8%)'
            : $clicks === 3
              ? 'scale(2) translateY(-8%)'
              : 'scale(2) translateY(-25%)'
      }"
    />
  </div>
</transition>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
  .fade-enter-active, .fade-leave-active { transition: opacity 0.4s ease; }
  .fade-enter-from, .fade-leave-to { opacity: 0; }
</style>

---
clicks: 4
---

# Function Calling / Tool Use

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">How LLMs interact with the outside world</div>

<div v-if="$clicks === 0" class="flex gap-6 items-start">
  <div class="relative group shrink-0">
    <img src="/function-calling.png" class="rounded-xl border border-[#222] h-64 object-contain cursor-pointer" />
    <div class="absolute inset-0 flex items-end justify-end p-2 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
      <span class="bg-black/80 text-gray-400 text-xs px-2 py-1 rounded font-mono">→ click to zoom</span>
    </div>
  </div>

  <div class="flex flex-col gap-2 flex-1 text-sm">
    <div v-for="[step, color, actor, desc] in [
      ['1', 'bg-blue-400', 'USER', 'Sends a natural language query'],
      ['2', 'bg-purple-400', 'LLM', 'Receives query + tool definitions'],
      ['3', 'bg-purple-400', 'LLM', 'Generates structured JSON output'],
      ['4', 'bg-orange-400', 'CODE', 'Parses JSON → executes API call'],
      ['5', 'bg-orange-400', 'CODE', 'Returns tool result to LLM'],
      ['6', 'bg-purple-400', 'LLM', 'Synthesizes final response'],
    ]" class="bg-[#141414] border border-[#222] rounded-lg px-3 py-2 flex items-center gap-3">
      <span :class="color" class="w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-extrabold text-black shrink-0">{{ step }}</span>
      <span class="text-gray-500 text-[10px] font-extrabold w-10 shrink-0">{{ actor }}</span>
      <span class="text-gray-300">{{ desc }}</span>
    </div>
  </div>
</div>

<transition name="fade">
  <div v-if="$clicks >= 1" class="absolute inset-0 overflow-hidden bg-[#0a0a0a] z-10">
    <img
      src="/function-calling.png"
      class="w-full h-full object-contain origin-center transition-transform duration-500 ease-in-out"
      :style="{
        transform: $clicks === 1
          ? 'scale(2) translateY(25%)'
          : $clicks === 2
            ? 'scale(2) translateY(8%)'
            : $clicks === 3
              ? 'scale(2) translateY(-8%)'
              : 'scale(2) translateY(-25%)'
      }"
    />
  </div>
</transition>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
  .fade-enter-active, .fade-leave-active { transition: opacity 0.4s ease; }
  .fade-enter-from, .fade-leave-to { opacity: 0; }
</style>

---

# Building AI integrations <br/> without a standard

<div class="mt-4 text-gray-400 text-lg">Every provider, every client — a different format</div>

<div class="mt-10 text-left max-w-xl mx-auto space-y-3">
  <div class="flex items-start gap-3" v-for="item in [
    'Function Calling requires building integrations from scratch',
    'API formats differ across OpenAI, Anthropic, Google & others',
    'Tool handling varies in Claude Code, ChatGPT, Cursor & more',
    'No standard means N providers × M clients = N×M integrations',
  ]">
    <span class="text-red-400 text-xl font-extrabold shrink-0">×</span>
    <span class="text-gray-200">{{ item }}</span>
  </div>
</div>

<div class="absolute bottom-8 left-12 right-12 bg-[#141414] border-l-3 border-red-400 rounded-r-md px-5 py-3 font-mono text-sm text-gray-500">
  No standard → N × M integrations to maintain forever
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; line-height: 1.2; }
  .slidev-layout { background: #0a0a0a; }
</style>

---

# Model Context Protocol

<div class="text-gray-400 text-base -mt-2">Proposed by Anthropic — November 2024</div>

<div class="mt-6 text-gray-300 text-lg max-w-xl">
  A standard protocol for connecting LLMs to external tools.<br/>
  Build <span class="text-green-400 font-bold">one MCP server</span> — connect it everywhere.
</div>

<div class="mt-8 grid grid-cols-2 gap-3 max-w-2xl">
  <div v-for="item in [
    'Build once, connect everywhere',
    'Works with Claude Code, Cursor, ChatGPT',
    'No custom client-side code per platform',
    'Consistent format for tools delivery',
  ]" class="bg-[#141414] border border-[#222] rounded-lg px-4 py-3 text-sm text-gray-200 flex items-start gap-3">
    <span class="text-green-400 text-lg font-extrabold shrink-0">✓</span>
    <span>{{ item }}</span>
  </div>
</div>

<div class="absolute bottom-8 left-12 right-12 bg-[#141414] border-l-3 border-green-400 rounded-r-md px-5 py-3 font-mono text-sm text-gray-500">
  With MCP → 1 server + N hosts = done
</div>

<style>
  h1 { color: #fff; font-size: 2.2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---
layout: default
---

# Architecture

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-6">Host → Clients → Servers</div>

<div class="flex gap-6 items-stretch">
  <!-- HOST -->
  <div class="border-2 border-green-400 rounded-xl bg-[#111] p-4 flex gap-3 min-w-[320px]">
    <!-- LLM -->
    <div class="bg-[#1a1a1a] border border-[#282828] rounded-lg flex flex-col items-center justify-center w-24 py-8">
      <span class="text-gray-500 text-xs font-semibold">LLM</span>
      <span class="text-white text-lg font-extrabold mt-1">Claude</span>
    </div>
    <!-- Clients -->
    <div class="flex flex-col gap-2 justify-center">
      <div v-for="c in ['Client A', 'Client B', 'Client C']" class="bg-[#1a1a1a] border border-[#282828] rounded-lg px-6 py-3 text-sm text-gray-300 font-semibold text-center">
        {{ c }}
      </div>
    </div>
  </div>

  <!-- Arrows -->
  <div class="flex flex-col justify-around text-gray-500 font-mono text-xs py-4">
    <div>── stdio ──→</div>
    <div>── stdio ──→</div>
    <div>── HTTP/SSE →</div>
  </div>

  <!-- Servers -->
  <div class="flex flex-col gap-2 justify-center">
    <div v-for="s in ['Linear', 'Google Calendar', 'Google Maps']" class="bg-[#141414] border border-dashed border-[#333] rounded-lg px-6 py-3 min-w-[200px]">
      <div class="text-green-400 text-[10px] font-extrabold tracking-widest">MCP SERVER</div>
      <div class="text-white text-base font-bold mt-1">{{ s }}</div>
    </div>
  </div>
</div>

<div class="absolute bottom-8 left-12 right-12 bg-[#141414] border-l-3 border-green-400 rounded-r-md px-5 py-3 font-mono text-sm text-gray-500">
  Host spawns one Client per Server — Clients live inside, Servers run outside
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---

# Integration

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">MCP + Native Tools → Unified Toolset</div>

<div class="grid grid-cols-2 gap-3">
  <!-- Native tools -->
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-green-400 rounded-lg p-4">
    <div class="text-green-400 text-xs font-extrabold tracking-wide mb-2">NATIVE TOOLS</div>

```python
native_tools = [{
    "type": "function",
    "name": "calculate",
    "parameters": { ... }
}]
```

  </div>

  <!-- Unified handlers -->
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-green-400 rounded-lg p-4">
    <div class="text-green-400 text-xs font-extrabold tracking-wide mb-2">UNIFIED HANDLERS MAP</div>

```python
handlers = {
    **{t.name: call_mcp(client, t)
       for t in mcp_tools},
    **native_handlers
}
```

  </div>

  <!-- MCP server -->
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-purple-400 rounded-lg p-4">
    <div class="flex items-center gap-2 mb-2">
      <span class="text-purple-400 text-xs font-extrabold tracking-wide">MCP SERVER</span>
      <span class="text-gray-500 text-[10px] border border-dashed border-gray-600 px-2 py-0.5 rounded">external process</span>
    </div>

```python
@server.tool()
async def get_weather(city: str):
    return {"content": [...]}
```

  </div>

  <!-- Agent runtime -->
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-orange-400 rounded-lg p-4">
    <div class="text-orange-400 text-xs font-extrabold tracking-wide mb-2">AGENT RUNTIME — ORIGIN AGNOSTIC</div>

```python
for call in response.tool_calls:
    handler = handlers[call.name]
    result = await handler(**call.args)
    # routes to MCP or native fn
```

  </div>
</div>

<div class="absolute bottom-8 left-12 right-12 bg-[#141414] border-l-3 border-purple-400 rounded-r-md px-5 py-3 font-mono text-sm text-gray-500">
  From the agent's perspective, tool origin doesn't matter — lookup by name only
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
  .slidev-code-wrapper { margin: 0 !important; }
  pre.shiki { background: transparent !important; padding: 0.25rem 0 !important; font-size: 0.8rem !important; }
</style>

---

# Execution

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">Agent Runtime — Tool Execution Flow</div>

<div class="flex gap-2 mb-4">
  <div v-for="[label, color] in [['User','bg-blue-400'],['Agent','bg-purple-400'],['Result','bg-yellow-600']]" class="flex items-center gap-2 text-xs text-gray-400 font-semibold">
    <span :class="color" class="w-2.5 h-2.5 rounded-full"></span> {{ label }}
  </div>
</div>

<div class="grid grid-cols-2 gap-4">
  <!-- Native Tool -->
  <div class="bg-[#141414] border border-[#222] rounded-xl p-5">
    <div class="text-green-400 text-xs font-extrabold tracking-widest mb-4">NATIVE TOOL</div>
    <div class="space-y-3">
      <div class="flex gap-3 items-start">
        <span class="text-[10px] font-bold text-blue-400 bg-blue-400/10 border border-blue-400/20 rounded px-2 py-0.5 shrink-0">USER</span>
        <span class="text-sm text-gray-200">Calculate 42 × 17</span>
      </div>
      <div class="flex gap-3 items-start">
        <span class="text-[10px] font-bold text-purple-400 bg-purple-400/10 border border-purple-400/20 rounded px-2 py-0.5 shrink-0">AGENT</span>
        <div>
          <span class="text-sm text-gray-200 font-mono">calculate</span>
          <span class="text-[9px] font-extrabold text-green-400 bg-green-400/10 rounded px-1.5 py-0.5 ml-2">NATIVE</span>
          <div class="text-xs text-gray-500 font-mono mt-0.5">{"op":"multiply","a":42,"b":17}</div>
        </div>
      </div>
      <div class="flex gap-3 items-start">
        <span class="text-[10px] font-bold text-yellow-600 bg-yellow-600/10 border border-yellow-600/20 rounded px-2 py-0.5 shrink-0">RESULT</span>
        <span class="text-sm text-gray-200 font-mono">{"result": 714}</span>
      </div>
      <div class="flex gap-3 items-start">
        <span class="text-[10px] font-bold text-purple-400 bg-purple-400/10 border border-purple-400/20 rounded px-2 py-0.5 shrink-0">AGENT</span>
        <span class="text-sm text-gray-200">42 × 17 = 714</span>
      </div>
    </div>
  </div>

  <!-- MCP Tool -->
  <div class="bg-[#141414] border border-[#222] rounded-xl p-5">
    <div class="text-blue-400 text-xs font-extrabold tracking-widest mb-4">MCP TOOL</div>
    <div class="space-y-3">
      <div class="flex gap-3 items-start">
        <span class="text-[10px] font-bold text-blue-400 bg-blue-400/10 border border-blue-400/20 rounded px-2 py-0.5 shrink-0">USER</span>
        <span class="text-sm text-gray-200">Weather in Tokyo?</span>
      </div>
      <div class="flex gap-3 items-start">
        <span class="text-[10px] font-bold text-purple-400 bg-purple-400/10 border border-purple-400/20 rounded px-2 py-0.5 shrink-0">AGENT</span>
        <div>
          <span class="text-sm text-gray-200 font-mono">get_weather</span>
          <span class="text-[9px] font-extrabold text-blue-400 bg-blue-400/10 rounded px-1.5 py-0.5 ml-2">MCP</span>
          <div class="text-xs text-gray-500 font-mono mt-0.5">{"city":"Tokyo"}</div>
        </div>
      </div>
      <div class="flex gap-3 items-start">
        <span class="text-[10px] font-bold text-yellow-600 bg-yellow-600/10 border border-yellow-600/20 rounded px-2 py-0.5 shrink-0">RESULT</span>
        <span class="text-sm text-gray-200 font-mono">{"sunny", "23°C"}</span>
      </div>
      <div class="flex gap-3 items-start">
        <span class="text-[10px] font-bold text-purple-400 bg-purple-400/10 border border-purple-400/20 rounded px-2 py-0.5 shrink-0">AGENT</span>
        <span class="text-sm text-gray-200">Tokyo: sunny, 23 °C</span>
      </div>
    </div>
  </div>
</div>

<div class="absolute bottom-8 left-12 right-12 bg-[#141414] border-l-3 border-orange-400 rounded-r-md px-5 py-3 font-mono text-sm text-gray-500">
  Agent routes to MCP client or native function automatically — origin is transparent
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---

# What MCP actually solves

<div class="text-gray-400 text-base -mt-2">A portable standard for storing and delivering tools</div>

<div class="mt-6 bg-[#141414] border-l-3 border-green-400 rounded-r-lg px-6 py-5 text-gray-400 text-base leading-relaxed max-w-2xl">
  From the agent's perspective, tool source is irrelevant.<br/>
  MCP defines how tools are <span class="text-green-400 font-bold">stored and delivered in a consistent format</span> —<br/>
  so one server plugs into any compatible host.
</div>

<div class="mt-8 grid grid-cols-2 gap-3 max-w-2xl">
  <div v-for="item in [
    'Tools are just functions — MCP standardizes how they\'re exposed',
    'One server → Claude Code, Cursor, ChatGPT & more',
    'Not just tools — resources and prompts are primitives too',
    'Protocol-level interoperability, zero per-client custom work',
  ]" class="bg-[#141414] border border-[#222] rounded-lg px-4 py-3 text-sm text-gray-300 flex items-start gap-3">
    <span class="text-green-400 text-lg font-extrabold shrink-0">›</span>
    <span>{{ item }}</span>
  </div>
</div>

<style>
  h1 { color: #fff; font-size: 2.2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---
layout: center
class: text-center
---

<div class="text-green-400 text-xs font-extrabold tracking-widest mb-4">SECTION 2</div>

# How to design tools for Agents

<div class="mt-4 text-gray-500 text-lg">7 principles for LLM-friendly tool design</div>

<style>
  h1 { color: #fff; font-size: 3rem; font-weight: 800; line-height: 1.2; }
  .slidev-layout { background: #0a0a0a; }
</style>

---
clicks: 4
---

# Generalizing generalization

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">Tool selection at scale</div>

<div v-if="$clicks === 0" class="flex gap-6 items-start">
  <div class="relative group shrink-0">
    <img src="/ai_devs_4_generalization-b9ae6fb2-a.png" class="h-64 object-contain rounded-xl border border-[#222] cursor-pointer" />
    <div class="absolute inset-0 flex items-end justify-end p-2 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
      <span class="bg-black/80 text-gray-400 text-xs px-2 py-1 rounded font-mono">→ click to zoom</span>
    </div>
  </div>
  <div class="flex flex-col gap-4 flex-1">
    <div class="bg-[#141414] border-l-3 border-yellow-400 rounded-r-lg px-5 py-4 text-gray-300 text-base leading-relaxed">
      You can have problems with just <span class="text-yellow-400 font-bold">two tools</span>.
    </div>
    <div class="bg-[#141414] border border-[#222] rounded-xl px-5 py-4">
      <div class="text-green-400 text-xs font-extrabold tracking-widest mb-3">THE SOLUTION</div>
      <div class="text-gray-300 text-sm leading-relaxed mb-3">
        Helping the model by providing it a <span class="text-green-400 font-bold">general process</span> on how to better choose correct tools helps significantly.
      </div>
      <div class="space-y-2 text-sm text-gray-400">
        <div class="flex items-start gap-3">
          <span class="text-green-400 font-extrabold shrink-0">›</span>
          <span>Write system prompts that describe <em>when</em> to use each tool, not just <em>what</em> it does</span>
        </div>
        <div class="flex items-start gap-3">
          <span class="text-green-400 font-extrabold shrink-0">›</span>
          <span>Provide decision heuristics — "prefer X when Y, use Z only if..."</span>
        </div>
        <div class="flex items-start gap-3">
          <span class="text-green-400 font-extrabold shrink-0">›</span>
          <span>Tool descriptions are part of your prompt engineering</span>
        </div>
      </div>
    </div>
  </div>
</div>

<transition name="fade">
  <div v-if="$clicks >= 1" class="absolute inset-0 bg-[#0a0a0a] z-10 flex items-center justify-center p-4">
    <div class="relative overflow-hidden rounded-xl border border-[#222] w-full h-full">
      <img
        src="/ai_devs_4_generalization-b9ae6fb2-a.png"
        class="w-full h-full object-contain origin-center transition-transform duration-500 ease-in-out"
        :style="{
          transform: $clicks === 1
            ? 'scale(1) translateY(0)'
            : $clicks === 2
              ? 'scale(2) translateY(25%)'
              : $clicks === 3
                ? 'scale(2) translateY(0%)'
                : 'scale(2) translateY(-25%)'
        }"
      />
    </div>
  </div>
</transition>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
  .fade-enter-active, .fade-leave-active { transition: opacity 0.4s ease; }
  .fade-enter-from, .fade-leave-to { opacity: 0; }
</style>

---
clicks: 6
---

# Designing Tools for LLM Agents

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-2">All 7 principles at a glance — <span class="text-green-400">click through to zoom each section</span></div>

<div class="relative overflow-hidden rounded-xl border border-[#222] mx-auto" style="height: 62vh">
  <img
    src="/designing-tools.png"
    class="w-full h-full object-contain origin-center transition-transform duration-500 ease-in-out"
    :style="{
      transform: $clicks === 0
        ? 'scale(1) translateY(0)'
        : $clicks === 1
          ? 'scale(2.5) translateY(27%)'
          : $clicks === 2
            ? 'scale(2.5) translateY(13%)'
            : $clicks === 3
              ? 'scale(2.5) translateY(0%)'
              : $clicks === 4
                ? 'scale(2.5) translateY(-20%)'
                : $clicks === 5
                  ? 'scale(2.5) translateY(-33%)'
                  : 'scale(2.5) translateY(-47%)'
    }"
  />
</div>

<div v-if="$clicks >= 1 && $clicks <= 6" class="mt-3 bg-[#141414] border border-[#333] rounded-xl px-5 py-2.5">
  <div v-if="$clicks === 1">
    <div class="text-green-400 font-extrabold text-xs tracking-widest mb-1">P1 — SELF-EXPLANATORY · P2 — UNIQUE NAMING</div>
    <div class="text-gray-300 text-sm">Name + description must tell the full story — no docs needed. Avoid generic names like send, get, update. The model reads descriptions at runtime.</div>
  </div>
  <div v-if="$clicks === 2">
    <div class="text-green-400 font-extrabold text-xs tracking-widest mb-1">P3 — HIGH SIGNAL-TO-NOISE</div>
    <div class="text-gray-300 text-sm">Every word in a description costs tokens — keep only what helps the model decide when and how to call the tool. Skip implementation details.</div>
  </div>
  <div v-if="$clicks === 3">
    <div class="text-green-400 font-extrabold text-xs tracking-widest mb-1">P4 — MINIMIZE STEPS</div>
    <div class="text-gray-300 text-sm">Each round-trip adds latency and a chance of error. Design tools that accomplish a complete intent in one call — batch related params instead of chaining calls.</div>
  </div>
  <div v-if="$clicks === 4">
    <div class="text-green-400 font-extrabold text-xs tracking-widest mb-1">P5 — LEAN SCHEMAS</div>
    <div class="text-gray-300 text-sm">Expose only what the model can meaningfully provide — hide db internals, retry counts, timeouts. Those are your code's responsibility.</div>
  </div>
  <div v-if="$clicks === 5">
    <div class="text-green-400 font-extrabold text-xs tracking-widest mb-1">P6 — CLEAR OWNERSHIP</div>
    <div class="text-gray-300 text-sm">Draw a hard boundary between semantic choices (model) and operational details (code). Mixing concerns leads to hallucinated configs.</div>
  </div>
  <div v-if="$clicks === 6">
    <div class="text-green-400 font-extrabold text-xs tracking-widest mb-1">P7 — MINIMAL RESPONSES</div>
    <div class="text-gray-300 text-sm">Return just enough — tool responses go back into the context window. Keep them small and include a "next" hint so the model knows what to do.</div>
  </div>
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>
