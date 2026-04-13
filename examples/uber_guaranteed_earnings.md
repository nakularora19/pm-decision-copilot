# Example: Uber Driver Guaranteed Earnings

**Input**
- Problem: Should Uber introduce guaranteed earnings windows for drivers during suburban evening rush hours, and how do we price it without destroying margin?
- Context: Driver supply shortages in suburban markets 5-8pm. Surge pricing active but insufficient. Drivers cite earnings uncertainty as top reason for not logging on.
- Constraints: Must not imply employment classification, must be testable in 6 weeks, needs a clear margin impact model

**Why this example is useful**
This run demonstrates the system handling a complex, multi-stakeholder decision with legal, operational, and financial constraints simultaneously. Note how the Discovery Agent surfaces a non-obvious assumption -- that earnings uncertainty is the primary barrier -- and how the Critique Agent correctly flags insufficient cost modeling despite an otherwise strong analysis.

---

> **Pipeline run:** `logs/run_20260413T022332Z.json`
> **Iterations:** 2 (analysis revised once after critique feedback)
> **Final critique score:** 7.0 / 10

---

## Stage 1 -- Discovery

### Reframed Problem

Uber experiences driver supply shortages in suburban markets during 5-8pm rush hours despite active surge pricing, with drivers citing earnings uncertainty as the primary barrier to logging on. The company needs to determine if guaranteed earnings windows can effectively increase driver supply during these periods while maintaining profitability and avoiding employment classification implications.

### Desired Outcome

Increase driver supply in suburban markets during 5-8pm by X% while maintaining or improving unit economics, with a pricing model that provides earnings certainty to drivers without creating unsustainable margin erosion or legal employment classification risks.

### Assumptions Surfaced

- Earnings uncertainty is the primary driver behavior barrier, not other factors like safety or vehicle costs
- Drivers will respond to guaranteed earnings by logging on during specified windows
- Current surge pricing mechanisms are functioning correctly but insufficient to attract supply
- Suburban demand patterns are predictable enough to model guarantee costs accurately
- Driver behavior in suburban markets is representative across different suburban geographies
- Competitors are not offering similar guarantees that would require matching

### Constraints Identified

- Cannot create employment classification implications through guarantee structure
- Must be implementable and testable within 6-week timeline
- Requires clear margin impact modeling methodology
- Must work within existing driver app and payment infrastructure
- Cannot compromise existing surge pricing mechanisms
- Must comply with local regulations across different suburban markets

---

## Stage 2 -- Analysis

### Option 1: Hourly Minimum Guarantee with Activity Thresholds

**Pros**
- Provides earnings certainty while maintaining IC status through minimum activity requirements (90% acceptance, 80% online time)
- Leverages existing demand forecasting to set sustainable guarantee floors based on historical 5th percentile earnings
- Can be geofenced to specific suburban zones and time windows to control cost exposure
- Creates strong behavioral incentives for consistent availability during peak periods
- Allows dynamic adjustment of guarantee levels based on real-time supply/demand ratios

**Cons**
- Complex monitoring infrastructure required to track acceptance rates and enforce thresholds in real-time
- Potential driver gaming behaviors like strategic trip rejection patterns or coordinated offline periods
- Risk of creating two-tier driver ecosystem with guarantee-eligible vs ineligible drivers
- Higher customer acquisition costs if guarantee floors exceed organic earnings in low-demand periods
- Technical fraud detection challenges requiring investment in behavioral analytics systems

---

### Option 2: Predictive Earnings Transparency with Bonus Multipliers ✅ Recommended

**Pros**
- Reduces earnings uncertainty through ML-powered hourly earnings forecasts without guarantee liability
- Dynamic bonus multipliers (1.2x-2.5x) during forecasted low-earnings periods maintain variable cost structure
- Preserves existing surge mechanics while providing additional earnings visibility
- Lower implementation complexity using existing bonus payment infrastructure
- Reduces employment classification risk by maintaining pure performance-based compensation

**Cons**
- Forecast accuracy challenges could erode driver trust if predictions consistently overestimate earnings
- Requires sophisticated demand modeling with suburban-specific variables and weather/event data integration
- May not provide sufficient earnings certainty to drive material behavior change
- Bonus multiplier costs could become unpredictable if demand forecasts prove systematically optimistic
- Limited competitive differentiation as transparency tools are easily replicated

---

### Option 3: Block Scheduling with Pre-Committed Earnings

**Pros**
- Drivers commit to specific 2-hour blocks in advance, receiving guaranteed earnings for committed time
- Pre-commitment reduces last-minute supply uncertainty and enables better demand-supply matching
- Employment classification protection through voluntary scheduling without work requirements
- Creates planning certainty for both drivers and Uber's operational forecasting
- Enables premium pricing communication to riders during guaranteed coverage periods

**Cons**
- Requires significant driver behavior change from current flexible, on-demand model
- Block-based system may reduce overall platform flexibility and surge response capabilities
- Risk of drivers no-showing for committed blocks without adequate penalty mechanisms
- Potential rider experience degradation if pre-committed drivers cluster in profitable areas within zones
- Complex cancellation and penalty policies needed to maintain reliability while preserving contractor status

---

### Recommendation

**Predictive Earnings Transparency with Bonus Multipliers.** This approach addresses the core earnings uncertainty problem while minimizing employment classification risk and implementation complexity. The forecasting-plus-bonus model can be deployed within the 6-week timeline using existing infrastructure, provides measurable behavior change incentives, and maintains cost predictability through capped multiplier ranges. Success metrics should include 15-20% increase in 5-8pm driver supply, improved forecast accuracy (within 15% of actual earnings), and maintained contribution margins. If successful, this creates a foundation for more sophisticated guarantee mechanisms while providing immediate market learnings about suburban driver elasticity.

### Key Tradeoffs

- **Earnings certainty vs employment classification risk** -- stronger guarantees increase legal exposure
- **Implementation speed vs operational sophistication** -- faster deployment limits monitoring and fraud prevention capabilities
- **Cost predictability vs driver behavior effectiveness** -- guaranteed minimums provide certainty but create fixed cost exposure during demand downturns
- **Platform flexibility vs supply reliability** -- block scheduling improves predictability but reduces surge responsiveness
- **Competitive differentiation vs regulatory compliance** -- more aggressive guarantee programs may face greater legal scrutiny

### Risks

- ⚠ Demand forecasting accuracy below 70% could erode driver trust and reduce adoption within 3-4 weeks of launch
- ⚠ State labor board investigations triggered by guarantee structures, potentially taking 6-12 months but creating immediate PR and legal costs
- ⚠ Driver stratification effects creating marketplace imbalances between guarantee-eligible and standard drivers in same geographic areas
- ⚠ Suburban market cannibalization where drivers shift from profitable non-guarantee hours to guarantee periods, reducing overall platform efficiency
- ⚠ Technical fraud scenarios including coordinated driver behavior to maximize guarantee payouts through artificial demand suppression
- ⚠ Competitor response with superior guarantee offerings forcing escalatory bidding war within 2-3 months of launch

---

## Stage 3 -- Critique

| Dimension | Score |
|---|---|
| Tradeoff completeness | 8 / 10 |
| Recommendation clarity | 7 / 10 |
| Risk realism | 6 / 10 |
| **Overall** | **7.0 / 10** |

### Critique Feedback

Solid strategic thinking with well-articulated options covering different risk profiles.

**What worked well:** Tradeoffs are thoughtfully identified, particularly the employment classification vs certainty tension. The recommendation shows practical judgment by choosing the middle path that balances speed and risk. Risk identification covers multiple failure modes with reasonable timelines.

**Critical gaps identified:**
1. **Insufficient cost analysis** -- no concrete modeling of guarantee payouts, bonus multiplier costs, or break-even thresholds
2. **Unsupported targets** -- the 15-20% supply increase target lacks justification
3. **Vague implementation details** -- particularly around ML forecasting requirements and bonus calculation logic
4. **Underweighted operational complexity** -- fraud detection, driver gaming, and forecast model maintenance are more challenging than suggested
5. **Missing rider impact** -- longer wait times during low supply, network effects between zones, and specific success criteria beyond high-level metrics are absent
6. **Recommendation hedges too much** -- no clear decision criteria for pivoting to other options if this approach underperforms

> **Verdict:** Passes threshold (7.0 >= 7.0) -- no further revision required.

---

> Note: all estimates and metrics in this output are illustrative. Validate against your organization's actual data before making decisions.
