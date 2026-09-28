# Zillow Recently Sold Scraper: Comps & CMA Sales Data

Scrape Zillow recently sold properties for CMA reports, investment analysis, and real estate market research. Filter by sold date range (30-365 days), price, beds, baths, and property type. Returns sold price, sold date, address, beds, baths, sqft, Zestimate, and listing URL.

**Run it on Apify:** [apify.com/themineworks/zillow-recently-sold](https://apify.com/themineworks/zillow-recently-sold)
**Docs, FAQ and pricing:** [themineworks.com/actors/zillow-recently-sold](https://themineworks.com/actors/zillow-recently-sold/)

**Price:** From $1.00 per 1,000 properties on Apify's higher plans ($2.00 on the free plan). Failed and empty results are never charged.

## What it returns

* Filter by sold date range: last 30, 90, 180, or 365 days
* Sold price and sale date for each property
* Price, beds, baths, sqft, Zestimate comparison
* Filter by price range, bedrooms, and property type
* Perfect for CMA reports and investment comp analysis
* GPS coordinates and Zillow listing URL

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/zillow-recently-sold").call(run_input={
    "location": "Austin, TX",
    "maxItems": 20,
    "soldInLast": 20,
    "propertyType": "SINGLE_FAMILY"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/zillow-recently-sold').call({
    "location": "Austin, TX",
    "maxItems": 20,
    "soldInLast": 20,
    "propertyType": "SINGLE_FAMILY"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~zillow-recently-sold/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"location": "Austin, TX", "maxItems": 20, "soldInLast": 20, "propertyType": "SINGLE_FAMILY"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 zillow_recently_sold_scraper.py --token YOUR_APIFY_TOKEN --location "Austin, TX" --max-items "20" --sold-in-last "20" --property-type "SINGLE_FAMILY"
node zillow_recently_sold_scraper.mjs --token YOUR_APIFY_TOKEN --location "Austin, TX" --max-items "20" --sold-in-last "20" --property-type "SINGLE_FAMILY"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `location` (required) | string |  | City, zip code, or neighborhood (for example 'Austin, TX', '78701', 'Palo Alto, CA') |
| `maxItems` | integer | `100` | Maximum number of recently sold properties to return |
| `soldInLast` | integer | `90` | Only return homes sold within the last N days |
| `propertyType` | string | `""` | Filter by property type, for example SINGLE_FAMILY, CONDO, TOWNHOUSE, MULTI_FAMILY, or LAND |
| `monitorMode` | boolean | `false` | Run this on a schedule and get ONLY sales not delivered in a previous run, so a daily comps watch bills you… |
| `minPrice` | integer |  | Minimum sale price in USD, to exclude cheaper closings from the results, for example 300000 |
| `maxPrice` | integer |  | Maximum sale price in USD, to exclude pricier closings from the results, for example 800000 |
| `minBeds` | integer |  | Minimum number of bedrooms a sold property must have to be included, for example 3 |
| `minBaths` | integer |  | Minimum number of bathrooms a sold property must have to be included, for example 2 |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `zpid` | string |  |
| `address` | string |  |
| `city` | string |  |
| `state` | string |  |
| `zipCode` | string |  |
| `price` | integer |  |
| `priceLabel` | string |  |
| `beds` | integer |  |
| `baths` | number |  |
| `sqft` | integer |  |
| `propertyType` | string |  |
| `statusType` | string |  |
| `zestimate` | integer |  |
| `latitude` | number |  |
| `longitude` | number |  |
| `detailUrl` | string |  |
| `imgSrc` | string |  |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/zillow-recently-sold
```

## FAQ

### What is a CMA and how does this help?

A Comparative Market Analysis compares recently sold homes to determine a property's fair market value. This actor pulls the sold comps data real estate agents and investors use for CMA reports.

### How far back can I go?

The soldInLast input supports 30, 90, 180, 365, and up to 730 days of sold history.

### What is the price?

Pay per result: from $1.00 per 1,000 properties on Apify's higher plans, $2.00 on the free plan. Failed results are never charged.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [B2B Leads Finder](https://themineworks.com/actors/b2b-leads-finder/): Business emails and LinkedIn profiles for target companies
* [LinkedIn Company Scraper](https://themineworks.com/actors/linkedin-company-details/): Company size, industry, website, and followers without login
* [Zillow Rental Listings Scraper](https://themineworks.com/actors/zillow-rental-listings/): Scrape Zillow for-rent listings by city or zip. $1 per 1,000 results

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
