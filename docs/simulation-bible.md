# Simulation Bible

## Purpose
This document defines the minimum conceptual contract for the simulation. It is intentionally engine-agnostic.

## Time
The simulation advances in monthly ticks. Quarterly and annual systems aggregate monthly outcomes. Elections, budgets, and major projects use explicit calendars.

## Spatial model
A region contains municipalities. Municipalities contain districts. Districts contain zones and service catchments. The vertical slice uses a small fixed region with authored topology and parameterized demographics.

## Core state
Each region tracks budget, population, household composition, housing stock, housing use, employment by sector, wages, commuting, transport capacity, healthcare capacity, tourism, business mix, public trust, political support, media environment, economic diversity, and resilience.

## Causal model
Every major metric must have inspectable contributors. Example:

`worker_accessibility = function(wage, housing_cost, commute_time, transport_reliability, service_access, job_stability)`

`tourism_pressure = function(visitor_volume, short_term_rental_share, public_space_capacity, seasonal_concentration, infrastructure_load)`

`institutional_trust = function(service_outcomes, transparency, perceived_fairness, scandal_exposure, corruption_debt)`

The first implementation should use simple, documented functions rather than opaque machine learning.

## Lags and thresholds
Policies can have immediate, delayed, and threshold effects. For example, housing conversion may improve tax revenue immediately, increase rents over several months, reduce worker accessibility later, and destabilize healthcare after a threshold is crossed.

## Population aggregation
The vertical slice uses household cohorts and worker cohorts rather than simulating every person. Cohorts retain district, income, household type, employment sector, tenure, mobility pressure, and satisfaction.

## Actors and memory
Actors maintain relationships and selected memories: promises, broken commitments, benefits received, harms experienced, investigations, and perceived fairness. Memory is bounded and testable.

## Projects
Projects have proposal, negotiation, approval, construction, operation, review, and closure or failure states. Public cost, private investment, jobs promised, jobs delivered, housing demand, service load, legal conditions, and failure risk are separate fields.

## Information model
The player sees a presentation model, not necessarily the full truth. Information has source, confidence, age, bias, and verification status. Complexity modes control how much uncertainty is exposed.

## Determinism
A run uses a seed. Given the same seed, configuration, content version, and decisions, simulation results must be reproducible. Randomness is isolated behind named streams.

## Safety and tone
Sensitive crisis content must represent affected people with dignity. Crime, violence, terrorism, addiction, migration, and poverty are systemic and human consequences, not spectacle or optimization targets.
