# PDGA_Stats

A clean, layered Python project for scraping PDGA (Professional Disc Golf Association) tournament data from the PDGA Live API.

## Overview

This project demonstrates best practices for building data ingestion + analytics pipelines with strict separation of concerns:

```
API Client (HTTP only) 
    ↓
Data Models (pure data structures)
    ↓
Orchestration (coordinate + parse)
    ↓
Storage (persist models)
```

**Key benefit:** Each layer can be tested, extended, and debugged independently.
