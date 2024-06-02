const app = require('./app');
require('dotenv').config();


const PORT = process.env.PORT || 8888;

app.listen(PORT, () => {
    console.log(`App running on http://54.206.117.183:${PORT}/chchWater`)
})

