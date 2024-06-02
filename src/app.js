const express = require('express');
// const bodyParser = require('body-parser');
const cors = require('cors');
// const helmet = require('helmet');
// const morgan = require('morgan');

const app = express();
app.use(express.json());

// Middleware
// app.use(helmet());
// app.use(bodyParser.json());
app.use(cors());
// app.use(morgan('combined'));

// Routes
const apiRoutes = require('./routes');
app.use('/chchWater', apiRoutes);

module.exports = app;
