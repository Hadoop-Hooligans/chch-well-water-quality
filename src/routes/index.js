const express = require('express');
const router = express.Router();
const db = require('../db.js')
require('dotenv').config();

// Example route
router.get('/', (req, res) => {
    res.send(`<h1>Christchurch Water Quality</h1>`);
});

router.get('/:well_id/acceptable', async (req, res) => {
    const wellID = req.params.well_id;

    try {
        // Get the latest sample ID
        const sample = await db.query(
            `SELECT sample_id FROM recordings WHERE well_id = $1 ORDER BY recording_date DESC LIMIT 1`,
            [wellID]
        );

        if (sample.rows.length === 0) {
            return res.status(404).json({ error: "No records found" });
        }

        const sampleId = sample.rows[0].sample_id;

        // Get the data from `sample_v2` and `acceptable_determinands_v2`
        const result = await db.query(
            `SELECT * FROM sample_v2 CROSS JOIN acceptable_determinands_v2 WHERE sample_id = $1`,
            [sampleId]
        );

        res.json(result.rows);
    } catch (err) {
        console.error("Database error:", err);
        res.status(500).json({ error: "Internal server error" });
    }
});

router.get('/acceptable_determinands', async (req, res) => {
    try {
        const result = await db.query(`SELECT * FROM acceptable_determinands_v2`);
        res.json(result.rows);
    } catch (err) {
        console.error("Database error:", err);
        res.status(500).json({ error: "Internal server error" });
    }
});


router.get('/well_metadata', async (req, res) => {
    console.log(`Fetching Data`);
    try {
        const result = await db.query(`SELECT * FROM well_metadata`);
        res.json(result.rows);
    } catch (err) {
        console.error(`Couldn't fetch data. Error: ${err}`);
        res.status(500).json({ error: "Internal server error" });
    }
});


router.get('/:well_id/:years?', async (req, res) => {
    const wellID = req.params.well_id;
    let years = parseInt(req.params.years, 10) || 1;  // Convert to integer, default is 1

    if (isNaN(years) || years < 1) {
        return res.status(400).json({ error: "Invalid years parameter" });
    }

    try {
        // Use parameterized queries to prevent SQL injection
        const sample = await db.query(
            `SELECT sample_id FROM recordings WHERE well_id = $1 ORDER BY recording_date DESC LIMIT $2`,
            [wellID, years]
        );

        if (sample.rows.length === 0) {
            return res.status(404).json({ error: "No records found" });
        }

        if (years > 1) {
            const sampleIds = sample.rows.map(row => row.sample_id);
            const result = await db.query(
                `SELECT * FROM sample_v2 WHERE sample_id = ANY($1)`,
                [sampleIds]
            );
            res.json(result.rows);
        } else {
            const result = await db.query(
                `SELECT * FROM sample_v2 WHERE sample_id = $1`,
                [sample.rows[0].sample_id]
            );
            res.json(result.rows);
        }
    } catch (err) {
        console.error("Database error:", err);
        res.status(500).json({ error: "Internal server error" });
    }
});


module.exports = router;
