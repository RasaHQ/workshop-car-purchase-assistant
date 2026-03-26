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
    'Core concepts & function calling',
    'MCP — tools as a standard',
    'Designing tools for agents',
    'A2A — agent delegation',
    'Three Rasa patterns + code walkthrough',
    'Workshop project architecture',
    'Hands-on demo & setup',
    'Lab exercise & quiz',
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
native_tools = [
    Tool(
        name="calculate",
        description="...",
        input_schema={...},
    )
]
```

  </div>

  <!-- Unified handlers -->
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-green-400 rounded-lg p-4">
    <div class="text-green-400 text-xs font-extrabold tracking-wide mb-2">UNIFIED HANDLERS MAP</div>

```python
handlers = {
    t.name: call_mcp(client, t)
    for t in mcp_tools
} | native_handlers
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
    result = await handler(**call.input)
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

---
clicks: 1
---

# Principles in Practice — Filesystem MCP

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">13 tools → 4 — applying the principles to a real MCP server</div>

<div v-if="$clicks === 0" class="grid grid-cols-2 gap-4">
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-red-400 rounded-xl p-5">
    <div class="text-red-400 text-xs font-extrabold tracking-widest mb-3">BEFORE — 13+ INDIVIDUAL TOOLS</div>
    <div class="grid grid-cols-2 gap-1.5">
      <div v-for="tool in ['read_file', 'write_file', 'edit_file', 'create_directory', 'list_directory', 'directory_tree', 'move_file', 'search_files', 'get_file_info', 'read_multiple_files', 'delete_file', 'rename_file', 'copy_file']" class="bg-[#0d0d0d] rounded px-2.5 py-1.5 text-xs font-mono text-gray-500">{{ tool }}</div>
    </div>
    <div class="mt-4 bg-[#141414] border-l-3 border-red-400 rounded-r-lg px-4 py-3 text-gray-400 text-xs">
      Every tool in the context window costs tokens. The model must pick from 13 nearly-identical options — confusion and wrong picks are inevitable.
    </div>
  </div>
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-green-400 rounded-xl p-5">
    <div class="text-green-400 text-xs font-extrabold tracking-widest mb-3">AFTER — 4 CATEGORIES</div>
    <div class="space-y-3">
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-3">
        <div class="text-green-400 font-mono text-sm font-bold">fs_search</div>
        <div class="text-gray-500 text-xs mt-1">Files, directories, details — one tool handles all search</div>
      </div>
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-3">
        <div class="text-green-400 font-mono text-sm font-bold">fs_read</div>
        <div class="text-gray-500 text-xs mt-1">Text, binary, multiple files — mode parameter picks behavior</div>
      </div>
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-3">
        <div class="text-green-400 font-mono text-sm font-bold">fs_write</div>
        <div class="text-gray-500 text-xs mt-1">Create + edit — with <span class="text-yellow-400">checksum</span> verification and <span class="text-yellow-400">dryRun</span> safety</div>
      </div>
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-3">
        <div class="text-green-400 font-mono text-sm font-bold">fs_manage</div>
        <div class="text-gray-500 text-xs mt-1">Move, rename, delete — delete restricted to single files + empty dirs</div>
      </div>
    </div>
  </div>
</div>
<div v-if="$clicks >= 1">
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-yellow-400 rounded-xl p-5 mb-3">
    <div class="text-yellow-400 text-xs font-extrabold tracking-widest mb-3">THE SECRET SAUCE — DYNAMIC HINTS</div>
    <div class="text-gray-300 text-sm mb-4">Designing for agents isn't just about the schema — it's about what your tools <span class="text-yellow-400 font-bold">say back</span>. Every response should help the agent decide what to do next.</div>
    <div class="grid grid-cols-2 gap-x-6 gap-y-2">
      <div class="flex items-start gap-3 text-sm">
        <span class="text-yellow-400 font-extrabold shrink-0">›</span>
        <span class="text-gray-400"><span class="text-white">Errors tell what to do</span>, not just what went wrong — "File updated. Read it again to verify."</span>
      </div>
      <div class="flex items-start gap-3 text-sm">
        <span class="text-yellow-400 font-extrabold shrink-0">›</span>
        <span class="text-gray-400"><span class="text-white">Status flags hidden constraints</span> — "Document exists but is write-protected by user settings."</span>
      </div>
      <div class="flex items-start gap-3 text-sm">
        <span class="text-yellow-400 font-extrabold shrink-0">›</span>
        <span class="text-gray-400"><span class="text-white">Next-step suggestions</span> — "Found 3 docs. Read their contents before editing."</span>
      </div>
      <div class="flex items-start gap-3 text-sm">
        <span class="text-yellow-400 font-extrabold shrink-0">›</span>
        <span class="text-gray-400"><span class="text-white">Wrong values suggest options</span> — "Invalid label. Available: 'draft', 'review', 'final'."</span>
      </div>
      <div class="flex items-start gap-3 text-sm">
        <span class="text-yellow-400 font-extrabold shrink-0">›</span>
        <span class="text-gray-400"><span class="text-white">Auto-corrections are reported</span> — "Requested lines 48–70 but file has 59. Loaded 48–59."</span>
      </div>
      <div class="flex items-start gap-3 text-sm">
        <span class="text-yellow-400 font-extrabold shrink-0">›</span>
        <span class="text-gray-400"><span class="text-white">Path resolution</span> — agent sends just "config.yml", tool resolves to full path automatically</span>
      </div>
    </div>
  </div>
  <div class="bg-[#141414] border-l-3 border-green-400 rounded-r-lg px-5 py-3 text-gray-400 text-xs">
    Source: <a href="https://github.com/iceener/files-stdio-mcp-server" target="_blank" class="text-green-400 font-mono hover:underline">github.com/iceener/files-stdio-mcp-server</a> — a real MCP server built with these principles
  </div>
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---
layout: center
class: text-center
---

<div class="text-green-400 text-xs font-extrabold tracking-widest mb-4">SECTION 3</div>

# Agent-to-Agent Protocol

<div class="mt-4 text-gray-500 text-lg">When tools aren't enough — delegate to autonomous agents</div>

<style>
  h1 { color: #fff; font-size: 3rem; font-weight: 800; line-height: 1.2; }
  .slidev-layout { background: #0a0a0a; }
</style>

---

# What is A2A?

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-6">Google's Agent-to-Agent protocol — April 2025</div>

<div class="grid grid-cols-2 gap-6">
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-purple-400 rounded-xl p-5">
    <div class="text-purple-400 text-xs font-extrabold tracking-widest mb-3">THE IDEA</div>
    <div class="text-gray-300 text-sm leading-relaxed mb-3">
      A standard for agents to <span class="text-purple-400 font-bold">discover, communicate with, and delegate tasks to</span> other agents — regardless of framework.
    </div>
    <div class="text-gray-500 text-xs font-mono bg-[#0d0d0d] rounded p-3">
      Orchestrator → Agent Card → Task → Artifacts
    </div>
  </div>
  <div class="flex flex-col gap-3">
    <div v-for="[label, desc] in [
      ['Agent Card', 'JSON manifest declaring skills, I/O modes, and endpoint URL'],
      ['Task lifecycle', 'submitted → working → input_required → completed / failed'],
      ['Artifacts', 'Structured data returned alongside conversational text'],
      ['Streaming', 'Real-time status updates while the agent works'],
    ]" class="bg-[#141414] border border-[#222] rounded-lg px-4 py-2.5 text-sm">
      <span class="text-purple-400 font-bold">{{ label }}</span>
      <span class="text-gray-500 ml-2">{{ desc }}</span>
    </div>
  </div>
</div>

<div class="mt-3 bg-[#141414] border-l-3 border-purple-400 rounded-r-md px-5 py-2 font-mono text-xs text-gray-500">
  MCP = portable tools · A2A = portable agents
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---

# A2A Task Lifecycle

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">State machine for agent delegation</div>

<div class="flex items-center justify-center gap-3 mb-6">
  <div v-for="[state, color, active] in [
    ['submitted', 'border-gray-500 text-gray-400', false],
    ['working', 'border-orange-400 text-orange-400', false],
    ['input_required', 'border-yellow-400 text-yellow-400', false],
    ['completed', 'border-green-400 text-green-400', false],
    ['failed', 'border-red-400 text-red-400', false],
  ]" class="flex items-center gap-3">
    <div :class="color" class="border-2 rounded-lg px-4 py-2 text-xs font-extrabold tracking-wide bg-[#141414]">{{ state }}</div>
    <span v-if="state !== 'failed'" class="text-gray-600 font-mono text-xs">→</span>
  </div>
</div>

<div class="grid grid-cols-2 gap-4">
  <div class="bg-[#141414] border border-[#222] rounded-xl p-5">
    <div class="text-orange-400 text-xs font-extrabold tracking-widest mb-3">ORCHESTRATOR SENDS TASK</div>
    <div class="space-y-2 text-sm">
      <div class="flex items-start gap-3">
        <span class="text-blue-400 font-extrabold shrink-0">1</span>
        <span class="text-gray-300">Orchestrator discovers agent via <span class="text-purple-400 font-bold">Agent Card</span></span>
      </div>
      <div class="flex items-start gap-3">
        <span class="text-blue-400 font-extrabold shrink-0">2</span>
        <span class="text-gray-300">Sends user query + context as a <span class="text-purple-400 font-bold">Task</span></span>
      </div>
      <div class="flex items-start gap-3">
        <span class="text-blue-400 font-extrabold shrink-0">3</span>
        <span class="text-gray-300">Agent streams <span class="text-orange-400 font-bold">working</span> status updates</span>
      </div>
    </div>
  </div>
  <div class="bg-[#141414] border border-[#222] rounded-xl p-5">
    <div class="text-green-400 text-xs font-extrabold tracking-widest mb-3">AGENT RETURNS RESULT</div>
    <div class="space-y-2 text-sm">
      <div class="flex items-start gap-3">
        <span class="text-blue-400 font-extrabold shrink-0">4</span>
        <span class="text-gray-300">May request more input → <span class="text-yellow-400 font-bold">input_required</span></span>
      </div>
      <div class="flex items-start gap-3">
        <span class="text-blue-400 font-extrabold shrink-0">5</span>
        <span class="text-gray-300">Returns <span class="text-green-400 font-bold">artifacts</span> with structured data</span>
      </div>
      <div class="flex items-start gap-3">
        <span class="text-blue-400 font-extrabold shrink-0">6</span>
        <span class="text-gray-300">Orchestrator maps artifacts → <span class="text-green-400 font-bold">slots</span></span>
      </div>
    </div>
  </div>
</div>

<div class="mt-3 bg-[#141414] border-l-3 border-green-400 rounded-r-md px-5 py-2 font-mono text-xs text-gray-500">
  State contract versioning ensures handoff stability across deployments
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---

# When to use which — in Rasa

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">Three patterns for connecting subagents to the orchestrator</div>

<div class="grid grid-cols-3 gap-3 mb-4">
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-green-400 rounded-xl p-4">
    <div class="text-green-400 text-xs font-extrabold tracking-widest mb-2">MCP + REACT AGENT</div>
    <div class="text-gray-300 text-sm leading-relaxed">Built-in Rasa agent that <span class="text-green-400 font-bold">autonomously reasons</span> over MCP tools in a ReAct loop. Can mix MCP and custom tools.</div>
    <div class="mt-3 text-gray-500 text-xs">MCPOpenAgent · MCPTaskAgent</div>
  </div>
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-orange-400 rounded-xl p-4">
    <div class="text-orange-400 text-xs font-extrabold tracking-widest mb-2">MCP DIRECT FLOW CALL</div>
    <div class="text-gray-300 text-sm leading-relaxed">Call <span class="text-orange-400 font-bold">one specific MCP tool</span> from a flow step. No agent reasoning — deterministic with explicit slot mapping.</div>
    <div class="mt-3 text-gray-500 text-xs">call + mcp_server + mapping</div>
  </div>
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-purple-400 rounded-xl p-4">
    <div class="text-purple-400 text-xs font-extrabold tracking-widest mb-2">A2A EXTERNAL AGENT</div>
    <div class="text-gray-300 text-sm leading-relaxed"><span class="text-purple-400 font-bold">Different team, different tech</span> — connected via Agent Card. Owns its own LLM, tools, deploy lifecycle.</div>
    <div class="mt-3 text-gray-500 text-xs">A2AAgent · AgentCard</div>
  </div>
</div>

<div class="bg-[#141414] border-l-3 border-yellow-400 rounded-r-lg px-5 py-4 text-gray-300 text-sm leading-relaxed">
  <span class="text-yellow-400 font-bold">Decision guide:</span> Does the task need <span class="text-green-400 font-bold">autonomous tool selection</span>? → ReAct agent. Is it a <span class="text-orange-400 font-bold">single predictable call</span>? → Direct flow. Is it <span class="text-purple-400 font-bold">built by another team or in a different stack</span>? → A2A.
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---
clicks: 1
---

# Pattern 1 — MCP + ReAct Agent

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">Workshop example: Car Research Agent — <span class="text-green-400">press → for implementation</span></div>

<div v-if="$clicks === 0" class="grid grid-cols-2 gap-4">
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-green-400 rounded-xl p-5">
    <div class="text-green-400 text-xs font-extrabold tracking-wide mb-3">SUB-AGENT CONFIG</div>

```yaml
# sub_agents/research_agent/config.yml
agent:
  name: research_new_cars
  protocol: rasa              # ← ReAct agent
configuration:
  module: custom.car_research_agent
    .CarResearchAgent
connections:
  mcp_servers:
    - name: tavily_search     # ← MCP tools
```

  </div>
  <div class="flex flex-col gap-4">
    <div class="bg-[#141414] border border-[#222] rounded-xl p-5">
      <div class="text-orange-400 text-xs font-extrabold tracking-wide mb-3">FLOW — ONE STEP</div>

```yaml
# data/flows/car_research.yml
flows:
  car_research:
    description: Help the user choose
      a car by searching the web
    steps:
      - call: research_new_cars
```

  </div>
    <div class="bg-[#141414] border-l-3 border-yellow-400 rounded-r-lg px-5 py-4 text-gray-300 text-sm leading-relaxed">
      The orchestrator just calls the sub-agent — the agent <span class="text-green-400 font-bold">autonomously decides</span> which MCP tools to invoke in its ReAct loop.
    </div>
  </div>
</div>
<div v-if="$clicks >= 1" class="grid grid-cols-2 gap-4">
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-green-400 rounded-xl p-5">
    <div class="text-green-400 text-xs font-extrabold tracking-wide mb-3">CLASS STRUCTURE</div>
    <div class="font-mono text-sm text-gray-300 mb-4">class CarResearchAgent(<span class="text-green-400">MCPOpenAgent</span>)</div>
    <div class="space-y-3">
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-3">
        <div class="text-green-400 font-mono text-xs font-bold">get_custom_tool_definitions()</div>
        <div class="text-gray-500 text-xs mt-1">Registers <span class="text-white">recommend_cars</span> alongside MCP tools</div>
      </div>
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-3">
        <div class="text-green-400 font-mono text-xs font-bold">recommend_cars(args)</div>
        <div class="text-gray-500 text-xs mt-1">Custom tool — calls <span class="text-white">gpt-4o-mini</span> to analyze Tavily results → structured JSON recs</div>
      </div>
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-3">
        <div class="text-green-400 font-mono text-xs font-bold">process_tool_output(results)</div>
        <div class="text-gray-500 text-xs mt-1">Extracts model names → <span class="text-white">SlotSet("recommended_car_models")</span></div>
      </div>
    </div>
  </div>
  <div class="flex flex-col gap-4">
    <div class="bg-[#141414] border-l-3 border-yellow-400 rounded-r-lg px-5 py-4 text-gray-300 text-sm leading-relaxed">
      The ReAct agent autonomously chains: <span class="text-green-400 font-bold">tavily_search</span> (MCP) → <span class="text-green-400 font-bold">recommend_cars</span> (custom) → slots set for next flow.
    </div>
    <div class="bg-[#141414] border border-[#222] rounded-xl p-5">
      <div class="text-orange-400 text-xs font-extrabold tracking-widest mb-3">LET'S LOOK AT THE CODE</div>
      <div class="text-gray-400 text-sm mb-2">Open in IDE:</div>
      <div class="font-mono text-xs text-green-400 bg-[#0d0d0d] rounded px-3 py-2">custom/car_research_agent.py</div>
      <div class="mt-3 text-gray-500 text-xs">Key things to notice: how <span class="text-white">get_custom_tool_definitions</span> wires both MCP and custom tools, and how <span class="text-white">process_tool_output</span> maps results to Rasa slots.</div>
    </div>
  </div>
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---
clicks: 1
---

# Pattern 2 — MCP Direct Flow Call

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">Workshop example: Appointment Booking — <span class="text-orange-400">press → for MCPTaskAgent code</span></div>

<div v-if="$clicks === 0" class="grid grid-cols-2 gap-4">
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-orange-400 rounded-xl p-5">
    <div class="text-orange-400 text-xs font-extrabold tracking-wide mb-3">FLOW — BOTH PATTERNS IN ONE</div>

```yaml
# data/flows/schedule_appointment.yml
flows:
  schedule_new_appointment:
    steps:
      - call: appointment_selector        # ← ReAct agent
        exit_if:
          - slots.selected_appointment_slot is not null
      - collect: user_confirmation        # ← confirm with user
        ask_before_filling: true
      - call: book_appointment            # ← DIRECT MCP call
        mcp_server: appointment_booking
        mapping:
          input:
            - param: appointment_slot
              slot: selected_appointment_slot
          output:
            - slot: appointment_confirmed
              value: result.structuredContent
                .appointment_confirmed
      - action: utter_appointment_confirmed
```

  </div>
  <div class="bg-[#141414] border border-[#222] rounded-xl p-5">
    <div class="text-yellow-400 text-xs font-extrabold tracking-widest mb-3">KEY INSIGHT</div>
    <div class="text-gray-300 text-sm leading-relaxed mb-4">
      Same flow uses <span class="text-green-400 font-bold">both patterns</span>:
    </div>
    <div class="space-y-3 text-sm">
      <div class="flex items-start gap-3">
        <span class="text-green-400 font-extrabold shrink-0">1</span>
        <span class="text-gray-300"><span class="text-green-400 font-bold">ReAct agent</span> (<span class="font-mono text-xs">appointment_selector</span>) reasons autonomously to find the best slot</span>
      </div>
      <div class="flex items-start gap-3">
        <span class="text-orange-400 font-extrabold shrink-0">2</span>
        <span class="text-gray-300"><span class="text-orange-400 font-bold">Direct MCP call</span> (<span class="font-mono text-xs">book_appointment</span>) confirms the booking — no reasoning needed</span>
      </div>
    </div>
    <div class="mt-6 bg-[#141414] border-l-3 border-orange-400 rounded-r-lg px-5 py-4 text-gray-400 text-sm">
      The flow orchestrates both: an autonomous agent for the complex part, a direct tool call for the simple part.
    </div>
  </div>
</div>
<div v-if="$clicks >= 1" class="grid grid-cols-2 gap-4">
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-green-400 rounded-xl p-5">
    <div class="text-green-400 text-xs font-extrabold tracking-wide mb-3">CLASS STRUCTURE</div>
    <div class="font-mono text-sm text-gray-300 mb-4">class AppointmentBookingAgent(<span class="text-green-400">MCPTaskAgent</span>)</div>
    <div class="space-y-3">
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-3">
        <div class="text-green-400 font-mono text-xs font-bold">process_input(input)</div>
        <div class="text-gray-500 text-xs mt-1">Filters slots — only passes <span class="text-white">dealer_name</span>, <span class="text-white">car_model</span>, <span class="text-white">selected_appointment_slot</span></div>
      </div>
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-3">
        <div class="text-orange-400 font-mono text-xs font-bold">Injects current_date_time</div>
        <div class="text-gray-500 text-xs mt-1">Agent needs to know "today" to find relevant slots — added as a synthetic slot</div>
      </div>
    </div>
    <div class="mt-4 bg-[#141414] border-l-3 border-orange-400 rounded-r-lg px-4 py-3 text-gray-500 text-xs">
      This MCPTaskAgent connects to <span class="text-green-400 font-mono">appointment_booking</span> MCP server — but the flow <span class="text-orange-400 font-bold">excludes</span> <span class="font-mono text-white">book_appointment</span> from the agent (it's called directly in the flow instead).
    </div>
  </div>
  <div class="bg-[#141414] border border-[#222] rounded-xl p-5">
    <div class="text-orange-400 text-xs font-extrabold tracking-widest mb-3">LET'S LOOK AT THE CODE</div>
    <div class="text-gray-400 text-sm mb-3">Two files to explore:</div>
    <div class="space-y-2">
      <div class="font-mono text-xs text-orange-400 bg-[#0d0d0d] rounded px-3 py-2">custom/appointment_booking_agent.py</div>
      <div class="font-mono text-xs text-orange-400 bg-[#0d0d0d] rounded px-3 py-2">sub_agents/appointment_selector/config.yml</div>
    </div>
    <div class="mt-4 text-gray-500 text-xs leading-relaxed">
      Notice how <span class="text-white">config.yml</span> uses <span class="text-orange-400 font-bold">exclude_tools: [book_appointment]</span> — this is what forces that tool to be called directly from the flow instead of by the agent.
    </div>
  </div>
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---
clicks: 1
---

# Pattern 3 — A2A External Agent

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">Workshop example: Car Shopping Agent — <span class="text-purple-400">press → for Rasa wrapper code</span></div>

<div v-if="$clicks === 0" class="grid grid-cols-2 gap-4">
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-purple-400 rounded-xl p-5">
    <div class="text-purple-400 text-xs font-extrabold tracking-wide mb-3">SUB-AGENT CONFIG + AGENT CARD</div>

```yaml
# sub_agents/shopping_agent/config.yml
agent:
  name: shopping_agent
  protocol: a2a           # ← A2A protocol
configuration:
  agent_card: ./agent_card.json
  module: custom.car_shopping_agent.CarShoppingAgent
```

  <div class="mt-3 bg-[#0d0d0d] rounded-lg px-4 py-3">
    <div class="text-purple-400 text-[10px] font-extrabold tracking-widest mb-1">AGENT CARD DECLARES</div>
    <div class="text-gray-500 text-xs font-mono">url: http://...A2A_server:10002</div>
    <div class="text-gray-500 text-xs font-mono">capabilities: { streaming: true }</div>
    <div class="text-gray-500 text-xs font-mono">skills: [{ id: "search_cars" }]</div>
  </div>
  </div>
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-purple-400 rounded-xl p-5">
    <div class="text-purple-400 text-xs font-extrabold tracking-wide mb-3">WHY A2A FOR THIS?</div>
    <div class="space-y-3 text-sm">
      <div class="flex items-start gap-3">
        <span class="text-purple-400 font-extrabold shrink-0">›</span>
        <span class="text-gray-300"><span class="text-white font-bold">Different team</span> — built and maintained independently from the orchestrator</span>
      </div>
      <div class="flex items-start gap-3">
        <span class="text-purple-400 font-extrabold shrink-0">›</span>
        <span class="text-gray-300"><span class="text-white font-bold">Different stack</span> — Google ADK + Gemini vs Rasa + GPT-4o</span>
      </div>
      <div class="flex items-start gap-3">
        <span class="text-purple-400 font-extrabold shrink-0">›</span>
        <span class="text-gray-300"><span class="text-white font-bold">Own deploy lifecycle</span> — ships, scales, updates independently</span>
      </div>
      <div class="flex items-start gap-3">
        <span class="text-purple-400 font-extrabold shrink-0">›</span>
        <span class="text-gray-300"><span class="text-white font-bold">Complex workflow</span> — multi-turn with own tools, state, reasoning</span>
      </div>
    </div>
    <div class="mt-3 bg-[#141414] border-l-3 border-purple-400 rounded-r-lg px-5 py-3 text-gray-400 text-sm">
      A2A solves the <span class="text-purple-400 font-bold">organizational problem</span> — different team, different tech, different release cycle.
    </div>
  </div>
</div>
<div v-if="$clicks >= 1" class="grid grid-cols-2 gap-4">
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-orange-400 rounded-xl p-5">
    <div class="text-orange-400 text-xs font-extrabold tracking-wide mb-3">CLASS STRUCTURE</div>
    <div class="font-mono text-sm text-gray-300 mb-4">class CarShoppingAgent(<span class="text-purple-400">A2AAgent</span>)</div>
    <div class="space-y-3">
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-3">
        <div class="text-purple-400 font-mono text-xs font-bold">process_input(input)</div>
        <div class="text-gray-500 text-xs mt-1">Filters slots — only passes <span class="text-white">recommended_car_models</span> and <span class="text-white">recommended_car_details</span> to the A2A agent</div>
      </div>
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-3">
        <div class="text-purple-400 font-mono text-xs font-bold">process_agent_output(output)</div>
        <div class="text-gray-500 text-xs mt-1">Extracts <span class="text-white">final_reservation_decision</span> from A2A artifacts</div>
      </div>
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-3">
        <div class="text-green-400 font-mono text-xs font-bold">State contract enforcement</div>
        <div class="text-gray-500 text-xs mt-1">Validates required fields (<span class="text-white">final_decision</span>, <span class="text-white">car_model</span>, <span class="text-white">dealer_name</span>, <span class="text-white">price</span>) before setting slots</div>
      </div>
    </div>
  </div>
  <div class="flex flex-col gap-4">
    <div class="bg-[#141414] border-l-3 border-purple-400 rounded-r-lg px-5 py-4 text-gray-300 text-sm leading-relaxed">
      On <span class="text-green-400 font-bold">reserve</span> decision: sets <span class="text-white font-mono text-xs">car_model</span>, <span class="text-white font-mono text-xs">car_price</span>, <span class="text-white font-mono text-xs">dealer_name</span> slots — these persist across flows for financing and booking.
    </div>
    <div class="bg-[#141414] border border-[#222] rounded-xl p-5">
      <div class="text-orange-400 text-xs font-extrabold tracking-widest mb-3">LET'S LOOK AT THE CODE</div>
      <div class="text-gray-400 text-sm mb-3">Two sides to explore:</div>
      <div class="space-y-2">
        <div class="font-mono text-xs text-purple-400 bg-[#0d0d0d] rounded px-3 py-2">custom/car_shopping_agent.py <span class="text-gray-600">← Rasa wrapper</span></div>
        <div class="font-mono text-xs text-purple-400 bg-[#0d0d0d] rounded px-3 py-2">servers/car_shopping_server/agent.py <span class="text-gray-600">← Gemini agent</span></div>
        <div class="font-mono text-xs text-purple-400 bg-[#0d0d0d] rounded px-3 py-2">servers/car_shopping_server/agent_executor.py <span class="text-gray-600">← A2A protocol</span></div>
      </div>
    </div>
  </div>
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---
layout: center
class: text-center
---

<div class="text-green-400 text-xs font-extrabold tracking-widest mb-4">SECTION 4</div>

# The Workshop Project

<div class="mt-4 text-gray-500 text-lg">Car Purchase Assistant — MCP + A2A orchestrated by Rasa</div>

<style>
  h1 { color: #fff; font-size: 3rem; font-weight: 800; line-height: 1.2; }
  .slidev-layout { background: #0a0a0a; }
</style>

---

# Architecture Overview

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">Docker Compose topology — 5 services</div>

<div class="flex gap-4 items-stretch">
  <div class="border-2 border-green-400 rounded-xl bg-[#111] p-4 flex flex-col gap-2 min-w-[220px]">
    <div class="text-green-400 text-[10px] font-extrabold tracking-widest mb-1">ORCHESTRATOR · :5005</div>
    <div class="text-white text-lg font-extrabold">Rasa Pro</div>
    <div class="text-gray-500 text-xs">GPT-4o · FlowPolicy</div>
    <div class="text-gray-500 text-xs">Routes intent → specialist</div>
    <div class="mt-2 bg-[#1a1a1a] border border-[#282828] rounded-lg px-3 py-2 text-xs text-gray-400">
      <div class="text-orange-400 font-bold text-[10px] mb-1">FLOWS</div>
      <div>car_research → MCP</div>
      <div>car_shopping → A2A</div>
      <div>schedule_appointment → MCP</div>
      <div>calculate_loan → native</div>
    </div>
  </div>
  <div class="flex flex-col justify-around text-gray-500 font-mono text-xs py-4">
    <div>── HTTP ──→</div>
    <div>── HTTP ──→</div>
    <div>── A2A ──→</div>
  </div>
  <div class="flex flex-col gap-2 justify-center flex-1">
    <div class="bg-[#141414] border border-dashed border-[#333] rounded-lg px-4 py-3">
      <div class="flex items-center gap-2">
        <span class="text-green-400 text-[10px] font-extrabold tracking-widest">MCP SERVER · :8001</span>
      </div>
      <div class="text-white text-sm font-bold mt-1">Tavily Web Search</div>
      <div class="text-gray-500 text-xs">FastMCP · tavily_search tool</div>
    </div>
    <div class="bg-[#141414] border border-dashed border-[#333] rounded-lg px-4 py-3">
      <div class="flex items-center gap-2">
        <span class="text-green-400 text-[10px] font-extrabold tracking-widest">MCP SERVER · :8002</span>
      </div>
      <div class="text-white text-sm font-bold mt-1">Appointment Booking</div>
      <div class="text-gray-500 text-xs">FastMCP · query_available + book_appointment</div>
    </div>
    <div class="bg-[#141414] border border-dashed border-purple-400/50 rounded-lg px-4 py-3">
      <div class="flex items-center gap-2">
        <span class="text-purple-400 text-[10px] font-extrabold tracking-widest">A2A SERVER · :10002</span>
      </div>
      <div class="text-white text-sm font-bold mt-1">Car Shopping Agent</div>
      <div class="text-gray-500 text-xs">Google ADK · Gemini 2.5-flash · own tools + LLM</div>
    </div>
  </div>
</div>

<div class="mt-3 bg-[#141414] border-l-3 border-green-400 rounded-r-md px-5 py-2 font-mono text-xs text-gray-500">
  ./scripts/workshop_start.sh → docker compose up — trains model + starts all 5 services
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---
layout: center
class: text-center
---

<div class="text-green-400 text-xs font-extrabold tracking-widest mb-4">SECTION 5</div>

# Hands-on

<div class="mt-4 text-gray-500 text-lg">Run it, break it, fix it</div>

<style>
  h1 { color: #fff; font-size: 3rem; font-weight: 800; line-height: 1.2; }
  .slidev-layout { background: #0a0a0a; }
</style>

---

# Setup & Run

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">Get the workshop running in 3 steps</div>

<div class="grid grid-cols-3 gap-4">
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-blue-400 rounded-xl p-5">
    <div class="text-blue-400 text-xs font-extrabold tracking-widest mb-3">1 · ENV</div>
    <div class="text-gray-300 text-sm mb-3">Get the <span class="text-blue-400 font-bold">.env</span> from 1Password shared file and place it in the repo root.</div>
    <div class="text-gray-500 text-xs font-mono bg-[#0d0d0d] rounded p-3">
      OPENAI_API_KEY=sk-...<br/>
      GOOGLE_API_KEY=AI...<br/>
      TAVILY_API_KEY=tvly-...<br/>
      MOCK_TAVILY_SEARCH=true
    </div>
  </div>
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-green-400 rounded-xl p-5">
    <div class="text-green-400 text-xs font-extrabold tracking-widest mb-3">2 · START</div>
    <div class="text-gray-300 text-sm mb-3">Run the workshop start script — it trains the model and brings up all services.</div>
    <div class="text-gray-500 text-xs font-mono bg-[#0d0d0d] rounded p-3">
      ./scripts/workshop_start.sh<br/><br/>
      # stops existing stack<br/>
      # trains rasa model<br/>
      # docker compose up -d --build
    </div>
  </div>
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-yellow-400 rounded-xl p-5">
    <div class="text-yellow-400 text-xs font-extrabold tracking-widest mb-3">3 · VERIFY</div>
    <div class="text-gray-300 text-sm mb-3">Validate that all endpoints are reachable and logs are clean.</div>
    <div class="text-gray-500 text-xs font-mono bg-[#0d0d0d] rounded p-3">
      ./scripts/workshop_verify.sh<br/><br/>
      # checks docker daemon<br/>
      # checks model artifact<br/>
      # checks localhost:5005<br/>
      # scans logs for errors
    </div>
  </div>
</div>

<div class="mt-3 bg-[#141414] border-l-3 border-green-400 rounded-r-md px-5 py-2 font-mono text-xs text-gray-500">
  Rasa runs in inspect mode (:5005) — open the browser to chat with the assistant
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---

# Happy Path Demo

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">End-to-end journey — 4 prompts across all protocols</div>

<div class="grid grid-cols-2 gap-4">
  <div class="bg-[#141414] border border-[#222] rounded-xl p-5">
    <div class="space-y-4">
      <div class="flex gap-3 items-start">
        <span class="bg-green-400 text-black w-6 h-6 rounded-full flex items-center justify-center text-xs font-extrabold shrink-0">1</span>
        <div>
          <div class="text-gray-200 text-sm font-bold">Research</div>
          <div class="text-gray-500 text-xs italic">"I need a reliable compact SUV under $35k."</div>
          <div class="text-green-400 text-[10px] font-extrabold mt-1">MCP → tavily_search → recommend_cars</div>
        </div>
      </div>
      <div class="flex gap-3 items-start">
        <span class="bg-purple-400 text-black w-6 h-6 rounded-full flex items-center justify-center text-xs font-extrabold shrink-0">2</span>
        <div>
          <div class="text-gray-200 text-sm font-bold">Shopping</div>
          <div class="text-gray-500 text-xs italic">"Find one at a dealer near me."</div>
          <div class="text-purple-400 text-[10px] font-extrabold mt-1">A2A → car shopping agent → finalize_purchase</div>
        </div>
      </div>
      <div class="flex gap-3 items-start">
        <span class="bg-orange-400 text-black w-6 h-6 rounded-full flex items-center justify-center text-xs font-extrabold shrink-0">3</span>
        <div>
          <div class="text-gray-200 text-sm font-bold">Financing</div>
          <div class="text-gray-500 text-xs italic">"Can I afford this with a 72-month loan?"</div>
          <div class="text-orange-400 text-[10px] font-extrabold mt-1">NATIVE → calculate_affordability action</div>
        </div>
      </div>
      <div class="flex gap-3 items-start">
        <span class="bg-blue-400 text-black w-6 h-6 rounded-full flex items-center justify-center text-xs font-extrabold shrink-0">4</span>
        <div>
          <div class="text-gray-200 text-sm font-bold">Booking</div>
          <div class="text-gray-500 text-xs italic">"Book me an appointment next Tuesday afternoon."</div>
          <div class="text-blue-400 text-[10px] font-extrabold mt-1">MCP → appointment_booking → book_appointment</div>
        </div>
      </div>
    </div>
  </div>
  <div class="flex flex-col gap-3">
    <div class="bg-[#141414] border border-[#222] rounded-xl p-4">
      <div class="text-yellow-400 text-xs font-extrabold tracking-widest mb-2">WHAT TO OBSERVE</div>
      <div class="space-y-2 text-sm">
        <div class="flex items-start gap-3">
          <span class="text-green-400 font-extrabold shrink-0">›</span>
          <span class="text-gray-300">Flow routing — watch which sub-agent is called</span>
        </div>
        <div class="flex items-start gap-3">
          <span class="text-green-400 font-extrabold shrink-0">›</span>
          <span class="text-gray-300">Slot handoff — car_model persists across flows</span>
        </div>
        <div class="flex items-start gap-3">
          <span class="text-green-400 font-extrabold shrink-0">›</span>
          <span class="text-gray-300">A2A streaming — "Checking availability..." status</span>
        </div>
        <div class="flex items-start gap-3">
          <span class="text-green-400 font-extrabold shrink-0">›</span>
          <span class="text-gray-300">State contract — structured data in artifacts</span>
        </div>
      </div>
    </div>
    <div class="bg-[#141414] border border-[#222] rounded-xl p-4">
      <div class="text-orange-400 text-xs font-extrabold tracking-widest mb-2">DEBUG TIP</div>
      <div class="text-gray-400 text-sm">Check <span class="text-orange-400 font-mono">docker compose logs -f</span> to see real-time MCP/A2A traffic between services.</div>
    </div>
  </div>
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---
clicks: 4
---

# Happy Path — Live

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">Click through the conversation — <span class="text-green-400">research → shopping → financing → booking</span></div>

<div class="flex justify-center items-start" style="height: 50vh">
  <transition name="fade" mode="out-in">
    <img v-if="$clicks === 0" key="1" src="/happy-path-1.png" class="object-contain rounded-xl border border-[#222]" style="max-height: 50vh; max-width: 260px" />
    <img v-else-if="$clicks === 1" key="2" src="/happy-path-2.png" class="object-contain rounded-xl border border-[#222]" style="max-height: 50vh; max-width: 260px" />
    <img v-else-if="$clicks === 2" key="3" src="/happy-path-3.png" class="object-contain rounded-xl border border-[#222]" style="max-height: 50vh; max-width: 260px" />
    <img v-else-if="$clicks === 3" key="4" src="/happy-path-4.png" class="object-contain rounded-xl border border-[#222]" style="max-height: 50vh; max-width: 260px" />
    <img v-else key="5" src="/happy-path-5.png" class="object-contain rounded-xl border border-[#222]" style="max-height: 50vh; max-width: 260px" />
  </transition>
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
  .fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
  .fade-enter-from { opacity: 0; }
</style>

---
clicks: 5
---

# Which pattern would you use?

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">Apply the decision framework — press → to reveal answers</div>

<div class="space-y-2.5">
  <div class="bg-[#141414] border border-[#222] rounded-xl px-5 py-3">
    <div class="flex items-start gap-3">
      <span class="text-blue-400 font-extrabold text-lg shrink-0">1</span>
      <div class="flex-1">
        <div class="text-gray-200 text-sm">A customer asks "what's the weather in Berlin?" and you need to call a weather API</div>
        <div v-if="$clicks >= 1" class="mt-2 flex items-center gap-2"><span class="text-orange-400 text-xs font-extrabold bg-orange-400/10 border border-orange-400/20 rounded px-2 py-0.5">MCP DIRECT FLOW CALL</span><span class="text-gray-500 text-sm">Single deterministic call, predictable I/O, no reasoning needed</span></div>
      </div>
    </div>
  </div>
  <div class="bg-[#141414] border border-[#222] rounded-xl px-5 py-3">
    <div class="flex items-start gap-3">
      <span class="text-blue-400 font-extrabold text-lg shrink-0">2</span>
      <div class="flex-1">
        <div class="text-gray-200 text-sm">User wants car recommendations — agent needs to search the web, analyze results, and extract structured data</div>
        <div v-if="$clicks >= 2" class="mt-2 flex items-center gap-2"><span class="text-green-400 text-xs font-extrabold bg-green-400/10 border border-green-400/20 rounded px-2 py-0.5">MCP + REACT AGENT</span><span class="text-gray-500 text-sm">Autonomous tool selection — search first, then analyze, then extract</span></div>
      </div>
    </div>
  </div>
  <div class="bg-[#141414] border border-[#222] rounded-xl px-5 py-3">
    <div class="flex items-start gap-3">
      <span class="text-blue-400 font-extrabold text-lg shrink-0">3</span>
      <div class="flex-1">
        <div class="text-gray-200 text-sm">Partner team built a flight booking service in Java with its own LLM — you want to integrate it</div>
        <div v-if="$clicks >= 3" class="mt-2 flex items-center gap-2"><span class="text-purple-400 text-xs font-extrabold bg-purple-400/10 border border-purple-400/20 rounded px-2 py-0.5">A2A EXTERNAL AGENT</span><span class="text-gray-500 text-sm">Different team, different stack, own lifecycle — organizational boundary</span></div>
      </div>
    </div>
  </div>
  <div class="bg-[#141414] border border-[#222] rounded-xl px-5 py-3">
    <div class="flex items-start gap-3">
      <span class="text-blue-400 font-extrabold text-lg shrink-0">4</span>
      <div class="flex-1">
        <div class="text-gray-200 text-sm">You need to save a confirmed booking to a database — slot values are already known</div>
        <div v-if="$clicks >= 4" class="mt-2 flex items-center gap-2"><span class="text-orange-400 text-xs font-extrabold bg-orange-400/10 border border-orange-400/20 rounded px-2 py-0.5">MCP DIRECT FLOW CALL</span><span class="text-gray-500 text-sm">or even a <span class="text-blue-400">native action</span> — no LLM reasoning, just write to DB</span></div>
      </div>
    </div>
  </div>
  <div class="bg-[#141414] border border-[#222] rounded-xl px-5 py-3">
    <div class="flex items-start gap-3">
      <span class="text-blue-400 font-extrabold text-lg shrink-0">5</span>
      <div class="flex-1">
        <div class="text-gray-200 text-sm">Agent must browse multiple MCP tools to find appointment slots, compare them, and pick the best one</div>
        <div v-if="$clicks >= 5" class="mt-2 flex items-center gap-2"><span class="text-green-400 text-xs font-extrabold bg-green-400/10 border border-green-400/20 rounded px-2 py-0.5">MCP + REACT AGENT</span><span class="text-gray-500 text-sm">Needs reasoning over multiple tools — exactly what MCPTaskAgent does in this workshop</span></div>
      </div>
    </div>
  </div>
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---

# Lab Exercise

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">Your turn — try the scenarios from the README</div>

<div class="grid grid-cols-2 gap-4">
  <div class="bg-[#141414] border border-[#222] border-t-3 border-t-green-400 rounded-xl p-5">
    <div class="text-green-400 text-xs font-extrabold tracking-widest mb-3">SCENARIO 1 · HAPPY PATH</div>
    <div class="space-y-2.5">
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-2 text-sm text-gray-300 italic">"I'm looking for a reliable used sedan under $25,000."</div>
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-2 text-sm text-gray-300 italic">"Show me options near me."</div>
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-2 text-sm text-gray-300 italic">"Can I afford this with a 72-month loan and $5,000 down?"</div>
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-2 text-sm text-gray-300 italic">"Yes, reserve it."</div>
      <div class="bg-[#0d0d0d] rounded-lg px-4 py-2 text-sm text-gray-300 italic">"Book a test-drive appointment next Tuesday afternoon."</div>
    </div>
  </div>
  <div class="flex flex-col gap-4">
    <div class="bg-[#141414] border border-[#222] border-t-3 border-t-purple-400 rounded-xl p-5">
      <div class="text-purple-400 text-xs font-extrabold tracking-widest mb-3">SCENARIO 2 · CROSS-AGENT HANDOFF</div>
      <div class="space-y-2.5">
        <div class="bg-[#0d0d0d] rounded-lg px-4 py-2 text-sm text-gray-300 italic">"I'm looking for a compact SUV under $35k. Recommend dealers nearby."</div>
        <div class="bg-[#0d0d0d] rounded-lg px-4 py-2 text-sm text-gray-300 italic">"New. Safety and dealer distance matter most."</div>
        <div class="bg-[#0d0d0d] rounded-lg px-4 py-2 text-sm text-gray-300 italic">"Check if I can afford it with a 72-month loan and $5k down."</div>
        <div class="bg-[#0d0d0d] rounded-lg px-4 py-2 text-sm text-gray-300 italic">"Yes, reserve it."</div>
      </div>
    </div>
    <div class="bg-[#141414] border border-[#222] rounded-xl p-4">
      <div class="text-yellow-400 text-xs font-extrabold tracking-widest mb-2">OBSERVE</div>
      <div class="text-gray-400 text-sm">Watch <span class="text-orange-400 font-mono">docker compose logs -f</span> — which flows fire? Do slots persist across agent handoffs? Does the state contract validate?</div>
    </div>
  </div>
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>

---
layout: center
class: text-center
---

# Wrap-up

<div class="mt-6 max-w-2xl mx-auto text-left space-y-4">
  <div class="bg-[#141414] border border-[#222] rounded-xl p-5">
    <div class="text-yellow-400 text-xs font-extrabold tracking-widest mb-3">WHAT YOU SAW TODAY</div>
    <div class="space-y-2 text-sm">
      <div class="flex items-start gap-3">
        <span class="text-green-400 font-extrabold shrink-0">›</span>
        <span class="text-gray-300"><span class="text-white font-bold">MCP</span> standardizes how tools are exposed — build once, connect everywhere</span>
      </div>
      <div class="flex items-start gap-3">
        <span class="text-purple-400 font-extrabold shrink-0">›</span>
        <span class="text-gray-300"><span class="text-white font-bold">A2A</span> solves the organizational problem — different team, different stack, one protocol</span>
      </div>
      <div class="flex items-start gap-3">
        <span class="text-orange-400 font-extrabold shrink-0">›</span>
        <span class="text-gray-300"><span class="text-white font-bold">Three patterns in Rasa</span> — ReAct agent, direct flow call, external A2A agent</span>
      </div>
    </div>
  </div>
  <div class="bg-[#141414] border-l-3 border-green-400 rounded-r-lg px-5 py-4 text-gray-300 text-sm leading-relaxed">
    This was a taste — more depth on tool design, agent orchestration, and production patterns coming from the AI Devs course. Questions?
  </div>
</div>

<style>
  h1 { color: #fff; font-size: 2.5rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>
