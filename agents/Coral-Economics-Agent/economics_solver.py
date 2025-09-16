import re
import math
from typing import Dict, List, Tuple, Optional

class EconomicsSolver:
    """
    A comprehensive economics problem solver for high school level economics.
    Handles various topics including supply/demand, elasticity, market structures, and macroeconomics.
    """
    
    def __init__(self):
        self.economic_formulas = {
            'elasticity_demand': "Price Elasticity of Demand = (% Change in Quantity Demanded) / (% Change in Price)",
            'elasticity_supply': "Price Elasticity of Supply = (% Change in Quantity Supplied) / (% Change in Price)",
            'consumer_surplus': "Consumer Surplus = 0.5 × Base × Height",
            'producer_surplus': "Producer Surplus = 0.5 × Base × Height", 
            'gdp_nominal': "Nominal GDP = Price × Quantity for all goods and services",
            'gdp_real': "Real GDP = Nominal GDP / GDP Deflator × 100",
            'inflation_rate': "Inflation Rate = ((CPI_new - CPI_old) / CPI_old) × 100",
            'unemployment_rate': "Unemployment Rate = (Unemployed / Labor Force) × 100"
        }
    
    async def solve_problem(self, problem: str) -> str:
        """
        Main problem-solving method that analyzes and solves economics problems.
        """
        problem_type = self._identify_problem_type(problem)
        
        if problem_type == "supply_demand":
            return await self._solve_supply_demand(problem)
        elif problem_type == "elasticity":
            return await self._solve_elasticity(problem)
        elif problem_type == "market_equilibrium":
            return await self._solve_market_equilibrium(problem)
        elif problem_type == "consumer_producer_surplus":
            return await self._solve_surplus(problem)
        elif problem_type == "gdp_analysis":
            return await self._solve_gdp(problem)
        elif problem_type == "inflation_unemployment":
            return await self._solve_macro_indicators(problem)
        elif problem_type == "market_structures":
            return await self._analyze_market_structure(problem)
        else:
            return await self._general_economics_explanation(problem)
    
    def _identify_problem_type(self, problem: str) -> str:
        """Identify the type of economics problem based on keywords."""
        problem_lower = problem.lower()
        
        if any(word in problem_lower for word in ['supply', 'demand', 'curve', 'shift']):
            return "supply_demand"
        elif any(word in problem_lower for word in ['elasticity', 'elastic', 'inelastic', 'responsive']):
            return "elasticity"
        elif any(word in problem_lower for word in ['equilibrium', 'market clearing', 'intersection']):
            return "market_equilibrium"
        elif any(word in problem_lower for word in ['consumer surplus', 'producer surplus', 'deadweight loss']):
            return "consumer_producer_surplus"
        elif any(word in problem_lower for word in ['gdp', 'gross domestic product', 'economic growth']):
            return "gdp_analysis"
        elif any(word in problem_lower for word in ['inflation', 'unemployment', 'cpi', 'price level']):
            return "inflation_unemployment"
        elif any(word in problem_lower for word in ['monopoly', 'competition', 'oligopoly', 'market structure']):
            return "market_structures"
        else:
            return "general"
    
    async def _solve_supply_demand(self, problem: str) -> str:
        """Solve supply and demand related problems."""
        solution = """
**SUPPLY AND DEMAND ANALYSIS**

**Problem Identification:**
This appears to be a supply and demand problem. Let me analyze the key components.

**Step-by-Step Solution:**

1. **Identify the Market Factors:**
   - What good/service is being analyzed?
   - What factors might shift supply or demand?
   - Are we looking at movements along curves or shifts of curves?

2. **Demand Analysis:**
   - Demand Law: As price increases, quantity demanded decreases (ceteris paribus)
   - Demand Shifters: Income, tastes, prices of substitutes/complements, expectations, population
   - Normal goods: Income ↑ → Demand ↑
   - Inferior goods: Income ↑ → Demand ↓

3. **Supply Analysis:**
   - Supply Law: As price increases, quantity supplied increases (ceteris paribus)
   - Supply Shifters: Input costs, technology, expectations, number of sellers, government policies

4. **Market Effects:**
   - Demand increase: Price ↑, Quantity ↑
   - Demand decrease: Price ↓, Quantity ↓
   - Supply increase: Price ↓, Quantity ↑
   - Supply decrease: Price ↑, Quantity ↓

**Key Concepts to Remember:**
- Distinguish between "change in demand/supply" (curve shifts) vs "change in quantity demanded/supplied" (movement along curve)
- Market equilibrium occurs where supply and demand curves intersect
- Shortages occur when price is below equilibrium; surpluses when price is above equilibrium

**Real-World Application:**
Consider how events like weather (affecting agricultural supply), income changes (affecting demand for luxury goods), or new technology (affecting production costs) impact markets.
"""
        return solution
    
    async def _solve_elasticity(self, problem: str) -> str:
        """Solve elasticity-related problems."""
        # Try to extract numerical values if present
        numbers = re.findall(r'-?\d+\.?\d*', problem)
        
        solution = f"""
**ELASTICITY ANALYSIS**

**Problem Identification:**
This is an elasticity problem. Elasticity measures responsiveness of one variable to changes in another.

**Key Formula:**
{self.economic_formulas['elasticity_demand']}

**Step-by-Step Solution:**

1. **Calculate Percentage Changes:**
   - % Change in Quantity = ((Q₂ - Q₁) / Q₁) × 100
   - % Change in Price = ((P₂ - P₁) / P₁) × 100

2. **Calculate Elasticity:**
   - Price Elasticity of Demand (PED) = % Change in Quantity Demanded / % Change in Price
   - Use absolute value for interpretation

3. **Interpret Results:**
   - |PED| > 1: Elastic (quantity is responsive to price changes)
   - |PED| < 1: Inelastic (quantity is not very responsive to price changes)
   - |PED| = 1: Unit elastic (proportional response)
   - |PED| = 0: Perfectly inelastic (no response)
   - |PED| = ∞: Perfectly elastic (infinite response)

4. **Factors Affecting Elasticity:**
   - Availability of substitutes (more substitutes → more elastic)
   - Necessity vs luxury (necessities → less elastic)
   - Time period (longer time → more elastic)
   - Proportion of income spent (larger proportion → more elastic)

**Revenue Implications:**
- Elastic demand: Price ↓ → Total Revenue ↑
- Inelastic demand: Price ↑ → Total Revenue ↑
- Unit elastic: Total Revenue remains constant

**Real-World Examples:**
- Gasoline: Inelastic (few substitutes, necessity)
- Restaurant meals: Elastic (many substitutes, luxury)
- Salt: Perfectly inelastic (no substitutes, tiny portion of budget)
"""
        
        if len(numbers) >= 4:
            # Attempt to calculate if we have enough numbers
            try:
                q1, q2, p1, p2 = float(numbers[0]), float(numbers[1]), float(numbers[2]), float(numbers[3])
                pct_change_q = ((q2 - q1) / q1) * 100
                pct_change_p = ((p2 - p1) / p1) * 100
                if pct_change_p != 0:
                    elasticity = abs(pct_change_q / pct_change_p)
                    solution += f"""

**Numerical Calculation (if applicable):**
- Initial Quantity: {q1}, New Quantity: {q2}
- Initial Price: {p1}, New Price: {p2}
- % Change in Quantity: {pct_change_q:.2f}%
- % Change in Price: {pct_change_p:.2f}%
- Price Elasticity: |{pct_change_q:.2f}/{pct_change_p:.2f}| = {elasticity:.2f}
- Interpretation: {'Elastic' if elasticity > 1 else 'Inelastic' if elasticity < 1 else 'Unit Elastic'}
"""
            except:
                pass
        
        return solution
    
    async def _solve_market_equilibrium(self, problem: str) -> str:
        """Solve market equilibrium problems."""
        solution = """
**MARKET EQUILIBRIUM ANALYSIS**

**Problem Identification:**
This involves finding where supply and demand curves intersect to determine equilibrium price and quantity.

**Step-by-Step Solution:**

1. **Set Up Equations:**
   - Demand equation: Qd = a - bP (downward sloping)
   - Supply equation: Qs = c + dP (upward sloping)
   - Where Q = quantity, P = price, a,b,c,d are constants

2. **Find Equilibrium:**
   - At equilibrium: Qd = Qs
   - Solve: a - bP = c + dP
   - Rearrange: a - c = bP + dP = P(b + d)
   - Equilibrium Price: Pe = (a - c) / (b + d)
   - Equilibrium Quantity: Qe = a - b × Pe (or c + d × Pe)

3. **Verify Solution:**
   - Substitute Pe back into both equations
   - Both should give the same Qe

4. **Analyze Market Conditions:**
   - If price > Pe: Surplus (Qs > Qd)
   - If price < Pe: Shortage (Qd > Qs)
   - Market forces push toward equilibrium

**Shifts in Equilibrium:**
- Demand increase: Pe ↑, Qe ↑
- Demand decrease: Pe ↓, Qe ↓
- Supply increase: Pe ↓, Qe ↑
- Supply decrease: Pe ↑, Qe ↓

**Graph Visualization:**
```
Price
  |    S
  |   /
Pe|--/----\\
  | /      \\D
  |/        \\
  +----------\\---> Quantity
  0           Qe
```

**Real-World Application:**
Market equilibrium explains how prices are determined in competitive markets and how they adjust when conditions change.
"""
        return solution
    
    async def _solve_surplus(self, problem: str) -> str:
        """Solve consumer and producer surplus problems."""
        solution = f"""
**CONSUMER AND PRODUCER SURPLUS ANALYSIS**

**Problem Identification:**
This involves calculating the welfare gains from trade in a market.

**Key Formulas:**
- {self.economic_formulas['consumer_surplus']}
- {self.economic_formulas['producer_surplus']}

**Step-by-Step Solution:**

1. **Consumer Surplus:**
   - Area between demand curve and market price
   - Represents benefit consumers receive from paying less than their maximum willingness to pay
   - Formula: CS = 0.5 × Base × Height = 0.5 × Qe × (Pmax - Pe)
   - Where Pmax is the price intercept of demand curve

2. **Producer Surplus:**
   - Area between supply curve and market price  
   - Represents benefit producers receive from selling above their minimum acceptable price
   - Formula: PS = 0.5 × Base × Height = 0.5 × Qe × (Pe - Pmin)
   - Where Pmin is the price intercept of supply curve

3. **Total Economic Surplus:**
   - Total Surplus = Consumer Surplus + Producer Surplus
   - Maximized in competitive equilibrium
   - Any price control reduces total surplus (creates deadweight loss)

4. **Effects of Price Controls:**
   - Price ceiling (below equilibrium): Reduces both CS and PS
   - Price floor (above equilibrium): Transfers surplus from consumers to producers
   - Deadweight loss = Lost total surplus due to market inefficiency

**Graphical Representation:**
```
Price
  |    S
  |   /|\\
  |  / | \\CS (Consumer Surplus)
Pe|-----|----\\
  | PS  |     \\D
  |/    |      \\
  +-------------- Quantity
  0     Qe
```

**Real-World Applications:**
- Welfare analysis of taxes and subsidies
- Evaluating efficiency of different market structures
- Understanding effects of trade policies
"""
        return solution
    
    async def _solve_gdp(self, problem: str) -> str:
        """Solve GDP and economic growth problems."""
        solution = f"""
**GDP ANALYSIS**

**Problem Identification:**
This involves calculating or analyzing Gross Domestic Product and economic growth.

**Key Formulas:**
- {self.economic_formulas['gdp_nominal']}
- {self.economic_formulas['gdp_real']}

**Step-by-Step Solution:**

1. **GDP Calculation Methods:**
   - **Expenditure Approach:** GDP = C + I + G + (X - M)
     * C = Consumption, I = Investment, G = Government spending
     * X = Exports, M = Imports
   - **Income Approach:** Sum of all incomes earned in production
   - **Production Approach:** Sum of value added by all industries

2. **Nominal vs Real GDP:**
   - **Nominal GDP:** Current year prices × Current year quantities
   - **Real GDP:** Base year prices × Current year quantities
   - **GDP Deflator:** (Nominal GDP / Real GDP) × 100

3. **Economic Growth Rate:**
   - Growth Rate = ((GDP_new - GDP_old) / GDP_old) × 100
   - Per capita GDP = GDP / Population

4. **GDP Limitations:**
   - Doesn't measure: Income distribution, quality of life, environmental costs
   - Includes: All legal market transactions
   - Excludes: Household production, underground economy

**Components Analysis:**
- **Consumption (C):** Usually largest component (~70% in US)
- **Investment (I):** Most volatile component
- **Government (G):** Relatively stable
- **Net Exports (X-M):** Can be positive or negative

**Business Cycle Connections:**
- GDP growth indicates economic expansion
- GDP decline (2+ quarters) indicates recession
- GDP per capita measures standard of living

**Real-World Application:**
GDP is the primary measure of a country's economic performance and is used for policy decisions and international comparisons.
"""
        return solution
    
    async def _solve_macro_indicators(self, problem: str) -> str:
        """Solve inflation and unemployment problems."""
        solution = f"""
**MACROECONOMIC INDICATORS ANALYSIS**

**Problem Identification:**
This involves analyzing inflation, unemployment, or related macroeconomic indicators.

**Key Formulas:**
- {self.economic_formulas['inflation_rate']}
- {self.economic_formulas['unemployment_rate']}

**Step-by-Step Solution:**

1. **Inflation Analysis:**
   - **CPI Calculation:** Market basket cost in current year / Market basket cost in base year × 100
   - **Inflation Rate:** ((CPI_new - CPI_old) / CPI_old) × 100
   - **Types:** Demand-pull, cost-push, built-in inflation

2. **Unemployment Analysis:**
   - **Labor Force:** Employed + Unemployed (actively seeking work)
   - **Unemployment Rate:** (Unemployed / Labor Force) × 100
   - **Types:** Frictional, structural, cyclical, seasonal

3. **Phillips Curve Relationship:**
   - Short-run tradeoff between inflation and unemployment
   - High inflation typically associated with low unemployment
   - Long-run: No permanent tradeoff (natural rate hypothesis)

4. **Effects of Inflation:**
   - **Winners:** Debtors with fixed-rate loans, people with fixed nominal incomes
   - **Losers:** Creditors, people on fixed incomes, savers
   - **Shoe leather costs:** Time/effort to minimize cash holdings
   - **Menu costs:** Costs of changing prices frequently

**Economic Policy Implications:**
- **Expansionary Policy:** Reduce unemployment, may increase inflation
- **Contractionary Policy:** Reduce inflation, may increase unemployment
- **Supply-side policies:** Can reduce both inflation and unemployment

**Real-World Applications:**
- Central bank monetary policy decisions
- Government fiscal policy planning
- Personal financial planning and investment decisions

**Key Relationships:**
- Okun's Law: 1% increase in unemployment ≈ 2% decrease in GDP
- Quantity Theory: MV = PQ (Money × Velocity = Price × Quantity)
"""
        return solution
    
    async def _analyze_market_structure(self, problem: str) -> str:
        """Analyze different market structures."""
        solution = """
**MARKET STRUCTURE ANALYSIS**

**Problem Identification:**
This involves analyzing the characteristics and behavior of different market structures.

**Step-by-Step Analysis:**

1. **Perfect Competition:**
   - **Characteristics:** Many sellers, identical products, easy entry/exit, perfect information
   - **Pricing:** Price takers (P = MR = MC)
   - **Efficiency:** Allocatively and productively efficient
   - **Examples:** Agricultural markets, stock market

2. **Monopolistic Competition:**
   - **Characteristics:** Many sellers, differentiated products, easy entry/exit
   - **Pricing:** Some price-setting power (P > MC)
   - **Efficiency:** Allocatively inefficient, excess capacity
   - **Examples:** Restaurants, clothing stores, hair salons

3. **Oligopoly:**
   - **Characteristics:** Few sellers, significant barriers to entry, interdependence
   - **Pricing:** Strategic pricing decisions, potential for collusion
   - **Models:** Kinked demand curve, game theory applications
   - **Examples:** Airlines, telecommunications, automobiles

4. **Monopoly:**
   - **Characteristics:** Single seller, unique product, high barriers to entry
   - **Pricing:** Price maker (P > MR = MC)
   - **Efficiency:** Allocatively inefficient, deadweight loss
   - **Regulation:** Price controls, antitrust laws
   - **Examples:** Utilities, patents, natural monopolies

**Comparison Matrix:**
```
Structure    | # of Firms | Product      | Entry/Exit | Price Control
-------------|------------|--------------|------------|---------------
Perfect Comp | Many       | Identical    | Easy       | None
Monop. Comp  | Many       | Different    | Easy       | Some
Oligopoly    | Few        | Similar/Diff | Difficult  | Significant
Monopoly     | One        | Unique       | Blocked    | Complete
```

**Welfare Analysis:**
- Consumer surplus decreases as market power increases
- Deadweight loss increases with market power
- Innovation effects vary by structure

**Policy Implications:**
- Antitrust regulation for monopolies and oligopolies
- Patent protection to encourage innovation
- Regulation of natural monopolies
"""
        return solution
    
    async def _general_economics_explanation(self, problem: str) -> str:
        """Provide general economics explanation for unclear problems."""
        solution = """
**GENERAL ECONOMICS GUIDANCE**

I notice this might be a general economics question. Let me provide a comprehensive approach to economics problem-solving:

**Key Economic Principles:**

1. **Scarcity and Choice:**
   - All economic problems stem from unlimited wants and limited resources
   - Every choice involves opportunity cost (next best alternative)

2. **Supply and Demand:**
   - Foundation of market analysis
   - Determines prices and quantities in free markets

3. **Marginal Analysis:**
   - Economic decisions made at the margin
   - Compare marginal benefit to marginal cost

4. **Economic Efficiency:**
   - Allocative efficiency: P = MC
   - Productive efficiency: Minimum cost production

**Problem-Solving Steps:**
1. **Identify** the economic concept(s) involved
2. **Define** key terms and relationships
3. **Apply** relevant economic models or theories
4. **Calculate** using appropriate formulas
5. **Interpret** results in economic context
6. **Consider** real-world implications

**Common High School Economics Topics:**
- Microeconomics: Individual markets, consumer choice, firm behavior
- Macroeconomics: Overall economy, GDP, inflation, unemployment
- International economics: Trade, exchange rates, globalization
- Economic systems: Capitalism, socialism, mixed economies

**Study Tips:**
- Draw graphs to visualize concepts
- Use real-world examples to understand abstract concepts
- Practice with numerical problems
- Understand the logic behind economic relationships

Please provide more specific details about your economics question, and I'll give you a detailed, step-by-step solution!
"""
        return solution