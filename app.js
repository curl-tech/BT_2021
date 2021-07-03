var express = require('express');
require('dotenv').config();
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var fileUpload = require('express-fileupload');
var indexRouter = require('./routes/index');
var usersRouter = require('./routes/nature');
var app = express();
// TODO: this configuration should be changed 
app.use(fileUpload({useTempFiles:true,tempFileDir:"uploaded_files"}));
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/', indexRouter);
app.use('/nature', usersRouter);
app.listen(process.env.PORT || 8080, () => {
    console.log('Server is started on 127.0.0.1:'+ (process.env.PORT || 8080))
})
module.exports = app;
