# References and Sources

This document lists external data sources, APIs, and algorithms used in the Travel Buddy project.

---

## Data Sources (Scraped Content)

### Japan
- https://www.japan.travel/en/

---

## External APIs

### Open-Meteo Weather API
- https://open-meteo.com/

### Google Gemini API
- https://ai.google.dev/

### Tavily Search API
- https://tavily.com/ 

### FireCrawl API
- https://firecrawl.dev/

---

## Algorithms and Formulas

### Haversine Formula
- https://github.com/TrafficGCN/haversine_mapping_for_spatial_integration_in_graph_convolutional_networks

In the Travel Buddy project, the Haversine formula is used to calculate geographic distances between 
two coordinates on Earth. The algorithm is implemented in the file services/transport_service.py 
(lines 19-30) and is used to:

1. Calculate distance between the user's position and nearby places
2. Determine transport options (walk, subway, taxi) based on distance
3. Calculate route distances between airports and hotel areas

The Haversine formula provides accurate "great-circle" distances, which is the shortest 
distance between two points on a sphere. This is more important than Euclidean distance 
(classical geometry, often taught in school) because the Earth is round and not flat.

The formula takes into account Earth's radius (6371 km) and uses latitude/longitude 
to calculate the distance in kilometers.

---


**Last updated:** 2026-02-05
