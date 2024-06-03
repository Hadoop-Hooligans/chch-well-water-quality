const express = require('express');
const router = express.Router();
const db = require('../db.js')

// Example route
router.get('/', (req, res) => {
    res.send('<h1>Christchurch Water Quality</h1>');
});

// router.get('/:well_id/:acceptable?', async (req, res) => {
//     const wellID = req.params.well_id
//     const acceptable = req.params.acceptable
//     const sample = await db.query(`SELECT sample_id FROM recordings WHERE well_id = '${wellID.replace('_', '/')}' ORDER BY recording_date DESC LIMIT 1`)
//     if (acceptable == 'acceptable') {
//         sampleIds = sample.rows[0].sample_id
//         const result = await db.query(`SELECT * from sample_v2 CROSS JOIN acceptable_determinands_v2 where sample_id = '${sampleIds}'`)
//         res.json(result.rows)
//     }
//     else {
//         res.send("<h1>Wrong</h1>")
//     }
// })


router.get('/acceptable_determinands', async (req, res) => {
    try {
        const result = await db.query(`SELECT * from acceptable_determinands_v2`)
        res.json(result.rows)
    }
    catch (err) {
        console.log(err)
    }
})


router.get('/well_metadata', async (req, res) => {
    try {
        const result = await db.query(`SELECT * from well_metadata`)
        res.json(result.rows)
    }
    catch (err) {
        console.log(`Couldn't fetch data. Error : ${err}`)
    }
})

router.get('/:well_id/:years?', async (req, res) => {
    const wellID = req.params.well_id
    const years = req.params.years
    try {
        const sample = await db.query(`SELECT sample_id FROM recordings WHERE well_id = '${wellID}' order by recording_date DESC LIMIT ${years ? years : 1}`)
        if (years > 1) {
            const sampleIds = sample.rows.map(item => item.sample_id)
            const sampleIdsString = sampleIds.map(id => `'${id}'`).join(", ")
            // res.send(sampleIdsString)
            const result = await db.query(`SELECT * from sample_v2 where sample_id IN (${sampleIdsString})`);
            res.json(result.rows)
        }
        else {
            sampleIds = sample.rows[0].sample_id
            const result = await db.query(`SELECT * from sample_v2 where sample_id = '${sampleIds}'`)
            res.json(result.rows)
        }

    }
    catch (err) {
        res.json(err)
    }
})


module.exports = router;
