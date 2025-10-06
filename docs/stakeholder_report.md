# Stakeholder Communication: Lending Club Analysis

## Executive Summary

After digging into Lending Club's loan data from 2007 to 2015, I've found that the grading system does a solid job of sorting borrowers by risk. However, the riskiest grades (F and G) have default rates that are higher than what I'd consider safe for a conservative lending approach. This is something we need to address soon.

## Key Business Insight

The current grading system works well to separate low-risk from high-risk borrowers. Grade A loans have about a 5% default rate, while Grade G jumps to nearly 51%. Grades F and G, in particular, are above our comfort zone for risk.

### Supporting Evidence
- Grade A loans are in line with industry standards for default rates
- There's a clear increase in risk as you move from A to G
- F and G grades make up a big chunk of our defaults
- The extra interest charged for riskier loans may not be enough to cover the losses

## What Should We Do Next?

### Main Recommendation: Tiered Risk Management

**Short Term (0-3 months):**
1. Put a cap on F-G loans—keep them under 15% of our total portfolio
2. Ask for more proof of income and employment for E-G borrowers
3. Adjust interest rates for F-G loans to better match the risk

**Medium Term (3-12 months):**
1. Build predictive models that look at more borrower details, not just grade
2. Consider new loan products for higher-risk borrowers, with extra safeguards
3. Set up a dashboard to track default rates by grade and get alerts if things change

**Expected Impact:**
- Lower our overall default rate by 2-4%
- Improve returns by keeping risk in check
- Stay competitive while protecting the business

## Questions We Expect From Stakeholders

### "What makes borrowers in each grade more likely to default?"

We'll need to look at things like:
- Debt-to-income ratios
- How long people have been at their jobs
- Where they live and local economic conditions
- Why they're taking out the loan and how much they're borrowing
- Their credit history and recent activity

We'll use logistic regression and decision trees to find the top factors for each grade, plus some maps to show where defaults are happening most.

### "If we tighten our lending criteria, what happens to volume and profits?"

We'll run scenarios to see:
- How many applications and loans we might lose
- How our revenue and profit would change
- What competitors might do if we get stricter
- The trade-off between less interest income and fewer defaults

### "Can we spot loans that are likely to default early on?"

We'll analyze payment patterns, customer behavior, and financial changes over time to find early warning signs. The goal is to step in before defaults happen.

## Risks and How We'll Handle Them

### Challenges
1. Cutting back on high-risk loans could mean fewer new loans
2. Competitors might pick up the customers we turn away
3. We need to make sure our policies are fair and don't discriminate
4. We might see a short-term dip in revenue

### Mitigation
1. Roll out changes gradually over six months
2. Offer alternative products to those we decline
3. Keep an eye on what competitors are doing
4. Double-check that we're following all lending regulations

## How We'll Measure Success

### Key Metrics
- Default rate (track monthly)
- Returns by grade
- Conversion rates from application to funded loan
- Market share by grade
- Customer acquisition costs

### Reporting
- Weekly: Monitor high-risk loan exposure
- Monthly: Review default rates and portfolio mix
- Quarterly: Full risk-return analysis
- Annually: Validate models and review grading system

## Communication Plan

### For Executives
- Focus on overall impact and competitive position
- Highlight risk-adjusted returns and compliance
- Share clear projections for the recommended changes

### For Product Teams
- Spell out new grade policies and timelines
- Discuss customer experience and competitor moves
- Note any tech needs for better verification

### For Risk Teams
- Share detailed analysis and model results
- Give clear risk thresholds and confidence levels
- Outline ongoing monitoring and escalation steps

In short, these recommendations turn our analysis into practical steps, balancing risk and growth while keeping everyone in the loop with clear, actionable updates.