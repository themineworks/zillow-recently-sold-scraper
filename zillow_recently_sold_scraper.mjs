#!/usr/bin/env node
// Node.js client for the themineworks/zillow-recently-sold actor on Apify: runs it and saves results.json.
// Flags map 1:1 to the actor's input. Free API token: https://console.apify.com/sign-up
// Docs and pricing: https://themineworks.com/actors/zillow-recently-sold/
import { ApifyClient } from 'apify-client';
import { writeFileSync } from 'node:fs';

const ACTOR = 'themineworks/zillow-recently-sold';

function parseArgs(argv) {
    const out = {};
    for (let i = 0; i < argv.length; i++) {
        if (!argv[i].startsWith('--')) continue;
        const key = argv[i].slice(2);
        out[key] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
    }
    return out;
}

const args = parseArgs(process.argv.slice(2));
const token = args.token || process.env.APIFY_TOKEN;
if (!token) {
    console.error('Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up');
    process.exit(1);
}

const runInput = {};
if (args['location'] !== undefined) runInput.location = String(args['location']);
if (args['max-items'] !== undefined) runInput.maxItems = parseInt(args['max-items'], 10);
if (args['sold-in-last'] !== undefined) runInput.soldInLast = parseInt(args['sold-in-last'], 10);
if (args['property-type'] !== undefined) runInput.propertyType = String(args['property-type']);
if (args['monitor-mode'] !== undefined) runInput.monitorMode = args['monitor-mode'] === true || args['monitor-mode'] === 'true';
if (args['min-price'] !== undefined) runInput.minPrice = parseInt(args['min-price'], 10);
if (args['max-price'] !== undefined) runInput.maxPrice = parseInt(args['max-price'], 10);
if (args['min-beds'] !== undefined) runInput.minBeds = parseInt(args['min-beds'], 10);
if (args['min-baths'] !== undefined) runInput.minBaths = parseInt(args['min-baths'], 10);

const client = new ApifyClient({ token });
console.log(`Running ${ACTOR} ...`);
const run = await client.actor(ACTOR).call(runInput);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
writeFileSync('results.json', JSON.stringify(items, null, 2));
console.log(`Saved ${items.length} results to results.json`);
