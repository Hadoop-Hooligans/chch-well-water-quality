require('dotenv').config()

const { Pool } = require('pg');
const { ssl } = require('pg/lib/defaults');

const pool = new Pool({
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    host: process.env.DB_HOST,
    port: 5432, // default Postgres port
    database: process.env.DB_NAME,
    ssl: { rejectUnauthorized: false }
});

module.exports = {
    query: (text, params) => pool.query(text, params)
};
