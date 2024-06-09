const { Pool } = require('pg');
const { ssl } = require('pg/lib/defaults');

require('dotenv').config()

const pool = new Pool({
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    host: process.env.DB_HOST,
    port: 5432, // default Postgres port
    database: process.env.DB_NAME,
    ssl: { rejectUnauthorized: false }
});

console.log(process.env)
module.exports = {
    query: (text, params) => pool.query(text, params)
};
// Example usage
pool.connect((err, client, release) => {
    if (err) {
        return console.error('Error acquiring client', err.stack);
    }
    client.query('SELECT NOW()', (err, result) => {
        release();
        if (err) {
            return console.error('Error executing query', err.stack);
        }
        console.log(result.rows);
    });
});
