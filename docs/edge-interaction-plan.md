# Edge Interaction / Highlight Plan

## Goal
When a user hovers over or clicks an edge in a diagram, show more information about it
(source project, target project, reference type). When highlighting an edge, also dim
other edges to make the selected one stand out.

## Current SVG Structure (Mermaid v11)

After Mermaid renders, the SVG contains:
- **Edges**: `<path>` elements inside `<g class="edgePaths">` with:
  - ID pattern: `L_<from-id>_<to-id>_0`
  - Classes: `edge-thickness-normal edge-pattern-solid flowchart-link`
  - Dashed edges (cross-category): `edge-pattern-dotted`
- **Edge labels**: `<g class="edgeLabel">` — no IDs, paired with edge paths by index
- **Nodes**: `<g class="node">` with ID `flowchart-<id>-<n>`, text content is display name
- **Arrow markers**: `<path class="arrowMarkerPath">` — separate from edge paths

## Approach 1: Mermaid Click Directive + CSS Hover (Try First)

### What Mermaid supports natively
- `click <nodeId> callback "tooltip"` — **nodes only**, not edges
- `securityLevel: 'loose'` required for JS callbacks
- `linkStyle N stroke:#color` — static edge styling by index number

### What we can add post-render
- **CSS hover on edges**: `.flowchart-link:hover { stroke: #f59e0b; stroke-width: 3px; }`
- **JS event listeners on edge `<path>` elements**: parse the ID to extract from/to node IDs
- **Tooltip on hover**: create a floating `<div>` positioned near the cursor showing edge details

### Implementation plan

#### Step 1: CSS hover highlight (minimal, zero risk)
Add CSS to the viewer that highlights edges on hover:
```css
.flowchart-link:hover {
    stroke: #3b82f6 !important;
    stroke-width: 3px !important;
    filter: drop-shadow(0 0 3px rgba(59, 130, 246, 0.5));
}
```
Dims non-hovered edges when any edge is hovered (using a parent `:has()` selector):
```css
.edgePaths:has(.flowchart-link:hover) .flowchart-link:not(:hover) {
    opacity: 0.2;
}
```

#### Step 2: Tooltip on edge hover (JS post-render)
After Mermaid renders each diagram, attach `mouseenter`/`mouseleave` listeners to all
`.flowchart-link` paths. On hover:
1. Parse the edge ID (`L_<from>_<to>_0`) to get source/target node IDs
2. Look up display names from the `.node` elements by matching IDs
3. Show a tooltip `<div>` near the cursor with: `Source → Target`

The edge ID uses underscores for the separator between from/to, but node IDs can also
contain underscores. To resolve this: build a lookup from the rendered node elements
(`flowchart-<id>-<n>` → text content), then match the edge ID's from/to segments
against known node IDs.

#### Step 3: Click to lock highlight + show detail panel
On click, lock the highlight state (stays highlighted until clicking elsewhere).
Show a small detail panel below the diagram with:
- Source project name and category
- Target project name and category
- Reference type (project-reference vs cross-repo-reference)
- For grouped diagrams: list of individual project-to-project edges in the group

This requires embedding edge metadata as a JSON blob in the HTML (in `generate_docs.py`).

### Data we need to embed
In `generate_docs.py`, emit a `<script>` block with edge metadata per diagram tab:
```javascript
var edgeData = {
    "cat_test": [
        {"from": "KurrentDB.Core.Tests", "to": "KurrentDB.Core.Testing", "type": "project-reference"},
        ...
    ],
    ...
};
```

### Risks and limitations
- Edge ID format (`L_from_to_0`) may change in future Mermaid versions
- Underscores in project names make ID parsing ambiguous — need lookup table
- CSS `:has()` selector not supported in older browsers (works in all modern ones)
- Grouped diagrams show aggregated edges — tooltip would show group name, not individual projects

### Testing
- Playwright: hover over an edge, screenshot, verify highlight appears
- Playwright: check tooltip text content after hover
- Test on all 7 datasets, verify no JS errors in console

---

## Approach 2: Cytoscape.js (Fallback if Mermaid interaction is too limited)

Replace Mermaid rendering with Cytoscape.js for the per-category detail diagrams.
Keep Mermaid for the Overview tab (small, simple, static).

### Why this would work well
- Full programmatic control over node/edge rendering
- Built-in hover, click, select events
- Built-in tooltips (via `tippy.js` extension or custom)
- Edge metadata directly accessible in the data model
- Better layout control (dagre, cola, breadthfirst)
- Pan and zoom built-in (replace our manual zoom buttons)

### Implementation plan
1. In `generate_docs.py`, emit Cytoscape graph data as JSON instead of Mermaid text for detail tabs
2. Add Cytoscape.js + dagre layout CDN scripts
3. Render each detail tab as a Cytoscape canvas
4. Style nodes by category (colours matching Mermaid theme)
5. Edge hover: highlight + tooltip with details
6. Edge click: show detail panel with full metadata

### Data format
```javascript
{
    nodes: [
        { data: { id: "proj-id", label: "Display Name", category: "test" } },
        ...
    ],
    edges: [
        { data: { source: "proj-a", target: "proj-b", type: "project-reference", label: "1" } },
        ...
    ]
}
```

### Risks
- Visual style will differ from Overview tab (Mermaid) vs Detail tabs (Cytoscape)
- Cytoscape layout may not match Mermaid's aesthetics
- Additional JS dependency (~400KB minified)
- More implementation effort

---

## Approach 3: D3.js Custom (Last Resort)

Roll our own force-directed or hierarchical layout using D3.js.

### When to use this
- Mermaid interaction too limited AND Cytoscape doesn't meet layout/style needs
- Need pixel-perfect control over every visual element
- Want to add features like animated edge traversal, filtering sliders, etc.

### Risks
- Significant implementation effort
- Must build layout, zoom/pan, styling, interaction from scratch
- D3 force layouts can be slow with 100+ nodes

---

## Recommendation

**Start with Approach 1** (CSS hover + JS tooltip on Mermaid SVG). It's low-risk,
no new dependencies, and gives us 80% of the value. Steps 1-2 can be done quickly.

If the Mermaid SVG interaction proves too fragile (ID format changes, edge label
matching issues, grouped diagram limitations), **fall back to Approach 2** (Cytoscape.js)
for the per-category detail tabs only.

**Approach 3** (D3) is insurance — only if Cytoscape's built-in layouts don't produce
readable diagrams for our graph shapes.

## Test Matrix

| Dataset       | Projects | Detail tabs to test          | Grouped? |
|---------------|----------|------------------------------|----------|
| eShop         | 24       | All small                    | No       |
| Lean          | 23       | All small                    | No       |
| EventStore    | 84       | Test (40), Library (28)      | No       |
| akka.net      | 109      | Test (48)                    | No       |
| StockSharp    | 140      | Library (59)                 | Yes      |
| NuGet.Client  | 115      | Test (76)                    | Yes      |
| OrchardCore   | 230      | Library (192)                | Yes      |
