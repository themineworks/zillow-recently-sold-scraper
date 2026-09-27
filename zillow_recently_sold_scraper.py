#!/usr/bin/env python3
"""Scrape Zillow sold homes & comps by location. $1 per 1,000 results. Python, Node.js and cURL clients for the Zillow Recently Sold Scraper on Apify, pay per result.

Command-line client for the themineworks/zillow-recently-sold actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/zillow-recently-sold/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/zillow-recently-sold"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--location", help="City, zip code, or neighborhood (for example 'Austin, TX', '78701', 'Palo Alto, CA')")
    ap.add_argument("--max-items", type=int, help="Maximum number of recently sold properties to return")
    ap.add_argument("--sold-in-last", type=int, help="Only return homes sold within the last N days")
    ap.add_argument("--property-type", help="Filter by property type, for example SINGLE_FAMILY, CONDO, TOWNHOUSE, MULTI_FAMILY, or…")
    ap.add_argument("--monitor-mode", action=argparse.BooleanOptionalAction, help="Run this on a schedule and get ONLY sales not delivered in a previous run, so a daily…")
    ap.add_argument("--min-price", type=int, help="Minimum sale price in USD, to exclude cheaper closings from the results, for example…")
    ap.add_argument("--max-price", type=int, help="Maximum sale price in USD, to exclude pricier closings from the results, for example…")
    ap.add_argument("--min-beds", type=int, help="Minimum number of bedrooms a sold property must have to be included, for example 3")
    ap.add_argument("--min-baths", type=int, help="Minimum number of bathrooms a sold property must have to be included, for example 2")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.location is not None: run_input["location"] = a.location
    if a.max_items is not None: run_input["maxItems"] = a.max_items
    if a.sold_in_last is not None: run_input["soldInLast"] = a.sold_in_last
    if a.property_type is not None: run_input["propertyType"] = a.property_type
    if a.monitor_mode is not None: run_input["monitorMode"] = a.monitor_mode
    if a.min_price is not None: run_input["minPrice"] = a.min_price
    if a.max_price is not None: run_input["maxPrice"] = a.max_price
    if a.min_beds is not None: run_input["minBeds"] = a.min_beds
    if a.min_baths is not None: run_input["minBaths"] = a.min_baths

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
