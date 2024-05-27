const express = require('express');
const router = express.Router();
const db = require('../db.js')

// Example route
router.get('/', (req, res) => {
    res.send('<h1>Christchurch Water Quality</h1>');
});

router.get('/:well_id', async (req, res) => {
    wellID = req.params.well_id
    try {
        const sample = await db.query(`SELECT sample_id FROM recordings WHERE well_id = '${wellID.replace('_', '/')}' ORDER BY recording_date DESC LIMIT 1`)
        sample_id = sample.rows[0].sample_id
        const result = await db.query(`SELECT * from sample_v2 where sample_id = '${sample_id}'`)
        res.json(result.rows)
    }
    catch (err) {

    }
})


module.exports = router;
