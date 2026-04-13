# Example: Mobile App Decision

**Input**
- Problem: Should we build a mobile app?
- Context: none provided
- Constraints: none provided

**Why this example is useful**
This run demonstrates the system handling maximum ambiguity -- a vague, one-line input with no context or constraints provided. The Discovery Agent reframes the question into a structured decision, surfaces six assumptions, and identifies eight constraints before any analysis begins.

---

> **Pipeline run:** `logs/run_20260413T001624Z.json`
> **Iterations:** 2 (analysis revised once after critique feedback)
> **Final critique score:** 8.0 / 10

---

## Stage 1 -- Discovery

### Reframed Problem

The organization needs to determine whether developing a mobile application represents the most effective use of resources to achieve specific business objectives, considering the target user needs that may be inadequately served by current digital touchpoints, the competitive landscape, technical feasibility, and expected return on investment.

### Desired Outcome

A data-driven recommendation on mobile app development that includes clear success metrics (user adoption targets, revenue impact, engagement benchmarks), resource requirements, timeline, and identified risks, enabling leadership to make an informed go/no-go decision aligned with business strategy.

### Assumptions Surfaced

- Current digital presence (website, social media, etc.) exists but may have gaps
- Target users have smartphones and would potentially download company apps
- Mobile app would provide differentiated value beyond existing touchpoints
- Organization has technical capability or budget to develop and maintain an app
- Mobile strategy aligns with overall business objectives
- Competitors may have mobile presence that influences user expectations

### Constraints Identified

- Budget limitations for development and ongoing maintenance
- Technical resources and expertise availability
- Platform decisions (iOS, Android, or both)
- App store approval processes and guidelines
- Timeline pressures or market timing considerations
- Integration requirements with existing systems
- Regulatory or compliance requirements for mobile applications
- User acquisition and retention costs in competitive app marketplace

---

## Stage 2 -- Analysis

### Option 1: Progressive Web App (PWA) Development ✅ Recommended

**Pros**
- 40% lower development cost than native apps with cross-platform compatibility
- Faster time-to-market (3-4 months vs 6-9 months for dual native)
- No app store approval bottlenecks or 30% revenue sharing fees
- Automatic updates without user friction or version fragmentation
- Leverages existing web development team skills, minimizing hiring needs
- SEO benefits and web discoverability maintain organic acquisition channels

**Cons**
- iOS Safari PWA limitations reduce functionality (no push notifications, limited storage)
- Performance gap vs native apps may impact user retention in high-engagement scenarios
- Lower perceived legitimacy among users who expect "real" apps from established brands
- Limited access to device-specific features (camera, contacts, biometrics)
- Inconsistent user experience across different mobile browsers
- Potential technical debt if native migration becomes necessary within 18 months

---

### Option 2: Native iOS + Android Development

**Pros**
- Maximum performance and user experience optimization for each platform
- Full access to platform-specific features (Face ID, Android Pay, push notifications)
- Higher user engagement and retention rates (typically 3x session length vs PWA)
- Premium brand perception and credibility in app stores
- Platform-optimized UI/UX follows user expectations and design guidelines
- Better monetization options through in-app purchases and subscription models

**Cons**
- 2.5x higher development cost requiring specialized iOS and Android developers
- Extended timeline (6-9 months) may miss critical market timing
- Ongoing maintenance complexity with two separate codebases
- App store approval risks and 30% revenue share on transactions
- Higher user acquisition costs in saturated app marketplace ($25-50 CAC)
- Version fragmentation issues and slower feature rollout cycles

---

### Option 3: White-label Partnership Solution

**Pros**
- Fastest market entry (4-6 weeks implementation) with proven technology stack
- Predictable monthly costs ($5K-15K) vs large upfront development investment
- Built-in compliance and security features reduce regulatory risks
- Partner handles technical maintenance, updates, and platform compatibility
- Access to partner's existing integrations and third-party services
- Lower technical resource requirements for internal team

**Cons**
- Limited customization restricts brand differentiation and unique value propositions
- Vendor lock-in creates long-term dependency and potential cost escalation
- Generic user experience may not address specific user journey pain points
- Revenue sharing or licensing fees reduce long-term profitability
- Less control over feature roadmap and development priorities
- Risk of partner discontinuation or acquisition affecting service continuity

---

### Recommendation

**Progressive Web App (PWA) Development.** This approach delivers 80% of native app benefits at 40% of the cost while maintaining strategic flexibility. Given budget constraints and the need for rapid market validation, PWA enables quick testing of mobile user engagement patterns without committing to expensive native development. Set clear migration triggers: if PWA achieves >10,000 monthly active users with >3 minute average session time within 6 months, or if iOS limitations cause >20% user drop-off, then justify native development investment. This staged approach minimizes risk while preserving future optionality.

### Key Tradeoffs

- **Development speed vs feature completeness** -- PWA launches faster but sacrifices iOS push notifications and advanced device integration
- **User experience quality vs resource allocation** -- native apps provide superior UX but require 2.5x budget and specialized developer hiring in a competitive talent market
- **Brand control vs time-to-market** -- white-label solutions launch quickly but limit differentiation in a crowded marketplace
- **Technical debt vs immediate capability** -- PWA may require costly migration to native if user engagement exceeds platform limitations
- **Acquisition cost vs retention quality** -- app store presence increases CAC but improves user lifetime value through better engagement tools

### Risks

- ⚠ High-impact failure mode: iOS Safari PWA performance issues causing 40%+ user abandonment, particularly for users with older devices or poor network connectivity
- ⚠ Strategic perception risk: enterprise clients or investors viewing PWA as a "budget solution" undermining premium brand positioning
- ⚠ Competitive displacement risk: key competitors launching superior native apps during PWA development window, capturing market share
- ⚠ Technical migration trap: PWA codebase creating architectural constraints that increase native development costs by 50% if migration becomes necessary
- ⚠ User acquisition challenge: lack of app store presence reducing discoverability by 60% compared to native apps, requiring higher marketing spend

---

## Stage 3 -- Critique

| Dimension | Score |
|---|---|
| Tradeoff completeness | 8 / 10 |
| Recommendation clarity | 9 / 10 |
| Risk realism | 7 / 10 |
| **Overall** | **8.0 / 10** |

### Critique Feedback

Strong analysis with well-researched options and specific metrics. Recommendation is actionable with clear migration triggers (>10K MAU, >3min sessions, >20% iOS drop-off).

**What worked well:** Comprehensive cost and timeline comparisons, realistic performance expectations, and a staged approach that minimizes risk.

**Critical gaps identified:**
1. **Missing user research validation** -- no evidence that PWA acceptability has been tested with target users
2. **No competitive benchmarking** -- no mention of competitor PWA/native mix for reference
3. **Some risk figures lack supporting data** -- the 40% abandonment and 60% discoverability reduction estimates need justification
4. **Technical migration cost estimate unsubstantiated** -- the 50% cost increase for native migration needs a basis
5. **Missing strategic context** -- target user demographics, use case complexity, and whether this is an MVP or established product expansion are not addressed
6. **Revenue model underexplored** -- app store fees vs marketing costs tradeoff is touched on but not resolved

Overall a solid framework, but could be strengthened with user research insights and more specific competitive intelligence.

> **Verdict:** Passes threshold (8.0 >= 7.0) -- no further revision required.

---

> Note: all estimates and metrics in this output are illustrative. Validate against your organization's actual data before making decisions.
