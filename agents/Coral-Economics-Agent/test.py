#!/usr/bin/env python3
"""
Test script for the Economics Agent
"""
import asyncio
from economics_solver import EconomicsSolver

async def test_economics_solver():
    """Test the economics solver with various problem types."""
    solver = EconomicsSolver()
    
    test_problems = [
        "Calculate the price elasticity of demand when price increases from $10 to $12 and quantity demanded decreases from 100 to 80 units.",
        "If the demand curve is Qd = 100 - 2P and the supply curve is Qs = 20 + 3P, find the market equilibrium.",
        "Explain the concept of consumer surplus and how it's calculated.",
        "What is GDP and how is it different from GNP?",
        "Analyze the characteristics of a monopolistic competition market structure.",
        "Calculate the inflation rate if CPI increased from 200 to 210.",
    ]
    
    print("=== ECONOMICS AGENT TEST ===\n")
    
    for i, problem in enumerate(test_problems, 1):
        print(f"TEST {i}: {problem}")
        print("-" * 80)
        solution = await solver.solve_problem(problem)
        print(solution)
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(test_economics_solver())